import os
from sqlalchemy import create_engine, Column, Integer, MetaData, Table, select, inspect, text, func, delete, Column, \
    String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base
from sklearndemo.config import DB_DIR


# 这是操作数据库的类
class DatabaseOperate:
    #初始化，创建引擎和会话
    def __init__(self,db_file="ml_dataset.db"):
        self.db_file = db_file
         # 1、连接数据库，若数据库不存在，先创建数据库，返回数据库引擎
        db_path = os.path.join(DB_DIR, self.db_file)
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)  # echo=True 可以看到生成的 SQL
        print(f"--- 数据库 '{db_file}' 已成功连接 ---")

        # 2.获取所有表名
        self.get_table_names()

        # 3. 创建一个新的 Base 类和 MetaData
        # 使用一个独立的 MetaData 对象可以更好地管理动态创建的表
        self.metadata = MetaData()
        # 创建基类
        self.base = declarative_base(metadata=self.metadata)

        # 4. 创建会话工厂
        self.Session = sessionmaker(bind=self.engine)


    # 使用 ORM 创建表和数据，建立SQLAlchemy ORM模型类
    def orm(self,table_name="user1", columns_definition={"name": Column(String(50))}):

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

        # 建立SQLAlchemy ORM模型动态类
        model_class_name = table_name.capitalize()
        model_class = type(model_class_name, (self.base,), class_attrs)

        return model_class


    def create_table_orm(self,table_name="user1", columns_definition={"name":"hj"}):
        try:
            model_class=self.orm()
            print(f"正在使用orm创建表 '{table_name}'...")
            model_class.__table__.create(bind=self.engine)
            print(f"表 '{model_class.__tablename__}' 创建成功！")
            self.get_table_names()
        except Exception as e:
            print(f"表格 '{table_name}' 已存在: {e}")

    def insert_orm(self, table_name="user", columns_definition={"name":"hj"}):
        User=self.create_table_orm(table_name,columns_definition)

        with self.Session() as session:
            new_user = User(name='Dynamic User')
            session.add(new_user)
            session.commit()
            print(f"已添加新用户: {session.query(User).first()}")


    #  使用 Core 反射表结构
    def core(self, table_name):
        # 创建一个新的 MetaData 对象用于反射（这是个好习惯，但不是必须的）
        reflection_metadata = MetaData()

        # 使用 Core 反射表结构
        print(f"正在使用 Core 反射表 '{table_name}'...")
        reflected_table = Table(table_name, reflection_metadata, autoload_with=self.engine)
        print(f"成功反射表 '{table_name}'。")

        return reflected_table


    # 获取所有表名
    def get_table_names(self):
        # 1、创建 Inspector 对象
        inspector = inspect(self.engine)
        # 2. 获取所有表名
        table_names = inspector.get_table_names()  # get_table_names() 会返回一个包含所有用户定义表名的列表
        # 2. 打印表名
        print(f"数据库中已有{len(table_names)}个表格")
        print(table_names)

    def create_table(self):
        pass

    # 使用Core反射并查询数据
    def query_sql(self, table_name= "iris"):
        reflected_table=self.core(table_name)
        try:
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


    # 使用Core反射并删除数据表
    def delete_sql(self, table_name="iris"):
        """
        使用 SQLAlchemy Core 删除指定的数据库表格。

        :param table_name: 要删除的表格名称。
        """
        print(f"准备删除表格 '{table_name}'...")

        try:
            # 使用 engine 直接执行 DDL 语句是更直接的方式
            # 'IF EXISTS' 确保如果表格不存在，操作不会失败
            drop_statement = text(f"DROP TABLE IF EXISTS {table_name}")

            # 使用 with 语句确保连接被正确关闭
            with self.engine.connect() as connection:
                # 执行删除操作
                connection.execute(drop_statement)
                # 提交事务，使删除生效
                connection.commit()

            print(f"成功删除表格 '{table_name}' (或表格不存在)。")

        except SQLAlchemyError as e:
            # 推荐捕获更具体的 SQLAlchemyError
            print(f"删除表格 '{table_name}' 时发生数据库错误: {e}")

        except Exception as e:
            print(f"删除表格 '{table_name}' 时发生未知错误: {e}")


    # 使用Core反射并对数据表添加自增主键
    def alter_table(self, table_name="iris"):
        # 执行ALTER—TABLE添加自增主键
        # 注意: 语法因数据库而异
        # 创建一个新的 MetaData 对象用于反射（这是个好习惯，但不是必须的）
        reflection_metadata = MetaData()
        #try:
            # 使用 Core 反射表结构
        with self.engine.connect() as conn:
            #  重命名表 -> 创建新表(带主键) -> 复制数据 -> 删除旧表
            print(f"正在使用 Core 反射表 '{table_name}'...")
            reflected_table = Table(table_name, reflection_metadata, autoload_with=self.engine)
            print(f"成功反射表 '{table_name}',包含列: {[c.name for c in reflected_table.c]}")

            quoted_columns = [col.key for col in reflected_table.c]
            columns_definitions = [f"{col.key} {col.type}" for col in reflected_table.c]
            columns_str = ', '.join(quoted_columns)
            conn.execute(text(f"ALTER TABLE {table_name} RENAME TO {table_name}_temp;"))

            create_sql = f"""
                    CREATE TABLE {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        {', '.join(columns_definitions)}
                    );
                """
            conn.execute(text(create_sql))
            conn.execute(text(f"INSERT INTO {table_name} ({columns_str}) SELECT {columns_str} FROM {table_name}_temp;"))
            conn.execute(text(f"DROP TABLE {table_name}_temp;"))
            print(f"成功为表 '{table_name}' 添加了自增主键 'id'。")

        #except Exception as e:
            #print(f"删除操作失败，已回滚。错误: {e}")

    # 使用Core反射并对数据表去重
    def reduplicates_sql(self, table_name="iris"):

        # 1.创建一个新的 MetaData 对象用于反射（这是个好习惯，但不是必须的）
        reflection_metadata = MetaData()

        try:
            # 使用 Core 反射表结构
            print(f"正在使用 Core 反射表 '{table_name}'...")
            reflected_table = Table(table_name, reflection_metadata, autoload_with=self.engine)
            print(f"成功反射表 '{table_name}'。")


            # 2. 构建一个子查询，找出所有需要保留的行的 id
            # 这个子查询会为每个email分组，并找到该组中最小的 id
            subquery = (
                select(func.min(reflected_table.c.id))
                .group_by(reflected_table.c.index)
                .scalar_subquery()  # 将其转换为标量子查询
            )

            # 3. 构建删除语句
            # 删除所有 id 不在我们保留列表中的行
            delete_stmt = delete(reflected_table).where(reflected_table.c.id.not_in(subquery))
            print("将要执行的删除语句:")
            print(delete_stmt)
            # 验证将要被删除的行
            verify_stmt = select(reflected_table).where(reflected_table.c.id.not_in(subquery))
            with self.engine.connect() as connection:
                for row in connection.execute(verify_stmt):
                    print(f"这行将会被删除: {row}")


        # 4. 执行删除操作 (!!! 危险操作 !!!)
            i=input("是否删除（Y/N）：")
            if i=="Y":
                with self.engine.connect() as connection:
                    # 开始一个事务
                    trans = connection.begin()

                    # 执行删除
                    result = connection.execute(delete_stmt)

                    # 提交事务，使删除生效
                    trans.commit()

                    print(f"成功删除了 {result.rowcount} 行重复数据。")


        except Exception as e:
            # 如果发生任何错误，回滚事务
            trans.rollback()
            print(f"删除操作失败，已回滚。错误: {e}")