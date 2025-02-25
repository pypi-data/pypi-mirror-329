from pygeai.core.managers import Geai

manager = Geai(alias="sdkorg")
# manager = Geai()


response = manager.get_project_list("full")
print(f"response: {response}")
