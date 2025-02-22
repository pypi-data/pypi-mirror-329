jsonable = (bool, str, int, float, type(None), type([]), type({}))


def is_jsonable(obj):
    """
    checks whether the data can be processed with json or not
    :param obj:
    :return:
    """
    return isinstance(obj, jsonable)


def stringify_game_history_dict(game_history_dict):
    """
    stringifies all the keys in game_history dict if they are not primitive type or array or dict
    :param game_history_dict:
    :return: dictionary
    """
    for key in game_history_dict.keys():
        if not is_jsonable(game_history_dict[key]):
            game_history_dict[key] = str(game_history_dict[key])

    return game_history_dict
