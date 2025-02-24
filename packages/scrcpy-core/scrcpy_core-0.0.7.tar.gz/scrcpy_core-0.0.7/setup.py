from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name='scrcpy-core',
    version='0.0.7',
    packages=find_packages(include=['scrcpy', 'scrcpy']),
    include_package_data=True,
    package_data={
        'scrcpy': ["*.jar"],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy==1.26.4",
        "av==14.0.1",
        "adbutils==2.8.0"
        # 项目依赖项列表
    ],
    python_requires='>=3.9',
    author="mortal_sjh",                                     # 作者
    author_email="mortal_sjh@qq.com"
)
