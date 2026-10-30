import argparse
import os
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parent
MATERIALS = ("2NiS-5", "1TiTe2-1", "1PdTe2-1", "1PdTe2-2")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ranks", type=int, default=8)
    args = parser.parse_args()
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1")
    for uid in MATERIALS:
        directory = ROOT / "results" / uid
        with (directory / "scf.out").open("w") as stream:
            subprocess.run(
                ["mpirun", "-np", str(args.ranks), "pw.x", "-in", "scf.in"],
                cwd=directory, env=env, stdout=stream, stderr=subprocess.STDOUT, check=True,
            )
        assert "convergence has been achieved" in (directory / "scf.out").read_text()
        shutil.copy2(directory / "scratch" / "osc.save" / "data-file-schema.xml", directory / "data-file-schema.xml")


if __name__ == "__main__":
    main()
