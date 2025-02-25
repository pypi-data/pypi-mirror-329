from pygeai.core.managers import Geai
from pygeai.core.base.models import UsageLimit, Project

client = Geai()

project = Project(
    id="1956c032-3c66-4435-acb8-6a06e52f819f",
    name="AI Project",
    description="An AI project focused on natural language processing and testing",
)


response = client.update_project(project)
print(f"response: {response}")
