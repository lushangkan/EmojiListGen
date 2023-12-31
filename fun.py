import pathlib
import re
import emoji as emoji_lib
from typing import Union


def get_emoji_obj(emoji: str, emoji_list: dict):
    for (emoji_list_group, emoji_list_group_list) in emoji_list.items():
        if emoji_list_group_list.get(emoji) is not None:
            return emoji_list_group_list[emoji], emoji_list_group
    return None


def get_emoji_by_name(emoji_name: str, emoji_list: dict) -> Union[tuple, None]:
    for (emoji_list_group, emoji_list_group_list) in emoji_list.items():
        for (emoji, emoji_obj) in emoji_list_group_list.items():
            if emoji_obj['name'] == emoji_name:
                return emoji, emoji_obj
    return None


def is_emoji(emoji: str, emoji_list: dict) -> bool:
    emoji_obj = get_emoji_obj(emoji, emoji_list)[0]
    if emoji_obj is None:
        return False
    if emoji_obj['type'] == 'fully-qualified':
        return True
    return False


def get_emoji_u_code(emoji: str) -> Union[str, bool]:
    if len(emoji) == 0:
        return False

    u_code = ''

    for x in emoji:
        u_code += hex(ord(x))[2:].lower() + '-'

    return u_code[:-1]


def get_emoji_from_u_code(u_code: str) -> str:
    emoji = ''

    for x in u_code.split('-'):
        emoji += chr(int(x, 16))

    return emoji


def check_file_is_exists(data_path: pathlib.Path, emoji_file: pathlib.Path, emoji_zwj_file: pathlib.Path) -> bool:
    if not data_path.exists():
        data_path.mkdir()
        print('Created ./datas')
        print('Please download emoji-test.txt from https://unicode.org/Public/emoji/{version}/emoji-test.txt and put '
              'it in ./datas')
        return False
    elif not emoji_file.exists():
        print('Please download emoji-test.txt from https://unicode.org/Public/emoji/{version}/emoji-test.txt and put '
              'it in ./datas')
        return False
    elif not emoji_zwj_file.exists():
        print('Please download emoji-zwj-sequences.txt from https://unicode.org/Public/emoji/{'
              'version}/emoji-zwj-sequences.txt and put it in ./datas')
        return False

    return True


def get_emoji_local_name(locals: list, emoji: str) -> list:
    local_name = []

    if emoji_lib.EMOJI_DATA.get(emoji) is not None:
        if emoji_lib.EMOJI_DATA[emoji].get('name') is not None:
            local_name.append(emoji_lib.EMOJI_DATA[emoji]['name'])
        if emoji_lib.EMOJI_DATA[emoji].get('alias') is not None and 'en' in locals:
            if isinstance(emoji_lib.EMOJI_DATA[emoji]['alias'], list):
                for alias in emoji_lib.EMOJI_DATA[emoji]['alias']:
                    alias = re.search(r':(.*):', alias).group(1).strip()
                    local_name.append(alias)
            elif isinstance(emoji_lib.EMOJI_DATA[emoji]['alias'], str):
                alias = re.search(r':(.*):', emoji_lib.EMOJI_DATA[emoji]['alias']).group(1).strip()
                local_name.append(alias)

        for local in locals:
            if emoji_lib.EMOJI_DATA[emoji].get(local) is not None and emoji_lib.EMOJI_DATA[emoji][local] != '' and \
                    emoji_lib.EMOJI_DATA[emoji][local] is not None:
                name = re.search(r':(.*):', emoji_lib.EMOJI_DATA[emoji][local]).group(1).strip()
                local_name.append(name)

    return local_name


