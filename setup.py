# 📄 setup.py
from setuptools import setup, find_packages

setup(
   name="pybro-cli",
   version="0.1.4",  # Increment version
   packages=find_packages(),
   include_package_data=True,
   install_requires=[
       "rich>=10.0.0",
       "pathlib>=1.0.1",
       "typing>=3.7.4",
   ],
   entry_points={
       "console_scripts": [
           "pybro=chrome_profile_manager.__main__:main",  # Fixed entry point
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