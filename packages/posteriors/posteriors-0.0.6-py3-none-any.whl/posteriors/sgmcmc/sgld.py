from typing import Any
from functools import partial
import torch
from torch.func import grad_and_value
from tensordict import TensorClass, NonTensorData

from posteriors.types import TensorTree, Transform, LogProbFn
from posteriors.tree_utils import flexi_tree_map, tree_insert_
from posteriors.utils import CatchAuxError


def build(
    log_posterior: LogProbFn,
    lr: float,
    beta: float = 0.0,
    temperature: float = 1.0,
) -> Transform:
    """Builds SGLD transform.

    Algorithm from [Welling and Teh, 2011](https://www.stats.ox.ac.uk/~teh/research/compstats/WelTeh2011a.pdf):
    $$
    θ_{t+1} = θ_t + ε \\nabla \\log p(θ_t, \\text{batch}) + N(0, ε  (2 - ε β) T \\mathbb{I})
    $$
    for learning rate $\\epsilon$ and temperature $T$.

    Targets $p_T(θ) \\propto \\exp( \\log p(θ) / T)$ with temperature $T$.

    The log posterior and temperature are recommended to be [constructed in tandem](../../log_posteriors.md)
    to ensure robust scaling for a large amount of data and variable batch size.

    Args:
        log_posterior: Function that takes parameters and input batch and
            returns the log posterior value (which can be unnormalised)
            as well as auxiliary information, e.g. from the model call.
        lr: Learning rate.
        beta: Gradient noise coefficient (estimated variance).
        temperature: Temperature of the sampling distribution.

    Returns:
        SGLD transform (posteriors.types.Transform instance).
    """
    update_fn = partial(
        update,
        log_posterior=log_posterior,
        lr=lr,
        beta=beta,
        temperature=temperature,
    )
    return Transform(init, update_fn)


class SGLDState(TensorClass["frozen"]):
    """State encoding params for SGLD.

    Attributes:
        params: Parameters.
        log_posterior: Log posterior evaluation.
        aux: Auxiliary information from the log_posterior call.
    """

    params: TensorTree
    log_posterior: torch.Tensor = torch.tensor([])
    aux: NonTensorData = None


def init(params: TensorTree) -> SGLDState:
    """Initialise SGLD.

    Args:
        params: Parameters for which to initialise.

    Returns:
        Initial SGLDState.
    """

    return SGLDState(params)


def update(
    state: SGLDState,
    batch: Any,
    log_posterior: LogProbFn,
    lr: float,
    beta: float = 0.0,
    temperature: float = 1.0,
    inplace: bool = False,
) -> SGLDState:
    """Updates parameters for SGLD.

    Update rule from [Welling and Teh, 2011](https://www.stats.ox.ac.uk/~teh/research/compstats/WelTeh2011a.pdf),
    see [build](sgld.md#posteriors.sgmcmc.sgld.build) for details.

    Args:
        state: SGLDState containing params.
        batch: Data batch to be send to log_posterior.
        log_posterior: Function that takes parameters and input batch and
            returns the log posterior value (which can be unnormalised)
            as well as auxiliary information, e.g. from the model call.
        lr: Learning rate.
        beta: Gradient noise coefficient (estimated variance).
        temperature: Temperature of the sampling distribution.
        inplace: Whether to modify state in place.

    Returns:
        Updated state (which are pointers to the input state tensors if inplace=True).
    """
    with torch.no_grad(), CatchAuxError():
        grads, (log_post, aux) = grad_and_value(log_posterior, has_aux=True)(
            state.params, batch
        )

    def transform_params(p, g):
        return (
            p
            + lr * g
            + (temperature * lr * (2 - temperature * lr * beta)) ** 0.5
            * torch.randn_like(p)
        )

    params = flexi_tree_map(transform_params, state.params, grads, inplace=inplace)

    if inplace:
        tree_insert_(state.log_posterior, log_post.detach())
        return state.replace(aux=NonTensorData(aux))
    return SGLDState(params, log_post.detach(), aux)
