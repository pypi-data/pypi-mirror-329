import os
from setuptools import setup, find_packages


__DIRNAME__ = os.path.dirname(os.path.abspath(__file__))
BASE_PACKAGE = "smartbulk_connector"
BASE_IMPORT = "smartbulk_connector"

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

def _install_requires():
    with open(os.path.join(__DIRNAME__, "requirements.txt"), "r", encoding="utf-8") as rf:
        return list(map(str.strip, rf.readlines()))


setup(
    name=BASE_PACKAGE,
    version="1.0.5",
    author="BioTuring",
    author_email="support@bioturing.com",
    url="https://app.bioturing.com/smartbulk",
    description="BioTuring Smartbulk Connector",
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={BASE_IMPORT: "smartbulk_connector"},
    packages=[BASE_IMPORT, *find_packages()],
    zip_safe=False,
    python_requires=">=3.8, <3.12",
    install_requires=_install_requires(),
)
