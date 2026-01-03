# E:\sklearndemo\setup.py

import setuptools

# 读取 README.md 文件内容，用于项目的长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    # --- 项目元数据 ---
    name="sklearndemo",                 # 项目名称，在 PyPI 上必须唯一
    version="0.0.1",                           # 项目版本号，遵循语义化版本 (SemVer)
    author="jiuson",                        # 作者
    #author_email="your.email@example.com",     # 作者邮箱
    #description="A short description of your project", # 项目简短描述
    long_description=long_description,         # 项目详细描述，通常来自 README.md
    long_description_content_type="text/markdown", # 长描述的格式
    #url="https://github.com/yourusername/my-awesome-project", # 项目主页 URL
    #project_urls={                             # 其他相关 URL
        #"Bug Tracker": "https://github.com/yourusername/my-awesome-project/issues",
   # },
   #  classifiers=[                              # 项目分类器，帮助用户在 PyPI 上找到你的项目
   #      "Programming Language :: Python :: 3",
   #      "License :: OSI Approved :: MIT License",
   #      "Operating System :: OS Independent",
   #  ],

    # --- 包和依赖项 ---
    packages=setuptools.find_packages(),       # 自动发现所有包含 __init__.py 的包
    python_requires=">=3.6",                   # 指定最低 Python 版本要求
    # install_requires=[                         # 项目运行依赖的库
    #     "requests >= 2.25.1",
    #     "numpy >= 1.19.5",
    # ],
    # extras_require={                           # 可选的额外依赖（例如，仅在开发或测试时需要）
    #     "dev": ["pytest>=6.0", "twine>=3.4"],
    # },

    # --- 定义命令行脚本 ---
    # entry_points={
    #     'console_scripts': [
    #         'my-awesome-command = my_awesome_project.main_module:main_function',
    #     ],
    # },
)