import pytest


from ewoksndreg.tests.data import data_for_registration

try:
    from ewoksndreg.intensities.torch_metrics import nmi_loss
    import torch
except ImportError:
    torch = None
import numpy as np


@pytest.mark.skipif(torch is None, reason="python version not supported by torch")
def test_rand_nmi():
    rand = torch.rand((3, 1, 20, 20))
    rand2 = torch.rand((3, 1, 20, 20))
    mixed = torch.clone(rand2)
    mixed[..., :10] = rand[..., :10]
    same = nmi_loss(rand, rand)
    half = nmi_loss(rand, mixed)
    random = nmi_loss(rand, rand2)
    torch.testing.assert_close(same < half, torch.ones((3), dtype=torch.bool))
    torch.testing.assert_close(half < random, torch.ones((3), dtype=torch.bool))


@pytest.mark.skipif(torch is None, reason="python version not supported by torch")
def test_img_nmi():
    images, active, passive = data_for_registration.images("translation", nimages=8)
    images = torch.tensor(np.array(images))
    images = images[:, None, ...]

    losses = [nmi_loss(images[0:1], images[i : i + 1]) for i in range(len(images - 1))]
    assert all(losses[i] < losses[i + 1] for i in range(len(losses) - 1))
