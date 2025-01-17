import numpy as np
import pickle

import federatedscope.register as register


def load_toy_data(config=None):

    generate = config.federate.mode.lower() == 'standalone'

    def _generate_data(client_num=5,
                       instance_num=1000,
                       feature_num=5,
                       save_data=False):
        """
        Generate data in FedRunner format
        Args:
            client_num:
            instance_num:
            feature_num:
            save_data:

        Returns:
            {
                '{client_id}': {
                    'train': {
                        'x': ...,
                        'y': ...
                    },
                    'test': {
                        'x': ...,
                        'y': ...
                    },
                    'val': {
                        'x': ...,
                        'y': ...
                    }
                }
            }

        """
        weights = np.random.normal(loc=0.0, scale=1.0, size=feature_num)
        bias = np.random.normal(loc=0.0, scale=1.0)
        data = dict()
        for each_client in range(1, client_num + 1):
            data[each_client] = dict()
            client_x = np.random.normal(loc=0.0,
                                        scale=0.5 * each_client,
                                        size=(instance_num, feature_num))
            client_y = np.sum(client_x * weights, axis=-1) + bias
            client_y = np.expand_dims(client_y, -1)
            client_data = {'x': client_x, 'y': client_y}
            data[each_client]['train'] = client_data

        # test data
        test_x = np.random.normal(loc=0.0,
                                  scale=1.0,
                                  size=(instance_num, feature_num))
        test_y = np.sum(test_x * weights, axis=-1) + bias
        test_y = np.expand_dims(test_y, -1)
        test_data = {'x': test_x, 'y': test_y}
        for each_client in range(1, client_num + 1):
            data[each_client]['test'] = test_data

        # val data
        val_x = np.random.normal(loc=0.0,
                                 scale=1.0,
                                 size=(instance_num, feature_num))
        val_y = np.sum(val_x * weights, axis=-1) + bias
        val_y = np.expand_dims(val_y, -1)
        val_data = {'x': val_x, 'y': val_y}
        for each_client in range(1, client_num + 1):
            data[each_client]['val'] = val_data

        # server_data
        data[0] = dict()
        data[0]['train'] = None
        data[0]['val'] = val_data
        data[0]['test'] = test_data

        if save_data:
            # server_data = dict()
            save_client_data = dict()

            for client_idx in range(0, client_num + 1):
                if client_idx == 0:
                    filename = 'data/server_data'
                else:
                    filename = 'data/client_{:d}_data'.format(client_idx)
                with open(filename, 'wb') as f:
                    save_client_data['train'] = {
                        k: v.tolist()
                        for k, v in data[client_idx]['train'].items()
                    }
                    save_client_data['val'] = {
                        k: v.tolist()
                        for k, v in data[client_idx]['val'].items()
                    }
                    save_client_data['test'] = {
                        k: v.tolist()
                        for k, v in data[client_idx]['test'].items()
                    }
                    pickle.dump(save_client_data, f)

        return data

    if generate:
        data = _generate_data(client_num=config.federate.client_num,
                              save_data=config.eval.save_data)
    else:
        with open(config.distribute.data_file, 'rb') as f:
            data = pickle.load(f)
        for key in data.keys():
            data[key] = {k: np.asarray(v)
                         for k, v in data[key].items()
                         } if data[key] is not None else None

    return data, config


def get_data(config):
    for func in register.data_dict.values():
        data_and_config = func(config)
        if data_and_config is not None:
            return data_and_config
    if config.data.type.lower() == 'toy':
        data, modified_config = load_toy_data(config)
    elif config.data.type.lower() in ['femnist', 'celeba']:
        from federatedscope.cv.dataloader import load_cv_dataset
        data, modified_config = load_cv_dataset(config)
    elif config.data.type.lower() in [
            'shakespeare', 'twitter', 'subreddit', 'synthetic'
    ]:
        from federatedscope.nlp.dataloader import load_nlp_dataset
        data, modified_config = load_nlp_dataset(config)
    elif config.data.type.lower() in [
            'cora',
            'citeseer',
            'pubmed',
            'dblp_conf',
            'dblp_org',
    ] or config.data.type.lower().startswith('csbm'):
        from federatedscope.gfl.dataloader import load_nodelevel_dataset
        data, modified_config = load_nodelevel_dataset(config)
    elif config.data.type.lower() in ['ciao', 'epinions', 'fb15k-237', 'wn18']:
        from federatedscope.gfl.dataloader import load_linklevel_dataset
        data, modified_config = load_linklevel_dataset(config)
    elif config.data.type.lower() in [
            'hiv', 'proteins', 'imdb-binary'
    ] or config.data.type.startswith('graph_multi_domain'):
        from federatedscope.gfl.dataloader import load_graphlevel_dataset
        data, modified_config = load_graphlevel_dataset(config)
    elif config.data.type.lower() == 'vertical_fl_data':
        from federatedscope.vertical_fl.dataloader import load_vertical_data
        data, modified_config = load_vertical_data(config, generate=True)
    elif 'movielens' in config.data.type.lower():
        from federatedscope.mf.dataloader import load_mf_dataset
        data, modified_config = load_mf_dataset(config)
    else:
        raise ValueError('Data {} is not provided'.format(config.data.type))

    return data, modified_config
