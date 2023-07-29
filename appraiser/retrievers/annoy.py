import os
import pickle

from annoy import AnnoyIndex
from loguru import logger
from operator import itemgetter
from appraiser.retrievers.retriever import Retriever, Extractor
import tqdm


class AnnoyRetriever(Retriever):

    def __init__(self, label: str, feature_extractor: Extractor, vector_size):
        super().__init__(label, feature_extractor)
        self.idx_x_path = None
        self.annoy_indexer = AnnoyIndex(vector_size, 'angular')
        self.idx_x_meta_path = os.path.join(self.label_save_dir, f'idx_x_meta_path_{feature_extractor.__name__}')
        self.vectors_base = self.initialize_vector_base()

    def get_cached_vectors(self):
        cached_buffer_exists = os.path.exists(self.vectors_full_path)
        if not cached_buffer_exists:
            return None
        else:
            with open(self.idx_x_meta_path, 'rb') as meta_file:
                self.idx_x_path = pickle.load(meta_file)
            vectors = self.annoy_indexer.load(self.vectors_full_path)
            return vectors

    def calculate_vectors(self):
        logger.info("Vector calculation started")
        idx_x_path = {}
        datapath = os.path.join(self.root_url, self.label)
        for idx, filename in tqdm.tqdm(enumerate(os.listdir(datapath))):
            img_full_path = os.path.join(datapath, filename)
            vec = self.feature_extractor(img_full_path)
            self.annoy_indexer.add_item(idx, vec[0])
            idx_x_path[idx] = img_full_path

        self.idx_x_path = idx_x_path

        if not os.path.exists(self.label_save_dir):
            os.mkdir(self.label_save_dir)
        with open(self.idx_x_meta_path, 'wb') as file:
            pickle.dump(idx_x_path, file)
        self.annoy_indexer.build(50)  # Choose right number of tree later
        self.annoy_indexer.save(self.vectors_full_path)

        return self.annoy_indexer

    def initialize_vector_base(self):
        vectors = self.get_cached_vectors()
        if vectors is not None:
            return vectors
        else:
            return self.calculate_vectors()

    def find_n_closest(self, search_vec, n_count, distance_comparator):
        closest_idx = self.annoy_indexer.get_nns_by_vector(search_vec, n_count)
        return itemgetter(*closest_idx)(self.idx_x_path)
