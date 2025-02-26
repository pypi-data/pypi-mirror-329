import json
import os
import argparse

def generate_speaker_map(names, output_folder="."):
    speaker_map = {f"Unknown {chr(65 + i)}": name for i, name in enumerate(names)}
    
    output_file = os.path.join(output_folder, "speakers.json")
    
    with open(output_file, 'w') as f:
        json.dump(speaker_map, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a speaker map from names.")
    parser.add_argument('names', nargs='+', help='List of names to include in the speaker map')
    parser.add_argument('--output', default='.', help='Output folder for the speakers.json file')
    args = parser.parse_args()

    names = args.names
    output = args.output

    generate_speaker_map(names, output)
