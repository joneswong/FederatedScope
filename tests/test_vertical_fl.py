# Copyright (c) Alibaba, Inc. and its affiliates.
import unittest

from federatedscope.core.auxiliaries.data_builder import get_data
from federatedscope.core.auxiliaries.worker_builder import get_client_cls, get_server_cls
from federatedscope.core.auxiliaries.utils import setup_seed, setup_logger
from federatedscope.core.configs.config import global_cfg
from federatedscope.core.fed_runner import FedRunner


class vFLTest(unittest.TestCase):
    def setUp(self):
        print(('Testing %s.%s' % (type(self).__name__, self._testMethodName)))

    def set_config(self, cfg):
        backup_cfg = cfg.clone()

        cfg.use_gpu = False

        cfg.federate.mode = 'standalone'
        cfg.federate.total_round_num = 30
        cfg.federate.client_num = 2

        cfg.model.type = 'lr'
        cfg.model.use_bias = False

        cfg.optimizer.lr = 0.05

        cfg.data.type = 'vertical_fl_data'
        cfg.data.size = 50

        cfg.vertical.use = True
        cfg.vertical.key_size = 256

        cfg.trainer.type = 'none'
        cfg.eval.freq = 5
        cfg.eval.best_res_update_round_wise_key = "test_loss"

        return backup_cfg

    def test_vFL(self):
        backup_cfg = self.set_config(global_cfg)
        setup_seed(global_cfg.seed)
        setup_logger(global_cfg)

        data, modified_config = get_data(global_cfg.clone())
        global_cfg.merge_from_other_cfg(modified_config)
        self.assertIsNotNone(data)

        Fed_runner = FedRunner(data=data,
                               server_class=get_server_cls(global_cfg),
                               client_class=get_client_cls(global_cfg),
                               config=global_cfg.clone())
        self.assertIsNotNone(Fed_runner)
        test_results = Fed_runner.run()
        global_cfg.merge_from_other_cfg(backup_cfg)
        print(test_results)
        self.assertGreater(test_results['server_global_eval']['test_acc'], 0.9)


if __name__ == '__main__':
    unittest.main()
