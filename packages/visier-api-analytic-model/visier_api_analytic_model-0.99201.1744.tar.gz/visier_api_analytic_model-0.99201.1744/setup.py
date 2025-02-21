# coding: utf-8

"""
    Visier Analytic Model APIs

    Visier APIs for retrieving and configuring your analytic model in Visier.

    The version of the OpenAPI document: 22222222.99201.1744
    Contact: alpine@visier.com

    Please note that this SDK is currently in beta.
    Functionality and behavior may change in future releases.
    We encourage you to provide feedback and report any issues encountered during your use.
"""  # noqa: E501


from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "visier-api-analytic-model"
VERSION = "0.99201.1744"
PYTHON_REQUIRES = ">=3.8"
REQUIRES = [
    "visier-api-core ~= 0.99201.1744",
]

setup(
    name=NAME,
    version=VERSION,
    description="Visier Analytic Model APIs",
    author="Visier",
    author_email="alpine@visier.com",
    url="",
    keywords=["Visier", "Visier-SDK", "Visier Analytic Model APIs"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="Apache License, Version 2.0",
    long_description_content_type='text/markdown',
    long_description="""\
    Visier APIs for retrieving and configuring your analytic model in Visier.
    """,  # noqa: E501
    package_data={"visier_api_analytic_model": ["py.typed"]},
)
