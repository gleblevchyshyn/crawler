import json
from itemadapter import ItemAdapter
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ShopCrawlerPipeline:
    def __init__(self):
        self.my_json_file = None

    def open_spider(self, spider):
        self.my_json_file = open('output.jsonl', 'w')

    def close_spider(self, spider):
        self.my_json_file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.my_json_file.write(line)
        return item
