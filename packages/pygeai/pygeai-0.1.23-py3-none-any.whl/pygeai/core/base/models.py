from datetime import datetime

from pydantic.main import BaseModel
from typing import Optional, Literal, Any


class Error(BaseModel):
    id: int
    description: str

    def __str__(self):
        error = {
            "id": self.id,
            "description": self.description
        }
        return str(error)


class AssistantRevisionMetadata(BaseModel):
    """
    {
      "key": "string",
      "type": "string",
      "value": "string"
    }
    """
    key: str
    type: str
    value: str

    def __str__(self):
        metadata = {
            "key": self.key,
            "type": self.type,
            "value": self.value
        }
        return str(metadata)


class AssistantRevision(BaseModel):
    """
    {
      "metadata": [
        ...
      ],
      "modelId": "string",
      "modelName": "string",
      "prompt": "string",
      "providerName": "string",
      "revisionDescription": "string",
      "revisionId": "string",
      "revisionName": "string",
      "timestamp": "timestamp"
    }
    """
    metadata: Optional[list[AssistantRevisionMetadata]] = []
    model_id: Optional[str] = None
    model_name: Optional[str] = None
    prompt: Optional[str] = None
    provider_name: Optional[str] = None
    revision_description: Optional[str] = None
    revision_id: int = None
    revision_name: str
    timestamp: Optional[datetime] = None

    def __str__(self):
        revision = {
            "modelId": self.model_id,
            "modelName": self.model_name,
            "prompt": self.prompt,
            "providerName": self.provider_name,
            "revisionDescription": self.revision_description,
            "revisionId": self.revision_id,
            "revisionName": self.revision_name,
            "timestamp": self.timestamp
        }
        if any(self.metadata):
            revision["metadata"] = self.metadata

        return str(revision)


class AssistantIntent(BaseModel):
    """
    {
          "assistantIntentDefaultRevision": "number",
          "assistantIntentDescription": "string",
          "assistantIntentId": "string",
          "assistantIntentName": "string",
          "revisions": [
            ...
          ]
        }
    """
    default_revision: float
    description: str
    id: str
    name: str
    revisions: Optional[list[AssistantRevision]] = []

    def __str__(self):
        intent = {
            "assistantIntentDefaultRevision": self.default_revision,
            "assistantIntentDescription": self.description,
            "assistantIntentId": self.id,
            "assistantIntentName": self.name
        }
        if any(self.revisions):
            intent["revisions"] = self.revisions

        return str(intent)


