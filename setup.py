# 📄 setup.py
from setuptools import setup, find_packages

setup(
   name="pybro-cli",  # New PyPI package name 
   version="0.1.0",
   packages=find_packages(),
   include_package_data=True,
   install_requires=[
       "rich>=10.0.0",
   ],
   entry_points={
       "console_scripts": [
           "pybro=chrome_profile_manager.__main__:main",  # Main command
           "pybro-chrome=chrome_profile_manager.__main__:main",  # Alternative command
       ],
   },
   author="Chris Trauco",
   author_email="dev@trau.co",
   description="🔥 PyBro CLI - A Collection of Python Dev Tools for Debian 24.04",
   long_description=open("README.md").read(),
   long_description_content_type="text/markdown",
   url="https://github.com/yourusername/pybro-cli",
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License", 
       "Operating System :: POSIX :: Linux",
       "Environment :: Console",
       "Topic :: Utilities",
       "Development Status :: 3 - Alpha",
   ],
   python_requires=">=3.8",
   keywords="cli, chrome, profile, manager, debian, linux, development, tools",
)