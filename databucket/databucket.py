"""Bucket source code.
"""
import os

from astropy.table import Table


def _load_bucketpath():
    try:
        with open("./path_to_bucket.txt", "r") as f:
            path_to_bucket = f.read().rstrip()

    except FileNotFoundError as e:
        current_dir = os.getcwd()
        print(e)
        print("You must make 'path_to_bucket.txt' in"
              "%s to indicate the bucket path.",
              current_dir)

    return path_to_bucket


def _acquire_dirname(object_name: str):
    dirname = object_name.replace(" ", "_").lower()
    if "+" in dirname:
        dirname = dirname.replace("+", "p")
    elif "-" in dirname:
        dirname = dirname.replace("-", "m")
    return dirname


class DataBucket():
    """
    """

    def __init__(self, target_name):

        self.target_name = target_name

        path_to_bucket = _load_bucketpath()
        dirname = _acquire_dirname(target_name)
        self.path_to_data = "/".join([path_to_bucket, dirname])

    def request_curve(self, obsid: str, dt: float,
                      energy_range: list, save_to: str = None):
        table = Table.load()
        return table

    def request_event(self, obsid: str):
        table = Table.load()
        return table
