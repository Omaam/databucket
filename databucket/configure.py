"""Module for configuration.

TODO:
    * (Omama) Complete this module to make proper configuration.
"""
import glob
import os
import subprocess
import re

from databucket import name


def acquire_backetpath():
    try:
        path_to_bucket = os.environ["DATABUCKET"]
    except KeyError:
        raise KeyError(
                "You must specify bucket path to DATABUCKET. "
                "For example,DATABUCKET=/path/to/bucket;"
                "export DATABUCKET.")
    return path_to_bucket


def update_eventfiles(object_name: str, satelite: str,
                      pathname_glob: str, clobber: bool = False):

    event_files = sorted(glob.glob(pathname_glob))

    for path_to_event in event_files:

        file_name = path_to_event.split("/")[-1]
        obsid = re.findall("[0-9]{10}", file_name)[0]

        object_name = name.convert_objectname(object_name)
        satelite = name.convert_satelitename(satelite)

        path_to_bucket = acquire_backetpath()
        path_to_dir_in_bucket = "/".join(
            [path_to_bucket, object_name, satelite, obsid]
        )
        os.makedirs(path_to_dir_in_bucket, exist_ok=True)

        new_name_event = "/".join(
            [path_to_bucket, object_name, satelite,
             obsid, f"event_{obsid}.evt"]
        )

        if clobber is True:
            print(path_to_event)
            do_remove = input("Do you remove rhese files. (y/n)")
            if do_remove == "y":
                cmd_rm = ["rm", path_to_event]
                subprocess.run(cmd_rm)
            else:
                print("These files will not be deleted.")

        do_update = (os.path.exists(new_name_event) is False) or \
                    (clobber is True)
        if do_update is True:
            cmd = ["ln", "-s", path_to_event, new_name_event]
            subprocess.run(cmd)
            print(f"update {new_name_event}")
