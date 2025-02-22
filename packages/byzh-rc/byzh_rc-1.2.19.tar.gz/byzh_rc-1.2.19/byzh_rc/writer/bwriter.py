import time
from pathlib import Path
import os

from ..drawer.terminal import BColor
from ..basic import Byzh

COLOR_DICT = {
    "default": BColor.RESET,

    "black": BColor.BLACK,
    "red": BColor.RED,
    "green": BColor.GREEN,
    "yellow": BColor.YELLOW,
    "blue": BColor.BLUE,
    "purple": BColor.PURPLE,
    "cyan": BColor.CYAN,
    "silver": BColor.SILVER
}

class BWriter(Byzh):
    def __init__(self, file=None, ifTime=False, color='default'):
        '''
        :param file: 日志保存路径
        :param ifTime: 是否输出时间
        '''
        super().__init__()
        self.file = Path(file)
        self.ifTime = ifTime
        self.toWant_file = False
        self.toWant_cmd = False

        self.__checkColor(color)
        self.color = color

        self.f = None
        if self.file:
            self.__createDir(self.file)
            self.f = open(self.file, "a", encoding="utf-8")

    def setFile(self, file, ifTime=False):
        '''

        :param file: 设置log路径
        :param ifTime:
        :return:
        '''
        if self.f:
            self.f.close()
        self.file = file
        self.ifTime = ifTime
        self.f = open(self.file, "a", encoding="utf-8")

    def clearFile(self):
        '''
        清空内容
        :return:
        '''
        assert self.f is not None, "请先调用setFile方法"
        self.f.close()
        self.f = open(self.file, 'w', encoding="utf-8")

    def closeFile(self):
        '''
        关闭log
        :return:
        '''
        if self.f:
            self.f.close()
            self.f = None

    def toCmd(self, string, color=None):
        '''
        打印到terminal
        :param string:
        :param color:
        :return:
        '''
        # 检查color是否在字典中
        if color is None:
            print(COLOR_DICT.get(self.color) + string + BColor.RESET)
        else:
            assert color in COLOR_DICT, f"color参数错误，请输入{COLOR_DICT.keys()}"
            print(COLOR_DICT.get(color) + string + BColor.RESET)

    def toFile(self, string, ifTime=False):
        '''
        写入到文件内
        '''
        assert self.f is not None, "请先调用setFile方法"

        if ifTime or self.ifTime:
            t = time.strftime("%Y-%m-%d %H:%M:%S ##### ", time.localtime())
            self.f.write(t)

        self.f.write(string)
        self.f.write("\n")
        self.f.flush()

    def toBoth(self, string, ifTime=False, color=None):
        '''
        同时写入到文件和terminal
        :param string:
        :param color:
        :return:
        '''
        self.toFile(string, ifTime)
        self.toCmd(string, color)

    def setWant(self, toCmd=False, toFile=False):
        '''
        toWant的全局选项设置
        '''
        self.toWant_cmd = toCmd
        self.toWant_file = toFile

    def toWant(self, string, ifTime=False, color=None):
        '''
        使用前先调用setWant方法
        '''
        if self.toWant_cmd and self.toWant_file:
            self.toBoth(string, ifTime, color)
        elif self.toWant_cmd:
            self.toCmd(string, color)
        elif self.toWant_file:
            self.toFile(string, ifTime)
        else:
            raise Exception("请先调用setWant方法, 设置toCmd或toFile为True")

    def __checkColor(self, color):
        assert color in COLOR_DICT, f"color参数错误，请输入{list(COLOR_DICT.keys())}"

    def __createDir(self, path):
        # 获取到该文件的文件夹
        dir = path.parents[0]
        os.makedirs(dir, exist_ok=True)