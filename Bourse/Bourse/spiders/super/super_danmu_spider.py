# from Bourse.items import init_sparkle_danmu_item
from Bourse.spiders.super.super_spider import SuperSpider


class SuperDanmuSpider(SuperSpider):

    def init_task(self, data):
        if 'sparkle' in data.get('task_type'):
            task = init_sparkle_danmu_item(data)
            return task
