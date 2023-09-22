# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from project_crawl.share.utils import print_line
from scrapy.utils.project import get_project_settings
from time import localtime, strftime
import logging
import json
import os


class ProjectCrawlPipeline:
    def process_item(self, item, spider):
        return item


# https://docs.scrapy.org/en/latest/topics/item-pipeline.html#write-items-to-a-json-lines-file
# https://stackoverflow.com/questions/14075941/how-to-access-scrapy-settings-from-item-pipeline
class JsonWriterPipeline:
    collection = {}

    def open_spider(self, spider):
        self.collection[spider.name] = []

    def close_spider(self, spider):
        data = self.collection[spider.name]

        if len(data) > 0:
            format_time = strftime("%H%M%S", localtime())
            self.settings = get_project_settings()
            output_folder = self.settings.get("JSON_PIPELINE_OUTPUT_FOLDER")
            output_file = f"{spider.name}_item-{format_time}.json"
            output_file_path = os.path.join(
                os.getcwd(),
                output_folder,
                output_file
            )

            self.file = open(output_file_path, "w", encoding="utf-8")
            self.file.write(json.dumps(data))
            self.file.close()
            self.collection[spider.name] = []
        else:
            message = f"[{spider.name}] data collection is empty!"
            logging.error(message)
            print_line(message)

    def process_item(self, item, spider):
        collects = self.collection[spider.name]

        if isinstance(item, dict):
            collects.append(item)
        else:
            collects.append(ItemAdapter(item).asdict())

        return item
