from pydantic import BaseModel, Field,validator
from typing import Optional, List
from datetime import datetime,date
from gai.rag.dtos.indexed_doc_chunkgroup import IndexedDocChunkGroupPydantic

class IndexedDocPydantic(BaseModel):
    Id: str = Field(...)
    CollectionName: str = Field(..., description="Name of the collection containing the document")
    ByteSize: int = Field(..., gt=0, description="Size of the document in bytes")
    FileName: Optional[str] = Field(None, description="Name of the file")
    FileType: Optional[str] = Field(None, description="Type of the file")
    File: Optional[bytes] = None  # Binary data of the file
    Source: Optional[str] = Field(None, description="Source from where the document was obtained")
    Abstract: Optional[str] = Field(None, description="Abstract of the document")
    Authors: Optional[str] = Field(None, description="Authors of the document")
    Title: Optional[str] = Field(None, description="Title of the document")
    Publisher: Optional[str] = Field(None, description="Publisher of the document")
    PublishedDate: Optional[date] = Field(None, description="Date when the document was published")
    Comments: Optional[str] = Field(None, description="Additional comments about the document")
    Keywords: Optional[str] = Field(None, description="Keywords associated with the document")
    CreatedAt: datetime = Field(default_factory=lambda: datetime.now(), description="Timestamp when the document entry was created")
    UpdatedAt: datetime = Field(default_factory=lambda: datetime.now(), description="Timestamp when the document entry was last updated")
    IsActive: bool = Field(True, description="Flag to indicate if the document is active")
    ChunkGroups: Optional[List[IndexedDocChunkGroupPydantic]] = Field(None, description="List of chunk groups associated with the document")

    def validate_dates(self):
        if self.CreatedAt > datetime.now() or self.UpdatedAt > datetime.now():
            raise ValueError("Dates cannot be in the future")