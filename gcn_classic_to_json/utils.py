import base64
from pathlib import Path

import numpy as np
from astropy.time import Time


def datetime_to_iso8601(date, time):
    """Converts time to ISO 8601 format.

    The function converts input into the ISO 8601 format from
    Truncated Julian Date by first converting it to Julian Date.

    Parameters
    ----------
    date : int
        Date must be in Truncated Julian Date format.
    time : int
        Time of day must in Seconds of Day format.

    Returns
    -------
    string
        returns datetime in ISO8601 format.

    Notes
    -----
    The zero point for Truncated Julian Day is given in https://en.wikipedia.org/wiki/Julian_day.
    """
    TJD0 = (2440000, 0.5)
    return Time(date + TJD0[0], time / 8640000 + TJD0[1], format="jd").isot + "Z"


def binary_to_string(binary):
    """Converts a binary array to a ASCII-string.

    The function converts `binary` into a C-style string,
    flips the position of every 4 bytes, strips excess null characters
    and then converts the result into ASCII characters.

    Parameters
    ----------
    binary : array-like
        A array for binary values encoded as 4-byte integers.

    Returns
    -------
    string:
        returns the corresponding ASCII string.

    Notes:
    ------
    The strings in the binary packets look like they were accidentally byte-swapped.
    """
    return (
        np.fliplr(binary.view("c").reshape(-1, 4))
        .ravel()
        .tobytes()
        .strip(b"\0")
        .decode()
    )


def attachments(set=None):
    """Get (set) the global list of attachments"""

    if not hasattr(attachments, "VALUE"):
        attachments.VALUE = {}

    if set is not None:
        attachments.VALUE = set

    return attachments.VALUE


def load_attachments(fname_jkey_tuples):
    # 2025-01-15 have[name] = path
    # If it were a Traversable, could simplify to .read_bytes
    have = attachments()

    json_attach = {}

    for fname, jkey in fname_jkey_tuples:
        if fname in have:
            print(f"\nfound {fname}- attempt load")
            # this could fail due to races in GCN
            path_obj = Path(have[fname])
            json_attach[jkey] = base64.b64encode(path_obj.read_bytes()).decode("ASCII")
        else:
            print(f"\nmissing {fname} attachment")

    return json_attach
