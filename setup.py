import os
from setuptools import setup, find_packages

setup(name="static_tl",
      version="0.1",
      description="Take control of your tweets",
      url="http://dmerej.info/tweets/",
      author="Dimitri Merejkowsky",
      author_email="d.merej@gmail",
      packages=find_packages(),
      install_requires=["arrow", "jinja2", "twitter"],
      license="BSD",
      entry_points = {
        "console_scripts" : [
            "static-tl   = static_tl.main:main"
        ]
      },
      classifiers=[
          "Environment :: Console",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 3 :: Only",
    ]
)
