# -*- coding: utf-8 -*-

# Imports ###########################################################

import os
from setuptools import setup


# Functions #########################################################

def package_data(pkg, root_list):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for root in root_list:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


# Main ##############################################################

setup(
    name='xblock-field-test',
    version='0.1',
    description='Field Test XBlock',
    packages=['xb_field_test'],
    install_requires=[
        'Jinja2',
        'XBlock',
        'xblock-utils',
    ],
    entry_points={
        'xblock.v1': [
            'field-test = xb_field_test:FieldTestXBlock',
            'field-test-other = xb_field_test:FieldTestXBlock',
        ],
    },
    package_data=package_data("xb_field_test", ["templates", "public"]),
)
