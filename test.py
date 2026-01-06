#1、导入iris数据
# from sklearndemo.src.fetch_data import FetchedData
# from sklearn.datasets import load_iris
# import pandas as pd
#
# if __name__ == '__main__':
#     iris=load_iris()
#     iris_df_features = pd.DataFrame(
#         data=iris.data,
#         columns=iris.feature_names
#     )
#     FetchedData.export_data(iris_df_features)
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float

#2、删除多余数据库表格
# from sklearndemo.database_models.database_operate import DatabaseOperate
# if __name__ == '__main__':
#     db = DatabaseOperate()
#     tablename=input("请输入要删除的表名：")
#     db.delete_sql(tablename)
#     db.get_table_names()

#3、去除表格中重复数据
from sklearndemo.database_models.database_operate import DatabaseOperate
if __name__ == '__main__':
    db = DatabaseOperate()
    #db.rename_table('iris_temp_temp_temp_temp_temp_temp_temp',"iris")
    #db.delete_sql('user1')
    #tablename=input("请输入要增加主键的表名：")
    #db.alter_table(tablename)
    #db.query_sql()
    #db.reduplicates_sql(tablename)
    #column={
       # 'id': Column(Integer, primary_key=True, autoincrement='auto'),
       # "sepal_length" : Column(Float, nullable=True, comment="花萼长度"),
       # "sepal_width" : Column(Float, nullable=True, comment="花萼宽度"),
       # "petal_length":Column(Float, nullable=True, comment="花瓣长度"),
       # "petal_width": Column(Float, nullable=True, comment="花瓣宽度")
   # }
    #tb=db.table_orm("iris",column)
    print(db.get_column_names("iris2"))
    list=['id',"sepal_length","sepal_width","petal_length","petal_width"]
    db.column_rename(list,"iris2")
    print(db.get_column_names("iris2"))
