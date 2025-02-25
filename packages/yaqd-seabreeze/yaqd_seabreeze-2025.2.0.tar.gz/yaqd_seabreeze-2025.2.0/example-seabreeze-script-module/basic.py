"""extract mean, std, min, and max of the acquisitions
"""

import numpy as np


# --- configure -----------------------------------------------------------------------------
# --- --- channels --------------------------------------------------------------------------

channel_names = ["mean", "std", "min", "max"]
channel_units = {k: "counts" for k in channel_names}
channel_mappings = {k: "wavelength" for k in channel_names}

# -------------------------------------------------------------------------------------------------


def process(raw: np.array) -> dict:
    out = {}

    if raw.shape[0] == 1:
        out["mean"] = out["min"] = out["max"] = raw[0]
        out["std"] = np.zeros(raw.shape[1:])
    else:
        out["mean"] = raw.mean(axis=0)
        out["max"] = raw.max(axis=0)
        out["min"] = raw.min(axis=0)
        out["std"] = raw.std(axis=0)

    return out
