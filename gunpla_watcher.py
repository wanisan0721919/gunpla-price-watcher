# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time

# アフィリエイトタグ
AFFILIATE_TAG = "infonatumi-22"

# 監視URL
URL = "https://www.amazon.co.jp/ガンプラストア-Amazon-co-jp/s?rh=n%3A4469780051%2Cp_6%3AAN1VRQENFRJN5"

# ヘッダーでUser-Agent設定
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "ja-JP,ja;q=0.9",
    "Connection": "keep-alive",  # 追加: 接続を維持する
    "Upgrade-Insecure-Requests": "1",  # 追加: セキュリティ強化
    "TE": "Trailers"  # 追加: HTTPリクエストでよく使われるフィールド
}
