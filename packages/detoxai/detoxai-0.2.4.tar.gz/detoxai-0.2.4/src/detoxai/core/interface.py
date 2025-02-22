import torch.nn as nn
from copy import deepcopy
import logging
import traceback
import signal
from datetime import datetime
import multiprocessing as mp

# Project imports
from ..methods import (
    SavaniRP,
    SavaniLWO,
    SavaniAFT,
    ZhangM,
    RRCLARC,
    PCLARC,
    ACLARC,
    LEACE,
    RejectOptionClassification,
    NaiveThresholdOptimizer,
    FineTune,
    ModelCorrectionMethod,
)
from .model_wrappers import FairnessLightningWrapper
from .results_class import CorrectionResult
from ..utils.dataloader import DetoxaiDataLoader
from ..metrics.fairness_metrics import AllMetrics
from .evaluation import evaluate_model
from .mcda_helpers import filter_pareto_front, select_best_method
from .interface_helpers import construct_metrics_config, infer_layers

logger = logging.getLogger(__name__)

SUPPORTED_METHODS = [
    "SAVANIRP",
    "SAVANILWO",
    "SAVANIAFT",
    "ZHANGM",
    "RRCLARC",
    "PCLARC",
    "ACLARC",
    "LEACE",
    "ROC",
    "NT",
    "FINETUNE",
]


DEFAULT_METHODS_CONFIG = {
    "global": {
        "last_layer_name": "last",
        "experiment_name": "default",
        "device": "cpu",
        "dataloader": None,
        "test_dataloader": None,
        "method_timeout": 600,  # seconds
    },
    "PCLARC": {
        "cav_type": "signal",
        "cav_layers": "penultimate",
        "use_cache": True,
    },
    "ACLARC": {
        "cav_type": "signal",
        "cav_layers": "penultimate",
        "use_cache": True,
    },
    "RRCLARC": {
        "cav_type": "signal",
        "cav_layers": "penultimate",
        "use_cache": True,
    },
    "LEACE": {
        "intervention_layers": "penultimate",
        "use_cache": True,
    },
    "SAVANIRP": {},
    "SAVANILWO": {
        "n_layers_to_optimize": 4,
    },
    "SAVANIAFT": {},
    "ZHANGM": {},
    "ROC": {
        "theta_range": (0.55, 0.95),
        "theta_steps": 20,
        "metric": "EO_GAP",
        "objective_function": "lambda fairness, accuracy: fairness * accuracy",  # ruff: noqa
    },
    "NT": {
        "threshold_range": (0.1, 0.9),
        "threshold_steps": 20,
        "metric": "EO_GAP",
        "objective_function": "lambda fairness, accuracy: -fairness",  # ruff: noqa
    },
    "FINETUNE": {
        "fine_tune_epochs": 1,
        "lr": 1e-4,
    },
}


def parse_methods_config(methods_config: dict) -> dict:
    """
    Here we compare what was passed and overwrite the default configuration
    """
    for key, dic in DEFAULT_METHODS_CONFIG.items():
        if key not in methods_config:
            methods_config[key] = dic
        else:
            # Else we overwrite common values with the passed ones
            # And add the missing ones
            for pk in dic:
                if pk not in methods_config[key]:
                    methods_config[key][pk] = dic[pk]

    return methods_config


