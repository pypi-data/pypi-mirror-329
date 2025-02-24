from setuptools import setup, find_packages # 导入setuptools打包工具

setup(
    name='piper_sdk',
    version='0.1.16',    # 包版本号，便于维护版本
    long_description=open('./CHANGELOG-0-1-16.MD').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/agilexrobotics/piper_sdk',  # 主页链接
    license='MIT License',  # 这里显式指定 License
    packages=find_packages(include=['piper_sdk', 'piper_sdk.*']),
    include_package_data=True,
    package_data={
        '': ['LICENSE','*.sh','*.MD'],  # 指定包含的文件
        'piper_sdk/asserts': ['*'],  # 包括 asserts 文件夹下的所有文件
    },
    install_requires=[
        'python-can>=3.3.4',
    ],
    entry_points={
    },
    author='RosenYin',  # 作者
    author_email='yinruocheng321@gmail.com',
    description='A sdk to control piper',   #包的简述
    platforms=['Linux'],
    # url="https://github.com/agilexrobotics/piper_sdk",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',    #对python的最低版本要求,18.04及以上
)

