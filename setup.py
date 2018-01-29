import os
from setuptools import setup


APP=['main.py']
setup(
	  app=APP,
    name = "Daisy",
    author = "Daisy Liu",
    author_email = "daisy.liu@thecarousell.com",
    description = "An tool to create bug/story ticket",
    setup_requires=['py2app'],
    install_requires=[
          'JIRA','requests','Image'
      ]

)