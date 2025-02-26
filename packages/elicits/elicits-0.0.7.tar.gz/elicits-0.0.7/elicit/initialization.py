# noqa SPDX-FileCopyrightText: 2024 Florence Bockting <florence.bockting@tu-dortmund.de>
#
# noqa SPDX-License-Identifier: Apache-2.0

import tensorflow as tf
import tensorflow_probability as tfp

import elicit as el
from elicit.types import (
    Parameter,
    Initializer,
    Trainer,
    Target,
    ExpertDict,
    NFDict,
    Uniform,
)
from typing import Union, Optional, Any, Iterable, List, Dict
from scipy.stats import qmc
from tqdm import tqdm

tfd = tfp.distributions


def uniform_samples(
    seed: int,
    hyppar: List[str],
    n_samples: int,
    method: str,
    mean: Union[float, Iterable[float]],
    radius: Union[float, Iterable[float]],
    parameters: List[Parameter],
):
    """
    Sample from uniform distribution for each hyperparameter.

    Parameters
    ----------
    seed : int
        user-specified seed defined in :func:`elicit.elicit.trainer`.
    hyppar : list
        list of hyperparameter names (strings) declaring the order for the
        list of **means** and **radius**.
        If **means** and **radius** are each a float, then this number is
        applied to all hyperparameter such that no order of hyperparameter
        needs to be specified. In this case ``hyppar=None``
    n_samples : int
        number of samples from the uniform distribution for each
        hyperparameter.
    method : str
        name of sampling method used for drawing samples from uniform.
        Currently implemented are "random", "lhs", and "sobol".
    mean : float or list
        Specification of the uniform distribution. The uniform distribution
        ranges from (**mean-radius**) to (**mean+radius**).
    radius : float or list
        Specification of the uniform distribution. The uniform distribution
        ranges from (**mean-radius**) to (**mean+radius**).
    parameters : list
        list including dictionary with all information about the (hyper-)parameters.
        Can be retrieved as attribute from the initialized
        :mod:`elicit.elicit.Elicit` obj (i.e., ``eliobj.parameters``)

    Raises
    ------
    ValueError
        ``method`` must be either "sobol", "lhs", or "random".
        ``n_samples`` must be a positive integer
    TypeError
        arises if ``method`` is not a string.

    Returns
    -------
    res_dict : dict
        dictionary with *keys* being the hyperparameters and *values* the
        samples from the uniform distribution.

    """
    # set seed
    tf.random.set_seed(seed)

    # Validate n_samples
    if not isinstance(n_samples, int) or n_samples <= 0:
        raise ValueError("n_samples must be a positive integer.")

    # Validate method
    if not isinstance(method, str):
        raise TypeError("method must be a string.")
    if method not in ["sobol", "lhs", "random"]:
        raise ValueError("Unsupported method. Choose from 'sobol', 'lhs', or 'random'.")

    # counter number of hyperparameters
    n_hypparam = 0
    name_hyper: List[str] = []
    res_dict = dict()

    if hyppar is None:
        if type(mean) is list:
            raise ValueError(
                "If different mean values should be specified per hyperparameter, the hyppar argument"
                + " cannot be None."
            )
        if type(radius) is list:
            raise ValueError(
                "If different radius values should be specified per hyperparameter, the hyppar argument"
                + " cannot be None."
            )
        for i in range(len(parameters)):
            for hyperparam in parameters[i]["hyperparams"]:
                dim = parameters[i]["hyperparams"][hyperparam]["dim"]
                name = parameters[i]["hyperparams"][hyperparam]["name"]
                n_hypparam += dim
                for j in range(dim):
                    name_hyper.append(name)

        # make sure type is correct
        mean = tf.cast(mean, tf.float32)
        radius = tf.cast(radius, tf.float32)

        # Generate samples based on the chosen method
        if method == "sobol":
            sampler = qmc.Sobol(d=n_hypparam, seed=seed)
            sample_data = sampler.random(n=n_samples)
        elif method == "lhs":
            sampler = qmc.LatinHypercube(d=n_hypparam, seed=seed)
            sample_data = sampler.random(n=n_samples)
        elif method == "random":
            uniform_samples = tfd.Uniform(
                tf.subtract(mean, radius), tf.add(mean, radius)
            ).sample((n_samples, n_hypparam))
        # Inverse transform
        if method == "sobol" or method == "lhs":
            sample_dat = tf.cast(tf.convert_to_tensor(sample_data), tf.float32)
            uniform_samples = tfd.Uniform(
                tf.subtract(mean, radius), tf.add(mean, radius)
            ).quantile(sample_dat)
        # store initialization results per hyperparameter
        for j, name in zip(range(n_hypparam), name_hyper):
            res_dict[name] = uniform_samples[:, j]
    else:
        if (type(mean) is not list) or (type(radius) is not list):
            raise ValueError(
                "mean and radius arguments of function uniform_samples must be of type list."
            )
        # initialize sampler
        if method == "sobol":
            sampler = qmc.Sobol(d=1, seed=seed)
        elif method == "lhs":
            sampler = qmc.LatinHypercube(d=1, seed=seed)

        for i, j, n in zip(mean, radius, hyppar):
            # make sure type is correct
            i = tf.cast(i, tf.float32)
            j = tf.cast(j, tf.float32)

            if method == "random":
                uniform_samples = tfd.Uniform(tf.subtract(i, j), tf.add(i, j)).sample(
                    (n_samples, 1)
                )
            else:
                sample_data = sampler.random(n=n_samples)
                # Inverse transform
                sample_dat = tf.cast(tf.convert_to_tensor(sample_data), tf.float32)
                uniform_samples = tfd.Uniform(tf.subtract(i, j), tf.add(i, j)).quantile(
                    sample_dat
                )

            res_dict[n] = tf.squeeze(uniform_samples, axis=-1)
    return res_dict


