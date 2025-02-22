from datetime import datetime
import mwt_games_manager.managers as mg
from mwt_games_manager.models.feature import Feature
from mwt_games_manager.models.product import Product


def add_product(product):
    """
    Add a product to the database
    :param product:
    :return:
    """
    mg.client.collection("products").document(product.product_id).add(product.__dict__)


def update_product(product):
    """
    Update a product from the database
    :param product:
    :return:
    """
    mg.client.collection("products").document(product.product_id).add(product.__dict__)


def delete_product(product_id):
    """
    Delete a product from the database
    :param product_id:
    :return:
    """
    mg.client.collection("products").document(product_id).delete()


def get_product(product_id):
    """
    Retrieve a product from the database
    :param product_id:
    :return:
    """
    product = mg.client.collection("products").document(product_id).get()
    product = Product(**product.to_dict())
    return product


def get_all_products():
    """
    Retrieve all the products from the database
    :return:
    """
    products = list(mg.client.collection("products").stream())
    products = [Product(**product.to_dict()) for product in products]
    return products


def add_product_feature(product_id, feature):
    """
    Add a product feature to the product
    :param product_id:
    :param feature:
    :return:
    """
    mg.client.collection("products").document(product_id).collection("features").add(feature.__dict__)


def get_product_features(product_id):
    """
    Retrieve all the product features from the database
    :param product_id:
    :return:
    """
    features = list(mg.client.collection("products").document(product_id).collection("features"))
    features = [Feature(**feature) for feature in features]
    return features


def add_user_product(username, product):
    """
    Add a product under a username
    :param username:
    :param product:
    :return:
    """
    mg.client.collection("users").document(username).collection("products").document(product.product_id).set(product.__dict__)


def update_user_product(username, product):
    """
    Update a product under a username
    :param username:
    :param product:
    :return:
    """
    mg.client.collection("users").document(username).collection("products").document(product.product_id).set(product.__dict__)


def delete_user_product(username, product_id):
    """
    Delete a product under a username
    :param username:
    :param product_id:
    :return:
    """
    mg.client.collection("users").document(username).collection("products").document(product_id).delete()


def get_user_product(username, product_id):
    """
    Get a product under a username
    :param username:
    :param product_id:
    :return:
    """
    product = mg.client.collection("users").document(username).collection("products").document(product_id).get()
    product = Product(**product.to_dict())
    return product
