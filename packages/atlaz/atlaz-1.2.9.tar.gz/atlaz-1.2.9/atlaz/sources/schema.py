from pydantic import BaseModel, Field # type: ignore
from typing import Union

class Textsource(BaseModel):
    StartOfSource: str = Field(
        ...,
        description=(
            "The beginning of the part of the text the information is extracted from. "
            "Should be an exact match character to character with the text but doesn't have to be more than a few words."
        )
    )
    EndOfSource: str = Field(
        ...,
        description=(
            "The end of the part of the text the information is extracted from. "
            "Should be an exact match character to character with the text but doesn't have to be more than a few words."
        )
    )

class Source(BaseModel):
    TextSource: Union[Textsource, str] = Field(
        ...,
        description="List of text sources for the object."
    )

class StrictSource(BaseModel):
    TextSource: Textsource = Field(
        ...,
        description="List of text sources for the object."
    )