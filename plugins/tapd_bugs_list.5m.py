#!/usr/bin/env python3

# <xbar.title>TAPD Bugs List</bitbar.title>
# <xbar.version>v1.0.0</bitbar.version>
# <xbar.author>Xylitol</bitbar.author>
# <xbar.author.github>C5H12O5</xbar.author.github>
# <xbar.dependencies>python</bitbar.dependencies>

# <xbar.var>string(Cookie=""): The Cookie HTTP request header</xbar.var>
# <xbar.var>string(Params=""): The /bugs_list API request params</xbar.var>

import json
import os
import urllib.request

# xbar environment variables
COOKIE = os.environ.get("Cookie")
PARAMS = os.environ.get("Params")

# default request parameters
HOST = "www.tapd.cn"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    " AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/120.0.0.0 Safari/537.36"
)

if __name__ == "__main__":
    if not COOKIE or not PARAMS:
        print("TAPD缺陷列表")
        print("---")
        print("请先在插件配置中设置Cookie和请求参数")
    else:
        url = f"https://{HOST}/api/entity/bugs/bugs_list"
        data = PARAMS.encode("utf-8")
        headers = {
            "Cookie": COOKIE,
            "User-Agent": UA,
            "Content-Type": "application/json",
        }
        try:
            request = urllib.request.Request(url, data, headers, method="POST")
            with urllib.request.urlopen(request) as response:
                data = json.loads(response.read().decode("utf-8"))["data"]
            print("剩余TAPD缺陷：" + data["total_count"])
            print("---")
            for bug in [item["Bug"] for item in data["bugs_list"]]:
                pid = bug["project_id"]
                bid = bug["id"]
                href = f"https://{HOST}/{pid}/bugtrace/bugs/view?bug_id={bid}"
                print(bug["title"] + " | href=" + href)
        except Exception as e:
            print("获取TAPD缺陷列表失败")
            print("---")
            print(e)
