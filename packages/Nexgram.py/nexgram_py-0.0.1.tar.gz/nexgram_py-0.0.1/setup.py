from setuptools import setup, find_packages

setup( 
  name="Nexgram.py",
  version="0.0.1",
  packages=find_packages(),
  install_requires=[
    # List your dependencies here,e.g. 
    # "requests>=2.25.1",
  ],
  author="Otazuki",
  author_email="otazuki004@gmail.com",
  description="A brief description of your package",
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  url="https://github.com/Otazuki004/Nexgram.py",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)
