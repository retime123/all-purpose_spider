# from Bourse.items import init_sparkle_comment_item
from Bourse.spiders.super.super_spider import SuperSpider


class SuperCommentSpider(SuperSpider):

    def init_task(self, data):
        if 'sparkle' in data.get('task_type'):
            task = init_sparkle_comment_item(data)
            return task
