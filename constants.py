from utils import average
from utils import least_misery
from utils import disagreement_variance
from utils import average_pairwise_disagreement
from utils import cosine_similarity
GROUP_UTILITY_SWITCH = {
    "average": average,
    "least_misery": least_misery
}

DISAGREEMENT_SWITCH = {
    "variance": disagreement_variance,
    "pair_wise": average_pairwise_disagreement
}

SIMILARITY_SWITCH={
    "cosine": cosine_similarity
}