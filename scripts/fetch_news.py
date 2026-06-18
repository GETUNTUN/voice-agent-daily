#!/usr/bin/env python3
"""抓取语音大模型行业动态"""

import json
import requests
from datetime import datetime

def fetch_news():
    # 这里使用Hacker News API作为示例，你可以替换为其他源
    # 真实场景可以接入多个API源
    news_sources = [
        'https://hacker-news.firebaseio.com/v0/newstories.json',
        'https://hn.algolia.com/api/v1/search_by_date?query=voice+LLM+speech'
    ]
    
    news_items = []
    
    # 从Hacker News获取
    try:
        response = requests.get(news_sources[12](@ref)
        if response.status_code == 200:
            story_ids = response.json()[:30]
            for sid in story_ids:
                story_url = f'https://hacker-news.firebaseio.com/v0/item/{sid}.json'
                story_resp = requests.get(story_url)
                if story_resp.status_code == 200:
                    story = story_resp.json()
                    title = story.get('title', '')
                    # 过滤语音相关标题
                    keywords = ['speech', 'voice', 'audio', 'LLM', 'dialogue', 'language model']
                    if any(k.lower() in title.lower() for k in keywords):
                        news_items.append({
                            'title': title[:150],
                            'url': story.get('url', f'https://news.ycombinator.com/item?id={sid}'),
                            'source': 'Hacker News',
                            'time': datetime.fromtimestamp(story.get('time', 0)).strftime('%Y-%m-%d')
                        })
    except Exception as e:
        print(f"抓取Hacker News失败: {e}")
    
    output = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'news': news_items[:5]
    }
    
    os.makedirs('output', exist_ok=True)
    with open('output/news.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"成功抓取 {len(news_items[:5])} 条行业动态")

if __name__ == '__main__':
    fetch_news()
