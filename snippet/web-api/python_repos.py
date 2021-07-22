import requests

# 执行 API 调用并存储响应
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'}  # 显式指定 API 版本
r = requests.get(url, headers=headers)
print(f'状态码：{r.status_code}')
# 将 API 响应赋给变量
response_dict = r.json()    # 将信息转换为字典并存储

# 处理结果
print(response_dict.keys())