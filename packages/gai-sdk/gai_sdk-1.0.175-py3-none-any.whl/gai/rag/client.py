import asyncio
import os
import json
from typing import Optional, Union
from gai.rag.dtos.indexed_doc import IndexedDocPydantic
import uuid
import mimetypes
import websockets

from gai.lib.http_utils import http_post_async, http_get_async,http_delete_async, http_put_async
from gai.lib.logging import getLogger
logger = getLogger(__name__)
from gai.lib.errors import ApiException, DocumentNotFoundException

from gai.lib.config import GaiClientConfig
from gai.rag.dtos.create_doc_header_request import CreateDocHeaderRequestPydantic
from gai.rag.dtos.update_doc_header_request import UpdateDocHeaderRequestPydantic
from gai.rag.dtos.indexed_doc_chunkgroup import IndexedDocChunkGroupPydantic
from gai.rag.dtos.indexed_doc_chunk_ids import IndexedDocChunkIdsPydantic
from gai.rag.dtos.encode_dto import EncodeResponse, EncodeRequest
from gai.rag.dtos.scrapers_dtos import SearchRequest, SearchResponse


'''
This is class is used by the client-side websocket to receive status updates from the server.
'''

class StatusListener:

    def __init__(self, ws_url):
        self.ws_url = ws_url

    async def listen(self, async_callback):
        async with websockets.connect(self.ws_url) as websocket:
            logger.info(f"Connected to {self.ws_url}")
            while True:
                try:
                    message = await websocket.recv()
                    logger.debug(f"StatusListener.listen: Client-side received from websocket {message}")                    
                    await async_callback(message)
                    # await asyncio.sleep(0)
                    # asyncio.create_task(callback(message))
                except websockets.ConnectionClosedError:
                    logger.warn("StatusListener.listen: Server disconnected.")
                    break
                except Exception as e:
                    logger.error(f"Error: {e}")
                    raise e
    


