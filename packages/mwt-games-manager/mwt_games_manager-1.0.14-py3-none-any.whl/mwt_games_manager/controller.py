from flask import Blueprint, Response, request, jsonify
import mwt_games_manager.managers as managers
import mwt_games_manager.utils as utils

mwt_game_manager_blueprint = Blueprint('mwt-game-manager', __name__)


@mwt_game_manager_blueprint.route('/get-all-user-history', methods=['GET'])
def get_all_user_history():
    if not managers.client:
        raise Exception("module has not been setup properly")

    username = request.args.get("username")
    if not username:
        return Response(response="No username provided", status=400)

    game_histories = list(managers.client.collection("users").document(username).collection("game-data").document(
        managers.default_game_name).collection("history").stream())
    game_histories = [utils.stringify_game_history_dict(game_history.to_dict()) for game_history in game_histories]
    return jsonify(game_histories)


@mwt_game_manager_blueprint.route('/get-user-data', methods=['GET'])
def get_user_data():
    if not managers.client:
        raise Exception("module has not been setup properly")

    username = request.args.get("username")
    if not username:
        return Response(response="No username provided", status=400)

    game_data = managers.client.collection("users").document(username).collection("game-data").document(managers.default_game_name).get()
    return jsonify(game_data.to_dict())
