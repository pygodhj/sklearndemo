import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional
import pandas as pd


#类名含义为获取的数据类，实例化对象为每个新获取的数据
class FetchedData:
    #从文件中获取数据的方法
    @classmethod
    def fetch_file(cls)->pd.DataFrame():
        path=cls.__file_selector()
        pass

    #从数据库中获取数据的方法
    @classmethod
    def fetch_database(cls)->pd.DataFrame():
        pass

    #从网络中获取数据的方法
    @classmethod
    def fetch_internet(cls)->pd.DataFrame():
        pass

    #导出数据到文件或数据库的方法
    @classmethod
    def export_data(cls,df:pd.DataFrame(),ext):
        pass

    #调用选取文件的窗口，并选取文件导出文件路径的方法（内部私有函数）
    @classmethod
    def __file_selector(cls)->os.path:
        pass