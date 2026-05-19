import os
import requests
import feedparser
from datetime import datetime
import pytz

# 깃허브 시크릿에서 키를 불러옵니다
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def add_to_notion(title, link, category):
    # 한국 시간 기준으로 오늘 날짜 구하기
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.now(kst).strftime("%Y-%m-%d")

    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "이름": {
                "title": [{"text": {"content": title}}]
            },
            "링크": {
                "url": link
            },
            "카테고리": {
                "select": {"name": category}
            },
            "날짜": {
                "date": {"start": today}
            }
        }
    }
    
    # 노션으로 데이터 보내기
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
    if response.status_code == 200:
        print(f"성공: [{category}] {title}")
    else:
        print(f"실패: {response.text}")

def fetch_news():
    # 구글 뉴스 RSS 주소 (경제, 시사/정치)
    feeds = {
        "경제": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=ko&gl=KR&ceid=KR:ko",
        "시사": "https://news.google.com/rss/headlines/section/topic/NATION?hl=ko&gl=KR&ceid=KR:ko"
    }

    for category, url in feeds.items():
        feed = feedparser.parse(url)
        # 위에서부터 딱 5개만 가져오기
        for entry in feed.entries[:5]:
            add_to_notion(entry.title, entry.link, category)

if __name__ == "__main__":
    fetch_news()
