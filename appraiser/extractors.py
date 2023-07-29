import torch
from PIL import Image
from transformers import ViTFeatureExtractor

from appraiser.config import MODEL_DIR

extractor = ViTFeatureExtractor.from_pretrained(MODEL_DIR)


def read_image(filename):
    extension = filename.split('.')[-1]
    if extension == 'png':
        test_image = Image.open(filename).convert('RGBA')
        new_image = Image.new("RGBA", test_image.size, "WHITE")  # Create a white rgba background
        new_image.paste(test_image, (0, 0), test_image)
        image = new_image.convert('RGB')
    else:
        image = Image.open(filename).convert("RGB")
    return image


def embeddings_vec(filename, model, class_idx, feature_extractor=extractor):
    image = read_image(filename)
    sv_full = feature_extractor(images=image, return_tensors="pt").to("cuda")['pixel_values']
    vec_for_search = model.get_input_embeddings()(sv_full.cpu()).squeeze()[class_idx]
    return vec_for_search.reshape(-1, 768)


def raw_vec(filename, feature_extractor=extractor):
    image = read_image(filename)
    sv_full = feature_extractor(images=image, return_tensors="pt").to("cuda")['pixel_values']
    return sv_full.cpu()


def raw_vec_flatten(filename, feature_extractor=extractor):
    def reshape_torch_to_1d(tensor):
        return torch.reshape(tensor, (1, 150528))

    return reshape_torch_to_1d(raw_vec(filename, feature_extractor))
