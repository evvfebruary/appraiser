import os
import pickle
from loguru import logger
import tqdm

from appraiser.retrievers.retriever import Retriever, Extractor


class BruteForceRetriever(Retriever):

    def __init__(self, label: str, feature_extractor: Extractor):

        super().__init__(label, feature_extractor)
        self.vectors_base = self.initialize_vector_base()
        if not os.path.exists(self.root_save_dir):
            os.mkdir(self.root_save_dir)

    def get_cached_vectors(self):
        cached_buffer_exists = os.path.exists(self.vectors_full_path)
        if not cached_buffer_exists:
            return None
        else:
            with open(self.vectors_full_path, 'rb') as vectors_file:
                vectors = pickle.load(vectors_file)
            return vectors

    def calculate_vectors(self):
        logger.info("Vector calculation started")
        vectors_base = []
        datapath = os.path.join(self.root_url, self.label)
        for idx, filename in tqdm.tqdm(enumerate(os.listdir(datapath))):
            img_full_path = os.path.join(datapath, filename)
            vec = self.feature_extractor(img_full_path)
            vectors_base.append({'vector': vec.cpu(),
                                 'img_full_path': img_full_path,
                                 "idx": idx})

        if not os.path.exists(self.label_save_dir):
            os.mkdir(self.label_save_dir)

        with open(self.vectors_full_path, 'wb') as vectors_file:
            pickle.dump(vectors_base, vectors_file)

        return vectors_base

    def initialize_vector_base(self):
        vectors = self.get_cached_vectors()
        if vectors is not None:
            return vectors
        else:
            return self.calculate_vectors()

    def find_n_closest(self, search_vec, n_count, distance_comparator):
        distances = {}
        for vec in self.vectors_base:
            distance = distance_comparator(search_vec, vec['vector'])
            idx = vec['idx']
            distances[idx] = {"img_full_path": vec['img_full_path'], 'distance': distance}
        n_closest = [item[-1]['img_full_path'] for item in
                     sorted(distances.items(), key=lambda item: item[-1]['distance'])[:n_count]]
        return n_closest
