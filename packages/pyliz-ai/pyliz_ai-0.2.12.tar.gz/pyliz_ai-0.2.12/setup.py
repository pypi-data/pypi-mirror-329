from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.2.12'
DESCRIPTION = 'Library to interact with local/remote LLM.'
LONG_DESCRIPTION = 'Small library to run LLM models locally or remotely.'

# Setting up
setup(
    name="pyliz-ai",
    version=VERSION,
    author="Gabliz",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "pylizlib",
        "pylizmedia",
        "google-generativeai",
        "mistralai",
        "ollama",
        "openai-whisper",
        "librosa",
        "torch",
        "huggingface-hub",
        "transformers==4.46.2",
        "eagleliz"
    ],
    keywords=['python', 'video', 'ai', 'utilities'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)