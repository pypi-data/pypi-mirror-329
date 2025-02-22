import datetime
from typing import List
from pydantic import BaseModel, Field

HIERARCHIE_DOCUMENT="document"
HIERARCHIE_DOSSIER="dossier"

class ExtractedMetadata (BaseModel):
    origine:str=Field(default="LEXIA")
    classe:str=Field(default="DIVERS") 
    classe_confidence:float=Field(default=0.0)
    documentId:str=Field(default="")
    traite_le:str=Field(default=str(datetime.datetime.today()))

class ChunkMetadata(BaseModel):
    chunk:int=Field(default=1)
    chunks:int=Field(default=1)
    title:str=Field(default="")
    description:str=Field(default="")
    source:str=Field(default="")
    hierarchie:str=Field(default=HIERARCHIE_DOCUMENT)

class Chunk(BaseModel):
    metadata:ChunkMetadata=Field(default=None)
    page_content:str=Field(default="")    

class ExtractedData(BaseModel) :
    metadata:ExtractedMetadata=Field(default=None)
    chunks:List[Chunk]=[]
    keywords:List[str]=[]
    summary:str=Field(default="")