# noqa SPDX-FileCopyrightText: 2024 Florence Bockting <florence.bockting@tu-dortmund.de>
#
# noqa SPDX-License-Identifier: Apache-2.0

import inspect
import tensorflow as tf
import tensorflow_probability as tfp

from typing import Optional, Union, Callable, Dict, List
from elicit.types import Trainer, Parameter, NFDict, ExpertDict

tfd = tfp.distributions


# initalize generator model
class Priors(tf.Module):
    """
    Initializes the hyperparameters (i.e., trainable variables)

    Parameters
    ----------
    ground_truth : bool
        True if expert data are simulated from a given ground truth (oracle)
    init_matrix_slice : dict[str, tf.Tensor], optional
        samples drawn from the initialization distribution to initialize
        the hyperparameter of the parametric prior distributions
        Only required for method="parametric_prior" otherwise None.
    trainer : dict
        specification of training settings and meta-information for
        workflow using :func:`elicit.elicit.trainer`
    parameters : list
        list of model parameters specified with
        :func:`elicit.elicit.parameter`.
    network : dict, optional
        specification of neural network using a method implemented in
        :mod:`elicit.networks`.
        Only required for ``deep_prior`` method. For ``parametric_prior``
        use ``None``.
    expert : dict
        provide input data from expert or simulate data from oracle with
        either the ``data`` or ``simulator`` method of the
        :mod:`elicit.elicit.Expert` module.
    seed : int
        seed used for learning.
    """

    def __init__(
        self,
        ground_truth: bool,
        init_matrix_slice: Optional[Dict[str, tf.Tensor]],
        trainer: Trainer,
        parameters: List[Parameter],
        network: Optional[NFDict],
        expert: ExpertDict,
        seed: int,
    ):

        self.ground_truth = ground_truth
        self.init_matrix_slice = init_matrix_slice
        self.trainer = trainer
        self.parameters = parameters
        self.network = network
        self.expert = expert

        # set seed
        tf.random.set_seed(seed)
        # initialize hyperparameter for learning (if true hyperparameter
        # are given, no initialization is needed)
        if not self.ground_truth:
            self.init_priors = intialize_priors(
                self.init_matrix_slice,
                self.trainer["method"],
                seed,
                self.parameters,
                self.network,
            )
        else:
            self.init_priors = None

    def __call__(self) -> tf.Tensor:  # shape=[B,num_samples,num_params]
        """
        Samples from the initialized prior distribution(s).

        Returns
        -------
        prior_samples : tf.Tensor, shape: [B,num_samples,num_params]
            Samples from prior distribution(s).

        """
        prior_samples = sample_from_priors(
            initialized_priors=self.init_priors,
            ground_truth=self.ground_truth,
            num_samples=self.trainer["num_samples"],
            B=self.trainer["B"],
            seed=self.trainer["seed"],
            method=self.trainer["method"],
            parameters=self.parameters,
            network=self.network,
            expert=self.expert,
        )

        return prior_samples


def intialize_priors(
    init_matrix_slice: Optional[Dict[str, tf.Tensor]],
    method: str,
    seed: int,
    parameters: List[Parameter],
    network: Optional[NFDict],
) -> Dict[str, tf.Tensor]:
    """
    Initialize prior distributions.

    Parameters
    ----------
    init_matrix_slice : tf.Tensor, optional
        samples drawn from the initialization distribution to initialize
        the hyperparameter of the parametric prior distributions
        Only for method="parametric_prior", otherwise None.
    method : str
        parametric_prior or deep_prior method as specified in
        :func:`elicit.elicit.trainer`
    seed : int
        seed of current workflow run as specified in
        :func:`elicit.elicit.trainer`
    parameters : list[dict]
        list of model parameter specifications using
        :func:`elicit.elicit.parameter`.
    network : dict, optional
        specification of neural network using a method implemented in
        :mod:`elicit.networks`.
        Only required for ``deep_prior`` method. For ``parametric_prior``
        use ``None``.

    Returns
    -------
    init_prior : dict[str, tf.Tensor]
        returns initialized prior distributions ready for prior sampling.

    """
    # set seed
    tf.random.set_seed(seed)

    if method == "parametric_prior":
        # create dict with all hyperparameters
        hyp_dict = dict()
        hp_keys = list()
        param_names = list()
        hp_names = list()
        initialized_hyperparam = dict()

        for i in range(len(parameters)):
            hyperparameter = parameters[i]["hyperparams"]
            num_hyperpar = len(hyperparameter)

            hyp_dict[f"param{i}"] = hyperparameter
            param_names += [parameters[i]["name"]] * num_hyperpar
            hp_keys += list(hyperparameter.keys())
            for j in range(num_hyperpar):
                current_key = list(hyperparameter.keys())[j]
                hp_names.append(hyperparameter[current_key]["name"])

        checked_params = list()
        for j, (i, hp_n, hp_k) in enumerate(
            zip(tf.unique(param_names).idx, hp_names, hp_keys)
        ):

            hp_dict = parameters[i]["hyperparams"][hp_k]

            if hp_dict["shared"] and hp_dict["name"] in checked_params:
                pass
            else:
                # get initial value
                initial_value = float(init_matrix_slice[hp_n])
                # initialize hyperparameter
                initialized_hyperparam[f"{hp_k}_{hp_n}"] = tf.Variable(
                    initial_value=initial_value,
                    trainable=True,
                    name=f"{hp_dict['constraint_name']}.{hp_n}",
                )

                # save initialized priors
                init_prior = initialized_hyperparam

            if hp_dict["shared"]:
                checked_params.append(hp_n)

    if method == "deep_prior":
        # for more information see BayesFlow documentation
        # https://bayesflow.org/api/bayesflow.inference_networks.html
        INN = network["inference_network"]

        invertible_neural_network = INN(**network["network_specs"])

        # save initialized priors
        init_prior = invertible_neural_network

    return init_prior


