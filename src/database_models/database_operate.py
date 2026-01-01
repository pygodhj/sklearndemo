import sqlite3
import os
DB_FILE = "ml_dataset.db"

class DatabaseOperate:

    # 1. 创建数据库和表
    @staticmethod
    def create_table(tablename,columns):
        # 1. 定义数据库文件的完整路径
        # 注意：路径分隔符在 Windows 上是 '\'，在 macOS/Linux 上是 '/'
        # 为了代码的跨平台兼容性，推荐使用 os.path.join()

        # --- 在 Windows 上 ---
        # db_path = "D:/my_app_data/user_database.db"
        # 或者使用原始字符串避免转义问题
        # db_path = r"C:\Users\YourUser\Documents\my_db.db"

        # --- 在 macOS / Linux 上 ---
        # db_path = "/home/user/data/app.db"

        # --- 使用 os.path.join() (推荐的跨平台方式) ---
        # 假设我们想在用户的主目录下的一个 'db' 文件夹里创建
        # 获取脚本根目录
        script_path = os.path.abspath(__file__)
        root_dir = os.path.dirname(script_path)
        # 定义目标文件夹
        target_dir = os.path.join(root_dir, "db")
        # 确保目标文件夹存在，如果不存在则创建
        os.makedirs(target_dir, exist_ok=True)  # exist_ok=True 表示如果文件夹已存在则不报错
        # 拼接完整的数据库文件路径
        db_path = os.path.join(target_dir, DB_FILE)
        try:
            # 连接到数据库。如果数据库不存在，它将被自动创建。

            with sqlite3.connect(db_path) as conn:  # 使用 with 语句可以确保连接和游标被自动关闭，是推荐的最佳实践
                print(f"成功连接到 '{DB_FILE}' 数据库。")

                # 创建一个游标对象。所有数据库操作都通过游标执行。
                cursor = conn.cursor()

                # 创建表 IF NOT EXISTS 确保如果表已存在，不会报错
                create_table_sql = f"""
                    CREATE TABLE IF NOT EXISTS {tablename} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        {columns}
                    );
                    """
                cursor.execute(create_table_sql)
                print("'students' 表创建成功或已存在。")

        except sqlite3.Error as e:
            print(f"创建数据库/表时出错: {e}")