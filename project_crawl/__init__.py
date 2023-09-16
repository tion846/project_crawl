import os
from time import gmtime, strftime
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


def check_folder_exists(folder):
    """ check folder is exists, if not create folder """
    folder_path = os.path.join(os.getcwd(), folder)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


settings = get_project_settings()

logging_folder = settings.get("LOG_FILE_FOLDER")
check_folder_exists(logging_folder)

output_folder = settings.get("JSON_PIPELINE_OUTPUT_FOLDER")
check_folder_exists(output_folder)

log_file_name = strftime("%Y%m%d", gmtime())
logging_setting = {
    "LOG_FILE": f"{logging_folder}\\{log_file_name}.txt"
}
configure_logging(logging_setting)
