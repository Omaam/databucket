"""The script to handle XSELECT in bash.
"""
import subprocess


def _calc_kev2pi(satelite: str):
    if satelite == "NICER":
        return 100


def _make_command(dt, pi_lower, pi_upper):

    xsel_cmd = f"""
        xselect << EOF
        xsel
        read eve bcTEST_OBSID_0mpu7_cl.evt
        /home/omama/Soft/git/databucket/databucket
        yes

        set binsize {dt}

        filter pha_cutoff {pi_lower} {pi_upper}
        ext curve
        save curve ../fits/lcTEST_OBSID_05t1keV_dt{dt}.fits

        exit
        no
        EOF
        """

    delete_space = "        "
    xsel_cmd = xsel_cmd.replace(delete_space, "")
    print(xsel_cmd)

    return xsel_cmd


def _make_bashscript(path_to_event: str, dt: float,
                     energy_range: list,
                     satelite: str = "NICER"):
    """
    """

    rate_kev2pi = _calc_kev2pi(satelite)

    pi_lower = rate_kev2pi * energy_range[0]
    pi_upper = rate_kev2pi * energy_range[1]

    xsel_cmd = _make_command(dt, pi_lower, pi_upper)

    with open("xselect_script.sh", "w") as f:
        f.write(xsel_cmd)

    bash_cmd = ["bash", "xselect_script.sh"]
    subprocess.run(bash_cmd)


def run_xselect_curve():
    pass