class RagClientAsync:

    def __init__(self, config: Optional[Union[GaiClientConfig|dict]]=None,name:Optional[str]="rag", file_path:str=None):
        self.config:GaiClientConfig = None
        
        # Load from default config file
        if isinstance(config, dict):
            # Load default config and patch with provided config
            self.config = GaiClientConfig.from_dict(config)
        elif isinstance(config, GaiClientConfig):
            self.config = config
        elif name:
            # If path is provided, load config from path
            self.config = GaiClientConfig.from_name(name=name,file_path=file_path)
        else:
            raise ValueError("Invalid config or path provided")
        
        self.url = self.config.url

    def _prepare_files_and_metadata(self, collection_name, file_path, metadata):
        mode = 'rb' if file_path.endswith('.pdf') else 'r'
        with open(file_path, mode) as f:
            files = {
                "file": (os.path.basename(file_path), f if mode == 'rb' else f.read(), "application/pdf"),
                "metadata": (None, json.dumps(metadata), "application/json"),
                "collection_name": (None, collection_name, "text/plain")
            }
            return files


    ### ----------------- MULTI-STEP INDEXING ----------------- ###
    async def step_header_async(
        self,
        collection_name, 
        file_path, 
        file_type="",
        title="",
        source="",
        authors="",
        publisher="",
        published_date="",
        comments="",
        keywords=""         
        ) -> IndexedDocPydantic:

        url=os.path.join(self.url,"step/header")
        create_doc_header_req=CreateDocHeaderRequestPydantic(
            CollectionName=collection_name,
            FilePath=file_path,
            FileType=file_type,
            Source=source,
            Title=title,
            Authors=authors,
            Publisher=publisher,
            PublishedDate = published_date,
            Comments=comments,
            Keywords=keywords
        )


        # Send file
        try:
            mode = 'rb'
            with open(create_doc_header_req.FilePath, mode) as f:
                files = {
                    "file": (os.path.basename(create_doc_header_req.FilePath), f, "application/pdf"),
                    "req": (None, create_doc_header_req.json(), "application/json"),
                }
                response = await http_post_async(url=url, files=files)
                if not response:
                    raise Exception("No response received")
                pydantic=response.json()
                return IndexedDocPydantic(**pydantic)
        except Exception as e:
            logger.error(f"index_document_header_async: Error creating document header. error={e}")
            raise e


    async def step_split_async(
            self,
            collection_name,
            document_id,
            chunk_size,
            chunk_overlap) -> IndexedDocChunkGroupPydantic:
        url=os.path.join(self.url,"step/split")
        try:
            response = await http_post_async(url=url, data={
                "collection_name": collection_name,
                "document_id": document_id,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap
            })
            return IndexedDocChunkGroupPydantic(**response.json())
        except Exception as e:
            logger.error(f"step_split_async: Error splitting document. error={e}")
            raise e

    async def step_index_async(
            self,
            collection_name,
            document_id,
            chunkgroup_id,
            async_callback=None) -> IndexedDocChunkIdsPydantic:
        url=os.path.join(self.url,"step/index")
        try:
            # Spin off listener task if async_callback is provided
            listen_task=None
            if async_callback:
                ws_url=os.path.join(self.url,f"index-file/ws/{collection_name}").replace("http","ws")
                listener = StatusListener(ws_url)
                listen_task=asyncio.create_task(listener.listen(async_callback))

            response = await http_post_async(url=url, data={
                "collection_name": collection_name,
                "document_id": document_id,
                "chunkgroup_id":chunkgroup_id
            },timeout=3600)

            # Cancel listener task if it was started
            if listen_task:
                listen_task.cancel()

            return IndexedDocChunkIdsPydantic(**response.json())
        except Exception as e:
            logger.error(f"step_index_async: Error splitting document. error={e}")
            raise e


    ### ----------------- SINGLE-STEP INDEXING ----------------- ###
    def save_temp_document(self, collection_name:str, file_content: bytes, file_content_type: str) -> str:
        """
        Save the uploaded document to a temporary directory and return the temp file name.
        This function is framework-agnostic and doesn't rely on FastAPI-specific components.
        """
        try:
            # Create temp directory "/tmp/{agent_id}"
            temp_dir = os.path.join("/tmp", collection_name)
            os.makedirs(temp_dir, exist_ok=True)

            # Create a random file name and guess the file extension based on content type
            temp_filename = str(uuid.uuid4()) + mimetypes.guess_extension(file_content_type)
            file_location = os.path.join(temp_dir, temp_filename)

            # Save file content to the temporary file
            with open(file_location, "wb") as file_object:
                file_object.write(file_content)

            return temp_filename
        except Exception as e:
            id = str(uuid.uuid4())
            logger.error(f"Failed to save uploaded document to tempfile. {id} Error=Failed to create document header,{str(e)}")
            raise e
            
    async def index_document_async(
        self, 
        collection_name, 
        file_path, 
        title,
        source,
        file_type="",
        authors="",
        publisher="",
        published_date="",
        comments="",
        keywords="",
        async_callback=None) -> IndexedDocPydantic:

        # Spin off listener task if async_callback is provided
        listen_task=None
        if async_callback:
            ws_url = self.config.extra["ws_url"]+"/"+collection_name
            listener = StatusListener(ws_url)
            listen_task=asyncio.create_task(listener.listen(async_callback))

        try:

            # Save a copy of the document to a temporary file
            temp_filename = ""
            with open(file_path, 'rb') as f:
                file_content = f.read()
                file_content_type = "text/plain"
                if file_path.endswith('.pdf'):
                    file_content_type = "application/pdf"
                temp_filename = self.save_temp_document(file_content=file_content, collection_name=collection_name, file_content_type=file_content_type)

            # Create the document header
            logger.info(f"Creating header for collection name {collection_name} at {file_path}")
            doc_header = await self.step_header_async(
                collection_name=collection_name,
                file_path=f"/tmp/{collection_name}/{temp_filename}",
                file_type="pdf" if file_path.endswith('.pdf') else "txt",
                title=title,
                source=source
            )

            # Split the document into chunks
            from gai.rag.dtos.split_doc_request import SplitDocRequestPydantic
            req = SplitDocRequestPydantic(
                DocumentId=doc_header.Id,
                ChunkSize=1000,
                ChunkOverlap=100,
            )
            logger.info(f"Splitting document {req.DocumentId} for collection {collection_name} with chunk size {req.ChunkSize} and overlap {req.ChunkOverlap}")
            chunkgroup = await self.step_split_async(
                collection_name=collection_name,
                document_id=req.DocumentId,
                chunk_size=req.ChunkSize,
                chunk_overlap=req.ChunkOverlap
            )

            # Index the document chunks
            logger.info(f"Indexing document {doc_header.Id} for collection {collection_name} with chunk group {chunkgroup.Id}")
            await self.step_index_async(
                collection_name=collection_name,
                document_id=doc_header.Id,
                chunkgroup_id=chunkgroup.Id,
                async_callback=async_callback
            )
            doc_header.File = file_content
            
            return doc_header

        except Exception as e:
            logger.error(f"index_document_async: Error indexing file. error={e}")
            raise e
        finally:
            # Cancel listener task if it was started
            if listen_task:
                listen_task.cancel()

    
    ### ----------------- RETRIEVAL ----------------- ###

    async def retrieve_async(self, collection_name, query_texts, n_results=None):
        url = os.path.join(self.url,"retrieve")
        data = {
            "collection_name": collection_name,
            "query_texts": query_texts
        }
        if n_results:
            data["n_results"] = n_results

        response = await http_post_async(url, data=data)
        return response.json()["retrieved"]

