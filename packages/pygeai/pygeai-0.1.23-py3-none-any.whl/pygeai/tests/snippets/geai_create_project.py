from pygeai.core.managers import Geai
from pygeai.core.base.models import UsageLimit, Project

manager = Geai()

usage_limit = UsageLimit(
    subscription_type="Monthly",
    usage_unit="Requests",
    soft_limit=500.0,
    hard_limit=1000.0,
    renewal_status="Renewable"
)

project = Project(
    name="New AI Project",
    description="An AI project focused on natural language processing",
    email="alejandro.trinidad@globant.com",
    usage_limit=usage_limit
)


response = manager.create_project(project)
print(f"response: {response}")