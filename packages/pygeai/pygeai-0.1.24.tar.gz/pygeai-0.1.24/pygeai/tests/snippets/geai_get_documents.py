from pygeai.assistant.managers import AssistantManager
from pygeai.core.managers import Geai

manager = AssistantManager()

response = manager.get_document_list(name="Test-Profile-WelcomeData-4")
print(response)