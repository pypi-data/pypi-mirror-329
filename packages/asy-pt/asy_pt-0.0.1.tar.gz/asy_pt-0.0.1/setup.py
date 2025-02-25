
from setuptools import setup

requirements = [
    'elasticsearch-dsl[async]'
]

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='asy_pt',
    version='0.0.1',
    packages=[
        "asy_pt",
    ],
    license='BSD License',  # example license
    description='asy_pt',
    long_description='这是一个通用的fastapi 开发工具包，帮助你快速的开发fastapi项目',
    install_requires=requirements,
    long_description_content_type="text/markdown",
    url='https://github.com/xulehexuwei',
    author='xuwei',
    author_email='15200813194@163.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
