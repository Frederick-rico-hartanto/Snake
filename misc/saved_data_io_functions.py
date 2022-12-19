"""Define collection of file I/O functions used throughout program.

This module holds a series of file I/O functions responsible for reading and
writing to critical txt files that store important information and data used
throughout the program. Specific file names used: game_options.txt,
high_scores.txt, and user_preferences.txt (for now).

Functions:
    get_file_dict: Converts entered txt file into dict and returns it.
    get_score_name_list: Gets list of all (score, name) pairs.
    get_page_of_user_row: Gets list of all (rank, score, name) pairs on the
        same page as the entered one, as well as the entered pair's index.
    save_new_player_score: Saves entered (score, name) pair to high_scores txt.
    set_new_user_preferences: Saves changes to game options in user pref txt.
    update_settings_real_time: Allows settings to be updated real time while
        in game options screen.
"""

import os
import pygame


def get_file_dict(file_name: str) -> dict:
    """Return dict with contents of game_options or user_preferences text file.

    This function takes in a file name string (of either game_options.txt or
    user_preferences.txt), reads that specific file, and turns each line into
    a "key: value" pair with each key being a game option label and each value
    being either the currently selected option (for user_preferences file) or
    a list of available options for that specific game option label (for
    game_options file).

    Args:
        file_name: A string containing name of "target" file.

    Returns:
        file_dict: Newly constructed sentence.
    """
    with open(f'saved_data_snake/{file_name}.txt', 'r') as options_file:
        clean_line_list = options_file.read().splitlines()
        if file_name == 'user_preferences':
            file_dict = {line.split(': ')[0]: line.split(': ')[1] for line in clean_line_list}
        elif file_name == 'game_options':
            file_dict = {line.split(': ')[0]: line.split(': ')[1].split(', ') for line in clean_line_list}
        else:
            print('no such file exists')

    return file_dict


def get_score_name_list() -> list[list[int, str]]:
    """Read high_scores.txt and return sorted list of score, name pairs."""
    with open('saved_data_snake/high_scores.txt', 'r') as score_file:
        clean_line_list = score_file.read().splitlines()
        score_name_list = [line.split(', ') for line in clean_line_list]
        for pair in score_name_list:
            pair[0] = int(pair[0])
        score_name_list.sort(key=lambda x: x[0], reverse=True)

    return score_name_list


def get_page_of_user_row(score_name_list: list[list[int, str]], user_score: int, user_name: str,
                         ) -> tuple[list[list[int, int, str]], int]:
    """Return "page" list containing entered user (score, name) pair with ranks included.

    Accepts a list of (score, name) pairs, an int (user_score), and a str
    (user_name), and returns a "page list" of up to 10 (rank, score, name)
    pairs, as well as the user's (rank, score, name) pair index number of that
    "page list".

    Args:
        score_name_list: A list of all current score, name pairs (user_score
            and user_name args included).
        user_score: A user score found in score_name_list arg.
        user_name: A user name found in score_name_list arg.

    Returns:
        page_of_user_row: A list representing a "page" of 10 (rank, score,
            name) list pairs (each representing a row on that "page"), one of
            which is the (rank, score, name) pair of the entered user score
            and name args.
        user_row_index: User's (rank, score, name) "row" index number of the
            returned "page" list (page_of_user_row).
    """

    # Algorithm explained:
    # Find all indices of the (user_score, user_name) pair then save the last instance (last instance is always going
    # to be the most recently saved (score, name) pair). Take the last instance's index number and make a list of all
    # the pairs that are in its 10s place (i.e.: rank 1-10 for index 4 or rank 41-50 for index 45).

    user_score_name_pair = [user_score, user_name.lower()]

    # Reverse list and use index method to find the index of the "first" instance of user's (rank, score, name) pair
    # and then reverse the index and save it. (The first instance in the reversed list will be the same as the last
    # instance in the unreversed list). The index location of the user's (score, name) pair is the same as the index
    # location of the user's (rank, score, name) pair or "row".
    reversed_score_name_list = list(reversed(score_name_list))
    user_rank_score_name_pair_index_reversed = reversed_score_name_list.index(user_score_name_pair)
    user_rank_score_name_pair_index = len(score_name_list) - user_rank_score_name_pair_index_reversed - 1

    # Make the row (rank, score, name) version of the original input list and get the user's row.
    rank_score_name_row_list = [[rank, score, name] for rank, (score, name) in enumerate(score_name_list, start=1)]
    user_row = rank_score_name_row_list[user_rank_score_name_pair_index]

    # Use floor division by 10 on the index number of the user's row to find a tens place number which happens to be
    # the same as the page number that the user's row is on. Then we can just make and save the page_of_user_row using
    # a list comprehension and slicing the row list with [(tens_place_page_index * 10):(tens_place_page_index+1 * 10)].
    tens_place_page_index = user_rank_score_name_pair_index // 10
    page_of_user_row = [row for row in
                        rank_score_name_row_list[(tens_place_page_index * 10):((tens_place_page_index + 1) * 10)]]
    user_row_index = page_of_user_row.index(user_row)

    return page_of_user_row, user_row_index


