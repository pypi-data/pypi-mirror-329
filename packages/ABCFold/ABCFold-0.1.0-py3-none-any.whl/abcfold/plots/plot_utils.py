import numpy as np


def get_plddt_regions(plddts: np.ndarray) -> dict:
    """
    Get the pLDDT regions for the model
    """
    regions = {}

    v_low = np.where(plddts <= 50)[0]
    regions["v_low"] = cif_file._get_regions(v_low)
    low = np.where((plddts > 50) & (plddts < 70))[0]
    regions["low"] = cif_file._get_regions(low)
    confident = np.where((plddts >= 70) & (plddts < 90))[0]
    regions["confident"] = cif_file._get_regions(confident)
    v_confident = np.where(plddts >= 90)[0]
    regions["v_high"] = cif_file._get_regions(v_confident)


def get_regions()