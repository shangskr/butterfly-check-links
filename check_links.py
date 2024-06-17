import yaml
import requests
import concurrent.futures

# 包含链接信息的YAML文件路径
yaml_file_path = 'link.yml'

# 列出所有无法访问链接的输出HTML文件路径
output_html_path = 'index.html'

# 加载YAML数据
with open(yaml_file_path, 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

# 模拟浏览器的User-Agent字符串
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

# 列表来存储无法访问的链接
inaccessible_links = []

# 使用HEAD请求检查链接是否可访问的函数
def check_link_accessibility(link):
    headers = {"User-Agent": user_agent}
    try:
        response = requests.head(link, headers=headers, timeout=5)
        if response.status_code != 200:
            inaccessible_links.append(link)
    except requests.RequestException:
        inaccessible_links.append(link)

# 使用ThreadPoolExecutor并发检查多个链接
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    links_to_check = []
    for section in data:
        if 'link_list' in section:
            for item in section['link_list']:
                links_to_check.append(item['link'])

    # 提交所有任务到执行器
    futures = [executor.submit(check_link_accessibility, link) for link in links_to_check]

    # 等待所有任务完成
    concurrent.futures.wait(futures)

# 生成HTML内容
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>无法访问的链接</title>
</head>
<body>
    <h1>无法访问的链接</h1>
    <ul>
"""
for link in inaccessible_links:
    html_content += f"<li>{link}</li>\n"

html_content += """
    </ul>
</body>
</html>
"""

# 将HTML内容写入文件
with open(output_html_path, 'w', encoding='utf-8') as file:
    file.write(html_content)

# 打印结果
print("HTML文件生成完毕:", output_html_path)