def debias(
    model: nn.Module,
    dataloader: DetoxaiDataLoader,
    methods: list[str] | str = "all",
    metrics: list[str] | str = "all",
    methods_config: dict = {},
    pareto_metrics: list[str] = ["balanced_accuracy", "equalized_odds"],
    return_type: str = "pareto-front",
    device: str = "cpu",
    include_vanila_in_results: bool = True,
    test_dataloader: DetoxaiDataLoader = None,
) -> CorrectionResult | list[CorrectionResult]:
    """
    Run a suite of correction methods on the model and return the results

    Args:
        `model`: Model to run the correction methods on
        `dataloader`: DetoxaiDataLoader object with the dataset
        `harmful_concept`: Concept to debias -- this is the protected attribute # NOT SUPPORTED YET
        `methods`: List of correction methods to run
        `metrics`: List of metrics to include in the configuration
        `methods_config`: Configuration for each correction method
        `pareto_metrics`: List of metrics to use for the pareto front and selection of best method
        `return_type` (optional): Type of results to return. Options are 'pareto-front', 'all', 'best'
            "pareto-front": Return the results CorrectionResult objects only for results on the pareto front
            "all": Return the results for all correction methods
            "best": Return the results for the best correction method, chosen with ideal point method from pareto front
        `device` (optional): Device to run the correction methods on
        `include_vanila_in_results` (optional): Include the vanilla model in the results
        `test_dataloader` (optional): DataLoader for the test dataset. If not provided, the original dataloader is used


    """

    logging.debug(f"Received configuration:\n  {methods_config}")

    # Parse methods config (deepcopy to avoid modifying the original)
    config = parse_methods_config(deepcopy(methods_config))

    logging.debug(f"Resolved configuration to:\n {config}")

    # Parse methods
    if methods == "all":
        methods = SUPPORTED_METHODS
    else:
        # Ensure all methods passed are supported
        for method in methods:
            if method.upper() not in SUPPORTED_METHODS:
                raise ValueError(f"Method {method} not supported")

        # Capitalize all methods
        methods = [method.upper() for method in methods]

    config["global"]["device"] = device

    # Append a timestamp to the experiment name
    timestep = datetime.now().strftime("%Y%m%d-%H%M%S%f")
    exp_name = f"{config['global']['experiment_name']}_{timestep}"
    config["global"]["experiment_name"] = exp_name
    logging.info(f"Experiment name: {config['global']['experiment_name']}")

    # # ------------------------------------------------
    # # DATASET HANDLING IS TODO HERE
    # # Load supported tags ie. protected attributes
    # supported_tags = load_supported_tags()
    # if harmful_concept not in supported_tags["attributes"]:
    #     raise ValueError(
    #         f"Attribute {harmful_concept} not found in supported attributes"
    #     )
    # else:
    #     prot_attr_arity = len(supported_tags["mapping"][harmful_concept])
    #     class_labels = NotImplementedError  # TODO: Take it from somewhere

    # pass

    class_labels = dataloader.get_class_names()
    prot_attr_arity = 2  # TODO only supported binary protected attributes

    # Create an AllMetrics object
    metrics_calculator = AllMetrics(
        construct_metrics_config(metrics),
        class_labels=class_labels,
        num_groups=prot_attr_arity,
    )

    # Wrap model
    model = FairnessLightningWrapper(
        model,
        performance_metrics=metrics_calculator.get_performance_metrics(),
        fairness_metrics=metrics_calculator.get_fairness_metrics(),
    )

    results = []
    for method in methods:
        logger.info("=" * 50 + f" Running method {method} " + "=" * 50)
        method_kwargs = config[method] | config["global"]
        method_kwargs["model"] = deepcopy(model)
        method_kwargs["dataloader"] = dataloader
        method_kwargs["test_dataloader"] = test_dataloader
        result = run_correction(method, method_kwargs, pareto_metrics)
        results.append(result)

    if include_vanila_in_results:
        vanilla_result = CorrectionResult(
            method="Vanilla",
            model=model,
            metrics=evaluate_model(
                model,
                dataloader if test_dataloader is None else test_dataloader,
                pareto_metrics,
                device=device,
            ),
        )
        results.append(vanilla_result)

    if return_type == "pareto-front":
        return filter_pareto_front(results)
    elif return_type == "all":
        return results
    elif return_type == "best":
        return select_best_method(results)
    else:
        raise ValueError(f"Invalid return type {return_type}")


