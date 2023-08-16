import requests
import regex as re

from bs4 import BeautifulSoup

cookies = {
    # Please generate your own
}

headers = {
    # Please generate your own
}

# optional
proxies = None

def get_emojipedia_page(emoji: str, local_code: str):
    r = requests.get('https://emojipedia.org/' + local_code + '/' + emoji, headers=headers, proxies=proxies,
                     cookies=cookies)

    if r.status_code == 200:
        return r.text
    else:
        return Exception('Could not get page')


def get_page_title(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title


def get_emoji_len(emoji: str):
    return len(emoji)


def get_name_from_title(title_ele: str, emoji_len: int):
    return re.sub(r"<.[^<>]*>", "", str(title_ele))[emoji_len + 1:-6:]


def get_emoji_local_name(emoji: str, local_code: str):
    page_html = get_emojipedia_page(emoji, local_code)
    emoji_len = get_emoji_len(emoji)

    if isinstance(page_html, Exception):
        return page_html

    page_title = str(get_page_title(page_html))

    # if title has emoji
    if page_title.find(emoji) != -1:
        local_name = get_name_from_title(page_title, emoji_len)
        return local_name
    else:
        return Exception('Could not get name')


# For test
if __name__ == '__main__':
    emoji = '👍'

    local_name = get_emoji_local_name(emoji, 'zh')
    print('\n' + local_name + '\n')
