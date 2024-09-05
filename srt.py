from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api.formatters import SRTFormatter
#For Docs https://pypi.org/project/youtube-transcript-api/


def GetCaptions(id):
    transcript_list = YouTubeTranscriptApi.list_transcripts(id)
    transcript = transcript_list.find_transcript(['en'])

    if transcript.is_translatable:
        translated_transcript = transcript.translate('ar')
        transcript = translated_transcript.fetch()

        text_formatter = TextFormatter().format_transcript(transcript)
        srt_formatter = SRTFormatter().format_transcript(transcript)
        with open('srt.txt', 'w', encoding='utf-8') as text_file:
            text_file.write(text_formatter)

        with open('srt.srt', 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_formatter)

GetCaptions('qw7xG1KGC_U')