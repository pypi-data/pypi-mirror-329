from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

# IndexedDocChunkPydantic doesn't store the content, the content is stored in the VectorStore.
# Each document may have duplicated IndexedDocChunkPydantic with different Ids but the same ChunkHash.
# Eg.
# ChunkGroup -->> Chunk --> RAGVSRepository.get_chunk(chunk_hash)

class IndexedDocChunkPydantic(BaseModel):
    Id: str = Field(..., description="Unique identifier for the document chunk")
    ChunkGroupId: str = Field(..., description="Unique identifier for the document chunk group")
    ChunkHash: str = Field(..., description="Hash of the chunk content")
    ByteSize: int = Field(..., description="Size of the chunk in bytes")
    IsDuplicate: bool = Field(..., description="Flag to indicate if the chunk is a duplicate")
    IsIndexed: bool = Field(..., description="Flag to indicate if the chunk has been indexed")
    Content: Optional[str] = Field(None, description="Content should be None means the chunk has been transferred to VectorStore. If Content is not None, that means this chunk is not indexed yet.")
    model_config = ConfigDict(from_attributes=True)

    def __eq__(self, other):
        if not isinstance(other, IndexedDocChunkPydantic):
            return NotImplemented
        return self.Id == other.Id and self.ChunkHash == other.ChunkHash