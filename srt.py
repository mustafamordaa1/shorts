from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api.formatters import SRTFormatter
from pytubefix import YouTube
from pytubefix.cli import on_progress
import subprocess
#For Docs https://pypi.org/project/youtube-transcript-api/


def GetCaptions(id):
    try:
        m = 1 + 'm'
        transcript_list = YouTubeTranscriptApi.list_transcripts(id)
        transcript = transcript_list.find_generated_transcript(['ar']).fetch()
        text_formatter = TextFormatter().format_transcript(transcript)
        srt_formatter = SRTFormatter().format_transcript(transcript)
        with open('srt.txt', 'w', encoding='utf-8') as text_file:
            text_file.write(text_formatter)

        with open('srt.srt', 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_formatter)
        
        return 0

    except:
        url = f"https://www.youtube.com/watch?v={id}"
        
        yt = YouTube(url, on_progress_callback = on_progress)
        print(yt.title)
        #print(yt.streams)
        yt.streams.get_by_itag(398).download()
        subprocess.run(["mv", f"{yt.title}.mp4", "video-long.mp4"])
        
        return 0

GetCaptions('ftbgcarkxS0')
#GetCaptions('69KmV22T-W4')

