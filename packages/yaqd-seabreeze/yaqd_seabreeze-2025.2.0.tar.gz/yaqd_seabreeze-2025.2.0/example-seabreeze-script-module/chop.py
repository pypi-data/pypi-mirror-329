"""
- take spectra and discern a chop phase by inspecting at a certain color.
- relies on measuring, at some color, light that switches with chopper phase
- aggregate blocked (a) and unblocked (b) phases acquisitions to measure
  a difference (b-a).
- for proper extaction, we assume chopping phase is pure (i.e. one shot per spectrum).
  e.g. use fastest acquisition time (3 ms), and 1/3 kHz rep rate on fs table
"""

import numpy as np


# --- configure -----------------------------------------------------------------------------
# --- --- channels --------------------------------------------------------------------------

channel_names = ["mean", "a", "b", "d_ba"]
channel_units = {k: "counts" for k in channel_names}
channel_mappings = {k: "wavelength" for k in channel_names}

# --- --- discriminator ---------------------------------------------------------------------

# e.g. discriminate spurious 2-shot acquisitions
discriminator_index = 631  # index used to discriminate spectra; use None to turn off
discriminator_limits = [0.3, 1.7]  # signals larger than 1.7x median value are removed

# --- --- chopping --------------------------------------------------------------------------

chop_index: int = 360  # index used to extract phase
chop_threshold = "extrema"  # mean, extrema, or fixed count value

# -------------------------------------------------------------------------------------------------


sel = (slice(None), chop_index)
des = (slice(None), discriminator_index)


def discriminator(x):
    xdes = x[des] / np.median(x[des])
    return (xdes > discriminator_limits[0]) & (xdes < discriminator_limits[1])


if chop_threshold == "mean":
    thresholder = lambda x: x[sel] < x[sel].mean()
elif chop_threshold == "extrema":
    thresholder = lambda x: x[sel] < 0.5 * (x[sel].min() + x[sel].max())
elif chop_threshold in [int, float]:
    thresholder = lambda x: x[sel] < chop_threshold


def process(raw: np.array) -> dict:
    out = {}

    if discriminator_index is not None:
        valid = discriminator(raw)
        if valid.any():
            raw = raw[valid]

    out["mean"] = raw.mean(axis=0)

    chop = thresholder(raw)

    out["a"] = raw[chop].mean(axis=0)
    out["b"] = raw[~chop].mean(axis=0)
    out["d_ba"] = out["b"] - out["a"]

    return out
