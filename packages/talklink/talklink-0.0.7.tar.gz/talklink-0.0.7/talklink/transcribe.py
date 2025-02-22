import argparse
import assemblyai as aai
import os
import json
from talklink.models import Transcript, TranscriptUtterance
import math

def transcribe_audio(file_url, output_path) -> Transcript:
    api_key = os.getenv('ASSEMBLYAI_API_KEY')
    aai.settings.api_key = api_key
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
        file_url,
        config=config
    )
    print(f"Transcription complete. Utterances saved to {output_path}")

    transcript_utterances = []
    
    for utterance in transcript.utterances:
        words = utterance.words
        while len(words) > 0:
            if len(words) > 160:
                cutoff_index = 150
                
                while cutoff_index < 200 and words[cutoff_index - 1].text[-1] not in ['.', '?', '!']:
                    cutoff_index += 1
                
                if cutoff_index >= len(words):
                    cutoff_index = len(words)
                
                new_statement = ' '.join(word.text for word in words[:cutoff_index])
                start_time = math.floor(words[0].start / 1000)
                end_time = math.floor(words[cutoff_index - 1].end / 1000)
                transcript_utterances.append(TranscriptUtterance(
                    start_time=start_time,
                    end_time=end_time,
                    text=new_statement,
                    speaker=f"Unknown {utterance.speaker}"
                ))
                words = words[cutoff_index:]
            else:
                new_statement = ' '.join(word.text for word in words)
                start_time = math.floor(words[0].start / 1000)
                end_time = math.floor(words[-1].end / 1000)
                transcript_utterances.append(TranscriptUtterance(
                    start_time=start_time,
                    end_time=end_time,
                    text=new_statement,
                    speaker=f"Unknown {utterance.speaker}"
                ))
                words = []

    print(f"Writing transcript to file {output_path}")

    transcript_data = Transcript(content_url=file_url, utterances=transcript_utterances)

    with open(output_path, 'w') as f:
        json.dump(transcript_data.model_dump(), f, indent=4)

    return transcript_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transcribe audio using AssemblyAI.')
    parser.add_argument('--audio', required=True, help='The path of the audio file to transcribe')
    parser.add_argument('--output', required=True, help='The path to save the output file')
    args = parser.parse_args()

    transcribe_audio(args.audio, args.output)


