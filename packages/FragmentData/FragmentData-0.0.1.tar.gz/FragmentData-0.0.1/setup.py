from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'An API for Telegram/fragment.com usernames and numbers'
LONG_DESCRIPTION = 'An API for Telegram/fragment.com usernames and numbers. Able to fetch prices and more useful information'

setup(
        name="FragmentData",
        version=VERSION,
        author="hurtmyfoot",
        author_email="hurtmyfoot@proton.me",
        url="https://github.com/hurtmyfoot/FragmentData",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],

        keywords=['fragment', 'telegram', 'api'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)