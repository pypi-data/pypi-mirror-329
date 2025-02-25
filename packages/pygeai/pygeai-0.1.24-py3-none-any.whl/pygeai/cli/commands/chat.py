import json
import sys

from pygeai.chat.clients import ChatClient
from pygeai.cli.commands import Command, Option, ArgumentsEnum
from pygeai.cli.commands.builders import build_help_text
from pygeai.cli.commands.common import get_messages, get_boolean_value, get_penalty_float_value
from pygeai.cli.texts.help import CHAT_HELP_TEXT
from pygeai.core.common.exceptions import MissingRequirementException, WrongArgumentError


def show_assistant_help():
    """
    Displays help text in stdout
    """
    help_text = build_help_text(chat_commands, CHAT_HELP_TEXT)
    sys.stdout.write(help_text)


def get_chat_completion(option_list: list):
    model = None
    message_list = []
    stream = False
    temperature = None
    max_tokens = None
    thread_id = None
    frequency_penalty = None
    presence_penalty = None
    for option_flag, option_arg in option_list:
        if option_flag.name == "model":
            model = option_arg
        if option_flag.name == "messages":
            try:
                message_json = json.loads(option_arg)
                if isinstance(message_json, list):
                    message_list = message_json
                elif isinstance(message_json, dict):
                    message_list.append(message_json)
            except Exception as e:
                raise WrongArgumentError(
                    "Each message must be in json format: '{\"role\": \"user\", \"content\": \"message content\"}' "
                    "It can be a dictionary or a list of dictionaries. Each dictionary must contain role and content")
        if option_flag.name == "stream":
            if option_arg:
                stream = get_boolean_value(option_arg)
        if option_flag.name == "temperature":
            temperature = option_arg
        if option_flag.name == "max_tokens":
            max_tokens = option_arg
        if option_flag.name == "thread_id":
            thread_id = option_arg
        if option_flag.name == "frequency_penalty":
            if option_arg:
                frequency_penalty = get_penalty_float_value(option_arg)
        if option_flag.name == "presence_penalty":
            if option_arg:
                presence_penalty = get_penalty_float_value(option_arg)

    messages = get_messages(message_list)

    if not (model and messages):
        raise MissingRequirementException("Cannot perform chat completion without specifying model and messages")

    client = ChatClient()
    result = client.chat_completion(
        model=model,
        messages=messages,
        stream=stream,
        temperature=temperature,
        max_tokens=max_tokens,
        thread_id=thread_id,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    sys.stdout.write(f"Chat completion detail: \n{result}\n")


chat_completion_options = [
    Option(
        "model",
        ["--model", "-m"],
        "The model needs to address the assistant type and name or  bot_id, depending on the Type. Then, the parameters"
        " will vary depending on the type. Its format is as follows: \n"
        "\t\"model\": \"saia:<assistant_type>:<assistant_name>|<bot_id>\"",
        True
    ),
    Option(
        "messages",
        ["--messages", "--msg"],
        "The messages element defines the desired messages to be added. The minimal value needs to be the following, "
        "where the content details the user input.\n"
        "\t{ \n"
        "\t\t\"role\": \"string\", /* user, system and may support others depending on the selected model */ \n"
        "\t\t\"content\": \"string\" \n"
        "\t}\n",
        True
    ),
    Option(
        "stream",
        ["--stream"],
        "If response should be streamed. Possible values: 0: OFF; 1: ON",
        True
    ),
    Option(
        "temperature",
        ["--temperature", "--temp"],
        "integer value to set volatility of the assistant's answers",
        True
    ),
    Option(
        "max_tokens",
        ["--max-tokens"],
        "integer value to set max tokens to use",
        True
    ),
    Option(
        "thread_id",
        ["--thread-id"],
        "optional uuid for conversation identifier",
        True
    ),
    Option(
        "frequency_penalty",
        ["--frequency-penalty"],
        "optional number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency "
        "in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
        True
    ),
    Option(
        "presence_penalty",
        ["--presence-penalty"],
        "optional number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in "
        "the text so far, increasing the model's likelihood to talk about new topics.",
        True
    ),

]


chat_commands = [
    Command(
        "help",
        ["help", "h"],
        "Display help text",
        show_assistant_help,
        ArgumentsEnum.NOT_AVAILABLE,
        [],
        []
    ),
    Command(
        "completion",
        ["completion", "comp"],
        "Get chat completion",
        get_chat_completion,
        ArgumentsEnum.REQUIRED,
        [],
        chat_completion_options
    ),
]
