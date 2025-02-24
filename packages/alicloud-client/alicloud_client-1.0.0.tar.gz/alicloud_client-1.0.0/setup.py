#!/usr/bin/python

from setuptools import setup, find_packages
PACKAGE = "alicloud-client"
DESCRIPTION = "cloud client"
VERSION = '1.0.0'

setup_args = {
    'version': VERSION,
    'description': DESCRIPTION,
    'license': "Apache License 2.0",
    'packages': find_packages(exclude=["tests*"]),
    'platforms': 'any',
    'install_requires': ["jmespath>=0.9.3,<1.0.0","alibabacloud_tea_util>=0.3.13, <1.0.0","alibabacloud_credentials>=0.3.5, <1.0.0","alibabacloud_openapi_util>=0.2.1, <1.0.0","alibabacloud_gateway_spi>=0.0.2, <1.0.0","alibabacloud_tea_xml>=0.0.2, <1.0.0","time_check_server>=0.0.1", "cryptography>=3.0.0"],
    'classifiers': (
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development',
    )
}

setup(name='alicloud-client', **setup_args)
