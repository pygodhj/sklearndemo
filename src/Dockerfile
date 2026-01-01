# 1. 选择一个基础镜像
# 我们使用 python:3.12-slim，它基于 Debian 操作系统
FROM python:3.12-slim-bookworm

# 2. 安装系统依赖
# tkinter 需要 tcl 和 tk 这两个系统库。
# 我们使用 apt-get (Debian/Ubuntu 的包管理器) 来安装它们。
# -y 参数会自动回答 yes，避免交互式提问。
RUN apt-get update && apt-get install -y \
    tk-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
# 在镜像中执行命令。这里用于安装应用运行所必需的系统级依赖。
# apt-get update: 更新 Debian 的软件包列表，确保 apt-get 知道最新的软件包版本和位置。
# &&: 逻辑 “与” 操作符。它确保只有在 apt-get update 成功执行后，才会继续执行后面的 apt-get install。
# apt-get install -y: 安装软件包。-y 参数会自动对所有提问回答 “是”，这在自动化构建中是必需的。
# tk-dev: 安装 Tcl/Tk 的开发文件。你的 Python 应用如果使用了 tkinter 库（用于创建图形用户界面），就必须安装这个系统依赖。
# build-essential: 这是一个元包，它会安装编译 C/C++ 代码所需的基础工具（如 gcc, g++, make 等）。像 pandas 这样的科学计算库，其底层有 C 或 Fortran 代码，在安装时需要编译，因此需要这个包。
# && rm -rf /var/lib/apt/lists/*:清理缓存，减小镜像体积。这是一个非常重要的最佳实践。
# apt-get update 会下载一个包列表文件，存放在 /var/lib/apt/lists/ 目录下。这个文件在安装完成后就没用了，但会占用镜像空间。这行命令就是删除这个目录，从而减小最终镜像的大小。

RUN groupadd -r appuser && useradd -r -g appuser -m -s /bin/bash appuser
# 在镜像中创建一个非 root 用户和用户组。
# groupadd -r appuser: 创建一个名为 appuser 的系统组 (-r 表示系统账户 / 组)。
# useradd -r -g appuser -m -s /bin/bash appuser: 创建一个名为 appuser 的系统用户。
# -g appuser: 将该用户加入到 appuser 组。
# -m: 自动创建用户的主目录 (/home/appuser)。
# -s /bin/bash: 设置该用户的默认 shell 为 bash。

WORKDIR /app
# 设置后续所有命令的工作目录。之后的 COPY, RUN, CMD 等命令都会在 /app 目录下执行。
# 如果 /app 目录不存在，Docker 会自动创建它。
RUN chown -R appuser:appuser /app
# 将 /app 目录及其所 有内容的所有权，从 root 用户转移到刚刚创建的 appuser 用户和用户组。
# -R 表示递归处理所有子目录和文件。
USER appuser
# 切换当前用户。从这一行开始，直到镜像构建结束，以及容器启动后，默认的用户都是 appuser，而不是 root。
# 这大大提高了安全性，因为即使应用被入侵，攻击者也只能获得有限的权限。

RUN pip install pandas openpyxl
# 使用 pip 安装 Python 包。

# 3. 设置工作目录并复制应用代码
WORKDIR /app
# 再次设置工作目录为 /app。
#虽然它已经被设置过了，但在 COPY 之前明确指定一下是一个好习惯，可以增加 Dockerfile 的可读性。
COPY --chown=appuser:appuser fetch_data.py  .
# 将宿主机上的文件复制到镜像中。
# fetch_data.py: 这是你本地项目目录中的 Python 脚本文件。
# .: 这是镜像中的目标路径，. 代表当前工作目录，即 /app。所以这行命令是将 fetch_data.py 复制到镜像的 /app/ 目录下。
# --chown=appuser:appuser: 这是一个非常重要的选项。它确保了被复制到镜像中的文件，其所有者直接就是 appuser，而不是 root。这避免了权限问题，因为后续运行应用的是 appuser


# 4. 定义容器启动时的默认命令
CMD ["python", "fetch_data.py"]