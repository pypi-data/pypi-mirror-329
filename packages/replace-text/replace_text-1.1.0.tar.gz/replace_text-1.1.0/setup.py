from setuptools import setup

with open ("README.md", "r") as d:
    description = d.read()

setup (
    name = 'replace_text',
    version = '1.1.0', # ! make sure to match version number in main.py for `-v` flag, and change version number in install.sh
    long_description = description,
    long_description_content_type = "text/markdown",
    entry_points = {
      "console_scripts": [
        "replace-text = main:replace_text"
      ]
    }
)