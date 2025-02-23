from pydantic import BaseModel
from typing import List
import json

class Claim(BaseModel):
    type: str
    text: str

class Utterance(BaseModel):
    start_time: float
    end_time: float
    speaker: str

class ClaimsUtterance(Utterance):
    claims: List[Claim]

class ClaimsData(BaseModel):
    utterances: List[ClaimsUtterance]

class TranscriptUtterance(BaseModel):
    start_time: float
    end_time: float
    text: str
    speaker: str

class Transcript(BaseModel):
    content_url: str
    utterances: List[TranscriptUtterance]

def load_transcript_from_json(file_path: str) -> Transcript:
    with open(file_path, "r") as file:
        data = json.load(file)
    return Transcript(**data)

def load_claims_from_json(file_path: str) -> ClaimsData:
    with open(file_path, "r") as file:
        data = json.load(file)
    return ClaimsData(**data)