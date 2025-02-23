# -*- coding: UTF-8 -*-
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    Log处理
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
import logging
from logging import handlers
import re

class Logger(object):
    #日志级别关系映射
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(
        self,
        filename,
        log2Screen='Y',
        level='info',
        when='D',
        backCount=7,
        fmt='%(asctime)s - %(levelname)s: %(message)s'):

        self.logger = logging.getLogger()

        # 将当前文件的handlers清空
        self.logger.handlers = []
        # 然后再次移除当前文件logging配置
        self.logger.removeHandler(self.logger.handlers)

        #设置日志格式
        format_str = logging.Formatter(fmt)

        #设置日志级别
        self.logger.setLevel(self.level_relations.get(level))

        #往屏幕上输出
        if log2Screen == 'Y':
            sh = logging.StreamHandler()
            #设置屏幕上显示的格式
            sh.setFormatter(format_str)
            #把对象加到logger里
            self.logger.addHandler(sh)

        # log_path = "/logs/log"

        #往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #   interval: 时间间隔
        #   backupCount: 备份文件的个数，如果超过这个个数，就会自动删除
        #   when: 间隔的时间单位，单位有以下几种：
        #        日志轮转的时间间隔，可选值为 ‘S’、‘M’、‘H’、‘D’、‘W’ 和 ‘midnight’，分别表示秒、分、时、天、周和每天的午夜；
        #        默认值为 ‘midnight’，即每天的午夜轮转，值不区分大小写；
        #        log会自动轮转，当天log默认为log（不带后缀名），日期变更，则自动轮转
        th = handlers.TimedRotatingFileHandler(
            # filename="D:/16_tecjt_projects/智能测试/03.source/01_app/current/logs/log",
            # filename=filename + log_path,
            filename=filename,
            when=when,
            interval=1,
            backupCount=backCount,
            encoding='utf-8')
        th.suffix = "%Y-%m-%d.log"
        th.extMatch = r"^\d{4}-\d{2}-\d{2}.log$"
        th.extMatch = re.compile(th.extMatch)
        #设置文件里写入的格式
        th.setFormatter(format_str)
        #把对象加到logger里
        self.logger.addHandler(th)

    def getlog(self):
        return self.logger

    # # 重写以下方法，且每次记录后清除logger
    # def info(self,message=None):
    #     self.__init__()
    #     self.logger.info(message)
    #     self.logger.removeHandler(self.logger.handlers)

    # def debug(self,message=None):
    #     self.__init__()
    #     self.logger.debug(message)
    #     self.logger.removeHandler(self.logger.handlers)

    # def warning(self,message=None):
    #     self.__init__()
    #     self.logger.warning(message)
    #     self.logger.removeHandler(self.logger.handlers)

    # def error(self,message=None):
    #     self.__init__()
    #     self.logger.error(message)
    #     self.logger.removeHandler(self.logger.handlers)

    # def critical(self, message=None):
    #     self.__init__()
    #     self.logger.critical(message)
    #     self.logger.removeHandler(self.logger.handlers)

# if __name__ == '__main__':
#     log = Logger(filename='.', log2Screen='Y').getlog()
#     log.debug('调试')
#     log.info('消息')
#     log.warning('警告')
#     log.error('报错')
#     log.critical('严重')