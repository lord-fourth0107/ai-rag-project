from .baseCrawler import BaseCrawler
from youtube_transcript_api import YouTubeTranscriptApi
from models.documentModels import VideoSubtitleDocument
from loguru import logger
from pytube import YouTube
from urllib.parse import urlparse, parse_qs
class YouTubeCrawler(BaseCrawler):
    model = VideoSubtitleDocument
    def __init__(self)->None:
        super().__init__()
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
            # video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
            # logger.debug(f"Video transcript extracted: {video_transcript}")
            # #continuous_string = " ".join(item['text'] for item in video_transcript)
            # logger.info(f"Video transcript extracted: {continuous_string}")
            logger.info(f"Video added to the database: {video_id}")
            #     "Title": YouTube(link).title,
            #     "Content": continuous_string    
            # }
            #print("data",data["Title"])
            #print(data)
            data = {
                "Title": "U",
                "Content": "U"
            }
            instance = self.model(
            )
            instance = self.model(
                platform="youtube",
                content=data,
                link=link,  
            )
            print(link)
            instance.save()
            logger.info(f"Video added to the database: {video_id}")
        except Exception as e:
            logger.error(f"An error occurred while extracting transcript: " + {e})
        return 
        