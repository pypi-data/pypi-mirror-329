from yamlc import Yamlc

Yamlc.load()

print(Yamlc.get("app"))
print(Yamlc.get("app.name"))
print(Yamlc.get("api.base_url"))