def run_correction(
    method: str, method_kwargs: dict, pareto_metrics: list[str] | None = None
) -> CorrectionResult:
    """
    Run the specified correction method

    Args:
        method: Correction method to run
        kwargs: Arguments for the correction method
    """
    metrics = {"pareto": {}, "all": {}}
    failed = False

    # Copy and remove model from kwargs used for debug printing
    __cfg_copy = deepcopy(method_kwargs)
    __cfg_copy.pop("model")
    logging.debug(f"Running correction method {method} with kwargs: \n {__cfg_copy}")

    match method.upper():
        case "SAVANIRP":
            corrector = SavaniRP(**method_kwargs)
        case "SAVANILWO":
            corrector = SavaniLWO(**method_kwargs)
        case "SAVANIAFT":
            corrector = SavaniAFT(**method_kwargs)
        case "ZHANGM":
            corrector = ZhangM(**method_kwargs)
        case "RRCLARC":
            corrector = RRCLARC(**method_kwargs)
        case "PCLARC":
            corrector = PCLARC(**method_kwargs)
        case "ACLARC":
            corrector = ACLARC(**method_kwargs)
        case "LEACE":
            corrector = LEACE(**method_kwargs)
        case "ROC":
            corrector = RejectOptionClassification(**method_kwargs)
        case "NT":
            corrector = NaiveThresholdOptimizer(**method_kwargs)
        case "FINETUNE":
            corrector = FineTune(**method_kwargs)
        case _:
            logger.error(ValueError(f"Correction method {method} not found"))
            failed = True

    if not failed:
        # Parse intervention layers
        if "intervention_layers" in method_kwargs:
            method_kwargs["intervention_layers"] = infer_layers(
                corrector, method_kwargs["intervention_layers"]
            )
            logging.info(
                f"Resolved intervention layers: {method_kwargs['intervention_layers']}"
            )

        # Parse cav layers
        if "cav_layers" in method_kwargs:
            method_kwargs["cav_layers"] = infer_layers(
                corrector, method_kwargs["cav_layers"]
            )
            logging.info(f"Resolved CAV layers: {method_kwargs['cav_layers']}")

        # Parse last layer name
        if "last_layer_name" in method_kwargs:
            method_kwargs["last_layer_name"] = infer_layers(
                corrector, method_kwargs["last_layer_name"]
            )[0]
            logging.info(
                f"Resolved last layer name: {method_kwargs['last_layer_name']}"
            )

        # Precompute CAVs if required
        if corrector.requires_acts:
            if "intervention_layers" not in method_kwargs:
                lays = method_kwargs["cav_layers"]
            else:
                lays = method_kwargs["intervention_layers"]
            corrector.extract_activations(method_kwargs["dataloader"], lays)

            logger.debug(f"Computing CAVs on layers: {lays}")

            if corrector.requires_cav:
                corrector.compute_cavs(method_kwargs["cav_type"], lays)

        logger.debug(f"Running correction method {method}")

        # Here we finally run the correction method
        try:
            timeout = method_kwargs.pop("method_timeout", None)
            if timeout is not None and timeout > 0:
                logger.debug(f"Running {method} w {timeout} s timeout")

                # if isinstance(corrector, LEACE):
                #     logger.debug(f"Running {method} with multiprocessing")
                #     success = _mp_apply_model_correction_w_timeout(
                #         corrector, method_kwargs, timeout
                #     )
                # else:
                success = _apply_model_correction_w_timeout(
                    corrector, method_kwargs, timeout
                )

                if not success:
                    failed = True
                    logger.error(traceback.format_exc())
                    logger.error(f"Correction method {method} failed")
            else:
                corrector.apply_model_correction(**method_kwargs)

            if not failed:
                logger.debug(f"Correction method {method} applied")

                method_kwargs["model"] = corrector.get_lightning_model()

                # Remove gradients
                for param in method_kwargs["model"].parameters():
                    param.requires_grad = False

                test_dl = method_kwargs["test_dataloader"]
                metrics = evaluate_model(
                    method_kwargs["model"],
                    method_kwargs["dataloader"] if test_dl is None else test_dl,
                    pareto_metrics,
                    device=method_kwargs["device"],
                )

                # Move to CPU
                method_kwargs["model"].to("cpu")

        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(f"Error running correction method {method}: {e}")
            failed = True

    else:
        metrics = {"pareto": {}, "all": {}}

    return CorrectionResult(
        method=method, model=method_kwargs["model"], metrics=metrics
    )


def _apply_model_correction_w_timeout(
    corrector: ModelCorrectionMethod, method_kwargs: dict, timeout: float
) -> bool:
    """
    Execute the apply_model_correction method of the corrector
    as a task with timeout to prevent infinite execution.

    Args:
        corrector: Object with an apply_model_correction method.
        method_kwargs: Arguments to pass to the method.
        timeout: Maximum execution time in seconds.

    Returns:
        bool: True if successful, False on error or timeout.
    """

    def handler(signum, frame):
        raise Exception("Timeout")

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(int(timeout))

    try:
        corrector.apply_model_correction(**method_kwargs)
        signal.alarm(0)  # Disable the alarm
        return True

    except Exception as e:
        signal.alarm(0)

        if "Timeout" not in str(e):
            logger.error(traceback.format_exc())
            logger.error(
                f"Error running correction method {corrector.__class__.__name__}: {e}"
            )
            return False
        else:
            logger.error(traceback.format_exc())
            logger.error(f"Correction method {corrector.__class__.__name__} timed out")
            return False


def _mp_apply_model_correction_w_timeout(
    corrector: ModelCorrectionMethod, method_kwargs: dict, timeout: float
) -> bool:
    """
    Execute the apply_model_correction method of the corrector in a separate process
    as a task with timeout to prevent infinite execution.

    Args:
        corrector: Object with an apply_model_correction method.
        method_kwargs: Arguments to pass to the method.
        timeout: Maximum execution time in seconds.

    Returns:
        bool: True if successful, False on error or timeout.
    """

    try:
        p = mp.Process(
            target=_apply_model_correction_w_timeout,
            args=(corrector, method_kwargs, timeout),
        )
        p.start()

        p.join(timeout)

        if p.is_alive():
            p.kill()
            p.join()
            return False
        else:
            return True
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(
            f"Error running correction method {corrector.__class__.__name__}: {e}"
        )
        return False