#Collections-------------------------------------------------------------------------------------------------------------------------------------------

    async def delete_collection_async(self, collection_name):
        url = os.path.join(self.url,"collection",collection_name)
        logger.info(f"RAGClient.delete_collection: Deleting collection {url}")
        try:
            response = await http_delete_async(url)
        except ApiException as e:
            if e.code == 'collection_not_found':
                return {"count":0}
            logger.error(e)
            raise e
        return json.loads(response.text)

    async def list_collections_async(self):
        url = os.path.join(self.url,"collections")
        response = await http_get_async(url)
        return json.loads(response.text)

#Documents-------------------------------------------------------------------------------------------------------------------------------------------

    async def list_documents_async(self, collection_name=None) -> list[IndexedDocPydantic]:
        if not collection_name:
            url = os.path.join(self.url,"documents")
            response = await http_get_async(url)
            return [IndexedDocPydantic.parse_obj(doc) for doc in response.json()]
    
        url = os.path.join(self.url,f"collection/{collection_name}/documents")
        response = await http_get_async(url)
        docs = [IndexedDocPydantic.parse_obj(doc) for doc in response.json()]
        return docs

#Document-------------------------------------------------------------------------------------------------------------------------------------------

    # Response:
    # - 200: { "document": {...} }
    # - 404: { "message": "Document with id {document_id} not found" }
    # - 500: { "message": "Internal error: {id}" }
    async def get_document_header_async(self, collection_name, document_id) -> IndexedDocPydantic:
        try:
            url = os.path.join(self.url,f"collection/{collection_name}/document/{document_id}")
            response = await http_get_async(url)
            jsoned = json.loads(response.text)
            pydantic = IndexedDocPydantic.parse_obj(jsoned)
            return pydantic
        except ApiException as e:
            if e.code == 'document_not_found':
                raise DocumentNotFoundException(document_id)
            logger.error(f"RAGClientAsync.update_document_header_async: Error={e}")
            raise e
        except Exception as e:
            logger.error(f"get_document_header_async: Error getting document header. error={e}")
            raise e

    # Response:
    # - 200: { "message": "Document with id {document_id} deleted successfully" }
    # - 404: { "message": "Document with id {document_id} not found" }
    # - 500: { "message": "Internal error: {id}" }
    async def delete_document_async(self,collection_name,document_id):
        try:
            url = os.path.join(self.url,f"collection/{collection_name}/document/{document_id}")
            response = await http_delete_async(url)
            return json.loads(response.text)
        except ApiException as e:
            if e.code == 'document_not_found':
                raise DocumentNotFoundException(document_id)
            logger.error(f"RAGClientAsync.update_document_header_async: Error={e}")
            raise e
        except Exception as e:
            logger.error(f"RAGClientAsync.delete_document_async: Error={e}")
            raise e

    # Response:
    # - 200: { "message": "Document updated successfully", "document": {...} }
    # - 404: { "message": "Document with id {document_id} not found" }
    # - 500: { "message": "Internal error: {id}" }
    async def update_document_header_async(self,collection_name,document_id,update_doc_header_req:UpdateDocHeaderRequestPydantic):
        try:
            url = os.path.join(self.url,f"collection/{collection_name}/document/{document_id}")
            response = await http_put_async(url,data=update_doc_header_req.model_dump(exclude_none=True))
            return json.loads(response.text)
        except ApiException as e:
            if e.code == 'document_not_found':
                raise DocumentNotFoundException(document_id)
            logger.error(f"RAGClientAsync.update_document_header_async: Error={e}")
            raise e
        except Exception as e:
            logger.error(f"RAGClientAsync.update_document_header_async: Error={e}")
            raise e

    async def get_document_file_async(self,collection_name,document_id,output_path=None):
        try:
            url = os.path.join(self.url,f"collection/{collection_name}/document/{document_id}/file")
            response = await http_get_async(url)

            doc = await self.get_document_header_async(collection_name=collection_name,document_id=document_id)
            if not output_path:
                cwd = os.curdir
                output_path=os.path.join(cwd,doc.FileName+"."+doc.FileType)
            with open(output_path,"wb") as f:
                f.write(response.content)
        except Exception as e:
            logger.error(f"RAGClientAsync.get_document_file_async: Error={e}")
            raise e


