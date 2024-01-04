#!/usr/bin/env python3

# <xbar.title>Weibo Hot Search</xbar.title>
# <xbar.version>v1.0.0</xbar.version>
# <xbar.author>Xylitol</xbar.author>
# <xbar.author.github>C5H12O5</xbar.author.github>
# <xbar.desc>Displays the hot search list on Sina Weibo.</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.abouturl>https://github.com/C5H12O5/xbar-plugins</xbar.abouturl>

# <xbar.var>number(LIMIT=20): Maximum number of topics to display.</xbar.var>

import json
import os
import urllib.request
from datetime import datetime
from urllib.parse import quote

# xbar environment variables
LIMIT = int(os.environ.get("LIMIT", 20))


def _gradient_red(level):
    if level < 0 or level > 5:
        return "#000000"
    else:
        # calculate brightness from level
        brightness = hex(255 - level * 51)[2:]
        if len(brightness) == 1:
            brightness = "0" + brightness
        return "#" + brightness + "0000"


if __name__ == "__main__":
    print(datetime.now().strftime("%H:%M:%S") + " 微博热搜")
    print("---")
    try:
        hot_search_api = "https://weibo.com/ajax/side/hotSearch"
        with urllib.request.urlopen(hot_search_api) as response:
            data = json.loads(response.read())["data"]["realtime"]
        for topic in [t for t in data if t.get("is_ad") != 1][:LIMIT]:
            rank = topic["rank"]
            word = f"  [{topic['category']}] {topic['word']}"
            tag = f"  [{topic['icon_desc']}]" if "icon_desc" in topic else ""
            hot = f"    {topic['raw_hot']}"
            color = _gradient_red(rank)
            href = f"https://s.weibo.com/weibo?q={quote(topic['word_scheme'])}"
            print(f"{rank + 1}{word}{tag}{hot} | color={color} href={href}")
    except Exception as e:
        print("获取微博热搜失败")
        print("---")
        print(e)
