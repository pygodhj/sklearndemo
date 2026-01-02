import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional
import pandas as pd
from database_models.database_operate import DatabaseOperate


#类名含义为获取的数据类，实例化对象为每个新获取的数据
class FetchedData:


    #从文件中获取数据的方法
    @classmethod
    def fetch_file(cls,**kwargs)->pd.DataFrame():
        file_path=cls.__file_selector()
        ext = os.path.splitext(file_path)[1].lower()

        # 根据文件后缀读取相应数据
        try:
            if ext in [".csv", ".txt"]:
                return pd.read_csv(file_path, **kwargs)
            elif ext in [".xlsx", ".xls"]:
                return pd.read_excel(file_path, **kwargs)
            elif ext == ".json":
                return pd.read_json(file_path, **kwargs)
            elif ext == ".parquet":
                return pd.read_parquet(file_path, **kwargs)
            elif ext == ".pkl":
                return pd.read_pickle(file_path, **kwargs)
            else:
                raise ValueError(f"不支持的文件格式：{ext}")
        except Exception as e:
            raise RuntimeError(f"读取文件失败：{e}")

    #从数据库中获取数据的方法
    @classmethod
    def fetch_database(cls)->pd.DataFrame():
        data=DatabaseOperate()
        tablename=input("请输入数据库表名：")
        data.query_sql_columns(tablename)
        df=pd.read_sql(f"SELECT * FROM {tablename}",data.engine).drop('id', axis=1)
        return df

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
    def __file_selector(cls, single_file: bool = True) -> Optional[str | tuple]:
        """
               调出文件选择窗口
               param single_file: True选择单个文件，False选择多个文件
               return: 选中的文件路径（单个为字符串，多个为元组），取消则返回None
        """

        SUPPORTED_FORMATS = {
            ".csv": pd.read_csv, ".txt": pd.read_csv,
            ".xlsx": pd.read_excel, ".xls": pd.read_excel,
            ".json": pd.read_json, ".parquet": pd.read_parquet,
            ".pkl": pd.read_pickle, ".pickle": pd.read_pickle
        }

        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口，只显示文件选择框
        supported_exts = " ".join([f"*{ext}" for ext in SUPPORTED_FORMATS.keys()])
        # 正确的file_types格式：[(类型名称, 后缀通配符), ...]
        file_types = [
            ("支持的文件", supported_exts),  # 拼接后的通配符字符串
            ("所有文件", "*.*")
        ]

        try:
            if single_file:
                # 选择单个文件
                file_path = filedialog.askopenfilename(
                    title="选择单个文件",
                    filetypes=file_types
                )
                return file_path if file_path else None
            else:
                # 选择多个文件
                file_paths = filedialog.askopenfilenames(
                    title="选择多个文件",
                    filetypes=file_types
                )
                return file_paths if file_paths else None
        finally:
            root.destroy()  # 销毁窗口，释放资源


if __name__=="__main__":
    print(FetchedData.fetch_database())
