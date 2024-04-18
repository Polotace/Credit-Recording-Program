import os
import datetime
from flask import Flask, render_template
from typing import Literal, Optional
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


# 彩色输出化
class Color:
    Default = "\033[0m"
    Black = "\033[0;30m"
    Red = "\033[0;31m"
    Green = "\033[0;32m"
    Yellow = "\033[0;33m"
    Blue = "\033[0;34m"
    Fuchsia = "\033[0;35m"  # 紫红色
    Ultramarine = "\033[0;36m"  # 青蓝色
    Gray = "\033[0;37m"


class ColorPrint:
    @staticmethod
    def getFormat(level: str = Literal['INFO', 'WARN', 'ERROR', 'CRITICAL']) -> str:
        color: Optional[str] = None
        lv: Optional[str] = None
        lv_zh: Optional[str] = None
        match level:
            case 'INFO':
                color = Color.Green
                lv = level
                lv_zh = '信息'
            case 'WARN':
                color = Color.Yellow
                lv = level
                lv_zh = '警告'
            case 'ERROR':
                color = Color.Red
                lv = level
                lv_zh = '错误'
            case 'CRITICAL':
                color = Color.Fuchsia
                lv = level
                lv_zh = '致命'
            case _:
                print(f"{Color.Red}ColorPrint出现错误{Color.Default}")
        color_format = "{Default}[{Time}] {color}{lv}{Default}|{color}{lv_zh} {Default}: {color}{msg}{Default}".format(
            Default=Color.Default, msg='{msg}', color=color, lv=lv, lv_zh=lv_zh,
            Time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return color_format

    def info(self, msg: str):
        out_stream = self.getFormat('INFO').format(msg=msg)
        print(out_stream, end='\n')

    def warn(self, msg: str):
        out_stream = self.getFormat('WARN').format(msg=msg)
        print(out_stream, end='\n')

    def error(self, msg: str):
        out_stream = self.getFormat('ERROR').format(msg=msg)
        print(out_stream, end='\n')

    def critical(self, msg: str):
        out_stream = self.getFormat('CRITICAL').format(msg=msg)
        print(out_stream, end='\n')


"""程序前置检查"""
log = ColorPrint()
exist_files = (os.path.exists('templates/'), os.path.exists('static/'))
if exist_files == (False, False):
    if not os.path.exists('学分记录'):
        log.warn('未在程序所在文件夹内找到程序文件夹')
    else:
        log.error('请将程序(.exe)移动至程序文件夹(默认为"学分记录")中')
        exit(0)
    log.info('即将从网络下载程序前置文件...是否继续？')
    loop: bool = True
    while loop:
        input(f"{Color.Ultramarine}按下Enter键后开始下载...{Color.Default}")


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 9999), app, log=None)
    server.serve_forever()
