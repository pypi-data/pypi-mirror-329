from setuptools import setup, find_packages

setup(
    name="soundcloud_downloader",
    version="0.1.3", 
    author="ATH_Studioo",
    author_email="ihor6285@gmail.com",  # Ваш email
    description="A library for downloading music from SoundCloud using scdl",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ATHStudioo/soundcloud_downloader",
    packages=find_packages(),
    install_requires=["scdl>=2.12.3"],
    python_requires=">=3.6",
)