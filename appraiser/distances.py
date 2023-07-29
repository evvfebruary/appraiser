from scipy.spatial import distance


def scapy_distance(vec1, vec2, measure='cosine'):
    return distance.cdist(vec1.detach().numpy(), vec2.detach().numpy(), measure)
