import requests
from plotly.graph_objs import Bar
from plotly import offline

# 执行 API 调用并存储响应
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'}
r = requests.get(url, headers=headers)
print(f"状态码：{r.status_code}")

# 处理结果
response_dict = r.json()
repo_dicts = response_dict['items']
repo_names, stars = [], [] # 用于存储在图标中呈现的数据（项目名称、星数）
for repo_dict in repo_dicts:
    repo_names.append(repo_dict['name'])
    stars.append(repo_dict['stargazers_count'])

# 可视化
data = [{ # 指定图标类型，并提高 x 、 y/（项目名称、星数）
    'type': 'bar',
    'x': repo_names,
    'y': stars,
}]

my_layout = { # 字典定义图表布局，指定图标名称以及坐标轴标签
    'title': 'GitHub 受欢迎的 Python 项目',
    'xaxis': {'title': '存储库'},
    'yaxis': {'title': '总星数'},
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='html\python_repos.html')