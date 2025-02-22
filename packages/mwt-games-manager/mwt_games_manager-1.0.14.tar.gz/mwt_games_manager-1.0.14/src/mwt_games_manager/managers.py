import datetime

import firebase_admin
from firebase_admin import firestore, get_app
from google.cloud.firestore_v1 import FieldFilter

from mwt_games_manager.models.game_history import GameHistory
from mwt_games_manager.models.general_game_data import GeneralGameData
from mwt_games_manager.models.user import User
from mwt_games_manager.models.feature import Feature
from mwt_games_manager.models.product import Product
from flask_bcrypt import check_password_hash

client = None
try:
    client = firestore.client(get_app("games-manager"))
except Exception as e:
    pass

default_game_name = ""


def setup_module(database_credentials, game_name):
    """
    required for initializing the sdk and setting up a default game name
    :param database_credentials:
    :param game_name:
    :return:
    """
    global client, default_game_name
    firestore_app = firebase_admin.initialize_app(database_credentials, name="games-manager")
    client = firestore.client(firestore_app)
    default_game_name = game_name


def is_user_first_game(username, game_name=False):
    """
    checks whether the user has played this game before or not
    :param username:
    :param game_name:
    :return:
    """
    global client, default_game_name
    if not game_name:
        game_name = default_game_name
    if not client:
        raise Exception("module has not been setup properly")

    game_data = client.collection("users").document(username).collection("game-data").document(game_name).get().exists
    return not game_data


def setup_user_game_data(username, game_data=GeneralGameData(), game_name=False):
    """
    setting up game data for a user
    :param username:
    :param game_data:
    :param game_name:
    :return:
    """
    global client, default_game_name
    if not game_name:
        game_name = default_game_name
    if not client:
        raise Exception("module has not been setup properly")

    if not game_data.game_name:
        game_data.game_name = game_name
    if not game_data.date_started:
        game_data.date_started = datetime.datetime.now()
    client.collection("users").document(username).collection("game-data").document(game_name).set(game_data.__dict__)


def update_user_game_data(username, game_data, game_name=False):
    """
    updating the game data for a user
    :param username:
    :param game_data:
    :param game_name:
    :return:
    """
    global client, default_game_name
    if not game_name:
        game_name = default_game_name
    if not client:
        raise Exception("module has not been setup properly")

    client.collection("users").document(username).collection("game-data").document(game_name).set(game_data.__dict__)


def get_user_game_data(username, game_name=False):
    """
    getting the game data for a user
    :param username:
    :param game_name:
    :return:
    """
    global client, default_game_name
    if not game_name:
        game_name = default_game_name
    if not client:
        raise Exception("module has not been setup properly")

    game_data = client.collection("users").document(username).collection("game-data").document(game_name).get()
    if not game_data.exists:
        return False
    return GeneralGameData(**game_data.to_dict())


def _initial_check(username, game_name=False):
    global client, default_game_name
    if not game_name:
        game_name = default_game_name
    if not client:
        raise Exception("module has not been setup properly")

    if is_user_first_game(username, game_name=game_name):
        setup_user_game_data(username, game_name=game_name)


def add_game_history(username, game_history, game_name=False):
    """
    adding a game history for the user
    :param username:
    :param game_history:
    :param game_name:
    :return:
    """
    global default_game_name
    if not game_name:
        game_name = default_game_name
    _initial_check(username, game_name)
    client.collection("users").document(username).collection("game-data").document(game_name).collection(
        "history").document(game_history.game_id).set(game_history.__dict__)


def update_game_history(username, game_history, game_name=False):
    """
    updating a game history for the user
    :param username:
    :param game_history:
    :param game_name:
    :return:
    """
    global default_game_name
    if not game_name:
        game_name = default_game_name
    _initial_check(username, game_name)
    client.collection("users").document(username).collection("game-data").document(game_name).collection(
        "history").document(game_history.game_id).set(game_history.__dict__)


def delete_game_history(username, game_id, game_name=False):
    """
    deleting a game history for the user
    :param username:
    :param game_id:
    :param game_name:
    :return:
    """
    global default_game_name
    if not game_name:
        game_name = default_game_name
    _initial_check(username, game_name)
    client.collection("users").document(username).collection("game-data").document(game_name).collection(
        "history").document(game_id).delete()


def get_game_history(username, game_id, game_name=False):
    """
    getting a game history for the user
    :param username:
    :param game_id:
    :param game_name:
    :return:
    """
    global default_game_name
    if not game_name:
        game_name = default_game_name
    _initial_check(username, game_name)
    game_history = client.collection("users").document(username).collection("game-data").document(game_name).collection(
        "history").document(game_id).get().to_dict()

    if game_history is None:
        return False

    game_history = GameHistory(**game_history)
    return game_history


def validate_user(username, password, game_name=False):
    """
    authenticate whether username and password are valid
    :param username:
    :param password:
    :param game_name:
    :return:
    """
    global default_game_name
    if not game_name:
        game_name = default_game_name
    _initial_check(username, game_name)
    user = client.collection("users").document(username).get()
    if not user.exists:
        return False

    user = User(**user.to_dict())

    return check_password_hash(user.password, password)


def fetch_user(username):
    """
    fetching the user information for the user
    :param username:
    :return:
    """
    doc = client.collection("users").document(username).get()
    if not doc.exists:
        return False

    user = User(**doc.to_dict())
    return user


def get_all_game_data(username):
    """
    fetching game data for all the games
    :param username:
    :return:
    """
    docs = list(client.collection("users").document(username).collection("game-data").stream())
    game_datas = [GeneralGameData(**game_data.to_dict()) for game_data in docs]
    return game_datas


def get_features(username, game_name=None):
    """
    fetches all the features the user has for a specific game
    :param username:
    :param game_name:
    :return:
    """
    global default_game_name
    if not game_name:
        game_name = default_game_name
    products = list(client.collection("users").document(username).collection("products").stream())
    products = [Product(**product.to_dict()) for product in products]

    features = []

    for product in products:
        product_features = list(client.collection("products").document(product.product_id).collection("features").where(
            filter=FieldFilter("game", "==", game_name)).stream())
        product_features = [Feature(**feature.to_dict()) for feature in product_features]
        features.append(product_features)

    return features
