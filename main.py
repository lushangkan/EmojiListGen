import json
import pathlib
import os

import fun

if __name__ == '__main__':

    print('\n')

    data_path = pathlib.Path('./datas')
    emoji_file = pathlib.Path('./datas/emoji-test.txt')
    emoji_zwj_file = pathlib.Path('./datas/emoji-zwj-sequences.txt')

    locals = ['en']
    print('locals:', *locals)

    # Check file is exists
    if not fun.check_file_is_exists(data_path, emoji_file, emoji_zwj_file):
        exit(1)

    # Get emoji list
    print('Getting emoji list...')
    emoji_list = fun.get_full_emoji_list(locals, emoji_file)
    # Get zwj emoji list
    print('Getting zwj emoji list...')
    zwj_emoji_list = fun.get_zwj_emoji_list(emoji_zwj_file)
    # Clean zwj emoji from emoji list
    print('Cleaning zwj emoji from emoji list...')
    fun.clean_zwj_emoji_from_emoji_list(emoji_list, zwj_emoji_list, ['other'],
                                        ['🧑‍🎄', '🧑🏻‍🎄', '🧑🏼‍🎄', '🧑🏽‍🎄', '🧑🏾‍🎄', '🧑🏿‍🎄', '🧑‍⚕️', '🧑‍⚖️', '🧑‍✈️', '🧑‍🌾',
                                         '🧑‍🍳', '🧑‍🍼', '🧑‍🎓', '🧑‍🎤', '🧑‍🎨', '🧑‍🏫', '🧑‍🏭', '🧑‍💻', '🧑‍💼', '🧑‍🔧', '🧑‍🔬',
                                         '🧑‍🚀', '🧑‍🚒', '🧑‍🦯', '🧑‍🦼', '🧑‍🦽', '🧜‍♀️', '🧜‍♂️'])
    # Convert to picker emoji list
    print('Converting to picker emoji list...')
    picker_emoji_list = fun.convert_to_picker_emoji_list(emoji_list)

    print('Saving emojis...')
    json.dump(picker_emoji_list, open('emoji_categories.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