def init_runs(
    expert_elicited_statistics: Dict[str, tf.Tensor],
    initializer: Initializer,
    parameters: List[Parameter],
    trainer: Trainer,
    model: Dict[str, Any],
    targets: List[Target],
    network: Optional,
    expert: ExpertDict,
    seed: int,
):
    """
    Computes the discrepancy between expert data and simulated data for
    multiple hyperparameter initialization values.

    Parameters
    ----------
    expert_elicited_statistics : dict
        user-specified expert data as provided by :func:`elicit.elicit.Expert`.
    initializer : dict
        user-input from :func:`elicit.elicit.initializer`.
    parameters : list
        user-input from :func:`elicit.elicit.parameter`.
    trainer : dict
        user-input from :func:`elicit.elicit.trainer`.
    model : dict
        user-input from :func:`elicit.elicit.model`.
    targets : list
        user-input from :func:`elicit.elicit.target`.
    network : dict, optional
        user-input from one of the methods implemented in the
        :mod:`elicit.networks` module.
    expert : dict
        user-input from :func:`elicit.elicit.Expert`.
    seed : int
        internal seed for reproducible results

    Returns
    -------
    loss_list : list
        list with all losses computed for each initialization run.
    init_var_list : list
        list with initializer prior model for each run.
    init_matrix : dict
        dictionary with *keys* being the hyperparameter names and *values*
        being the drawn initial values per run.

    """
    # create a copy of the seed variable for incremental increase of seed
    # for each initialization run
    seed_copy = tf.identity(seed)
    # set seed
    tf.random.set_seed(seed)
    # initialize saving of results
    loss_list = []
    init_var_list = []
    save_prior = []

    # sample initial values
    if initializer["distribution"] is not None:
        init_matrix = uniform_samples(
            seed=seed,
            hyppar=initializer["distribution"]["hyper"],
            n_samples=initializer["iterations"],
            method=initializer["method"],
            mean=initializer["distribution"]["mean"],
            radius=initializer["distribution"]["radius"],
            parameters=parameters,
        )

    print("Initialization")

    for i in tqdm(range(initializer["iterations"])):
        # update seed
        seed_copy = seed_copy + 1
        # extract initial hyperparameter value for each run
        init_matrix_slice = {f"{key}": init_matrix[key][i] for key in init_matrix}
        # initialize prior distributions based on initial hyperparameters
        prior_model = el.simulations.Priors(
            ground_truth=False,
            init_matrix_slice=init_matrix_slice,
            trainer=trainer,
            parameters=parameters,
            network=network,
            expert=expert,
            seed=seed_copy,
        )

        # simulate from priors and generative model and compute the
        # elicited statistics corresponding to the initial hyperparameters
        (training_elicited_statistics, *_) = el.utils.one_forward_simulation(
            prior_model=prior_model,
            model=model,
            targets=targets,
            seed=seed
        )

        # compute discrepancy between expert elicited statistics and
        # simulated data corresponding to initial hyperparameter values
        (loss, *_) = el.losses.total_loss(
            elicit_training=training_elicited_statistics,
            elicit_expert=expert_elicited_statistics,
            targets=targets,
        )
        # save loss value, initial hyperparameter values and initialized prior
        # model for each run
        init_var_list.append(prior_model)
        save_prior.append(prior_model.trainable_variables)
        loss_list.append(loss.numpy())

    print(" ")
    return loss_list, init_var_list, init_matrix


