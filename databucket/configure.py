"""Module for configuration.
"""
import glob
import os
import subprocess
import re


def link_eventfiles(pathname_glob: str):

    event_files = sorted(glob.glob(pathname_glob))

    for path_to_event in event_files:

        file_name = path_to_event.split("/")[-1]
        obsid = re.findall("[0-9]{10}", file_name)[0]

        path_to_obsid_in_bucket = PATH_TO_BUCKET + "/" + obsid
        os.makedirs(path_to_obsid_in_bucket, exist_ok=True)

        new_name_event = PATH_TO_BUCKET + "/" + f"{obsid}/{obsid}.evt"
        if os.path.exists(new_name_event) is False:
            cmd = ["ln", "-s", path_to_event, new_name_event]
            subprocess.run(cmd)
            print("link from\n{} to\n{}".format(
                  path_to_event, new_name_event))


def update_eventfiles(pathname_glob: str):

    event_files = sorted(glob.glob(pathname_glob))

    for path_to_event in event_files:

        file_name = path_to_event.split("/")[-1]
        obsid = re.findall("[0-9]{10}", file_name)[0]

        path_to_obsid_in_bucket = PATH_TO_BUCKET + "/" + obsid
        os.makedirs(path_to_obsid_in_bucket, exist_ok=True)

        new_name_event = PATH_TO_BUCKET + "/" + f"{obsid}/{obsid}.evt"
        if os.path.exists(new_name_event) is False:
            cmd = ["cp", path_to_event, new_name_event]

            subprocess.run(cmd)


if __name__ == "__main__":

    pathname = "/home/omama/Data/MAXI_J1820p070/nicer/RawData_Old/" \
               "*/xti/event_cl/bc*.evt"

    PATH_TO_BUCKET = "/home/omama/Data/Bucket"

    link_eventfiles(pathname)
