# -*- coding: utf-8 -*-
import sys
import json
import asyncio
import platform
import datetime
import traceback
import redis

import settings
from tools.logger import logger
from tools import db
from tools.tool import send_mail
from tools.tool import write_log
from tools.tool import execute_mysql_insert
from tools.tool import new_sshclient_execmd as sshclient_execmd
from tools.tool import aiorequest

'''
- 功能 -
1.正式服务器环境下,传参，settings里面的机器一键启动/停止
# 2.git模式----> 判断spider进程>>>删除文件>>>然后下拉git
'''

class WatchStatus(object):

    summary_all = 0
    summary_success = 0
    summary_fail = 0
    summary_report = []
    summary_error_count = {}

    def __init__(self,  prefix=None, role=None, task_type=None, platform_id=None, debug=0):
        self.redis_conn = redis.Redis(connection_pool=db.MyRedis())

        self.logger = logger()

        self.prefix = prefix
        self.role = role
        self.task_type = task_type

        self.platform_id = platform_id

        self.rerun_count = settings.RERUN_COUNT

        self.wait_end_time = settings.WAIT_END_TIME

        self.wait_no_growth_count = settings.WAIT_NO_GROWTH_COUNT

        self.loop = asyncio.get_event_loop()

        self.errorstatus_name_map = settings.ERRORSTATUS_NAME_MAP

        # self.platform_name = settings.PLATFORMID_NAME_MAP

        self.start_time = datetime.datetime.now()

        self.debug = debug

    # # 发送汇总报告
    # def send_summay_report(self):
    #     error_type_str = ''
    #     for k in self.summary_error_count:
    #         error_type_str = error_type_str + k + ' ' + str(self.summary_error_count[k]) + ' 条  #  '
    #
    #     result_mail = 'redis总任务：  {}  成功数：  {}  失败数：  {} ({})'.format(
    #         self.summary_all, self.summary_success, self.summary_fail, error_type_str)
    #
    #     for elm in self.summary_report:
    #         result_mail = result_mail + '\n' + elm
    #     email_title = '{}_{}_{}_爬虫运行报告'.format(datetime.datetime.now().strftime('%Y-%m-%d'), self.prefix, self.task_type)
    #     send_mail(email_title, result_mail, to_addrs=self.get_mail_receiver())

    # 主函数
    def run(self):
        # 启动spider
        if platform.uname()[1] in settings.SERVERS:
            if self.role in ['git_pull']:
                self.git_pull()
            elif self.task_type in ['day_data', 'RT_data']:
                if self.role == 'start':
                    self.start_spider()
                elif self.role in ['shut']:
                    self.shut_spider()
                else:
                    print('参数错误...{}'.format(self.role))
            else:
                print('参数错误...{}'.format(self.role))
        else:
            print('不再settings内，直接启动 start_spider.py文件！！！')
        # # 异步的向redis中压任务
        # tasks = []
        # for pid in self.platform_id:
        #     tasks.append(self.watch_task(pid, self.task_type))
        # #
        # try:
        #     # 开始执行异步任务
        #     self.loop.run_until_complete(asyncio.wait(tasks))
        #
        #     # # 发送汇总报告
        #     # self.send_summay_report()
        #
        #     # 删除redis中的键
        #     self.delete_redis_key()
        #
        #     # 关闭spider
        #     if platform.uname()[1] in settings.SERVERS:
        #         self.shut_spider()
        #
        #     # 其他自定义操作
        #     self.custom_operation()
        # except KeyboardInterrupt:
        #     self.logger.info('手动退出')
        #     exit(0)

    # 启动所有spider
    def start_spider(self):
        servers = None
        if self.task_type == 'day_data':
            servers = settings.SERVERSa
        elif self.task_type == 'RT_data':
            servers = settings.SERVERSb
        server_param = settings.SERVER_PARAM
        for key in servers:
            sshclient_execmd(
                host=server_param[key], execmd='start-{} {} {}-worker'.format(self.prefix, self.task_type, self.debug))

    # 关闭所有spider
    def shut_spider(self):
        servers = None
        if self.task_type == 'day_data':
            servers = settings.SERVERSa
        elif self.task_type == 'RT_data':
            servers = settings.SERVERSb
        server_param = settings.SERVER_PARAM
        for key in servers:
            sshclient_execmd(
                host=server_param[key], execmd='shut-{} {} {}-worker'.format(self.prefix, self.task_type, self.debug))

    # git pull
    def git_pull(self):
        servers = settings.SERVERS
        server_param = settings.SERVER_PARAM
        for key in servers:
            sshclient_execmd(
                host=server_param[key],
                execmd='git_pull')



    # 清空redis中残留的键
    def delete_redis_key(self):
        pipeline = self.redis_conn.pipeline()
        for redis_key in self.redis_conn.keys('{}_{}_*'.format(self.prefix, self.task_type)):
            pipeline.delete(redis_key)
        delete_result = pipeline.execute()
        if delete_result:
            self.logger.info('删除redis中所有{}_{}任务成功'.format(self.prefix, self.task_type))
        else:
            self.logger.info('删除redis中所有{}_{}任务失败'.format(self.prefix, self.task_type))

    async def watch_task(self, platform_id, task_type):
        last_items_num = 0
        wait_end_time = 0
        no_growth_num = 0
        last_errors_num = 0
        rerun_num = 0
        try:
            while True:
                items_num = self.redis_conn.hlen(self.get_redis_key(platform_id, 'items'))
                errors_num = self.redis_conn.llen(self.get_redis_key(platform_id, 'errors'))
                norun_tasks_num = self.redis_conn.llen(self.get_redis_key(platform_id, 'tasks'))

                if wait_end_time >= 40:
                    send_mail(self.get_redis_key(platform_id, 'tasks') + '阻塞,强制关闭',
                              '该渠道已阻塞{}分钟,强制关闭'.format(wait_end_time),
                              to_addrs=self.get_mail_receiver())
                    await self.make_report(platform_id, task_type)
                    break
                # 如果所有任务都跑完了,并且过了等待时间,开始做处理
                if norun_tasks_num == 0 and wait_end_time >= self.wait_end_time:
                    remain_num = self.redis_conn.hlen(self.get_redis_key(platform_id, 'remains'))
                    self.logger.info('{} 第{}次抓取 剩余任务{}条 失败任务{}条 上次失败任务{}条'.format(
                        self.get_redis_key(platform_id, 'task'), rerun_num + 1, remain_num, errors_num, last_errors_num))

                    # 优酷的任务/无剩余任务/失败数等于剩余数并且等于上次失败数/超过重跑次数   以上情况发送报告
                    if remain_num == 0 or (remain_num == errors_num and last_errors_num == errors_num) or rerun_num >= self.rerun_count or self.task_type == 'sparkle_hot':
                        await self.make_report(platform_id, task_type)
                        break
                    else:
                        rerun_num += 1
                        last_errors_num = errors_num
                        last_items_num = 0

                        pipeline = self.redis_conn.pipeline()

                        pipeline.delete(self.get_redis_key(platform_id, 'errors'))

                        remain_tasks = self.redis_conn.hvals(self.get_redis_key(platform_id, 'remains'))
                        for task in remain_tasks:
                            pipeline.rpush(self.get_redis_key(platform_id, 'tasks'), task)
                            self.logger.info('重跑任务: {}'.format(str(task)))
                        pipeline.execute()

                if last_items_num == items_num and (last_items_num != 0 or rerun_num != 0):
                    wait_end_time += 1
                    self.logger.info(
                        '{} 上次：{} 这次：{} 当前等待{}分钟'.format(self.get_redis_key(platform_id, 'tasks'),
                                                         last_items_num, items_num, wait_end_time))
                else:
                    wait_end_time = 0
                item_per_mim = items_num - last_items_num
                try:
                    task_num = int(
                        self.redis_conn.lrange(self.get_redis_key(platform_id, 'count'), 0, 0)[0].decode(
                            'utf-8'))
                    # 如果没有数据,直接结束
                    if task_num == -1:
                        break
                except Exception:
                    task_num = 0
                message = '{} 总任务：{} 条，现已抓取：{} 条， {}/min 失败：{} 条'
                self.logger.debug(
                    message.format(self.get_redis_key(platform_id, 'tasks'), task_num, items_num,
                                   item_per_mim, errors_num))
                last_items_num = items_num
                # 反爬或改版预警
                if item_per_mim < 50:
                    no_growth_num += 1
                else:
                    no_growth_num = 0
                if no_growth_num == self.wait_no_growth_count:
                    if self.task_type == 'sparkle_hot':
                        break
                    if self.redis_conn.hlen(self.get_redis_key(platform_id, 'items')):
                        send_mail(self.get_redis_key(platform_id, 'tasks') + '被反爬', '{}分钟前该渠道被严重反爬'.format(self.wait_no_growth_count),
                                  to_addrs=self.get_mail_receiver())
                    else:
                        send_mail(self.get_redis_key(platform_id, 'tasks') + '有改版的可能', '{}分钟内此渠道未抓到任何数据'.format(self.wait_no_growth_count),
                                  to_addrs=self.get_mail_receiver())

                await asyncio.sleep(60)

        except Exception:
            exc_type, exc_instance, exc_traceback = sys.exc_info()
            formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
            message = '\n{0}\n{1}:\n{2}'.format(
                formatted_traceback,
                exc_type.__name__,
                exc_instance
            )
            self.logger.error(exc_type(message))

    def get_mail_receiver(self):
        return settings.REPORT_RECEIVER

    def mark_error_task(self, task, video_ids, task_type):
        if task.get('error_status')[0] in [-300, 404]:
            video_ids.append(task.get('id'))
        # else:
        #     temp_task = {}
        #     temp_task['id'] = task.get('id')
        #     temp_task['cp_id'] = task.get('cp_id')
        #     temp_task['platform_id'] = task.get('platform_id')
        #     temp_task['url'] = task.get('url')
        #     temp_task['extra'] = task.get('extra')
        #     temp_task['extra_id'] = task.get('extra_id')
        #     write_log(json.dumps(temp_task),
        #               filename='{}_{}_fail'.format(self.platform_name.get(int(task.get('platform_id'))).get('English'), task_type), has_hour=False)

    def append_error_count(self, task, error_count):
        error_status = int(task.get('error_status')[0])
        if error_status in error_count:
            error_count[error_status].append(task)
        else:
            error_count[error_status] = [task]

    async def make_report(self, platform_id, task_type):
        items_num = self.redis_conn.hlen(self.get_redis_key(platform_id, 'items'))
        errors_num = self.redis_conn.hlen(self.get_redis_key(platform_id, 'remains'))
        try:
            video_num = int(self.redis_conn.lpop(self.get_redis_key(platform_id, 'count')).decode('utf-8'))
        except Exception:
            video_num = 0
        try:
            db_num = int(self.redis_conn.lpop(self.get_redis_key(platform_id, 'count_db')).decode('utf-8'))
        except Exception:
            db_num = 0

        mess_list = ['{} 开始运行，用时 {} 分'.format(self.start_time.strftime('%H:%M:%S'), (datetime.datetime.now() - self.start_time).seconds // 60)]
        message = '{}  #  数据库中总任务: {} 条，redis压入: {} 条，成功任务: {} 条，失败任务: {} 条'.format(
            self.get_redis_key(platform_id, 'tasks'), db_num, video_num, items_num, errors_num)
        mess_list.append(message)

        self.summary_all += video_num
        self.summary_success += items_num
        self.summary_fail += errors_num

        send_message = '\n'.join(mess_list)
        self.logger.debug(send_message)

        if platform.uname()[1] == settings.MASTER_SERVER:
            email_title = '{}运行报告'.format(self.get_redis_key(platform_id, 'tasks'))
        else:
            email_title = '{}测试运行报告'.format(self.get_redis_key(platform_id, 'tasks'))

        video_ids = []
        error_count = {}
        for elm in self.redis_conn.lrange(self.get_redis_key(platform_id, 'errors'), 0, -1):
            task = json.loads(elm.decode('utf-8'))
            self.append_error_count(task, error_count)

        mess_list.append('------------------------------------------------------------------------')

        errors_str = ''
        if error_count:
            for k in error_count:
                error_message = '{} {} 条'.format(self.errorstatus_name_map.get(k) or k, len(error_count[k]))
                self.summary_error_count[(self.errorstatus_name_map.get(k) or k)] = self.summary_error_count.get(
                    (self.errorstatus_name_map.get(k) or k), 0) + len(error_count[k])
                errors_str = errors_str + error_message + '  #  '
                mess_list.append(error_message)
            mess_list.append('------------------------------------------------------------------------')
            for k in error_count:
                for error in error_count[k]:
                    mess_list.append(error.get('error_message'))
                    self.mark_error_task(error, video_ids, task_type)
        if errors_str:
            errors_str = '(' + errors_str.strip(' #') + ')'
        self.summary_report.append(message + errors_str)

        if video_ids:
            self.logger.info('{} mark error videos : {}'.format(
                self.get_redis_key(platform_id, 'tasks'), video_ids))
            write_log('{} {}'.format(self.platform_name.get(str(platform_id)), str(video_ids)), filename='post_ids')
            await self.process_invalid_video(video_ids)
        send_message = '\n'.join(mess_list)
        if errors_num:
            send_mail(email_title, send_message, to_addrs=self.get_mail_receiver())
        self.generate_data_exception_report(platform_id, self.redis_conn.hvals(
                            self.get_redis_key(platform_id, 'exceptions')))

    def generate_data_exception_report(self, platform_id, error_list):
        temp_list = []
        for elm in error_list:
            task = json.loads(elm.decode('utf-8'))
            temp_list.append('Database_id: {} # {} {} {} {} url: {}'.format(task.get('id'), task.get('play_error'),
                                                                          task.get('comment_error'), task.get('up_error'), task.get('down_error'), task.get('url')))

        content = '\n'.join(temp_list)
        if len(temp_list):
            send_mail('{}数据抓取异常'.format(self.get_redis_key(platform_id, 'tasks')), content, to_addrs=self.get_mail_receiver())

    # 获取redis key
    def get_redis_key(self, platform_id, suffix):
        return '{}_{}_{}_{}'.format(
            self.prefix, self.task_type, self.platform_name.get(int(platform_id)).get('English'), suffix)

    def custom_operation(self):
        if 'sparkle_data' == self.task_type:
            # 正式服务器跑完任务给php发标记信息
            if platform.uname()[1] == settings.MASTER_SERVER:
                insert_sql = "INSERT INTO `huox_task_order` (`type`,`status`,`finish_date`,`quantity`) " \
                             "VALUES ('pytn_video_data','1','{}',1) " \
                             "ON DUPLICATE KEY UPDATE `status` = 1, `finish_time` = '{}' , `quantity` = `quantity` + 1".format(
                    datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%Y-%m-%d'))
                execute_mysql_insert(insert_sql, debug=self.debug)

    async def process_invalid_video(self, video_ids):
        if 'sparkle' in self.task_type:
            # 每次处理1000个id
            start_index = 0
            while start_index < len(video_ids):
                # await aiorequest(url=settings.MARK_STATUS_URL, loop=self.loop,
                #                  data={'video_ids[]': video_ids[start_index:start_index + 1000]})
                update_sql = 'update huox_video set `status` = 0 where id in ({})'.format(', '.join([str(elm) for elm in video_ids[start_index:start_index + 1000]]))
                execute_mysql_insert(update_sql, debug=self.debug)
                start_index += 1000
        elif 'caas' in self.task_type:
            database = caas_conf.MONGODB_DBNAME
            videos_table = caas_conf.MONGODB_VIDEOS_TABLE
            # 每次处理1000个id
            for video_id in video_ids:
                loop_result = db.MyMongodb(debug=self.debug)[database][videos_table].find_one({'id': video_id}, {'loop': 1, '_id': 0})
                loop = int(loop_result.get('loop') + 1)
                if loop >= 6:
                    db.MyMongodb(debug=self.debug)[database][videos_table].update({'id': video_id},
                                                                  {'$set': {'status': 0, 'loop': loop}})
                else:
                    db.MyMongodb(debug=self.debug)[database][videos_table].update({'id': video_id}, {'$set': {'loop': loop}})


def get_params(prefix, role, task_type, platform_id, debug):
    if platform_id == '[]':
        if 'day_data' in task_type:
            platform_id = [160, 170, 180]
        elif 'RT_data' in task_type:
            platform_id = [160, 170, 180]
    else:
        plist = []
        for elm in platform_id.strip('[]').split(','):
            plist.append(int(elm))
        platform_id = plist

    return prefix, role, task_type, platform_id, int(debug)


if __name__ == '__main__':
    '''
            - 启动参数 -
            :正式环境为服务器环境，settings里面的服务器机型才能启动正式环境
            :param 启动方式: 

            :param 其他电脑: python3 start_spider
        '''


    # 正式环境运行此代码
    if platform.uname()[1] in settings.SERVERS:
        '''
        :param spider启动:python3 watch_status.py start day_data
        :param spider停止:python3 watch_status.py shut day_data
        :param git下拉:python3 watch_status.py git_pull data
        '''
        prefix, role, task_type, platform_id, debug = get_params(1, sys.argv[1], sys.argv[2], '[]', 0)
    # 本机环境运行此代码
    else:
        prefix, role, task_type, platform_id, debug = get_params(2017, 'start', 'day_data', '[]', 0)

    pt = WatchStatus(prefix=prefix, role=role, task_type=task_type, platform_id=platform_id, debug=debug)
    pt.run()
    '''
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log/%s.log' % (today,),
                    filemode='w')
                    '''