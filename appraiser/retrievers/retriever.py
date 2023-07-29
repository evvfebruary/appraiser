import abc
import os
from io import BytesIO
from typing import Callable, TypeAlias

import torch

Extractor: TypeAlias = Callable[[str | BytesIO], torch.tensor]

ROOT_URL = "C:\\research\\data\\fashion_images_structured"
BUFFER_DIR = "C:\\research\\buffer"


class Retriever(abc.ABC):
    def __init__(
        self,
        label: str,
        feature_extractor: Extractor,
        root_url=ROOT_URL,
        vector_=None,
    ):
        self.label = label
        self.feature_extractor = feature_extractor
        self.root_url = root_url
        self.root_save_dir = os.path.join(BUFFER_DIR, type(self).__name__)
        if not os.path.exists(self.root_save_dir):
            os.mkdir(self.root_save_dir)
        self.label_save_dir = os.path.join(self.root_save_dir, label)
        self.vector_save_filename = (
            f"vectors_calculated_by_{feature_extractor.__name__}"
        )
        self.vectors_full_path = os.path.join(
            self.label_save_dir, self.vector_save_filename
        )

    @abc.abstractmethod
    def initialize_vector_base(self):
        ...

    @abc.abstractmethod
    def find_n_closest(self, n_count, search_vec, distance_comparator):
        ...
