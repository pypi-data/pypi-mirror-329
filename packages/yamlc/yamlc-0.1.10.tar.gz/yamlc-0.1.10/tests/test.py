from yamlc import Yamlc as yc

yc.load()

print(yc.get("app"))
print(yc.get("app.name"))
print(yc.get("api.base_url"))
