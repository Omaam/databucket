"""Bucket source code.
"""
import os

from astropy.table import Table
# import numpy as np
import pandas as pd

from databucket import xselect_handler
from databucket import configure


def _acquire_dirname(object_name: str):
    dirname = object_name.replace(" ", "_").lower()
    if "+" in dirname:
        dirname = dirname.replace("+", "p")
    elif "-" in dirname:
        dirname = dirname.replace("-", "m")
    return dirname


def _convert_value2string(value: int or float):
    value_str = str(value).replace(".", "p")
    return value_str


def _convert_enrange2string(energy_range_kev):
    energy_lower = _convert_value2string(energy_range_kev[0])
    energy_upper = _convert_value2string(energy_range_kev[1])
    return energy_lower + "t" + energy_upper


def _get_curvename(obsid, dt, energy_range_kev):
    dt_exp = "{:.0e}".format(dt)
    enrange = _convert_enrange2string(energy_range_kev)
    name_curve = f"curve{obsid}_dt{dt_exp}_range{enrange}kev.lc"

    return name_curve


def _must_run_xselect(path_to_curve, clobber):
    isexist = os.path.exists(path_to_curve)
    if (clobber is True) or (isexist is False):
        return True
    return False


class DataBucket():
    """
    """

    def __init__(self, object_name, satelite):

        self.object_name = object_name
        self.satelite = satelite.lower()

        path_to_bucket = configure.acquire_backetpath()
        dirname = _acquire_dirname(object_name)
        self.path_to_object = "/".join([path_to_bucket, dirname])

    def request_curve(self, obsid: str, dt: float,
                      energy_range_kev: list,
                      save_to: str = None,
                      clobber: bool = False):
        """
        """

        name_event = f"event{obsid}.evt"

        # Check existence for event file.
        path_to_event = "/".join([self.path_to_object, self.satelite,
                                  obsid, name_event])
        if os.path.exists(path_to_event) is False:
            raise FileExistsError(
                f"{path_to_event} does not exists."
                )

        name_curve = _get_curvename(obsid, dt, energy_range_kev)
        path_to_curve = "/".join(
            [self.path_to_object, self.satelite,
             obsid, name_curve]
        )

        # Run XSELECT, if needed.
        mustrun = _must_run_xselect(path_to_curve, clobber)
        if mustrun is True:
            xselect_handler.run_xselect_curve(
                path_to_event, path_to_curve,
                dt, energy_range_kev, "NICER")

        table = Table.read(path_to_curve, format="fits", hdu=1)
        df = table.to_pandas()

        return df

    def request_event(self, obsid: str, clobber: bool = False):
        """
        """

        filename = f"{obsid}.evt"

        path_to_event_evt = "/".join(
            [self.path_to_object, obsid, filename])
        if os.path.exists(path_to_event_evt) is False:
            raise FileExistsError(
                f"{path_to_event_evt} does not exists."
                )

        path_to_event_csv = "/".join(
            [self.path_to_object, obsid, filename])
        if os.path.exists(path_to_event_csv) is False:
            tbl = Table.read(path_to_event_evt, format="fits", hdu=1)
            df = tbl.to_pandas()
        else:
            df = pd.read_csv(path_to_event_csv, index=None)

        return df
