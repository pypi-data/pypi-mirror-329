from setuptools import setup

setup (
    name='replace-text',
    version='0.0.1',

    entry_points={
      "console_scripts": [
        "replace-text = main:replace_text"
      ]
    }
)