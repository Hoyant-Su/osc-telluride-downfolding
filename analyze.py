import csv
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np


ROOT = Path(__file__).resolve().parent
HARTREE_EV = 27.211386245988
MATERIALS = ("2NiS-5", "1TiTe2-1", "1PdTe2-1", "1PdTe2-2")


def analyze(uid, scoring):
    output = ET.parse(ROOT / "results" / uid / "data-file-schema.xml").getroot().find("output")
    bands = output.find("band_structure")
    ks = bands.findall("ks_energies")
    weights = np.array([float(k.find("k_point").get("weight")) for k in ks])
    weights /= weights.sum()
    energies = np.array([np.fromstring(k.findtext("eigenvalues"), sep=" ") for k in ks]) * HARTREE_EV
    occupations = np.array([np.fromstring(k.findtext("occupations"), sep=" ") for k in ks])
    ef = float(bands.findtext("fermi_energy")) * HARTREE_EV
    nat = int(output.find("atomic_structure").get("nat"))
    nelec = float(bands.findtext("nelec"))
    reconstructed = float(2 * weights @ occupations.sum(axis=1))
    np.testing.assert_allclose(reconstructed, nelec, rtol=0, atol=1e-7)
    density = 2 * weights @ occupations
    crossing = np.flatnonzero((energies.min(axis=0) < ef) & (ef < energies.max(axis=0)))
    active = int(crossing[np.argmin(np.abs(density[crossing] - 1))])
    filling = float(np.clip(density[active], 0, 2))
    bandwidth = float(np.ptp(energies[:, active]))
    sigma = 0.15
    gaussian = np.exp(-0.5 * ((energies - ef) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))
    nef = float(2 * weights @ gaussian.sum(axis=1) / nat)
    ne = round(filling * 36)
    ne = min(70, max(2, ne - ne % 2))
    mapped = min(ne, 72 - ne)
    reference = scoring["A_by_Ne"].get(str(mapped))
    amplitude = reference[1] if reference else None
    index = scoring["scale"] * round(nef, 5) * max(amplitude, 0) if reference else None
    return {
        "material_id": uid,
        "atoms": nat,
        "irreducible_kpoints": len(ks),
        "electron_count": nelec,
        "electron_count_from_occupations": reconstructed,
        "fermi_energy_ev": ef,
        "active_band_zero_based": active,
        "n_band": filling,
        "nef_states_per_ev_atom": nef,
        "bandwidth_ev": bandwidth,
        "t_ev": bandwidth / 8,
        "U_over_t": 8,
        "solver_Ne": ne,
        "solver_delta": 1 - ne / 36,
        "scoring_Ne_after_particle_hole_mapping": mapped,
        "published_A_d": amplitude,
        "index_from_published_table": index,
        "scoring_status": "published table estimate" if reference else "requires organizer reference at Ne=6",
        "crossing_bands": [
            {"band_zero_based": int(b), "n_band": float(density[b]), "bandwidth_ev": float(np.ptp(energies[:, b]))}
            for b in crossing
        ],
    }


def main():
    scoring = json.loads((ROOT / "reference" / "scoring_meta.json").read_text())
    rows = [analyze(uid, scoring) for uid in MATERIALS]
    control = rows[0]
    np.testing.assert_allclose(control["n_band"], 0.8435, rtol=0, atol=1e-4)
    np.testing.assert_allclose(control["nef_states_per_ev_atom"], 1.40205, rtol=0, atol=1e-4)
    assert control["solver_Ne"] == 30
    (ROOT / "results" / "summary.json").write_text(json.dumps(rows, indent=2) + "\n")
    columns = [key for key in rows[0] if key != "crossing_bands"]
    with (ROOT / "results" / "summary.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps([{key: row[key] for key in ("material_id", "n_band", "nef_states_per_ev_atom", "solver_Ne", "index_from_published_table")} for row in rows], indent=2))


if __name__ == "__main__":
    main()
