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
    tablename=input("请输入要去重的表名：")
    db.query_sql(tablename)
    db.reduplicates_sql(tablename)