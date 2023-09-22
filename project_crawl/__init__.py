from scrapy.utils.project import get_project_settings
from project_crawl.share.utils import init_folder_path


settings = get_project_settings()

logging_folder = settings.get("LOG_FILE_FOLDER")
init_folder_path(logging_folder)

output_folder = settings.get("JSON_PIPELINE_OUTPUT_FOLDER")
init_folder_path(output_folder)
