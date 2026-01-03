from sqlalchemy import create_engine, Column, Integer, MetaData, Table, select,inspect
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 这是操作数据库的类
class DatabaseOperate:
    #初始化，创建引擎和会话
    def __init__(self,db_file="ml_dataset.db"):
        self.db_file = db_file
         # 1、连接数据库，若数据库不存在，先创建数据库，返回数据库引擎
        script_path = os.path.abspath(__file__)
        root_dir = os.path.dirname(script_path)
        target_dir = os.path.join(root_dir, "db")
        os.makedirs(target_dir, exist_ok=True)
        db_path = os.path.join(target_dir, self.db_file)
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)  # echo=True 可以看到生成的 SQL
        print(f"--- 数据库 '{db_file}' 已成功连接 ---")

        # 2.获取所有表名
        self.get_table_names()

        # 3. 创建一个新的 Base 类和 MetaData
        # 使用一个独立的 MetaData 对象可以更好地管理动态创建的表
        self.metadata = MetaData()
        self.base = declarative_base(metadata=self.metadata)

        # 4. 创建会话工厂
        self.Session = sessionmaker(bind=self.engine)

    def get_table_names(self):

        # 1、创建 Inspector 对象
        inspector = inspect(self.engine)

        # 2. 获取所有表名
        table_names = inspector.get_table_names()  # get_table_names() 会返回一个包含所有用户定义表名的列表

       # 2. 打印表名
        print(table_names)


    #使用 ORM 创建表和数据，建立SQLAlchemy ORM 模型类
    def create_dynamic_model(self,table_name, columns_definition):

        # 1、确保表名是合法的（可选，但推荐）
        if not table_name.isalnum() and '_' not in table_name:
            raise ValueError("表名只能包含字母、数字和下划线。")

        # 2、定义类属性字典
        class_attrs = {
            '__tablename__': table_name,
            # 通常需要一个主键
            'id': Column(Integer, primary_key=True, autoincrement=True),
        }
        # 将传入的列定义更新到类属性中
        class_attrs.update(columns_definition)  # 这会覆盖掉同名的默认属性（如果有的话）

        # 类名最好和表名相关，方便调试
        model_class =  self.base.__class__(table_name.capitalize(), (self.base,), class_attrs)

        return model_class

    #使用Core反射并查询数据
    def query_sql_columns(self, table_name= "user_data_123"):

        # 创建一个新的 MetaData 对象用于反射（这是个好习惯，但不是必须的）
        reflection_metadata = MetaData()

        try:
            # 使用 Core 反射表结构
            print(f"正在使用 Core 反射表 '{table_name}'...")
            reflected_table = Table(table_name, reflection_metadata, autoload_with=self.engine)
            print(f"成功反射表 '{table_name}'。")

            # 在同一个 Session 中使用 Core 查询
            with self.Session() as session:
                print(f"正在使用 Core 查询表 '{table_name}' 的数据...")
                stmt = select(reflected_table)
                result = session.execute(stmt)
                print(" | ".join(result.keys()))
                for row in result:
                    print(row)

             # 动态打印结果
                print("-" * 30)
                return ()

        except Exception as e:
            print(f"使用 Core 查询时发生错误: {e}")



