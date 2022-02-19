"""The script to handle XSELECT in bash.
"""
import os
import subprocess


def _calc_kev2pi(satelite: str):
    if satelite == "NICER":
        return 100


def _make_command(path_to_event, path_to_curve,
                  dt, pi_lower, pi_upper):

    event_file = path_to_event.split("/")[-1]
    path_to_dir = "/".join(path_to_event.split("/")[:-1])

    xsel_cmd = f"""
        xselect << EOF
        xsel
        read event {event_file}
        {path_to_dir}
        yes

        set binsize {dt}

        filter pha_cutoff {pi_lower+1} {pi_upper}
        ext curve
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
                     satelite: str = "NICER"):
    """
    """

    rate_kev2pi = _calc_kev2pi(satelite)
    pi_lower = rate_kev2pi * energy_range[0]
    pi_upper = rate_kev2pi * energy_range[1]

    xsel_cmd = _make_command(path_to_event, path_to_curve,
                             dt, pi_lower, pi_upper)

    path_to_script = "xselect_script.sh"
    with open(path_to_script, "w") as f:
        f.write(xsel_cmd)

    return path_to_script


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

    os.remove(path_to_script)