class Organization(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

    def __str__(self):
        organization = {
            "organizationId": self.id,
            "organizationName": self.name
        }
        return str(organization)


class ProjectSearchProfile(BaseModel):
    """
     {
      "name": "string",
      "description": "string"
    }
    """
    name: str
    description: str

    def __str__(self):
        search_profile = {
            "name": self.name,
            "description": self.description
        }
        return str(search_profile)


class ProjectToken(BaseModel):
    """
     {
      "description": "string",
      "id": "string",
      "name": "string",
      "status": "string", /* Active, Blocked */
      "timestamp": "timestamp"
    }
    """
    description: Optional[str] = None
    token_id: str
    name: str
    status: str
    timestamp: datetime

    def __str__(self):
        token = {
            "description": self.description,
            "id": self.token_id,
            "name": self.name,
            "status": self.status,
            "timestamp": self.timestamp
        }
        return str(token)


class UsageLimit(BaseModel):
    """
    "hardLimit": "number",                // Upper usage limit
    "id": "string",                       // Usage limit ID
    "relatedEntityName": "string",        // Name of the related entity
    "remainingUsage": "number",           // Remaining usage
    "renewalStatus": "string",            // Renewal status (Renewable, NonRenewable)
    "softLimit": "number",                // Lower usage limit
    "status": "integer",                  // Status (1: Active, 2: Expired, 3: Empty, 4: Cancelled)
    "subscriptionType": "string",         // Subscription type (Freemium, Daily, Weekly, Monthly)
    "usageUnit": "string",                // Usage unit (Requests, Cost)
    "usedAmount": "number",               // Amount used (decimal or scientific notation)
    "validFrom": "timestamp",             // Start date of the usage limit
    "validUntil": "timestamp"             // Expiration or renewal date
    """
    hard_limit: Optional[float] = None
    id: Optional[str] = None
    related_entity_name: Optional[str] = None
    remaining_usage: Optional[float] = None
    renewal_status: Optional[Literal["Renewable", "NonRenewable"]] = None
    soft_limit: Optional[float] = None
    status: Optional[Literal[1, 2, 3, 4]] = None
    subscription_type: Optional[Literal["Freemium", "Daily", "Weekly", "Monthly"]] = None
    usage_unit: Optional[Literal["Requests", "Cost"]] = None
    used_amount: Optional[float] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None

    def to_dict(self):
        usage_limit = {
            "hardLimit": self.hard_limit,
            "renewalStatus": self.renewal_status,
            "softLimit": self.soft_limit,
            "subscriptionType": self.subscription_type,
            "usageUnit": self.usage_unit,
        }
        if self.id is not None:
            usage_limit["id"] = self.id

        if self.related_entity_name is not None:
            usage_limit["relatedEntityName"] = self.related_entity_name

        if self.remaining_usage is not None:
            usage_limit["remainingUsage"] = self.remaining_usage

        if self.status is not None:
            usage_limit["status"] = self.status

        if self.used_amount is not None:
            usage_limit["usedAmount"] = self.used_amount

        if self.valid_from is not None:
            usage_limit["validFrom"] = self.valid_from

        if self.valid_until is not None:
            usage_limit["validUntil"] = self.valid_until

        return usage_limit

    def __str__(self):
        usage_limit = self.to_dict()
        return str(usage_limit)


class Project(BaseModel):
    """
     {
      "projectActive": "boolean",
      "projectDescription": "string",
      "projectId": "string",
      "projectName": "string",
      "projectStatus": "integer", /* 0:Active, 2:Hidden */
    }
    """
    organization: Optional[Organization] = None
    active: Optional[bool] = None
    description: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    status: Optional[int] = None
    search_profiles: Optional[list[ProjectSearchProfile]] = []
    tokens: Optional[list[ProjectToken]] = []
    usage_limit: Optional[UsageLimit] = None

    def __str__(self):
        project = {
            "projectName": self.name
        }

        if self.id:
            project["projectId"] = self.id

        if self.organization:
            project["organization"] = self.organization

        if self.active is not None:
            project["projectActive"] = self.active

        if self.description is not None:
            project["projectDescription"] = self.description

        if self.status is not None:
            project["projectStatus"] = self.status

        if self.search_profiles is not None and any(self.search_profiles):
            project["searchProfiles"] = self.search_profiles

        if self.tokens is not None and any(self.tokens):
            project["tokens"] = self.tokens

        if self.usage_limit is not None:
            project["usageLimit"] = self.usage_limit

        return str(project)


class ProjectItem(BaseModel):
    """
    {
      "assistant": "string",
      "intent": "string",
      "timestamp": "string",
      "prompt": "string",
      "output": "string",
      "inputText": "string",
      "status": "string"
    }
    """
    assistant: str
    intent: Optional[str] = None
    timestamp: str
    prompt: Optional[str] = None
    output: Optional[str] = None
    input_text: Optional[str] = None
    status: str

    def __str__(self):
        item = {
            "assistant": self.assistant,
            "intent": self.intent,
            "timestamp": self.timestamp,
            "prompt": self.prompt,
            "output": self.output,
            "inputText": self.input_text,
            "status": self.status
        }
        return str(item)


class GuardrailSettings(BaseModel):
    llm_output: Optional[bool] = False
    input_moderation: Optional[bool] = False
    prompt_injection: Optional[bool] = False

    def to_dict(self):
        return {
            "llmOutputGuardrail": self.llm_output,
            "inputModerationGuardrail": self.input_moderation,
            "promptInjectionGuardrail": self.prompt_injection
        }

    def __str__(self):
        settings = self.to_dict()
        return str(settings)


class LlmSettings(BaseModel):
    """
    "llmSettings": {
        "providerName": "string",
        "modelName": "string",
        "temperature": "decimal",
        "maxTokens": "integer",
        "uploadFiles": "boolean",
        "llmOutputGuardrail": "boolean",
        "inputModerationGuardrail": "boolean",
        "promptInjectionGuardrail": "boolean"
      }
    """
    provider_name: Optional[str] = None
    model_name: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    upload_files: Optional[bool] = None
    guardrail_settings: Optional[GuardrailSettings] = None

    def to_dict(self):
        settings = {
            "providerName": self.provider_name,
            "modelName": self.model_name,
            "temperature": self.temperature,
            "maxTokens": self.max_tokens,
            "frequencyPenalty": self.frequency_penalty,
            "presence_penalty": self.presence_penalty,
            "uploadFiles": self.upload_files,
        }
        guardrail_settings = self.guardrail_settings.to_dict() if self.guardrail_settings is not None else {}
        settings.update(guardrail_settings)
        return settings

    def __str__(self):
        llm_setting = self.to_dict()
        return str(llm_setting)


class WelcomeDataFeature(BaseModel):
    """
    {
        "title": "string",
        "description": "string"
    }
    """
    title: str
    description: str

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description
        }

    def __str__(self):
        feature = self.to_dict()
        return str(feature)


