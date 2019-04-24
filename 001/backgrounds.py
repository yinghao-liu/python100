#!/usr/bin/env python3
import urllib.request
import urllib.error
import html.parser
import ctypes
import time
import re
import os
import sys

def url_read(url):
    head = {}
    #head["User-Agent"]="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    request = urllib.request.Request(url, headers=head)
    for tick in range(3):
        try:
            with urllib.request.urlopen(request, timeout=5) as rst:
                html = rst.read()
                return html
        except urllib.error.HTTPError as err:
            print("err is {}, errno is {}, err reason is {}".format(err, err.code, err.reason))
        except urllib.error.URLError as err:
            print("err is {}".format(err))
            continue
    else:
        return None


def find_element(data, key, re_pattern):
    re_exp = re.compile(re_pattern)
    index = 0
    while True:
        tmp=data.find(key, index)
        if -1 == tmp:
            break
        index = tmp + len(key)
        print("element info is {}".format(data[index:index+100]))
        element = re_exp.search(data, index)
        if None == element:
            continue
        return element.group(1)

def main():
    host  = "https://www.bing.com"
    html = url_read(host)
    if None == html:
        sys.exit(1)

    name_key = b'd="sh_cp"'
    name_pat = b'title="(.*?)"'
    image_name = find_element(html, name_key, name_pat)

    date = time.strftime("%m-%d_")
    image_name = date + image_name.decode()

    original_str = "，/ "
    translate_str = "_" * len(original_str)
    drop_str = "():"
    translate_table = str.maketrans(original_str, translate_str, drop_str)
    image_name = image_name.translate(translate_table)

    image_key = b'g_img={url'
    image_pat = b'"(.*?\.jpg)'
    image_url = find_element(html, image_key, image_pat).decode()
    suffix = image_url.rpartition(".")
    image_name += suffix[1] + suffix[2]
    print("image_name : {}".format(image_name))
    print("image_url : {}".format(image_url))

    image = url_read(host+image_url)
    with open(image_name, "wb") as fd:
        fd.write(image)

    image_path = os.path.join(os.getcwd(), image_name)
    print(image_path)
    # about this function, refer to README.md
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 1)


if "__main__" == __name__:
    try:
        main()
    except Exception as main_err:
        print(main_err)