def sample_from_priors(
    initialized_priors: Union[Dict[str, tf.Variable], Callable],
    ground_truth: bool,
    num_samples: int,
    B: int,
    seed: int,
    method: str,
    parameters: List[Parameter],
    network: Optional[NFDict],
    expert: ExpertDict,
) -> tf.Tensor:  # shape=[B,num_samples,num_params]
    """
    Samples from initialized prior distributions.

    Parameters
    ----------
    initialized_priors : dict[str, tf.Variable] or Callable
        initialized prior distributions ready for prior sampling.
    ground_truth : bool
        True if expert data is simulated from ground truth.
    num_samples : int
        number of samples from the prior(s).
    B : int
        batch size.
    seed : int
        seed used for learning.
    method : str
        parametric_prior or deep_prior method as specified in
        :func:`elicit.elicit.trainer`
    parameters : list
        list of model parameters specified with
        :func:`elicit.elicit.parameter`.
    network : dict, optional
        specification of neural network using a method implemented in
        :mod:`elicit.networks`.
        Only required for ``deep_prior`` method. For ``parametric_prior``
        use ``None``.
    expert : callable
        provide input data from expert or simulate data from oracle with
        either the ``data`` or ``simulator`` method of the
        :mod:`elicit.elicit.Expert` module.

    Returns
    -------
    prior_samples : tf.Tensor, shape: [B, num_samples, num_params]
        Samples from prior distributions.

    """
    # set seed
    tf.random.set_seed(seed)
    if ground_truth:
        # number of samples for ground truth
        rep_true = expert["num_samples"]
        priors = []

        for prior in list(expert["ground_truth"].values()):
            # sample from the prior distribution
            prior_sample = prior.sample((1, rep_true))
            # ensure that all samples have the same shape
            if len(prior_sample.shape) < 3:
                prior = tf.expand_dims(prior_sample, -1)
            else:
                prior = prior_sample
            priors.append(prior)
        # concatenate all prior samples into one tensor
        prior_samples = tf.concat(priors, axis=-1)

    if (method == "parametric_prior") and (not ground_truth):
        priors = []

        for i in range(len(parameters)):
            # get the prior distribution family as specified by the user
            prior_family = parameters[i]["family"]

            hp_k = list(parameters[i]["hyperparams"].keys())
            init_dict = {}
            for k in hp_k:
                hp_n = parameters[i]["hyperparams"][k]["name"]
                hp_constraint = parameters[i]["hyperparams"][k]["constraint"]
                init_key = f"{k}_{hp_n}"
                # init_dict[f"{k}"]=initialized_priors[init_key]
                init_dict[f"{k}"] = hp_constraint(initialized_priors[init_key])
            # sample from the prior distribution
            priors.append(prior_family(**init_dict).sample((B, num_samples)))
        # stack all prior distributions into one tf.Tensor of
        # shape (B, S, num_parameters)
        if len(priors[0].shape) < 3:
            prior_samples = tf.stack(priors, axis=-1)
        else:
            prior_samples = tf.concat(priors, axis=-1)

    if (method == "deep_prior") and (not ground_truth):
        # initialize base distribution
        base_dist = network["base_distribution"](num_params=len(parameters))
        # sample from base distribution
        u = base_dist.sample((B, num_samples))
        # apply transformation function to samples from base distr.
        (unconstr_priors, _) = initialized_priors(u, condition=None, inverse=False)
        # apply parameter constraints if specified
        constr_priors = []
        for j in range(len(parameters)):
            constr = parameters[j]["constraint"]
            constr_priors.append(constr(unconstr_priors[:, :, j]))
        prior_samples = tf.stack(constr_priors, axis=-1)
    return prior_samples


def simulate_from_generator(
    prior_samples: tf.Tensor, seed: int, model: dict  # shape=[B,num_samples,num_params]
) -> Dict[str, tf.Tensor]:
    """
    Simulates data from the specified generative model.

    Parameters
    ----------
    prior_samples : tf.Tensor, shape: [B, num_samples, num_params]
        samples from prior distributions.
    seed : int
        seed used for learning. Specification in :func:`elicit.elicit.trainer`.
    model : dict
        specification of generative model using :func:`elicit.elicit.model`.

    Returns
    -------
    model_simulations : dict[str, tf.Tensor]
        simulated data from generative model.

    """
    # set seed
    tf.random.set_seed(seed)
    # get model and initialize generative model
    GenerativeModel = model["obj"]
    generative_model = GenerativeModel()
    # get model specific arguments (that are not prior samples)
    add_model_args = model.copy()
    add_model_args.pop("obj")
    # simulate from generator
    if add_model_args is None:
        model_simulations = generative_model(prior_samples)
    elif "kwargs" not in inspect.getfullargspec(GenerativeModel.__call__)[0]:
        model_simulations = generative_model(prior_samples, **add_model_args)
    else:
        add_model_args["seed"] = seed
        model_simulations = generative_model(prior_samples, **add_model_args)

    return model_simulations
