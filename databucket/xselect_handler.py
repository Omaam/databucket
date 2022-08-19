"""The script to handle XSELECT in bash.
"""
import datetime
import os
import shutil
import subprocess


def _calc_kev2pi(satelite: str):
    if satelite == "nicer":
        return 100


def _make_command(path_to_event, path_to_curve,
                  dt, pi_lower, pi_upper):

    event_file = path_to_event.split("/")[-1]
    path_to_dir = "/".join(path_to_event.split("/")[:-1])

    logname = path_to_curve + ".log"

    xsel_cmd = f"""
        xselect > {logname} 2>&1 << EOF
        xsel
        read event {event_file}
        {path_to_dir}
        yes

        set binsize {dt}

        filter pha_cutoff {pi_lower+1} {pi_upper}
        ext curve offset=no
        save curve {path_to_curve}

        exit
        no
        EOF
        """

    delete_space = "        "
    xsel_cmd = xsel_cmd.replace(delete_space, "")

    return xsel_cmd


def _make_bashscript(path_to_event: str,
                     path_to_curve: str,
                     dt: float,
                     energy_range: list,
                     satelite: str):
    """
    """

    rate_kev2pi = _calc_kev2pi(satelite)
    pi_lower = int(rate_kev2pi * energy_range[0])
    pi_upper = int(rate_kev2pi * energy_range[1])

    xsel_cmd = _make_command(path_to_event, path_to_curve,
                             dt, pi_lower, pi_upper)

    path_to_script = "xselect_script.sh"

    with open(path_to_script, "w") as f:
        f.write(xsel_cmd)

    return path_to_script


def change_directory(func):

    def _change_directory(*args, **kargs):
        now = datetime.datetime.now().isoformat()
        workdir = "xselect_" + now

        try:
            os.mkdir(workdir)
            os.chdir(workdir)
            func(*args, **kargs)
            os.chdir("..")
            shutil.rmtree(workdir)

        except KeyboardInterrupt:
            os.chdir("..")
            shutil.rmtree(workdir)

    return _change_directory


@change_directory
def run_xselect_curve(path_to_event: str,
                      path_to_curve: str,
                      dt: float,
                      energy_range: list,
                      satelite: str = "NICER"):

    path_to_script = _make_bashscript(
        path_to_event, path_to_curve, dt,
        energy_range, satelite)

    bash_cmd = ["bash", path_to_script]

    subprocess.run(bash_cmd)