#Chunkgroup-------------------------------------------------------------------------------------------------------------------------------------------

    async def list_chunkgroup_ids_async(self):
        url = os.path.join(self.url,f"chunkgroups")
        response = await http_get_async(url)
        return json.loads(response.text)

    async def get_chunkgroup_async(self,chunkgroup_id):
        url = os.path.join(self.url,f"chunkgroup/{chunkgroup_id}")
        response = await http_get_async(url)
        return json.loads(response.text)
    
    # Delete a chunkgroup to resplit and index
    async def delete_chunkgroup_async(self,collection_name, chunkgroup_id):
        url = os.path.join(self.url,f"collection/{collection_name}/chunkgroup/{chunkgroup_id}")
        response = await http_delete_async(url)
        return json.loads(response.text)

#Chunks-------------------------------------------------------------------------------------------------------------------------------------------
    # Use this to get chunk ids only
    async def list_chunks_async(self,chunkgroup_id=None):
        if not chunkgroup_id:
            url = os.path.join(self.url,"chunks")
            response = await http_get_async(url)
            return json.loads(response.text)
        url = os.path.join(self.url,f"chunks/{chunkgroup_id}")
        response = await http_get_async(url)
        return json.loads(response.text)

    # Use this to get chunks of a document from db and vs
    async def list_document_chunks_async(self,collection_name,document_id):
        url = os.path.join(self.url,f"collection/{collection_name}/document/{document_id}/chunks")
        response = await http_get_async(url)
        return json.loads(response.text)
    
    # Use this to get a chunk from db and vs
    async def get_document_chunk_async(self,collection_name, chunk_id):
        url = os.path.join(self.url,f"collection/{collection_name}/chunk/{chunk_id}")
        response = await http_get_async(url)
        return json.loads(response.text)
    
    async def encode_async(self,text) -> EncodeResponse:
        url = os.path.join(self.url,"encode")
        response = await http_get_async(url,data=EncodeRequest(text=text).model_dump())
        result = json.loads(response.text)
        return EncodeResponse(**result)

    async def web_search_async(self,
                               search_query,
                               link_limit=3,
                               chunk_size=1000,
                               chunk_overlap=0.1,
                               skip_char=500,
                               skip_chunk=0,
                               chunk_limit=3
                               ) -> SearchResponse:
        url = os.path.join(self.url,f"websearch")
        req = SearchRequest(
            search_query=search_query,
            link_limit=link_limit,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            skip_char=skip_char,
            skip_chunk=skip_chunk,
            chunk_limit=chunk_limit
            ).model_dump() 
        
        response = await http_get_async(url,data=req,timeout=6000)
        result = json.loads(response.text)
        response = SearchResponse(**result)
        logger.info(f"RagClientAsync.web_search_async: query={response.query} chunks={len(response.chunks)}")
        return response