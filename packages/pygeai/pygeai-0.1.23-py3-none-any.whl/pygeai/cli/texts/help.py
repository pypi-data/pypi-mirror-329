HELP_TEXT = """
GEAI CLI
--------

NAME
    geai - Command Line Interface for Globant Enterprise AI

SYNOPSIS
    geai <command> [<subcommand>] [--option] [option-arg]

DESCRIPTION
    geai is a cli utility that interacts with the PyGEAI SDK to handle common tasks in Globant Enterprise AI,
    such as creating organizations and projects, defining assistants, managing workflows, etc.
    
    The available subcommands are as follows:
    {available_commands}
    
    You can consult specific options for each command using with:
    geai <command> h
    or
    geai <command> help
    
EXAMPLES
    The command:
        geai --configure
    will help you setup the required environment variables to work with GEAI.
    
    The command:
        ...
    
AUTHORS 
    Developed and maintained by:
        - Alejandro Trinidad <alejandro.trinidad@globant.com>
        
    Copyright 2025, Globant.
"""

ORGANIZATION_HELP_TEXT = """
GEAI CLI - ORGANIZATION
-----------------------

NAME
    geai - Command Line Interface for Globant Enterprise AI

SYNOPSIS
    geai organization <subcommand> --[flag] [flag_arg]

DESCRIPTION
    geai organization is a command from geai cli utility, developed to interact with key components of GEAI
    such as creating organizations and projects, defining assistants, managing workflows, etc.
    
    The options are as follows:
    {available_commands}
    
EXAMPLES
    The command:
        geai c
    starts an interactive tool to configure API KEY and BASE URL to work with GEAI.
    
    The command:
        geai organization list-projects
    list available projects. For this, an organization API KEY is required.
    
    The command:
        ...
    
AUTHORS 
    Developed and maintained by:
        - Alejandro Trinidad <alejandro.trinidad@globant.com>
        
    Copyright 2025, Globant.
"""

ASSISTANT_HELP_TEXT = """
GEAI CLI - ASSISTANT
-----------------------

NAME
    geai - Command Line Interface for Globant Enterprise AI

SYNOPSIS
    geai assistant <subcommand> --[flag] [flag_arg]

DESCRIPTION
    geai assistant is a command from geai cli utility, developed to interact with assistant in GEAI.
    
    The options are as follows:
    {available_commands}
    
EXAMPLES
    The command:
        
    
    The command:
        ...
    
AUTHORS 
    Developed and maintained by:
        - Alejandro Trinidad <alejandro.trinidad@globant.com>
        
    Copyright 2025, Globant.
"""

RAG_ASSISTANT_HELP_TEXT = """
GEAI CLI - RAG ASSISTANT
-----------------------

NAME
    geai - Command Line Interface for Globant Enterprise AI

SYNOPSIS
    geai rag <subcommand> --[flag] [flag_arg]

DESCRIPTION
    geai RAG assistant is a command from geai cli utility, developed to interact with RAG assistant in GEAI.
    
    The options are as follows:
    {available_commands}
    
EXAMPLES
    The command:
        
    
    The command:
        ...
    
AUTHORS 
    Developed and maintained by:
        - Alejandro Trinidad <alejandro.trinidad@globant.com>
        
    Copyright 2025, Globant.
"""

CHAT_HELP_TEXT = """
GEAI CLI - CHAT
-----------------------

NAME
    geai - Command Line Interface for Globant Enterprise AI

SYNOPSIS
    geai chat <subcommand> --[flag] [flag_arg]

DESCRIPTION
    geai chat is a command from geai cli utility, developed to chat with assistant in GEAI.
    
    The options are as follows:
    {available_commands}
    
EXAMPLES
    The command:
        
    
    The command:
        ...
    
AUTHORS 
    Developed and maintained by:
        - Alejandro Trinidad <alejandro.trinidad@globant.com>
        
    Copyright 2025, Globant.
"""

ADMIN_HELP_TEXT = """
GEAI CLI - ADMIN
-----------------------

NAME
    geai - Command Line Interface for Globant Enterprise AI

SYNOPSIS
    geai admin <subcommand> --[flag] [flag_arg]

DESCRIPTION
    geai admin is a command from geai cli utility, developed to interact instance of GEAI.
    
    The options are as follows:
    {available_commands}
    
EXAMPLES
    The command:
        
    
    The command:
        ...
    
AUTHORS 
    Developed and maintained by:
        - Alejandro Trinidad <alejandro.trinidad@globant.com>
        
    Copyright 2025, Globant.
"""


LLM_HELP_TEXT = """
GEAI CLI - LLM
-----------------------

NAME
    geai - Command Line Interface for Globant Enterprise AI

SYNOPSIS
    geai llm <subcommand> --[flag] [flag_arg]

DESCRIPTION
    geai llm is a command from geai cli utility, developed to retrieve information about available models and providers 
    in GEAI.
    
    The options are as follows:
    {available_commands}
    
EXAMPLES
    The command:
        
    
    The command:
        ...
    
AUTHORS 
    Developed and maintained by:
        - Alejandro Trinidad <alejandro.trinidad@globant.com>
        
    Copyright 2025, Globant.
"""

FILES_HELP_TEXT = """
GEAI CLI - FILES
-----------------------

NAME
    geai - Command Line Interface for Globant Enterprise AI

SYNOPSIS
    geai files <subcommand> --[flag] [flag_arg]

DESCRIPTION
    geai files is a command from geai cli utility, developed to interact with files in GEAI.
    
    The options are as follows:
    {available_commands}
    
EXAMPLES
    The command:
        
    
    The command:
        ...
    
AUTHORS 
    Developed and maintained by:
        - Alejandro Trinidad <alejandro.trinidad@globant.com>
        
    Copyright 2025, Globant.
"""

USAGE_LIMIT_HELP_TEXT = """
GEAI CLI - USAGE LIMITS
-----------------------

NAME
    geai - Command Line Interface for Globant Enterprise AI

SYNOPSIS
    geai usage-limit <subcommand> --[flag] [flag_arg]

DESCRIPTION
    geai usage-limits is a command from geai cli utility, developed to manager usage limits in GEAI.
    
    The options are as follows:
    {available_commands}
    
EXAMPLES
    The command:
        
    
    The command:
        ...
    
AUTHORS 
    Developed and maintained by:
        - Alejandro Trinidad <alejandro.trinidad@globant.com>
        
    Copyright 2025, Globant.
"""


CLI_USAGE = """
geai <command> [<subcommand>] [--option] [option-arg]
"""
