import yt_dlp
import argparse
import json

def format_title(title):
    return ''.join(char if char.isalnum() or char.isspace() else '' for char in title).replace(" ", "_").lower()

def download_audio(youtube_url, output_path="downloads") -> str:
    try:
        with yt_dlp.YoutubeDL({}) as ydl:
            print(f"Fetching video info from {youtube_url}...")
            info_dict = ydl.extract_info(youtube_url, download=False)
            # Limit fields to just "id", "title", "channel_id", and "webpage_url"
            info_dict = {key: info_dict[key] for key in ["id", "title", "channel_id", "webpage_url", "duration_string", "upload_date"] if key in info_dict}
            video_title = format_title(info_dict.get("title", "unknown"))
            with open(f'{output_path}/video_info.json', 'w') as f:
                json.dump(info_dict, f, indent=4)

        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '64',
            }],
            'outtmpl': f'{output_path}/{video_title}.%(ext)s',
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            print(f"Downloading audio from {youtube_url}...")
            ydl.download([youtube_url])
            print("Download complete!")
        return f'{output_path}/{video_title}.mp3'
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import os
    output_dir = "downloads"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    parser = argparse.ArgumentParser(description="Download audio from a YouTube video.")
    parser.add_argument('-u', '--url', type=str, required=True, help="YouTube video URL")
    args = parser.parse_args()

    download_audio(args.url, output_path=output_dir)
