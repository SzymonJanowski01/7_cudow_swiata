from typing import List


def get_color_pattern(points_list: List[int]) -> List[str]:
    """
    Returns a list of colors based on the number and value of points provided in the list
    :param points_list: List of points to be colored
    :return: List of colors
    """

    # Remove duplicates from the list
    points_list = set(points_list)
    list_len = len(points_list)

    color_patterns = {
        1: ["yellow"],
        2: ["darkgreen", "darkred"],
        3: ["darkgreen", "yellow", "darkred"],
        4: ["darkgreen", "lightgreen", "#FF474C", "darkred"],
        5: ["darkgreen", "green", "yellow", "red", "darkred"],
        6: ["darkgreen", "green", "lightgreen", "#FF474C", "red", "darkred"],
        7: ["darkgreen", "green", "lightgreen", "yellow", "#FF474C", "red", "darkred"]
    }

    return color_patterns[list_len]
