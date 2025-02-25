from setuptools import setup

with open ("README.md", "r") as d:
    description = d.read()

setup (
    name = 'replace-text',
    version = '1.0.0',
    long_description = description,
    long_description_content_type = "text/markdown",
    entry_points = {
      "console_scripts": [
        "replace-text = main:replace_text"
      ]
    }
)