import requests

# 执行 API 调用并存储响应
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'}  # 显式指定 API 版本
r = requests.get(url, headers=headers)
print(f'状态码：{r.status_code}')

# 将 API 响应赋给变量
response_dict = r.json()    # 将信息转换为字典并存储
print(f"总存储库：{response_dict['total_count']}")

# 探索有关仓库信息
repo_dicts = response_dict['items']
print(f'返回存储库：{len(repo_dicts)}')

# 研究第一个仓库
repo_dict = repo_dicts[0]
# # 循环仓库 API 字典所有键
# print(f'\n键：{len(repo_dict)}')
# for key in sorted(repo_dict.keys()):
#     print(key)

print("\n关于第一个存储库的选择信息：")
print(f"昵称：{repo_dict['name']}")
print(f"归属：{repo_dict['owner']['login']}")
print(f"星星：{repo_dict['stargazers_count']}")
print(f"仓库：{repo_dict['html_url']}")
print(f"创建：{repo_dict['created_at']}")
print(f"更新：{repo_dict['updated_at']}")
print(f"描述：{repo_dict['description']}")