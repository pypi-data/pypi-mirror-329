from pygeai.core.managers import Geai


manager = Geai()


response = manager.get_assistant_list("full")
print(f"response: {response}")
