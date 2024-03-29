"""Bucket source code.
"""
import os
import shutil
import warnings

from astropy.table import Table
# import numpy as np
import pandas as pd

from databucket import configure
from databucket import name
from databucket import xselect_handler


def _acquire_dirname(object_name: str):
    dirname = object_name.replace(" ", "_").lower()
    if "+" in dirname:
        dirname = dirname.replace("+", "p")
    elif "-" in dirname:
        dirname = dirname.replace("-", "m")
    return dirname


def _convert_enrange2string(energy_range_kev):
    energy_lower = str(energy_range_kev[0]).replace(".", "p")
    energy_upper = str(energy_range_kev[1]).replace(".", "p")
    return energy_lower + "t" + energy_upper


def _get_curvename(obsid, dt, energy_range_kev):
    dt_exp = "{:.5f}".format(dt).replace(".", "p")
    enrange = _convert_enrange2string(energy_range_kev)
    name_curve = f"curve_{obsid}_dt{dt_exp}_range{enrange}kev.lc"

    return name_curve


def _must_run_xselect(path_to_curve, clobber):
    isexist = os.path.exists(path_to_curve)
    if (clobber is True) or (isexist is False):
        return True
    return False


def _tidy_float2int(value):
    if value == int(value):
        value = int(value)
    return value


class DataBucket():
    """
    """

    def __init__(self, object_name, satelite):

        self.object_name = object_name
        self.satelite = satelite.lower()

        path_to_bucket = configure.acquire_backetpath()
        object_name = name.convert_objectname(object_name)
        self.path_to_object = "/".join([path_to_bucket, object_name])

    def request_curve(self, obsid: str, dt: float,
                      energy_range_kev: list,
                      copy_fits_to: str = None,
                      save_fits_to: str = None,
                      save_csv: bool = True,
                      clobber: bool = False):
        """
        """

        name_event = f"event_{obsid}.evt"

        # Check existence for event file.
        path_to_event = "/".join([self.path_to_object, self.satelite,
                                  obsid, name_event])
        if os.path.exists(path_to_event) is False:
            raise FileExistsError(
                f"{path_to_event} does not exists.")

        energy_range_kev = list(energy_range_kev)
        energy_range_kev[0] = _tidy_float2int(energy_range_kev[0])
        energy_range_kev[1] = _tidy_float2int(energy_range_kev[1])

        name_curve = _get_curvename(obsid, dt, energy_range_kev)
        path_to_curve = "/".join(
            [self.path_to_object, self.satelite,
             obsid, name_curve]
        )

        if (os.path.exists(path_to_curve) is True) and (clobber is True):
            os.remove(path_to_curve)

        mustrun = _must_run_xselect(path_to_curve, clobber)
        if mustrun is True:
            print("Run xselect")
            xselect_handler.run_xselect_curve(
                path_to_event, path_to_curve,
                dt, energy_range_kev, self.satelite)
            print("Finish xselect")

        table = Table.read(path_to_curve, format="fits", hdu=1)
        df = table.to_pandas()

        if save_csv is True:
            path_to_csv = os.path.splitext(
                path_to_curve)[0] + ".csv"
            df.to_csv(path_to_csv, index=None)

        if save_fits_to is not None:
            warnings.warn(
                "Don't use argment 'save_fits_to'."
                "Instead, use argment 'copy_fits_to'.",
                UserWarning
            )
            copy_fits_to = save_fits_to

        if copy_fits_to is not None:
            savefile = os.path.basename(path_to_curve)
            savefile = os.path.join(
                copy_fits_to,
                os.path.splitext(savefile)[0] + ".fits"
            )
            shutil.copyfile(path_to_curve, savefile)

        return df

    def request_event(self, obsid: str, clobber: bool = False):
        """
        """

        filename = f"event_{obsid}.evt"

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
