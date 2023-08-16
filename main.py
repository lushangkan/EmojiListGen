import json
import time
from concurrent.futures import ThreadPoolExecutor
import local_name as ln

if __name__ == '__main__':

    emoji_full = json.load(open('./emoji.json', 'r', encoding='utf-8'))

    categories = {}

    threadpool = ThreadPoolExecutor(max_workers=16)
    threads = []
    failure_emojis = []

    # If you want to get the local name of the emoji, please uncomment the following code
    # local_code = 'zh'

    def get_emoji_u_code(emoji: str):
        u_code = ''

        for x in emoji:
            u_code += hex(ord(x))[2:].lower() + '-'

        return u_code[:-1]


    def get_emoji_from_u_code(u_code: str):
        emoji = ''

        for x in u_code.split('-'):
            emoji += chr(int(x, 16))

        return emoji


    # If you want to get the local name of the emoji, please uncomment the following code
    # def get_local_name(obj: dict):
    #
    #     emoji = get_emoji_from_u_code(obj['u'])
    #
    #     local_name = ln.get_emoji_local_name(emoji, local_code)
    #
    #     if (local_name is None) or (isinstance(local_name, Exception)):
    #         print('Emoji: ' + emoji + ' Failed')
    #         failure_emojis.append(obj)
    #         return
    #
    #     obj['n'].append(local_name)


    print('Reordering...')
    for emoji_obj in emoji_full:
        emoji_category = str(emoji_obj['category']).replace(' ', '').replace('&', '_').lower()

        if emoji_category not in categories:
            categories[emoji_category] = []

        emoji_name = emoji_obj['aliases']
        emoji_name.append(emoji_obj['description'])

        new_obj = {
            'n': emoji_name,
            'u': get_emoji_u_code(emoji_obj['emoji'])
        }

        categories[emoji_category].append(new_obj)

    # If you want to get the local name of the emoji, please uncomment the following code
    # print('Getting local name...')
    # for emoji_category in categories:
    #     for emoji_obj in categories[emoji_category]:
    #         threads.append(threadpool.submit(get_local_name, emoji_obj))
    #
    # last_alive_threads = 0
    # last_update_alive_time = time.time()
    #
    # while True:
    #     alive_threads = 0
    #     dead_threads = 0
    #     for thread in threads:
    #         if thread.done():
    #             dead_threads += 1
    #         else:
    #             alive_threads += 1
    #
    #     print('Alive: ' + str(alive_threads) + ' Dead: ' + str(dead_threads) + ' Total: ' + str(
    #         len(threads)) + ' Failure: ' + str(len(failure_emojis)) + ' Last Alive Threads: ' + str(
    #         last_alive_threads) + ' Last Alive Time: ' + str(
    #         time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_update_alive_time))))
    #
    #     if alive_threads != last_alive_threads:
    #         last_update_alive_time = time.time()
    #         last_alive_threads = alive_threads
    #     elif time.time() - last_update_alive_time > 60:
    #         print('Timeout')
    #         for thread in threads:
    #             thread.cancel()
    #         break
    #     if alive_threads == 0:
    #         break
    #
    #     time.sleep(5)

    print('Saving emojis...')
    json.dump(categories, open('emoji_categories.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

