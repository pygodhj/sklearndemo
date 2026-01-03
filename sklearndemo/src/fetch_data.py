from __future__ import annotations
import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional
import pandas as pd
from sklearndemo.database_models.database_operate import DatabaseOperate
import json
from sklearndemo import __path__ as sklearndemo_path


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
    def export_data(cls,df:pd.DataFrame(),**kwargs):
        target_dir = cls.get_dir()
        ext=input(r"请输入储存格式[sql\csv\xlsx]：")
        try:
            if ext =="sql":
                table_name = input("请输入要创建的表名：")
                data = DatabaseOperate()
                df.to_sql(table_name,data.engine,if_exists='append',**kwargs)
                data.get_table_names()
                data.query_sql_columns(table_name)
            elif  ext =="csv":
                table_name = input("请输入要创建的表名：")
                target_path =os.path.join(target_dir,f"{table_name}.csv")
                df.to_csv(target_path ,encoding='utf-8',mode='a',**kwargs)
            elif ext == "xlsx":
                table_name = input("请输入要创建的表名：")
                target_path = os.path.join(target_dir,f"{table_name}.xlsx")
                df.to_excel(target_path,engine='openpyxl',**kwargs)
            else:
                raise ValueError(f"不支持的文件格式：{ext}")
        except Exception as e:
            raise RuntimeError(f"输出文件失败：{e}")

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

    @classmethod
    def get_dir(cls):
        """从配置文件中获取数据目录的绝对路径"""
        # 1. 定义配置文件的路径
        current_script_path = sklearndemo_path[0]
        root_dir = os.path.dirname(current_script_path)
        config_path = os.path.join(root_dir, "config.json")

        # 2. 读取配置文件
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            # 3. 获取相对路径并构建绝对路径
            relative_data_dir = config.get("data_raw_dir", "data")
            absolute_data_dir = os.path.join(root_dir, relative_data_dir)

            return absolute_data_dir

        except FileNotFoundError:
            print(f"警告: 配置文件 '{config_path}' 未找到。")
            # 返回一个默认路径作为后备
            return os.path.join(root_dir, "data", "raw")




if __name__=="__main__":
    df=FetchedData.fetch_database()
    FetchedData.export_data(df)
