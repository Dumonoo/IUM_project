from models.validation.validation import validate_model
from models.knn_model import KNNModel
from models.kmean_model import KMeanModel

from models.popular_model import PopularModel
from models.random_model import RandomModel

if __name__ == "__main__":
    print("KMean:", validate_model(KMeanModel()))
    print("KNN:", validate_model(KNNModel()))
    print("Random:", validate_model(RandomModel()))
    print("Popular:", validate_model(PopularModel()))
