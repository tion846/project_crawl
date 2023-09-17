# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import os
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings


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
        self.settings = get_project_settings()

        output_folder = self.settings.get("JSON_PIPELINE_OUTPUT_FOLDER")
        output_file = f"{spider.name}_items.json"
        output_file_path = os.path.join(os.getcwd(), output_folder, output_file)

        data = self.collection[spider.name]
        if len(data) > 0:
            self.file = open(output_file_path, "w")
            self.file.write(json.dumps(data))
            self.file.close()
            self.collection[spider.name] = []

    def process_item(self, item, spider):
        collects = self.collection[spider.name]
        collects.append(ItemAdapter(item).asdict())
        return item