def get_full_emoji_list(locals: list, emoji_file: pathlib.Path) -> dict:
    emoji_list = {}
    with open(emoji_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            # If line is group name
            if line.startswith('# group:'):
                group_name = line[9:-1:]
                group_id = group_name.replace(' ', '').replace('&', '_').lower()
                if group_id not in emoji_list.keys():
                    emoji_list[group_id] = {}
                continue
            # If line is comment
            elif line.startswith('#'):
                continue
            # If line is empty line
            elif line == '\n' or line == '':
                continue

            regex = r"^(.*?)[^\S\n]{2,};\s(.*?)\s*#\s(\S+)\s(E[\w.]*)\s(.*?)$"

            line_group = re.search(regex, line, re.MULTILINE & re.UNICODE)

            if line_group is None or not line_group or len(line_group.groups()) == 0:
                continue

            emoji_u_code = line_group.group(1).strip().replace(' ', '-').lower()
            emoji_type = line_group.group(2).strip()
            emoji = line_group.group(3).strip()
            emoji_version = line_group.group(4).strip()
            emoji_name = line_group.group(5).strip()

            local_name = get_emoji_local_name(locals, emoji)

            emoji_list[list(emoji_list.keys())[-1]][emoji] = {
                'u_code': emoji_u_code,
                'type': emoji_type,
                'name': emoji_name,
                'local_name': local_name,
                'version': emoji_version,
            }

    return emoji_list


def get_zwj_emoji_list(emoji_zwj_file: pathlib.Path):
    zwj_emoji_list = {}
    with open(emoji_zwj_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith('# RGI_Emoji_ZWJ_Sequence: '):
                group_name = line.split('# RGI_Emoji_ZWJ_Sequence: ')[1].strip()
                group_id = group_name.replace(' ', '').replace('&', '_').lower()
                zwj_emoji_list[group_id] = {}
            elif line.startswith('#'):
                continue
            elif line == '\n' or line == '':
                continue

            regex = r"^(.*?)[^\S\n]*;[^\S\n](.*?)[^\S\n]*;[^\S\n](.*?)(?:[^\S\n]+)#[^\S\n]*(E[\w.]*)[^\S\n]*(?:\[\w\])[^\S\n]*\((.*)\)$"

            line_group = re.search(regex, line, re.MULTILINE & re.UNICODE)

            if line_group is None or not line_group or len(line_group.groups()) == 0:
                continue

            emoji_u_code = line_group.group(1).strip().replace(' ', '-').lower()
            emoji_type = line_group.group(2).strip()
            emoji_name = line_group.group(3).strip()
            emoji_version = line_group.group(4).strip()
            emoji = line_group.group(5).strip()

            zwj_emoji_list[list(zwj_emoji_list.keys())[-1]][emoji] = {
                'u_code': emoji_u_code,
                'type': emoji_type,
                'name': emoji_name,
                'version': emoji_version,
            }

    return zwj_emoji_list


def clean_zwj_emoji_from_emoji_list(emoji_list: dict, zwj_emoji_list: dict, exclude_groups: list = None, exclude_emojis: list = None):
    for (group_name, group_emoji_list) in zwj_emoji_list.items():
        if exclude_groups is not None and group_name in exclude_groups:
            continue

        for (emoji, emoji_obj) in group_emoji_list.items():
            if len(emoji_obj['name'].split(':')[0]) > 1:
                original_name = emoji_obj['name'].split(':')[0]
                original_emoji = get_emoji_by_name(original_name, zwj_emoji_list)
                if original_emoji is not None:
                    original_emoji, original_emoji_obj = original_emoji
                    is_exist = False
                    for exclude_emoji in exclude_emojis:
                        if exclude_emoji in original_emoji or exclude_emoji == original_emoji:
                            is_exist = True
                            continue
                    if is_exist:
                        continue

            is_exist = False
            for exclude_emoji in exclude_emojis:
                if exclude_emoji in emoji or exclude_emoji == emoji:
                    is_exist = True
                    continue

            if is_exist:
                continue

            for (emoji_list_group, emoji_list_group_list) in emoji_list.items():
                if emoji_list_group_list.get(emoji) is not None:
                    del emoji_list[emoji_list_group][emoji]
                    break


def is_has_component(emoji: str, emoji_list: dict) -> Union[Exception, bool]:
    components = ['🏻', '🏼', '🏽', '🏾', '🏿', '🦰', '🦱', '🦳', '🦲']
    emoji_obj, emoji_group = get_emoji_obj(emoji, emoji_list)
    if emoji_obj is None:
        return Exception('Could not get emoji object')
    elif emoji_group == 'food_drink' or emoji_group == 'animals_nature' or emoji_group == 'travel_places' or emoji_group == 'activities' or emoji_group == 'objects' or emoji_group == 'symbols' or emoji_group == 'flags':
        return False
    elif len(emoji_obj['name'].split(':')) > 1:
        return True
    for component in components:
        if emoji.find(component) != -1:
            return True


def get_original_emoji(emoji_group: str, emoji_list: dict, emoji: str) -> Union[str, Exception]:
    components = ['🏻', '🏼', '🏽', '🏾', '🏿', '🦰', '🦱', '🦳', '🦲']
    emoji_name = emoji_list[emoji_group][emoji]['name']

    if get_emoji_from_u_code('200d') not in emoji or emoji_name.split(':')[0] == 1:
        for component in components:
            if component in emoji:
                original_emoji = emoji.replace(component, '')
                if is_emoji(original_emoji, emoji_list):
                    if len(original_emoji) == 1 and len(
                            get_emoji_obj(original_emoji, emoji_list)[0]['name'].split(':')) == 1:
                        return original_emoji
                    elif len(get_emoji_obj(original_emoji, emoji_list)[0]['name'].split(':')) > 1:
                        original_emoji_name = get_emoji_obj(original_emoji, emoji_list)[0]['name'].split(':')[0]
                        original_emoji = get_emoji_by_name(original_emoji_name, emoji_list)[0]
                        if original_emoji is None:
                            return Exception('Could not get original emoji')
                        else:
                            return original_emoji
                    return original_emoji
                elif len(original_emoji) == 1 and is_emoji(original_emoji + get_emoji_from_u_code('fe0f'), emoji_list):
                    return original_emoji + get_emoji_from_u_code('fe0f')
                else:
                    return Exception('Could not get original emoji')
        if len(get_emoji_obj(emoji, emoji_list)[0]['name'].split(':')) > 1:
            original_emoji_name = get_emoji_obj(emoji, emoji_list)[0]['name'].split(':')[0]
            original_emoji = get_emoji_by_name(original_emoji_name, emoji_list)[0]
            if original_emoji is None:
                return Exception('Could not get original emoji')
            else:
                return original_emoji
        return Exception('Could not get original emoji')
    else:
        original_emoji_name = emoji_name.split(':')[0]
        result = get_emoji_by_name(original_emoji_name, emoji_list)
        if result is None:
            return Exception('Could not get original emoji')
        return result[0]


def convert_to_picker_emoji_list(emoji_list: dict) -> dict:
    picker_emoji_list = {}
    for (emoji_list_group, emoji_list_group_list) in emoji_list.items():

        if emoji_list_group == 'component':
            continue

        # If emoji_list_group is not exists in picker_emoji_list
        if picker_emoji_list.get(emoji_list_group) is None:
            picker_emoji_list[emoji_list_group] = []

        picker_emoji_group = picker_emoji_list[emoji_list_group]

        for (emoji, emoji_obj) in emoji_list_group_list.items():

            # If emoji are not supported
            if emoji_obj['type'] == 'minimally-qualified' or emoji_obj['type'] == 'unqualified':
                continue

            # If it has skin tone
            appended_v = False
            if is_has_component(emoji, emoji_list):
                original_emoji = get_original_emoji(emoji_list_group, emoji_list, emoji)

                if original_emoji is Exception:
                    print('Could not get original emoji')

                for picker_emoji in picker_emoji_group:
                    if picker_emoji.get('u') is not None and picker_emoji['u'] == get_emoji_u_code(original_emoji):
                        if picker_emoji.get('v') is None:
                            picker_emoji['v'] = []
                        picker_emoji['v'].append(emoji_obj['u_code'])
                        appended_v = True
                        break
            if appended_v:
                continue

            picker_emoji_group.append({
                'n': [emoji_obj['name'], *emoji_obj['local_name']],
                'u': emoji_obj['u_code'],
            })

    return picker_emoji_list
