from datetime import datetime
from project_crawl.share.models import Base
from scrapy import Request
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from types import SimpleNamespace
import logging
import os
import sqlalchemy


# region http
"""This module contains the ``SeleniumRequest`` class"""


class CrawlRequest(Request):
    """Scrapy ``Request`` subclass providing additional arguments"""

    def __init__(self,
                 wait_time=None,
                 wait_until=None,
                 screenshot=False,
                 script=None,
                 before_response_callback=None,
                 *args,
                 **kwargs):
        """Initialize a new selenium request

        Parameters
        ----------
        wait_time: int
            The number of seconds to wait.
        wait_until: method
            One of the "selenium.webdriver.support.expected_conditions". The response
            will be returned until the given condition is fulfilled.
        screenshot: bool
            If True, a screenshot of the page will be taken and the data of the screenshot
            will be returned in the response "meta" attribute.
        script: str
            JavaScript code to execute.
        before_response_callback: method
            will be web driver execute script callback.
        """

        self.wait_time = wait_time
        self.wait_until = wait_until
        self.screenshot = screenshot
        self.script = script
        self.before_response_callback = before_response_callback

        super().__init__(*args, **kwargs)
# endregion


# region export method
def get_settings(name):
    """ get value from settings.py """
    return CrawlUtils.get_setting(name=name)


def get_db_connect_string():
    db_folder = get_settings("DB_FOLDER")
    db_name = get_settings("DB_NAME")
    db_connect_string = os.path.join(os.getcwd(), db_folder, db_name)
    return db_connect_string


def init_db_connect():
    """
    connect slqite db
    create db file if not exiest
    See https://stackoverflow.com/a/11599344
    """
    db_connect_string = get_db_connect_string()
    engine = create_engine(f"sqlite:///{db_connect_string}")

    # engine.connect() 建立連線, 產生{db_name}.db檔案
    # has_table() 建立不存在的Table
    with engine.connect() as connection:
        if not sqlalchemy.inspect(engine).has_table("Product"):
            Base.metadata.create_all(engine)


def init_folder_path(folder):
    """ make sure the folder path exist. """
    folder_path = os.path.join(os.getcwd(), folder)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def init_logging():
    """ use LOG_FILE_FOLDER from settings.py
        initial log output file path """
    CrawlUtils.init_logging()


def is_env_production():
    """ return True/False
        check ENVIRONMENT from settins.py is equal 'PRODUCTION' """
    return CrawlUtils.is_env_production()


def print_line(*args):
    """ print with time """
    CrawlUtils.print_line(*args)

# endregion


# region implement
""" implement CrawlUtils class """


class CrawlUtils():
    settings = get_project_settings()
    const_date_pattern = "%Y%m%d"
    const_datetime_pattern = "%Y-%m-%d %H:%M:%S"
    const_name_env = SimpleNamespace(Development="DEVELOPMENT",
                                     Production="PRODUCTION")

    @classmethod
    def get_setting(self, name):
        return self.settings.get(name=name)

    @classmethod
    def init_logging(self):
        logging_folder = self.settings.get("LOG_FILE_FOLDER")
        log_file_name = datetime.now().strftime(self.const_date_pattern)
        configure_logging(
            {"LOG_FILE": f"{logging_folder}\\{log_file_name}.txt"}
        )

    @classmethod
    def is_env_production(self):
        env = self.settings.get("ENVIRONMENT")
        return env == self.const_name_env.Production

    @classmethod
    def print_line(self, *args):
        time_format = datetime.now().strftime(self.const_datetime_pattern)
        print(f"[{time_format}]", *args)
        message = "".join(map(str, args))
        logging.debug(message)

# endregion
