from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime,date
from gai.rag.dtos.indexed_doc_chunkgroup import IndexedDocChunkGroupPydantic

class IndexedDocHeaderPydantic(BaseModel):
    Id: str = Field(..., description="Unique identifier for the document")
    CollectionName: str = Field(..., description="Name of the collection containing the document")
    ByteSize: int = Field(..., gt=0, description="Size of the document in bytes")
    FileName: Optional[str] = Field(None, description="Name of the file")
    FileType: Optional[str] = Field(None, description="Type of the file")
    Source: Optional[str] = Field(None, description="Source from where the document was obtained")
    Abstract: Optional[str] = Field(None, description="Abstract of the document")
    Authors: Optional[str] = Field(None, description="Authors of the document")
    Title: Optional[str] = Field(None, description="Title of the document")
    Publisher: Optional[str] = Field(None, description="Publisher of the document")
    PublishedDate: Optional[date] = Field(None, description="Date when the document was published")
    Comments: Optional[str] = Field(None, description="Additional comments about the document")
    Keywords: Optional[str] = Field(None, description="Keywords associated with the document")
    CreatedAt: datetime = Field(..., description="Timestamp when the document entry was created")
    UpdatedAt: datetime = Field(..., description="Timestamp when the document entry was last updated")
    IsActive: bool = Field(True, description="Flag to indicate if the document is active")
    ChunkGroups: Optional[List[IndexedDocChunkGroupPydantic]] = Field(None, description="List of chunk groups associated with the document")

