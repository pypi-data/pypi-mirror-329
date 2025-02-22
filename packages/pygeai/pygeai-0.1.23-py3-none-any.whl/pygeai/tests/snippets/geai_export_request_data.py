
from pygeai.core.managers import Geai


client = Geai()


response = client.export_request_data()
print(f"response: {response}")
