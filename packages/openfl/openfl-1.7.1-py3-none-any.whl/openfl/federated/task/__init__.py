# Copyright 2020-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0


"""Task package."""

from importlib import util
from warnings import catch_warnings, simplefilter

with catch_warnings():
    simplefilter(action="ignore", category=FutureWarning)
    if util.find_spec("tensorflow") is not None:
        # ignore deprecation warnings in command-line interface
        import tensorflow  # NOQA

from openfl.federated.task.runner import TaskRunner  # NOQA

if util.find_spec("keras") is not None:
    from openfl.federated.task.fl_model import FederatedModel  # NOQA
    from openfl.federated.task.runner_keras import KerasTaskRunner  # NOQA
if util.find_spec("torch") is not None:
    from openfl.federated.task.fl_model import FederatedModel  # NOQA
    from openfl.federated.task.runner_pt import PyTorchTaskRunner  # NOQA
if util.find_spec("xgboost") is not None:
    from openfl.federated.task.fl_model import FederatedModel  # NOQA
    from openfl.federated.task.runner_xgb import XGBoostTaskRunner  # NOQA
