# coding: utf-8

"""
    domian-paas-sdk-python
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "dhicn_domain_paas_sdk_python"
VERSION = "1.0.16"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]
# with open('README.md', encoding='utf-8') as f:
#     readme = f.read()

setup(
    name=NAME,
    version=VERSION,
    author="dhi",
    author_email="wafe@dhigroup.com",
    url="https://github.com/DHICN/Domain-Paas-SDK-Python",
    keywords=["sdk", "python", "domain-paas"],
    install_requires=REQUIRES,
    packages=find_packages(where='src',exclude=["test", "tests"]),
    include_package_data=True,
    long_description="这是一个[DHI 中国 业务中台](https://online-products.dhichina.cn/) 的 Client SDK 开发辅助包，帮您快速通过我们的业务中台构建应用。",
    package_dir={'':'src'},
    license='MIT'
)
