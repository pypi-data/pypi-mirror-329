from pygeai.core.base.models import UsageLimit, Project, Organization
from pygeai.organization.limits.managers import UsageLimitManager



organization = Organization(id="4aa15b61-d3c7-4a5c-99b8-052d18a04ff2")
project = Project(id="1956c032-3c66-4435-acb8-6a06e52f819f")
manager = UsageLimitManager(alias="sdkorg", organization_id=organization.id)

response = manager.get_all_usage_limits_from_organization()

print(f"response: {response}")
