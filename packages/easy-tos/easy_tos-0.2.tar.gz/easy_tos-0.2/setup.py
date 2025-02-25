from setuptools import setup, find_packages


setup(
    name="easy_tos",  # 库的名称
    version="0.2",      # 版本号
    packages=find_packages(),  # 自动找到所有包
    install_requires=[  
        'tos'
    ],
    classifiers=[  # 可选，帮助别人找到你的库
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)