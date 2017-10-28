from yixun.items import init_sparkle_data_item
from yixun.items import init_caas_data_item
from yixun.spiders.super.super_spider import SuperSpider


class SuperDataSpider(SuperSpider):

    def init_task(self, data):
        if 'sparkle' in data.get('task_type'):
            task = init_sparkle_data_item(data)
        elif 'caas' in data.get('task_type'):
            task = init_caas_data_item(data)
        return task