def save_new_player_score(player_score: int, player_name: str) -> None:
    """Save entered player (score, name) pair into high_scores.txt file."""
    with open('saved_data_snake/high_scores.txt', 'a') as score_file:
        score = player_score
        name = player_name.lower()
        score_file.write(f'\n{score}, {name}')


def set_new_user_preferences(new_pref_list: list) -> None:
    """Overwrite user_preferences.txt with contents of entered pref list."""
    with open('saved_data_snake/user_preferences.txt', 'w') as pref_file:
        for item in new_pref_list:
            if item != new_pref_list[-1]:
                pref_file.write(item + '\n')
            else:
                pref_file.write(item)


def update_settings_real_time(bg_width: int, bg_height: int, old_user_prefs: dict = None,
                              ) -> tuple[str, str, pygame.Surface]:
    """Check if user preferences have been changed and return necessary data accordingly.

    This function establishes all user preferences settings and returns
    necessary data so that it can be saved and used in classes.

    Args:
        bg_width: Used to determine width of background return variable.
        bg_height: Used to determine height of background return variable.
        old_user_prefs: Optional dict argument used in game options screen in
            order to prevent music from restarting every time the settings are
            updated real time.

    Returns:
        sfx_bool: The currently selected option for whether sfx are on or off.
        music_setting: The currently selected option for whether music is on
            or off.
        background: The currently selected background for the game/program.
    """
    user_prefs = get_file_dict('user_preferences')
    sfx_bool = user_prefs.get('SOUND').split('~')[1]
    background_choice = user_prefs.get('BACKGROUND').split('~')[1]
    background = pygame.transform.scale(pygame.Surface.convert(pygame.image.load(
        os.path.join('project_assets', 'backgrounds', f'{background_choice}'))), (bg_width, bg_height))

    old_music_setting = None if old_user_prefs is None else old_user_prefs.get('MUSIC').split('~')[1]
    music_setting = user_prefs.get('MUSIC').split('~')[1]

    if old_user_prefs is None:  # Checks if no user_pref dict is entered (during initial game boot up).
        if music_setting == 'True':
            pygame.mixer.music.play(-1)
        else:
            pass
    # If old music setting is false and new music setting is true, play music from start.
    elif old_music_setting != music_setting == 'True':
        pygame.mixer.music.play(-1)
    # If old music setting is true and new music setting is false, stop music.
    elif old_music_setting != music_setting == 'False':
        pygame.mixer.music.stop()
    # If old and new music settings are both false or both true do nothing (this prevents the music from restarting or
    # running the unnecessary stop music method if the setting wasn't changed).
    else:
        pass

    return sfx_bool, music_setting, background
