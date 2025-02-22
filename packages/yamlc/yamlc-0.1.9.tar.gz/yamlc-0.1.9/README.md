## yamlc

`yamlc` 是一个简单的 Python 库，用于读取和管理 YAML 配置文件。它允许用户轻松加载、访问和重新加载配置。


## 特性

- 点语法访问嵌套的配置项。
- 支持重新加载配置文件。
- 可以设置配置文件路径。


## 安装
使用 pip 安装：
```
pip install yamlc
```

## 示例用法：
```python
from yamlc import Yamlc

# 可选方法，用于加载 YAML 配置文件。若未调用，会在首次访问配置时自动加载。
# 未指定路径时，按优先级依次尝试：
# 1. 当前工作目录下的 "config.yaml"
# 2. 主脚本所在目录下的 "config.yaml"
Yamlc.load()

# 自定义路径加载配置文件
Yamlc.load("/path/to/config.yaml")

# 获取配置项
value = Yamlc.get("database.host")
print(value)  # 输出: localhost (假设配置文件中有此项)

# 获取配置项并指定默认值
value = Yamlc.get("database.host", default="localhost")
print(value) # 如果配置中没有 "database.host"，则返回 "localhost"

# 获取 "database" 配置块
database_config = Yamlc.get("database")
print(database_config)
# 输出: {'host': 'localhost', 'port': 5432, 'username': 'user', 'password': 'pass'}
# 假设配置文件中有 "database" 配置块
```


## 重新加载配置文件
如果配置文件有修改，可以调用`reload`方法重新加载配置。
```python
# 重新加载配置文件
Yamlc.reload()
```

## 配置文件示例
`yaml`配置文件格式如下所示：

```yaml
database:
  host: localhost
  port: 5432
  username: user
  password: pass
```