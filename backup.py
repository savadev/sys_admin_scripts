"""
Back Up Files Script
Author: Mike Tung <miketung2013@gmail.com>
2/22/2018
"""

import os
import json


def load_configs() -> dict:
    return json.load('./settings.json')

