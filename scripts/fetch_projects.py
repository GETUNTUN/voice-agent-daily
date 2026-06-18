#!/usr/bin/env python3
"""抓取GitHub上语音对话相关热门项目"""

import os
import json
import requests
from datetime import datetime

def fetch_projects():
    keywords = os.getenv('PROJECT_KEYWORDS', 'speech,voice,audio,dialogue')
    token = os.getenv('GITHUB_TOKEN')
    
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    if token:
        headers['Authorization'] = f'token {token}'
    
    # 搜索今日创建/更新的仓库
    today = datetime.now().strftime('%Y-%m-%d')
    query = f'language:python {keywords} created:>={today}'
    
    url = 'https://api.github.com/search/repositories'
    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
        'per_page': 10
    }
    
    response = requests.get(url, headers=headers, params=params)
    projects = []
    
    if response.status_code == 200:
        data = response.json()
        for item in data.get('items', [])[:5]:
            project = {
                'name': item['full_name'],
                'description': item.get('description', '暂无描述')[:200],
                'stars': item['stargazers_count'],
                'language': item.get('language', '未知'),
                'url': item['html_url'],
                'created': item['created_at'][:10]
            }
            projects.append(project)
    
    output = {
        'date': today,
        'projects': projects
    }
    
    os.makedirs('output', exist_ok=True)
    with open('output/projects.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"成功抓取 {len(projects)} 个GitHub项目")

if __name__ == '__main__':
    fetch_projects()
