
import yt_dlp
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
import os
import sys
import subprocess
from yt_dlp import YoutubeDL
import csv
import re
from typing import Optional, Dict


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

class YouTubeDownloader:
    """
    A class for downloading YouTube videos.
    """

    @staticmethod
    def download_playlist_as_csv(playlist_url, output_file="playlist.csv"):
        ydl_opts = {'quiet': True, 'extract_flat': True}
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(playlist_url, download=False)
            if 'entries' in result:
                entries = result['entries']
                with open(output_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=["Title", "URL", "ID"])
                    writer.writeheader()
                    for entry in entries:
                        writer.writerow({
                            "Title": entry.get("title"),
                            "URL": f"https://www.youtube.com/watch?v={entry.get('id')}",
                            "ID": entry.get("id")
                        })
                print(f"Playlist details saved to {output_file}")

                
    @staticmethod
    def download_youtube(link, data_product_id, environment, output_dir=None):
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("download_youtube"):
            try:
                logger.info(f"output_dir:{output_dir}")
                output_template = '%(title)s.%(ext)s'
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                    output_template = os.path.join(output_dir, output_template)

                ydl_opts = {
                    'format': 'bv*+ba/b',
                    'outtmpl': output_template,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=True)
                    filename = ydl.prepare_filename(info)
                    return filename

            except Exception as ex:
                error_msg = f"Error: {str(ex)}"
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def clean_filename(title: str) -> str:
        """
        Clean filename to be safe for all operating systems
        """
        # Remove or replace unsafe characters
        title = re.sub(r'[<>:"/\\|?*]', '', title)
        # Replace spaces with underscores
        title = title.replace(' ', '_')
        # Remove any consecutive underscores
        title = re.sub(r'_+', '_', title)
        # Convert to lowercase
        title = title.lower()
        # Remove leading/trailing underscores
        title = title.strip('_')
        return title

    @staticmethod
    def _get_ydl_opts() -> dict:
        """Get default yt-dlp options"""
        return {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
    @classmethod
    def get_video_info(cls, url: str) -> Optional[Dict]:
        """Extract metadata for a single video"""
        try:
            with yt_dlp.YoutubeDL(cls._get_ydl_opts()) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'video_id': info.get('id', ''),
                    'title': info.get('title', ''),
                    'channel_id': info.get('channel_id', ''),
                    'channel': info.get('channel', ''),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'comment_count': info.get('comment_count', 0),
                    'duration': info.get('duration', 0),
                    'upload_date': info.get('upload_date', ''),
                    'description': info.get('description', ''),
                    'tags': ','.join(info.get('tags', [])),
                    'categories': ','.join(info.get('categories', [])),
                    'webpage_url': info.get('webpage_url', ''),
                    'average_rating': info.get('average_rating', 0),
                }
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return None
    
    @classmethod
    def download_youtube_captions(cls, link, data_product_id, environment, output_dir=None, language="en"):
        """
        Download YouTube captions using yt-dlp.

        :param video_url: URL of the YouTube video.
        :param output_dir: Directory to save the captions file.
        :param language: Language code for the captions (default: 'en').
        :return: Path to the downloaded captions file or an error message.
        """
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()
        
        with tracer.start_as_current_span("download_youtube_captions"):
                    
            try:
                # First get video info to clean the title
                with YoutubeDL({'quiet': True}) as ydl:
                    info_dict = ydl.extract_info(link, download=False)
                    original_title = info_dict['title']
                    clean_title = cls.clean_filename(original_title)
                    
                # Configure options with clean title template
                options = {
                    'skip_download': True,
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitleslangs': ['en'],
                    'subtitlesformat': 'srt',
                    'outtmpl': os.path.join(output_dir, clean_title + '.%(ext)s'),
                    'quiet': True,
                    'no_warnings': True
                }

                with YoutubeDL(options) as ydl:
                    # Download captions using clean title
                    ydl.download([link])
                    
                    # Check for caption file with clean name
                    caption_path = os.path.join(output_dir, f"{clean_title}.en.vtt")
                    
                    if os.path.exists(caption_path):
                        logger.info(f"Captions downloaded successfully: {caption_path}")
                        return caption_path
                    
                    # Fallback: look for any caption file that matches the clean title
                    dir_contents = os.listdir(output_dir)
                    matching_files = [
                        f for f in dir_contents 
                        if f.startswith(clean_title) and f.endswith('.srt')
                    ]
                    
                    if matching_files:
                        actual_path = os.path.join(output_dir, matching_files[0])
                        logger.info(f"Captions found at: {actual_path}")
                        return actual_path
                    
                    logger.info(f"No captions available for video: {original_title}")
                    return None
            
            except Exception as ex:
                error_msg = f"Error downloading captions: {str(ex)}"
                exc_info = sys.exc_info()
                logger.error(error_msg, exc_info=exc_info)
                return None