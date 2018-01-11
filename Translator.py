# coding: utf-8

import sys
import requests

url = "https://translate.google.com/translate_a/single"

headers = {
    "Host": "translate.google.com",
    "Accept": "*/*",
    "Cookie": "",
    "User-Agent": "GoogleTranslate/5.9.59004 (iPhone; iOS 10.2; ja; iPhone9,1)",
    "Accept-Language": "ja-jp",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    }

params = {
    "client": "it",
    "dt": ["t", "rmt", "bd", "rms", "qca", "ss", "md", "ld", "ex"],
    "otf": "2",
    "dj": "1",
    "hl": "ja",
    "ie": "UTF-8",
    "oe": "UTF-8",
    }

def translate(sentence : str, fromLang, toLang):
    params['text'] = sentence
    params['sl'] = fromLang
    params['tl'] = toLang
    res = requests.get(
        url=url,
        headers=headers,
        params=params,
    )

    res = res.json()
    sentences = [s['trans'] for s in res['sentences'] if 'trans' in s.keys()]
    return ''.join(sentences)