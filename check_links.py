import yaml
import requests
import concurrent.futures

# 包含链接信息的YAML文件路径
yaml_file_path = 'link.yml'

# 列出所有无法访问链接的输出文本文件路径
output_txt_path = 'inaccessible_links.txt'

# 加载YAML数据
with open(yaml_file_path, 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

# 模拟浏览器的User-Agent字符串
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

# 字典来存储可访问和无法访问的链接及其原始索引
accessible_links = {}
inaccessible_links = {}

# 使用HEAD请求检查链接是否可访问的函数
def check_link_accessibility(link, index):
    headers = {"User-Agent": user_agent}  # 添加User-Agent到请求头
    try:
        # 发送HEAD请求而不是GET请求
        response = requests.head(link, headers=headers, timeout=5)
        if response.status_code == 200:
            accessible_links[index] = link  # 存储可访问链接及其索引
            print(f"可访问: {link}", flush=True)  # 打印可访问链接
        else:
            inaccessible_links[index] = link  # 存储无法访问链接及其索引
    except requests.RequestException:
        inaccessible_links[index] = link  # 存储无法访问链接及其索引

# 使用ThreadPoolExecutor并发检查多个链接
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # 收集YAML数据中的所有链接
    links_to_check = []
    index = 0  # 维护原始顺序的索引
    for section in data:
        if 'link_list' in section:
            for item in section['link_list']:
                links_to_check.append((index, item['link']))  # 记录索引
                index += 1

    # 提交所有任务到执行器，带原始索引
    futures = [executor.submit(check_link_accessibility, link, idx) for idx, link in links_to_check]

    # 确保所有任务完成
    concurrent.futures.wait(futures)

# 将无法访问的链接按原始顺序写入输出文本文件
with open(output_txt_path, 'w', encoding='utf-8') as file:
    if inaccessible_links:
        file.write("无法访问的链接:\n")
        for idx in sorted(inaccessible_links.keys()):  # 按索引排序以保持顺序
            file.write(f"{inaccessible_links[idx]}\n")
    else:
        file.write("所有链接均可访问。")

# 按原始顺序打印可访问的链接
print("可访问的链接:")
for idx in sorted(accessible_links.keys()):  # 按索引排序以保持顺序
    print(accessible_links[idx], flush=True)
