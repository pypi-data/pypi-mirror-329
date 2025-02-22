import os
from ggfm.data import graph as gg
from typing import Callable, List, Optional
from ggfm.data import download_url,extract_zip


class DBLP:
    r"""A subset of the DBLP computer science bibliography website, as
    collected in the `"MAGNN: Metapath Aggregated Graph Neural Network for
    Heterogeneous Graph Embedding" <https://arxiv.org/abs/2002.01680>`_ paper.

    DBLP is a heterogeneous graph containing four types of entities - authors
    (4,057 nodes), papers (14,328 nodes), terms (7,723 nodes), and conferences
    (20 nodes).
    The authors are divided into four research areas (database, data mining,
    artificial intelligence, information retrieval).
    Each author is described by a bag-of-words representation of their paper
    keywords.
    see in ggfm.nginx.show/download/dataset/DBLP
    """





    url = 'https://www.dropbox.com/s/yh4grpeks87ugr2/DBLP_processed.zip?dl=1'

    def __init__(self, root: str = None, transform: Optional[Callable] = None,
                 pre_transform: Optional[Callable] = None, force_reload: bool = False):
        super().__init__(root, transform, pre_transform, force_reload=force_reload)
        self.data, self.slices = self.load_data(self.processed_paths[0])

    @property
    def raw_file_names(self) -> List[str]:
        return [
            'adjM.npz', 'features_0.npz', 'features_1.npz', 'features_2.npy',
            'labels.npy', 'node_types.npy', 'train_val_test_idx.npz'
        ]

    @property
    def processed_file_names(self) -> str:
        return 'DBLP_pre_data.pt'

    def download(self):
        path = download_url(self.url, self.raw_dir)
        extract_zip(path, self.raw_dir)
        os.remove(path)

    def process(self):
        data = gg()

        # node_types = ['author', 'paper', 'term', 'conference']
        # for i, node_type in enumerate(node_types[:2]):
        #     x = sp.load_npz(osp.join(self.raw_dir, f'features_{i}.npz'))
        #     data[node_type].x = tlx.convert_to_tensor(x.todense(), dtype=tlx.float32)
        #
        # x = np.load(osp.join(self.raw_dir, 'features_2.npy'))
        # data['term'].x = tlx.convert_to_tensor(x, dtype=tlx.int64)
        #
        # node_type_idx = np.load(osp.join(self.raw_dir, 'node_types.npy'))
        # node_type_idx = tlx.convert_to_tensor(node_type_idx, dtype=tlx.int64)
        # data['conference'].num_nodes = int(tlx.reduce_sum(tlx.cast(node_type_idx == 3, dtype=tlx.int64)))
        #
        # y = np.load(osp.join(self.raw_dir, 'labels.npy'))
        # data['author'].y = tlx.convert_to_tensor(y, dtype=tlx.int64)
        #
        # split = np.load(osp.join(self.raw_dir, 'train_val_test_idx.npz'))
        # for name in ['train', 'val', 'test']:
        #     idx = split[f'{name}_idx']
        #     idx = tlx.convert_to_tensor(idx, dtype=tlx.int64)
        #     mask = tlx.zeros((data['author'].num_nodes,), dtype=tlx.bool)
        #     mask = tlx.convert_to_numpy(mask)
        #     mask[idx] = True
        #     data['author'][f'{name}_mask'] = tlx.convert_to_tensor(mask, dtype=tlx.bool)
        #
        # s = {}
        # N_a = data['author'].num_nodes
        # N_p = data['paper'].num_nodes
        # N_t = data['term'].num_nodes
        # N_c = data['conference'].num_nodes
        # s['author'] = (0, N_a)
        # s['paper'] = (N_a, N_a + N_p)
        # s['term'] = (N_a + N_p, N_a + N_p + N_t)
        # s['conference'] = (N_a + N_p + N_t, N_a + N_p + N_t + N_c)
        #
        # A = sp.load_npz(osp.join(self.raw_dir, 'adjM.npz'))
        # for src, dst in product(node_types, node_types):
        #     A_sub = A[s[src][0]:s[src][1], s[dst][0]:s[dst][1]].tocoo()
        #     if A_sub.nnz > 0:
        #         row = tlx.convert_to_tensor(A_sub.row, dtype=tlx.int64)
        #         col = tlx.convert_to_tensor(A_sub.col, dtype=tlx.int64)
        #         data[src, dst].edge_index = tlx.stack([row, col], axis=0)
        #
        # if self.pre_transform is not None:
        #     data = self.pre_transform(data)
        #
        # self.save_data(self.collate([data]), self.processed_paths[0])
        pass
        # todo

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'