# replace-text

## Links

[PyPI Package Page](https://pypi.org/project/replace-text/)  
[GitHub Repo](https://github.com/zdodson21/replace-text?tab=GPL-3.0-1-ov-file)

## Usage

Run `replace-text -h` or `replace-text --help` will display the help menu

```
usage: replace-text [-d] [-h] [-o] [-r] [-v] [target]

positional arguments:
  target                The target file or directory of files

options:
  -d, --developer       enables developer console output
  -h, --help            show this help message and exit
  -o , --original-text 
                        the text to be replaced
  -r , --replacement-text 
                        the new text to replace the old
  -v, --version         displays the version number
```

## Contributing

### Local Development

For local development, this project requires the `setuptools` and `wheel` packages.  
You can install these tools using `pip` with the following script:
`pip install setuptools wheel`

### Build Script

A build shell script is included which executes this command:

```shell
python3 setup.py sdist bdist_wheel;
```

### Install Locally

An install shell script is included which executes this command:

```shell
pip install dist/replace_text-0.0.1-py3-none-any.whl --force-reinstall;
```

### Testing

The `tests/` directory includes one directory and two test files to test replacing text in a whole directory (`tests/`) or in a single file (`test-file.txt`). You can also run the following test scripts included in the files of this project:

#### Test Directory

```shell
replace-text tests -o test -r new;
```

#### Test File

```shell
replace-text tests/test-file.txt -o test -r new;
```

## Submit Issues / Feature Requests

* [GitHub Issues](https://github.com/zdodson21/replace-text/issues)