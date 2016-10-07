import os
from setuptools import setup, find_packages

setup(name="static_tl",
      version="0.5.2",
      description="Generate a static HTML website from your twitter time line",
      url="https://github.com/dmerejkowsy/static_tl",
      author="Dimitri Merejkowsky",
      author_email="d.merej@gmail.com",
      packages=find_packages(),
      package_data={
          "static_tl" : [
              "static/*",
              "templates/*",
          ],
      },
      install_requires=[
          "arrow",
          "feedgenerator",
          "flask",
          "jinja2",
          "toml",
          "twitter"
      ],
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
