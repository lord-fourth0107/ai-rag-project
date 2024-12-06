from .baseCrawler import BaseCrawler
from youtube_transcript_api import YouTubeTranscriptApi
from models.documentModels import YoutubeDocument
from loguru import logger
import yt_dlp
import requests
from urllib.parse import urlparse, parse_qs
class YouTubeCrawler(BaseCrawler):
    model = YoutubeDocument
    def get_title(link):
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return info.get('title', 'Title not found')

    def get_data(self, link: str, **kwargs):
        try:
            parsed_url = urlparse(url=link)

        # Case 1: Standard URL (query parameters)
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
             query_params = parse_qs(parsed_url.query)
             return query_params.get("v", [""])[0]

        # Case 2: Shortened URL
            if parsed_url.hostname in ['youtu.be']:
                return parsed_url.path.lstrip('/')

        # Case 3: Embedded URL
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com'] and parsed_url.path.startswith('/embed/'):
                return parsed_url.path.split('/embed/')[1]

            return ""
        except Exception as e:
            logger.error(f"Error parsing URL: {e}")
            return ""

    def extract(self, link: str, **kwargs):
        video_id = self.get_data(link)
        isVideoAlreadyPresent = self.model.find(link=video_id)
        if isVideoAlreadyPresent is not None:
            logger.info(f"Video already exists in the database: {video_id}")
            return
        try:
            logger.info(f"Starting scrapping YouTube video: {link}")
            video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
            # logger.debug(f"Video transcript extracted: {video_transcript}")
            continuous_string = " ".join(item['text'] for item in video_transcript)
            data = {
                "Title": "U",
                "Content": continuous_string
            }
            instance = self.model(
                platform="youtube",
                content=data,
                link=link,  
                # name="U"
            )
            instance.save()
            logger.info(f"Video added to the database: {video_id}")
        except Exception as e:
            logger.error(f"An error occurred while extracting transcript: " + {e})
        return 
        