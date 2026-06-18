#!/usr/bin/env python3
"""推送报告到飞书"""

import json
import os
import requests

def send_to_feishu():
    webhook_url = os.getenv('FEISHU_WEBHOOK_URL')
    if not webhook_url:
        print("错误：未设置 FEISHU_WEBHOOK_URL")
        return
    
    # 读取报告
    with open('output/report.json', 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    # 构建飞书消息卡片
    if 'ai_summary' in report:
        # 有AI深度解读
        message = build_ai_card(report)
    else:
        # 基础报告
        message = build_basic_card(report)
    
    # 发送请求
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook_url, json=message, headers=headers)
    
    if response.status_code == 200:
        print("成功推送到飞书")
    else:
        print(f"推送失败: {response.status_code} - {response.text}")

def build_ai_card(report):
    """构建带AI解读的卡片"""
    return {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": report['title']
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": report['ai_summary']
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": "数据来源：arXiv、GitHub、Hacker News | 由AI自动生成"
                        }
                    ]
                }
            ]
        }
    }

def build_basic_card(report):
    """构建基础卡片"""
    elements = []
    
    # 论文部分
    if report.get('papers'):
        paper_text = "**📄 最新论文**\n"
        for i, paper in enumerate(report['papers'][:5], 1):
            paper_text += f"{i}. [{paper['title']}]({paper['link']})\n"
            if paper.get('abstract'):
                paper_text += f"   > {paper['abstract'][:150]}...\n"
        elements.append({"tag": "markdown", "content": paper_text})
        elements.append({"tag": "hr"})
    
    # 项目部分
    if report.get('projects'):
        project_text = "**🔧 热门项目**\n"
        for project in report['projects'][:3]:
            project_text += f"- [{project['name']}]({project['url']}) ⭐{project['stars']}\n"
            if project.get('description'):
                project_text += f"  {project['description']}\n"
        elements.append({"tag": "markdown", "content": project_text})
        elements.append({"tag": "hr"})
    
    # 行业动态
    if report.get('news'):
        news_text = "**📰 行业动态**\n"
        for news in report['news'][:3]:
            news_text += f"- [{news['title']}]({news['url']})\n"
        elements.append({"tag": "markdown", "content": news_text})
    
    # 统计数据
    if report.get('stats'):
        stats = report['stats']
        elements.append({
            "tag": "note",
            "elements": [
                {"tag": "plain_text", "content": f"今日发现论文{stats['papers_found']}篇 | 项目{stats['projects_found']}个 | 动态{stats['news_found']}条"}
            ]
        })
    
    return {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": report['title']
                },
                "template": "blue"
            },
            "elements": elements
        }
    }

if __name__ == '__main__':
    send_to_feishu()
