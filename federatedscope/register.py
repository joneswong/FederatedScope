from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import logging


def register(key, module, module_dict):
    if key in module_dict:
        logging.warning('Key {} is already pre-defined, overwritten.'.format(key))
    module_dict[key] = module


data_dict = {}


def register_data(key, module):
    register(key, module, data_dict)


model_dict = {}


def register_model(key, module):
    register(key, module, model_dict)


trainer_dict = {}


def register_trainer(key, module):
    register(key, module, trainer_dict)


config_dict = {}


def register_config(key, module):
    register(key, module, config_dict)


metric_dict = {}


def register_metric(key, module):
    register(key, module, metric_dict)


criterion_dict = {}


def register_criterion(key, module):
    register(key, module, criterion_dict)


regularizer_dict = {}


def register_regularizer(key, module):
    register(key, module, regularizer_dict)


auxiliary_data_loader_PIA_dict = {}


def register_auxiliary_data_loader_PIA(key, module):
    register(key, module, auxiliary_data_loader_PIA_dict)
