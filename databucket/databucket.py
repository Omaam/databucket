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


def _must_run_xselect(path_to_file, clobber):
    isexist = _check_existence(path_to_file)
    if (clobber is True) or (isexist is False):
        return True
    return False


class DataBucket():
    """
    """

    def __init__(self, target_name):

        self.target_name = target_name

        path_to_bucket = _load_bucketpath()
        dirname = _acquire_dirname(target_name)
        self.path_to_object = "/".join([path_to_bucket, dirname])

    def request_curve(self, obsid: str, dt: float,
                      energy_range: list, save_to: str = None,
                      clobber: bool = False):
        """
        """
        _check_obsid(self.target_name, obsid)

        dt_exp = "{:.1e}".format(dt)
        enrange = _conver_enrange(energy_range_kev)
        filename = "dt%s_enrange%skev.lc".format(dt_exp, enrange)
        path_to_file = "/".join([self.path_to_object, obsid, filename])

        mustrun = _must_run_xselect(path_to_file, clobber)
        if mustrun is True:
            _run_xselect()

        table = Table.load(path_to_file, format="fits", hdu=1)

        return table

    def request_event(self, obsid: str, clobber: bool = False):
        """
        """
        _check_obsid(self.target_name, obsid)

        filename = "event.evt.gz"
        path_to_file = "/".join([self.path_to_object, obsid, filename])

        table = Table.load(path_to_file, format="fits", hdu=1)
        table = Table.load()

        return table
