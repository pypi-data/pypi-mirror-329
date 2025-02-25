import h5py
import numpy as np

from typing import Sequence, List, Tuple, Dict


def calculate_exclusions(string: str) -> Sequence[float]:
    exclusions = []
    if string is None:
        return exclusions
    slices = string.replace(" ", "").split(",")
    for slice in slices:
        try:
            if slice.split("-")[0] == slice:
                exclusions.append(float(slice + ".1"))
            else:
                split = slice.split("-")
                start = float(split[0] + ".1")
                stop = float(split[1] + ".1")
                exclusions.extend(np.arange(start, stop))
        except ValueError:
            raise ValueError(
                'The exclude syntax should be like "3, 12-15, 56, 57 - 58 "'
            )
    return exclusions


def get_stack(
    path: str,
    stack: str,
    exclusions: Sequence = list(),
    energy_counter: str = "Edcmund",
) -> Tuple[List[np.ndarray], List[float]]:
    images = list()
    energies = list()
    with h5py.File(path) as f:
        title = f["2.1"]["title"].asstr()[()]
        title = title.split()
        ysize, xsize = int(title[4]), int(title[-2]) + 1
        length = xsize * ysize

        # Iterating over f.keys() is not possible as the keys are in lexicographic order
        for index in np.arange(1.1, len(f.keys()) + 1, 1.0):
            if index in exclusions:
                continue
            index = str(index)
            if (
                "measurement" in f[index].keys()
                and stack in f[index]["measurement"].keys()
            ):
                flat = f[index]["measurement"][stack]
                if np.all(np.array(flat) == 0):
                    break
                if flat.size == length and np.all(np.isfinite(flat)):
                    image = np.reshape(flat, (xsize, ysize))
                    images.append(image)
                    energies.append(
                        f[index]["instrument"]["positioners"][energy_counter][()]
                    )

    if len(images) == 0:
        raise ValueError("With the given configuration, no images were collected")
    return images, energies


def get_stack_dict(
    path: str, stack: str, exclusions: Sequence = list()
) -> Tuple[List[np.ndarray], List[float]]:
    images = dict()
    with h5py.File(path) as f:
        title = f["2.1"]["title"].asstr()[()]
        title = title.split()
        ysize, xsize = int(title[4]), int(title[-2]) + 1
        length = xsize * ysize

        # Iterating over f.keys() is not possible as the keys are in lexicographic order
        for energy in np.arange(1.1, len(f.keys()) + 1, 1.0):
            if energy in exclusions:
                continue
            energy = str(energy)
            if (
                "measurement" in f[energy].keys()
                and stack in f[energy]["measurement"].keys()
            ):
                flat = f[energy]["measurement"][stack]
                if np.all(np.array(flat) == 0):
                    break
                if flat.size == length and np.all(np.isfinite(flat)):
                    image = np.reshape(flat, (xsize, ysize))
                    images[energy] = image

    if len(images) == 0:
        raise ValueError("With the given configuration, no images were collected")
    return images


def get_all_stacks(
    path: str, stacks: List[str], exclusions: Sequence = list()
) -> Dict[str, Dict[str, np.ndarray]]:
    imagestacks = dict()
    with h5py.File(path) as f:
        title = f["2.1"]["title"].asstr()[()]
        title = title.split()
        ysize, xsize = int(title[4]), int(title[-2]) + 1
        length = xsize * ysize

        # Iterating over f.keys() is not possible as the keys are in lexicographic order
        bad_stacks = []

        for energy in np.arange(2.1, len(f.keys()) + 1, 1.0):
            images = dict()
            if energy in exclusions:
                continue
            energy = str(energy)
            try:
                scan = f[energy]["measurement"]
            except KeyError:
                continue
            if all(
                [scan[stack].size != length for stack in stacks if stack in scan.keys()]
            ):
                continue
            for stack in stacks:
                if stack not in scan.keys():
                    bad_stacks.append(stack)
                    continue
                image = scan[stack]
                if np.all(np.array(image) == 0) or image.size != length:
                    bad_stacks.append(stack)
                    continue
                if not np.all(np.isfinite(image)):
                    bad_stacks.append(stack)
                    continue
                image = np.reshape(image, (xsize, ysize))
                images[stack] = image

            stacks = [stack for stack in stacks if stack not in bad_stacks]

            # if all counters only have valid values, we can add this energy

            imagestacks[energy] = images
        # for every energy remove all stacks that are faulty at some energy
        [
            [scan.pop(bad) for bad in bad_stacks if bad in scan.keys()]
            for scan in imagestacks.values()
        ]

    if len(imagestacks) == 0:
        raise ValueError("With the given configuration, no images were collected")
    return imagestacks
