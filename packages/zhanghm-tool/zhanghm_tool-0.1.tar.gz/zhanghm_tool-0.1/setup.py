from setuptools import setup, find_packages

setup(
    name='zhanghm-tool',
    version='0.1',     # version：版本号。
    packages=find_packages(),  # description：描述。
    description='A simple example package',
    long_description=open('README.md').read(),
    # python3，readme文件中文报错
    # long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/yourusername/zhanghm-tool',
    author='zhanghm',
    author_email='704806663@qq.com',
    license='MIT',
    install_requires=[
        # 依赖列表
    ],
    classifiers=[
        # 分类信息
    ]
)
