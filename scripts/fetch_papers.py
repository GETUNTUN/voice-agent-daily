#!/usr/bin/env python3
"""抓取arXiv上语音大模型相关最新论文"""

import os
import json
from datetime import datetime, timedelta
import arxiv

def fetch_papers():
    # 从环境变量获取配置
    keywords = os.getenv('ARXIV_KEYWORDS', 'speech language model')
    max_papers = int(os.getenv('MAX_PAPERS', '10'))
    
    # 构建搜索查询
    search_queries = [
        'cat:cs.CL AND (speech OR spoken OR voice OR audio OR dialogue) AND language model',
        'cat:cs.SD AND speech',
        'cat:eess.AS AND language model'
    ]
    
    all_papers = []
    
    for query in search_queries:
        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        for result in search.results():
            paper = {
                'title': result.title,
                'authors': [author.name for author in result.authors],
                'abstract': result.summary[:300] + '...',  # 截取前300字符
                'link': result.entry_id,
                'published': result.published.strftime('%Y-%m-%d'),
                'categories': result.categories
            }
            all_papers.append(paper)
    
    # 去重并排序
    seen = set()
    unique_papers = []
    for paper in all_papers:
        if paper['title'] not in seen:
            seen.add(paper['title'])
            unique_papers.append(paper)
    
    # 保存到文件，供后续步骤使用
    output = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'papers': unique_papers[:max_papers],
        'total_found': len(unique_papers)
    }
    
    os.makedirs('output', exist_ok=True)
    with open('output/papers.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"成功抓取 {len(unique_papers[:max_papers])} 篇论文")

if __name__ == '__main__':
    fetch_papers()
