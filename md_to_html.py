import os
import markdown
from datetime import datetime

# 配置常量
DAILY_DIR = 'daily'
DAILY_FILE = os.path.join(DAILY_DIR, 'daily.md')
HTML_FILE = os.path.join(DAILY_DIR, 'daily.html')


def convert_md_to_html():
    """
    将daily.md转换为HTML文件
    """
    try:
        if not os.path.exists(DAILY_FILE):
            print(f"错误: {DAILY_FILE} 不存在")
            return False

        with open(DAILY_FILE, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # 启用表格扩展
        html_content = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'codehilite']
        )

        # 提取报告日期
        date_match = md_content.split('\n')[0].strip()
        report_date = date_match.replace('# ', '') if date_match.startswith('# ') else datetime.now().strftime('%Y-%m-%d')

        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_date} 安全威胁态势报告</title>
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --border-color: #30363d;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --text-muted: #6e7681;
            --accent-blue: #58a6ff;
            --accent-green: #3fb950;
            --accent-red: #f85149;
            --accent-orange: #d29922;
            --accent-purple: #a371f7;
            --accent-pink: #db61a2;
            --code-bg: #161b22;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', Helvetica, Arial, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.7;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        /* Header */
        .report-header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 1px solid var(--border-color);
        }}

        .report-header h1 {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }}

        .report-header .subtitle {{
            color: var(--text-secondary);
            font-size: 0.95rem;
        }}

        /* Cards */
        .card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 24px;
        }}

        .card-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
        }}

        .card-header h2 {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
        }}

        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}

        .stat-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}

        .stat-card .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent-blue);
            margin-bottom: 4px;
        }}

        .stat-card .stat-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
        }}

        /* Threat type badges */
        .threat-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .threat-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            font-size: 0.85rem;
            color: var(--text-primary);
        }}

        .threat-badge .count {{
            background: var(--accent-blue);
            color: #fff;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.75rem;
            font-weight: 600;
        }}

        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 0.9rem;
        }}

        thead {{
            background: var(--bg-tertiary);
        }}

        th {{
            text-align: left;
            padding: 12px 16px;
            font-weight: 600;
            color: var(--text-secondary);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid var(--border-color);
        }}

        td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
            vertical-align: middle;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tbody tr {{
            transition: background 0.15s;
        }}

        tbody tr:hover {{
            background: var(--bg-tertiary);
        }}

        td a {{
            color: var(--accent-blue);
            text-decoration: none;
            transition: color 0.15s;
        }}

        td a:hover {{
            color: var(--text-primary);
            text-decoration: underline;
        }}

        .source-tag {{
            display: inline-block;
            padding: 2px 8px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            font-size: 0.75rem;
            color: var(--text-secondary);
        }}

        /* Category sections */
        .category-section {{
            margin-bottom: 32px;
        }}

        .category-section:last-child {{
            margin-bottom: 0;
        }}

        .category-title {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--accent-blue);
        }}

        /* Article list */
        .article-list {{
            list-style: none;
        }}

        .article-list li {{
            padding: 10px 0;
            border-bottom: 1px solid var(--border-color);
        }}

        .article-list li:last-child {{
            border-bottom: none;
        }}

        .article-list a {{
            color: var(--accent-blue);
            text-decoration: none;
            font-size: 0.95rem;
        }}

        .article-list a:hover {{
            text-decoration: underline;
        }}

        .article-date {{
            color: var(--text-muted);
            font-size: 0.8rem;
            margin-left: 8px;
        }}

        /* Source group */
        .source-group {{
            margin-bottom: 20px;
        }}

        .source-title {{
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--accent-green);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        /* Code blocks */
        pre {{
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            font-size: 0.85rem;
            line-height: 1.5;
        }}

        code {{
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
            font-size: 0.85rem;
        }}

        p code {{
            background: var(--code-bg);
            padding: 2px 6px;
            border-radius: 4px;
            color: var(--accent-pink);
        }}

        /* Blockquotes / notes */
        blockquote {{
            border-left: 3px solid var(--accent-blue);
            padding-left: 16px;
            margin: 16px 0;
            color: var(--text-secondary);
        }}

        /* Footer */
        .report-footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 24px;
            border-top: 1px solid var(--border-color);
            color: var(--text-muted);
            font-size: 0.8rem;
        }}

        .report-footer p {{
            margin-bottom: 4px;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .container {{
                padding: 20px 16px;
            }}

            .report-header h1 {{
                font-size: 1.5rem;
            }}

            .stats-grid {{
                grid-template-columns: 1fr 1fr;
            }}

            table {{
                font-size: 0.8rem;
            }}

            th, td {{
                padding: 8px 10px;
            }}
        }}

        /* Markdown content styles */
        body h1, body h2, body h3, body h4, body h5, body h6 {{
            color: var(--text-primary);
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
        }}

        body h1 {{ font-size: 1.6rem; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }}
        body h2 {{ font-size: 1.3rem; color: var(--accent-blue); }}
        body h3 {{ font-size: 1.1rem; color: var(--text-secondary); }}
        body h4 {{ font-size: 1rem; color: var(--text-secondary); }}

        body ul, body ol {{
            padding-left: 24px;
            margin: 12px 0;
        }}

        body li {{
            margin-bottom: 6px;
        }}

        body strong {{
            color: var(--text-primary);
            font-weight: 600;
        }}

        body hr {{
            border: none;
            border-top: 1px solid var(--border-color);
            margin: 24px 0;
        }}

        body em {{
            color: var(--text-secondary);
        }}

        body p {{
            margin-bottom: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="report-header">
            <h1>{report_date} 安全威胁态势报告</h1>
            <p class="subtitle">威胁情报聚合与可视化分析</p>
        </header>

        {html_content}

        <footer class="report-footer">
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>微信文章安全归档系统</p>
        </footer>
    </div>
</body>
</html>
"""

        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(full_html)

        print(f"成功将 {DAILY_FILE} 转换为 {HTML_FILE}")
        return True

    except Exception as e:
        print(f"转换Markdown到HTML时出错: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    convert_md_to_html()
