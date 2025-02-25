import torch
import torch.nn.functional as F


def nmi_loss(
    source: torch.Tensor, target: torch.Tensor, bandwidth: int = 0.01, reduction="none"
):
    """
    Calculates the Normalized Mutual Information between batch source and batch target

    param source: Batch of Tensors
    param target: Batch of Tensors with same size as source
    param bandwidth: The size of the kernel function, determines the sample rate of the histogramm(default: 0.01)
    param reduction: If None: returns Tensor of NMI for every element in batch. If Sum or Mean: Applies operation to the resulting tensor

    """
    eps = 1e-10
    m = source.flatten(start_dim=1)
    t = target.flatten(start_dim=1)
    batch = m.size()[0]
    bins = round(0.5 / bandwidth)

    samples = torch.linspace(0, 1, bins)
    # samples has size [bins]
    samples = samples.unsqueeze(0).expand((batch, -1))
    # m has size [N,items], samples has size [N, bins]
    m_outer = m[..., None] - samples[:, None, ...]
    m_outer = quartic_kernel(m_outer / bandwidth)

    t_outer = t[:, None, ...] - samples[..., None]
    t_outer = quartic_kernel(t_outer / bandwidth)
    # m_outer and t_outer have shape [N,bins, items] and [N,items,bins]
    # result has dimensions[N,bins,bins]

    joint_hgram = torch.matmul(t_outer, m_outer)
    joint_hgram = F.normalize(joint_hgram, p=1, dim=(1, 2))
    m_hgram = torch.sum(joint_hgram, dim=1)
    t_hgram = torch.sum(joint_hgram, dim=2)

    m_hgram[m_hgram <= eps] = eps
    t_hgram[t_hgram <= eps] = eps
    joint_hgram[joint_hgram <= eps] = eps

    m_ent = (m_hgram * torch.log2(m_hgram)).nansum(dim=1)
    t_ent = (t_hgram * torch.log2(t_hgram)).nansum(dim=1)
    joint_ent = (joint_hgram * torch.log2(joint_hgram)).nansum(dim=(1, 2))

    mut_inf = -((m_ent + t_ent) / joint_ent)
    if reduction == "none":
        return mut_inf
    elif reduction == "mean":
        return mut_inf.mean()
    elif reduction == "sum":
        return mut_inf.sum()
    else:
        raise ValueError(f"reduction must either be none, mean or sum. Got {reduction}")


def quartic_kernel(data: torch.Tensor) -> torch.Tensor:
    result = torch.zeros_like(data)
    result[torch.logical_and(data < 1, data > -1)] = (
        15 / 16 * (1 - data[torch.logical_and(data < 1, data > -1)] ** 2) ** 2
    )
    return result


def block_kernel(data: torch.Tensor) -> torch.Tensor:
    result = torch.zeros_like(data)
    result[torch.logical_and(data < 1, data > -1)] = 1
    return result