def init_prior(
    expert_elicited_statistics: Dict[str, tf.Tensor],
    initializer: Optional[Initializer],
    parameters: List[Parameter],
    trainer: Trainer,
    model: Dict[str, Any],
    targets: List[Target],
    network: Optional[NFDict],
    expert: ExpertDict,
    seed: int,
):
    """
    Extracts target loss, corresponding initial hyperparameter values, and
    initialized prior model from :func:`init_runs`.

    Parameters
    ----------
    expert_elicited_statistics : dict
        user-specified expert data as provided by :func:`elicit.elicit.Expert`.
    initializer : dict, optional
        user-input from :func:`elicit.elicit.initializer`.
    parameters : list
        user-input from :func:`elicit.elicit.parameter`.
    trainer : dict
        user-input from :func:`elicit.elicit.trainer`.
    model : dict
        user-input from :func:`elicit.elicit.model`.
    targets : list
        user-input from :func:`elicit.elicit.target`.
    network : dict, optional
        user-input from one of the methods implemented in the
        :mod:`elicit.networks` module.
    expert : dict
        user-input from :func:`elicit.elicit.Expert`.
    seed : int
        internally used seed for reproducible results

    Returns
    -------
    init_prior_model : :mod:`elicit.simulations.Priors` object
        initialized priors that will be used for the training phase.
    loss_list : list
        list with all losses computed for each initialization run.
    init_prior : list
        list with initializer prior model for each run.
    init_matrix : dict
        dictionary with *keys* being the hyperparameter names and *values*
        being the drawn initial values per run.

    """

    if trainer["method"] == "parametric_prior" and initializer is not None:

        if initializer["hyperparams"] is None:

            loss_list, init_prior, init_matrix = init_runs(
                expert_elicited_statistics=expert_elicited_statistics,
                initializer=initializer,
                parameters=parameters,
                trainer=trainer,
                model=model,
                targets=targets,
                network=None,
                expert=expert,
                seed=seed,
            )

            # extract pre-specified quantile loss out of all runs
            # get corresponding set of initial values
            loss_quantile = initializer["loss_quantile"]
            index = tf.squeeze(
                tf.where(loss_list == tfp.stats.percentile(loss_list, [loss_quantile]))
            )

            init_prior_model = init_prior[int(index)]
        else:
            # prepare generative model
            init_prior_model = el.simulations.Priors(
                ground_truth=False,
                init_matrix_slice=initializer["hyperparams"],
                trainer=trainer,
                parameters=parameters,
                network=None,
                expert=expert,
                seed=seed,
            )
            # initialize empty variables for avoiding return conflicts
            loss_list, init_prior, init_matrix = (None, None, None)
    if trainer["method"] == "deep_prior" and network is not None:
        # prepare generative model
        init_prior_model = el.simulations.Priors(
            ground_truth=False,
            init_matrix_slice=None,
            trainer=trainer,
            parameters=parameters,
            network=network,
            expert=expert,
            seed=seed,
        )
        # initialize empty variables for avoiding return conflicts
        loss_list, init_prior, init_matrix = (None, None, None)

    return init_prior_model, loss_list, init_prior, init_matrix


def uniform(
    radius: Union[float, List[float]] = 1.0,
    mean: Union[float, List[float]] = 0.0,
    hyper: Optional[List[str]] = None,
) -> Uniform:
    """
    Specification of uniform distribution used for drawing initial values for
    each hyperparameter. Initial values are drawn from a uniform distribution
    ranging from ``mean-radius`` to ``mean+radius``.

    Parameters
    ----------
    radius : float or list[float]
        Initial values are drawn from a uniform distribution ranging from
        ``mean-radius`` to ``mean+radius``.
        If a ``float`` is provided the same setting will be used for all
        hyperparameters.
        If different settings per hyperparameter are required, a ``list`` of
        length equal to the number of hyperparameters should be provided.
        The order of values should be equivalent to the order of hyperparameter
        names provided in **hyper**.
        The default is ``1.``.
    mean : float or list[float]
        Initial values are drawn from a uniform distribution ranging from
        ``mean-radius`` to ``mean+radius``.
        If a ``float`` is provided the same setting will be used for all
        hyperparameters.
        If different settings per hyperparameter are required, a ``list`` of
        length equal to the number of hyperparameters should be provided.
        The order of values should be equivalent to the order of hyperparameter
        names provided in **hyper**.
        The default is ``0.``.
    hyper : list[str], optional
        List of hyperparameter names as specified in :func:`elicit.elicit.hyper`.
        The values provided in **radius** and **mean** should follow the order
        of hyperparameters indicated in this list.
        If a float is passed to **radius** and **mean** this argument is not
        necessary.

    Raises
    ------
    AssertionError
        ``hyper``, ``mean``, and ``radius`` must have the same length.

    Returns
    -------
    init_dict : dict
        Dictionary with all seetings of the uniform distribution used for
        initializing the hyperparameter values.

    """  # noqa: E501
    if hyper is not None:
        if len(hyper) != len(mean):
            raise AssertionError(
                "`hyper`, `mean`, and `radius` must have the same length."
            )

    init_dict = dict(radius=radius, mean=mean, hyper=hyper)

    return init_dict
