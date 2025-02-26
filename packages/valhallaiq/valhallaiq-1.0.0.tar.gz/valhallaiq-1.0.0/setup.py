from setuptools import setup, find_packages

setup(
    name="valhallaiq",
    version="1.0.0",
    author="Ahmed",
    author_email="almkhtrt@gmail.com",
    description="A Telegram bot for sending emails with customizable settings.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/valhalla505/valhallabot",
    packages=find_packages(),
    install_requires=[
        "pyTelegramBotAPI",  
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)