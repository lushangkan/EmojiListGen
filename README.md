# EmojiListGen

A simple Python3 script to generate an emoji list for vue3-emoji-picker

## Usage

1. Install the dependencies:

        pip install -r requirements.txt

2. Download full emoji list from [Gemoji project](https://github.com/github/gemoji/blob/master/db/emoji.json) (Many thanks to Gemoji for the emoji files!😊), put it in the same directory as main.py, and rename it to emoji.json

3. Run main.py

        python main.py

If you need to get the local name of the emoji, please flow the steps below:

1. Open main.py ,uncomment the the code that is commented out as getting the local name part of the code

    like this:

        # File /main.py
        # ...

        - # If you want to get the local name of the emoji, please uncomment the following code
        - #local_code = 'zh'

        + local_code = 'zh'

2. Modify the local_code variable to the language code you want to get

    like this:

        # File /main.py
        # ...

        - local_code = 'zh'
        + local_code = 'ja'

3. Open get_loacl_name.py, set cookies and headers to their own

    1. Open [emojipedia](https://emojipedia.org/) use chromium browser (like Chrome, Edge)
    
    2. Open the developer tools (Usually press the F12 key)

    3. Click the Network tab

    4. Refresh the page

    5. Find the request named "emojipedia.org" in the Network tab (Usually the first request)

    6. Right-click the request and select "Copy" -> "Copy as cURL (bash)"

    7. Open [CurlConverter](https://curlconverter.com/), paste the copied content into the text box, and select "Python - requests" in the drop-down box below

    8. Copy the cookies and headers in the generated code to the corresponding variables in get_loacl_name.py

4. If you need to use proxies, please modify the proxies variable in get_loacl_name.py, instead, if you don't need to use the proxy, set the proxies variable to None or remove the proxies variable