class WelcomeDataExamplePrompt(BaseModel):
    """
    {
        "title": "string",
        "description": "string",
        "promptText": "string"
    }
    """
    title: str
    description: str
    prompt_text: str

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "promptText": self.prompt_text
        }

    def __str__(self):
        example_prompt = self.to_dict()
        return str(example_prompt)


class WelcomeData(BaseModel):
    """
    "title": "string",
    "description": "string",
    "features": [
        ],
        "examplesPrompt": [
        ]
      }
    """
    title: Optional[str]
    description: Optional[str]
    features: Optional[list[WelcomeDataFeature]] = []
    examples_prompt: Optional[list[WelcomeDataExamplePrompt]] = []

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "features": [feature.to_dict() for feature in self.features],
            "examplesPrompt": [example.to_dict() for example in self.examples_prompt]
        }

    def __str__(self):
        welcome_data = self.to_dict()
        return str(welcome_data)


class ChatMessage(BaseModel):
    role: str
    content: str
    function_call: Optional[Any] = None
    refusal: Optional[Any] = None
    tool_calls: Optional[Any] = None

    def to_dict(self):
        message = {
            "role": self.role,
            "content": self.content
        }
        if self.function_call:
            message["function_call"] = self.function_call

        if self.refusal:
            message["refusal"] = self.refusal

        if self.tool_calls:
            message["tool_calls"] = self.tool_calls

        return message

    def __str__(self):
        message = self.to_dict()
        return str(message)


class ChatMessageList(BaseModel):
    messages: list[ChatMessage]

    def to_list(self):
        messages = list()
        for message in self.messages:
            messages.append(message.to_dict())

        return messages


class ChatVariable(BaseModel):
    key: str
    value: str

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value
        }

    def __str__(self):
        variable = self.to_dict()
        return str(variable)


class ChatVariableList(BaseModel):
    variables: list[ChatVariable]

    def to_list(self):
        variables = list()
        for variable in self.variables:
            variables.append(variable.to_dict())

        return variables


class Assistant(BaseModel):
    """
    {
      "assistantId": "string",
      "assistantName": "string",
      "intents": [ /* full option */

      ]
    }
    """
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal[1, 2]] = 1
    priority: Optional[int] = 0
    type: Optional[str] = None
    prompt: Optional[str] = None
    intents: Optional[list[AssistantIntent]] = []
    project: Optional[Project] = None
    welcome_data: Optional[WelcomeData] = None
    llm_settings: Optional[LlmSettings] = None

    def __str__(self):
        assistant = {
            "assistantId": self.id,
            "assistantName": self.name,
            "assistantType": self.type,
            "assistantPriority": self.priority,
            "assistantStatus": self.status
        }
        if self.intents is not None and any(self.intents):
            assistant["intents"] = self.intents

        if self.description is not None:
            assistant['assistantDescription'] = self.description

        if self.prompt is not None:
            assistant['prompt'] = self.prompt

        if self.project is not None:
            assistant['project'] = self.project

        if self.welcome_data is not None:
            assistant['welcomeData'] = self.welcome_data

        if self.llm_settings is not None:
            assistant['llmSettings'] = self.llm_settings

        return str(assistant)


class TextAssistant(Assistant):
    type: Literal["text"] = "text"


class ChatAssistant(Assistant):
    type: Literal["chat"] = "chat"


class DataAnalystAssistant(Assistant):
    pass


class ChatWithDataAssistant(Assistant):
    pass


