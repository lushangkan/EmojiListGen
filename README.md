# EmojiListGen

A simple Python3 script to generate an emoji list for vue3-emoji-picker

## Usage

1. Install the dependencies:

        pip install -r requirements.txt

2. Download emoji-test.txt and emoji-zwj-sequences.txt from [Unicode.org](https://unicode.org/Public/emoji/latest/), put it in ./datas directory (create it if not exists).

3. Run main.py

        python main.py

If you need to get the local name of the emoji, add your local code to locals variable in main.py.   
   
Supported local codes:

| Code |      Language      |
|:----:|:------------------:|
|  en  |      English       |
|  es  |      Spanish       |
|  pt  |     Portuguese     |
|  it  |      Italian       |
|  fr  |       French       |
|  de  |       German       |
|  fa  |   Farsi/Persian    |
|  id  |     Indonesian     |
|  zh  | Simplified Chinese |
|  ja  |      Japanese      |
|  ko  |       Korean       |

If you need other languages, pleases see [Emoji Python](https://github.com/carpedm20/emoji/tree/master/utils)