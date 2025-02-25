# noqa SPDX-FileCopyrightText: 2024 Florence Bockting <florence.bockting@tu-dortmund.de>
#
# noqa SPDX-License-Identifier: Apache-2.0

import tensorflow as tf
import tensorflow_probability as tfp

from elicit.types import NFDict
from typing import Callable

tfd = tfp.distributions


def NF(
    inference_network: Callable, network_specs: dict, base_distribution: Callable
) -> NFDict:
    """
    specification of the normalizing flow used from BayesFlow library

    Parameters
    ----------
    inference_network : callable
        type of inference network as specified by bayesflow.inference_networks.
    network_specs : dict
        specification of normalizing flow architecture. Arguments are inherited
        from chosen bayesflow.inference_networks.
    base_distribution : callable
        Base distribution from which should be sampled during learning.
        Normally the base distribution is a multivariate normal.

    Returns
    -------
    nf_dict : dict
        dictionary specifying the normalizing flow settings.

    """
    nf_dict: NFDict = dict(
        inference_network=inference_network,
        network_specs=network_specs,
        base_distribution=base_distribution,
    )

    return nf_dict


class BaseNormal:
    def __call__(self, num_params: int) -> Callable:
        """
        Multivariate standard normal distribution with as many dimensions as
        parameters in the generative model.

        Parameters
        ----------
        num_params : int
            number of model parameters. Is internally specified in
            :func:`elicit.simulations.sample_from_priors`

        Returns
        -------
        callable
            tfp.distributions object.

        """

        base_dist = tfd.MultivariateNormalDiag(
            loc=tf.zeros(num_params), scale_diag=tf.ones(num_params)
        )
        return base_dist


# initialized instance of the BaseNormal class
base_normal = BaseNormal()
