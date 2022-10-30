from setuptools import setup, find_packages

setup(
    name="DiscordPyExt",
    version="0.0.1",
    author="Zackary W",
    description="extended utilities for discord.py",
    long_description="extended utilities for discord.py",
    long_description_content_type="text/markdown",
    url="https://www.github.com/ZackaryW/discordPyExt",
    packages=[
        "discordPyExt",
        "discordPyExt.components",
        "discordPyExt.utils",
        "discordPyExt.ext",
        "discordPyExt.interfaces",
        "discordPyExt.setup",
        "discordPyExt.setup.ext",
        "discordPyExt.static",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        #alpha
        "Development Status :: 3 - Alpha",
        # for devs
        "Intended Audience :: Developers",
    ],

)
