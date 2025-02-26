import argparse
import json
import tiktoken
from openai import OpenAI
from typing import Dict, Any, List
from talklink.models import ClaimsData, Transcript, load_transcript_from_json

client = OpenAI()
system_prompt = """
### System Prompt: Enhanced Claim Extraction from Transcripts

#### Objective
You are an AI assistant specialized in extracting claims from conversation transcripts. Each claim must be **precise, contextually complete, and self-contained**, ensuring clarity and verifiability without reference to the original transcript.

#### Claim Types
- **Opinion**: Subjective statements or personal viewpoints. Cite occurrences in the transcript.
- **Fact**: Verifiable statements based on objective reality.
- **Prediction**: Assertions about future events.
- **Evaluation**: Judgments or qualitative assessments.
- **Other**: If the statement does not fit the above categories.

#### Input Format
You will receive a structured conversation transcript including:
- Multiple **speakers**
- **Timestamps** per utterance

**Example Input:**
```json
{
  "content_url": "file.mp3",
  "utterances": [
    {
      "start_time": 0.16,
      "end_time": 36.76,
      "text": "I'm very excited about robotics, but I think we should be realistic...",
      "speaker": "Harald Schafer"
    }
  ]
}
```

#### Example Output:
```json
{
  "utterances": [
    {
      "time_range": "00:00 - 00:05",
      "speaker": "Speaker 1",
      "claims": [
        {
          "type": "opinion",
          "text": "Fascism is a serious problem in modern society.",
          "occurrences": [
            {
              "utterance_index": 1,
              "timestamp": "00:02"
            }
          ]
        },
        {
          "type": "fact",
          "text": "Certain political movements exhibit authoritarian tendencies."
        },
        {
          "type": "evaluation",
          "text": "People often distort reality to fit their narratives."
        }
      ]
    }
  ]
}
```

#### Processing Guidelines

1. **Extract Claims**
   - Identify statements of belief, assertion, or evaluation.
   - Ensure each claim is contextually complete and can stand alone.

2. **Reformat Claims**
   - **Convert to third-person perspective** where applicable.
   - Maintain precision and avoid vague references.

3. **Classify Claims**
   - Categorize each claim accurately.
   - For **opinions**, provide an `"occurrences"` field linking to the transcript.

#### Rules & Constraints

- Claims must be **self-contained** (no vague pronouns or missing context).
- Ensure **concise yet clear** claim formulation.
- **No extraneous text** outside the structured JSON response.
- **Objectivity is key**—do not infer speaker intent beyond the text.
- **Use timestamps** (`"MM:SS"`) from the transcript when available.
- If an utterance has **no claims**, return an empty `"claims"` array.

#### Examples of Poor vs. Correct Claim Extraction

##### ❌ Poor Extraction (Vague, Incomplete)
```json
{
  "claims": [
    { "type": "opinion", "text": "It was crazy." },
    { "type": "fact", "text": "That was a big mistake." }
  ]
}
```

##### ✅ Correct Extraction (Clear, Self-Contained)
```json
{
  "claims": [
    { 
      "type": "opinion", 
      "text": "The company's decision to launch early was reckless.",
      "occurrences": [
        {
          "utterance_index": 3,
          "timestamp": "05:12"
        }
      ]
    },
    { 
      "type": "fact", 
      "text": "The government withdrew from the conflict in 2022, leading to instability." 
    }
  ]
}
```

---
This ensures extracted claims are **accurate, independent, and ready for verification**, making them useful for research, analysis, or further processing.
"""
# Model settings
MODEL_NAME = "gpt-4o"
MAX_TOKENS = 8000  # Token limit per API call
encoder = tiktoken.encoding_for_model(MODEL_NAME)

def chunk_transcript(transcript: Transcript, max_tokens: int) -> List[Transcript]:
    """Splits transcript into chunks that fit within the model's token limit."""
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for utterance in transcript.utterances:
        utterance_tokens = len(encoder.encode(json.dumps(utterance.model_dump())))
        if current_tokens + utterance_tokens > max_tokens:
            if current_chunk:
                chunks.append(Transcript(content_url=transcript.content_url, utterances=current_chunk))
                current_chunk = []
                current_tokens = 0
        
        current_chunk.append(utterance)
        current_tokens += utterance_tokens
    
    if current_chunk:
        chunks.append(Transcript(content_url=transcript.content_url, utterances=current_chunk))
    
    return chunks

def extract_claims_from_chunk(chunk: Transcript) -> ClaimsData:
    """Extracts claims from a given transcript chunk using OpenAI's GPT model."""
    try:
        completion = client.beta.chat.completions.parse(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": chunk.model_dump_json()}
            ],
            response_format=ClaimsData
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        print(f"Error extracting claims for chunk: {e}")
        return ClaimsData(utterances=[])

def extract_claims_from_transcript_model(transcript: Transcript) -> ClaimsData:
    """Extracts claims from a full transcript, handling chunking if needed."""
    print(f"Processing {len(transcript.utterances)} utterances...")
    
    chunks = chunk_transcript(transcript, MAX_TOKENS)
    claims_data = ClaimsData(utterances=[])
    
    for index, chunk in enumerate(chunks):
        print(f"Processing chunk {index+1}/{len(chunks)}...")
        claims = extract_claims_from_chunk(chunk)
        claims_data.utterances.extend(claims.utterances)
    
    print(f"Finished processing {len(claims_data.utterances)} utterances.")
    return claims_data

def main(transcript_path: str, output_path: str):
    transcript = load_transcript_from_json(transcript_path)
    claims_data = extract_claims_from_transcript_model(transcript)
    
    with open(output_path, "w") as file:
        json.dump(claims_data.model_dump(), file, indent=4)
    
    print(f"Claims extracted and saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract claims from a transcript.")
    parser.add_argument("--transcript", required=True, help="Path to the transcript JSON file.")
    parser.add_argument("--output", required=True, help="Path to the output JSON file for extracted claims.")
    args = parser.parse_args()
    main(args.transcript, args.output)
