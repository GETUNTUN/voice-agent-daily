#!/usr/bin/env python3
"""使用大模型生成结构化报告"""

import json
import os
from openai import OpenAI

def generate_report():
    # 读取之前抓取的数据
    papers = json.load(open('output/papers.json', 'r'))
    projects = json.load(open('output/projects.json', 'r'))
    news = json.load(open('output/news.json', 'r'))
    
    # 如果没有配置API Key，直接使用原始数据
    api_key = os.getenv('DEEPSEEK_API_KEY') or os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        # 不使用大模型，直接拼接
        report = generate_basic_report(papers, projects, news)
    else:
        # 使用大模型生成深度解读
        report = generate_ai_report(papers, projects, news, api_key)
    
    # 保存报告
    os.makedirs('output', exist_ok=True)
    with open('output/report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("报告生成完成")

def generate_basic_report(papers, projects, news):
    """生成基础报告（不调用大模型）"""
    report = {
        'title': f"语音大模型日报 - {papers['date']}",
        'papers': [
            {
                'title': p['title'],
                'link': p['link'],
                'abstract': p['abstract'][:200],
                'author': p['authors'][0] if p['authors'] else 'Unknown'
            }
            for p in papers['papers'][:5]
        ],
        'projects': projects['projects'][:3],
        'news': news['news'][:3],
        'stats': {
            'papers_found': papers['total_found'],
            'projects_found': len(projects['projects']),
            'news_found': len(news['news'])
        }
    }
    return report

def generate_ai_report(papers, projects, news, api_key):
    """使用AI生成深度解读报告"""
    # 判断API类型
    if os.getenv('DEEPSEEK_API_KEY'):
        client = OpenAI(
            api_key=api_key,
            base_url='https://api.deepseek.com'
        )
        model = 'deepseek-chat'
    else:
        client = OpenAI(api_key=api_key)
        model = 'gpt-4o-mini'
    
    # 构建提示词
    prompt = f"""请为今天的语音大模型日报生成一份结构化报告（中文）。

日期：{papers['date']}

**最新论文（共{papers['total_found']}篇）：**
{chr(10).join([f"- [{p['title']}]({p['link']})" for p in papers['papers'][:5]])}

**GitHub趋势项目：**
{chr(10).join([f"- {p['name']}: {p['description'][:100]}" for p in projects['projects'][:3]])}

**行业动态：**
{chr(10).join([f"- {n['title']}" for n in news['news'][:3]]) if news['news'] else '- 暂无'}

请按以下格式输出：
1. **今日亮点**（2-3句话总结今日最重要进展）
2. **论文精选**（选择最重要的2-3篇论文，每篇给出标题、链接、核心创新点解读）
3. **开源项目**（列出新项目及其用途）
4. **行业动态**（厂商/团队最新发布）
5. **技术前沿**（如果论文中有涉及模态代沟、全双工对话等前沿方向，请特别指出）
"""
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是语音大模型领域的专家，擅长用简洁的语言总结研究进展。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=2000
    )
    
    report = {
        'title': f"语音大模型日报 - {papers['date']}",
        'ai_summary': response.choices[0].message.content,
        'raw_data': {
            'papers': papers['papers'][:5],
            'projects': projects['projects'][:3],
            'news': news['news'][:3]
        }
    }
    return report

if __name__ == '__main__':
    generate_report()
