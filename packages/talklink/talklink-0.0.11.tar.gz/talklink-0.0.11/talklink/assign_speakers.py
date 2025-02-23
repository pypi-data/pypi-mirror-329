import json
import argparse
from typing import Dict, Tuple

from talklink.models import ClaimsData, load_claims_from_json, load_transcript_from_json, Transcript

def load_speaker_map(speaker_map_path: str) -> Dict[str, str]:
    try:
        with open(speaker_map_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def replace_speaker_labels_in_utterances(transcript_obj: Transcript, speaker_map: Dict[str, str]) -> Transcript:
    for utterance in transcript_obj.utterances:
        speaker_label = utterance.speaker
        if speaker_label in speaker_map:
            utterance.speaker = speaker_map[speaker_label]
    return transcript_obj


def assign_speakers_to_transcript(transcript_path: str, speaker_map_path: str) -> Tuple[Transcript, str]:
    speaker_map = load_speaker_map(speaker_map_path)

    transcript_obj = load_transcript_from_json(transcript_path)
    
    with open(transcript_path, 'w') as f:
        transcript_obj = replace_speaker_labels_in_utterances(transcript_obj, speaker_map)
        json.dump(transcript_obj.model_dump(), f, indent=4)

    if speaker_map:
        return transcript_obj, ','.join(speaker_map.values())
    else:
        unique_speakers = list(set(utterance.speaker for utterance in transcript_obj.utterances))
        return transcript_obj, ','.join(unique_speakers)

def assign_speakers_to_claims(claims_path: str, speaker_map_path: str) -> Tuple[ClaimsData, str]:
    speaker_map = load_speaker_map(speaker_map_path)

    claims_obj = load_claims_from_json(claims_path)
    
    with open(claims_path, 'w') as f:
        claims_obj = replace_speaker_labels_in_utterances(claims_obj, speaker_map)
        json.dump(claims_obj.model_dump(), f, indent=4)

    if speaker_map:
        return claims_obj, ','.join(speaker_map.values())
    else:
        unique_speakers = list(set(utterance.speaker for utterance in claims_obj.utterances))
        return claims_obj, ','.join(unique_speakers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a transcript and replace speaker labels with names.")
    subparsers = parser.add_subparsers(dest="mode")

    transcript_parser = subparsers.add_parser("transcript")
    transcript_parser.add_argument("--transcript", required=True, help="Path to the transcript file.")
    transcript_parser.add_argument("--speakers", required=True, help="Path to the speaker map JSON file.")
    transcript_parser.add_argument("--output", required=True, help="Path to the output processed transcript file.")

    claims_parser = subparsers.add_parser("claims")
    claims_parser.add_argument("--claims", required=True, help="Path to the claims file.")
    claims_parser.add_argument("--speakers", required=True, help="Path to the speaker map JSON file.")
    transcript_parser.add_argument("--output", required=True, help="Path to the output processed transcript file.")
    
    args = parser.parse_args()
    
    if args.mode == "transcript":
        assign_speakers_to_transcript(args.transcript, args.speakers, args.output) 
    elif args.mode == "claims":
        assign_speakers_to_claims(args.claims, args.speakers, args.output) 