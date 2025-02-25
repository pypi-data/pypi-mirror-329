import os
import re
import fabio
from glob import glob
import matplotlib.pyplot as plt


def getfiles(basepath, recsuffix):
    ret = {}
    files = glob(os.path.join(basepath, "*", "*.info"))
    energypattern = re.compile(r"Energy=\s+([0-9\.]+)")
    prefixpattern = re.compile(r"Prefix=\s+([^\s]+_)1_")
    for filename in files:
        energy, prefix = None, None
        with open(filename, "r") as f:
            content = f.readlines()
        for s in content:
            s = s.strip()
            m = energypattern.match(s)
            if m:
                energy = float(m.groups()[0])
            m = prefixpattern.match(s)
            if m:
                prefix = m.groups()[0]
        if energy and prefix:
            recfile = os.path.join(basepath, prefix, prefix + recsuffix)
            if os.path.isfile(recfile):
                ret[energy] = recfile

    energies, files = zip(*sorted(ret.items()))
    return list(energies), list(files)


if __name__ == "__main__":
    scandir = "/tmp_14_days/phasexas/25nm/"
    recsuffix = "6_0p05_rec30000_1.edf"
    energies, files = getfiles(scandir, recsuffix)
    scandir = "/tmp_14_days/phasexas/25nm_cut/"
    recsuffix = "6_0p05_rec30000_1.edf"
    energies[41:48], files[41:48] = getfiles(scandir, recsuffix)
    for filename, energy in zip(files, energies):
        with fabio.open(filename) as f:
            image = f.data
            print(energy, image.shape)
            plt.imshow(image)
            plt.show()
