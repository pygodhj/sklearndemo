import sqlite3
import os

# --- 1. 准备工作：定义数据库文件名和清理旧数据库（用于演示） ---
DB_FILE = "students.db"

# 如果数据库文件已存在，则删除，以便每次运行脚本都能从头开始
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print(f"旧的 '{DB_FILE}' 已删除。")

# --- 2. 创建数据库和表 ---
# 使用 with 语句可以确保连接和游标被自动关闭，是推荐的最佳实践
try:
    # 连接到数据库。如果数据库不存在，它将被自动创建。
    # ':memory:' 可以用于创建一个内存中的临时数据库
    with sqlite3.connect(DB_FILE) as conn:
        print(f"成功连接到 '{DB_FILE}' 数据库。")

        # 创建一个游标对象。所有数据库操作都通过游标执行。
        cursor = conn.cursor()

        # 创建表
        # IF NOT EXISTS 确保如果表已存在，不会报错
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            major TEXT
        );
        """
        cursor.execute(create_table_sql)
        print("'students' 表创建成功或已存在。")

except sqlite3.Error as e:
    print(f"创建数据库/表时出错: {e}")


# --- 3. 数据操作 (CRUD) ---

# --- 3.1. 增加 (Create) - 插入数据 ---
def insert_student(name, age, major):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # 使用 ? 作为占位符来传递参数，可以有效防止SQL注入攻击
            sql = "INSERT INTO students (name, age, major) VALUES (?, ?, ?)"
            cursor.execute(sql, (name, age, major))
            # with 语句会自动提交事务，所以不需要 conn.commit()
            print(f"成功插入学生: {name}")
    except sqlite3.Error as e:
        print(f"插入数据时出错: {e}")


# 插入一些示例数据
insert_student("张三", 20, "计算机科学")
insert_student("李四", 22, "软件工程")
insert_student("王五", 19, "数据科学")
print("-" * 20)


# --- 3.2. 查询 (Read) - 读取数据 ---
def get_all_students():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            # 让查询结果以字典形式返回，更方便使用
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, age, major FROM students")

            # 获取所有结果
            all_students = cursor.fetchall()

            print("所有学生信息:")
            for student in all_students:
                # 可以通过列名访问
                print(f"ID: {student['id']}, 姓名: {student['name']}, 年龄: {student['age']}, 专业: {student['major']}")

    except sqlite3.Error as e:
        print(f"查询数据时出错: {e}")


get_all_students()
print("-" * 20)


# --- 3.3. 修改 (Update) - 更新数据 ---
def update_student_age(student_id, new_age):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            sql = "UPDATE students SET age = ? WHERE id = ?"
            cursor.execute(sql, (new_age, student_id))

            # cursor.rowcount 返回被修改的行数
            if cursor.rowcount > 0:
                print(f"ID 为 {student_id} 的学生年龄已更新为 {new_age}。")
            else:
                print(f"未找到 ID 为 {student_id} 的学生。")

    except sqlite3.Error as e:
        print(f"更新数据时出错: {e}")


# 将 ID 为 1 的学生年龄更新为 21
update_student_age(1, 21)
print("更新后的学生信息:")
get_all_students()  # 再次查询以验证更新
print("-" * 20)


# --- 3.4. 删除 (Delete) - 删除数据 ---
def delete_student(student_id):
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            sql = "DELETE FROM students WHERE id = ?"
            cursor.execute(sql, (student_id,))  # 注意元组的逗号

            if cursor.rowcount > 0:
                print(f"ID 为 {student_id} 的学生已被删除。")
            else:
                print(f"未找到 ID 为 {student_id} 的学生。")

    except sqlite3.Error as e:
        print(f"删除数据时出错: {e}")


# 删除 ID 为 2 的学生
delete_student(2)
print("删除后的学生信息:")
get_all_students()  # 再次查询以验证删除
print("-" * 20)


# --- 4. 删除表 ---
def drop_students_table():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS students")
            print("'students' 表已被删除。")
    except sqlite3.Error as e:
        print(f"删除表时出错: {e}")

# 取消下面这行的注释以执行删除表操作
# drop_students_table()

