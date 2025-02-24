import inspect
from pydantic import BaseModel

from openai.types.chat_model import ChatModel
from openai import OpenAI
from typing import get_args,Union, Optional,Callable

from gai.lib.config import GaiClientConfig
from gai.openai.attach_extractor import attach_extractor
from gai.lib.logging import getLogger
logger = getLogger(__name__)

def is_BaseModel(item):
    """
    Check if the given item is a subclass of BaseModel.
    This is used to validate response_format.

    Parameters:
        item: The item to check.

    Returns:
        bool: True if the item is a subclass of BaseModel, False otherwise.
    """
    return inspect.isclass(item) and issubclass(item, BaseModel)    

# openai_create(): This function calls the original unpatched chat.completions.create() function.

def openai_create(patched_client, **kwargs):
    stream=kwargs.get("stream",False)
    response = patched_client.chat.completions.original_openai_create(**kwargs)
    response = attach_extractor(response,stream)
    return response

# ollama_create(): This function calls the ollama chat() function.

def ollama_create(client_config, **kwargs):
    from ollama import chat
    
    # Map openai parameters to ollama parameters
    kwargs={
        # Get actual model from config and not from model parameter
        "model": client_config.model,
        "messages": kwargs.get("messages", None),
        "options": {
            "temperature": kwargs.get("temperature", None),
            "top_k": kwargs.get("top_k", None),
            "top_p": kwargs.get("top_p", None),
            "num_predict" : kwargs.get("max_tokens", None),
        },
        "stream": kwargs.get("stream", False),
        "tools": kwargs.get("tools", None),
    }
    
    # Change the default context length of 2048
    if client_config.extra and client_config.extra.get("num_ctx", None):
        kwargs["options"]["num_ctx"] = client_config.extra.get("num_ctx")
    
    if kwargs.get("tools"):
        kwargs["stream"] = False
    response = chat(**kwargs)
    
    # Format ollama output to match openai output
    stream = kwargs["stream"]
    tools = kwargs["tools"]
    
    from gai.openai.ollama_response_builders.completions_factory import CompletionsFactory
    factory = CompletionsFactory()
    if stream and not tools:
        response = factory.chunk.build_stream(response)
        response = attach_extractor(response,stream)  
        response = (chunk for chunk in response)
    else:
        if tools:
            response = factory.message.build_toolcall(response)
        else:
            response = factory.message.build_content(response)
        response = attach_extractor(response,stream)
    return response


# gai_create(): This function calls the gai TTTClient() function.

def gai_create(client_config, **kwargs):
    from gai.ttt.client import TTTClient    
    
    # Map openai parameters to gai parameters
    kwargs = {
        "messages": kwargs.get("messages", None),
        "stream": kwargs.get("stream", False),
        "max_tokens": kwargs.get("max_tokens", None),
        "temperature": kwargs.get("temperature", None),
        "top_p": kwargs.get("top_p", None),
        "top_k": kwargs.get("top_k", None),
        "tools": kwargs.get("tools", None),
        "tool_choice": kwargs.get("tool_choice", None),
        "stop": kwargs.get("stop", None),
        "timeout": kwargs.get("timeout", None),
    }

    ttt = TTTClient(client_config)
    response = ttt(**kwargs)
    return response

# openai_parse(): This function calls the original unpatched beta.chat.completions.parse() function.

def openai_parse(patched_client, **kwargs):
    response = patched_client.beta.chat.completions.original_openai_parse(**kwargs)
    response = attach_extractor(response,is_stream=False)
    return response

# ollama_parse(): This function calls the ollama chat() function.

def ollama_parse(client_config,response_format, **kwargs):
    from ollama import chat
    
    # Map openai parameters to ollama parameters
    kwargs={
        # Get actual model from config and not from model parameter
        "model": client_config.model,
        "messages": kwargs.get("messages", None),
        "options": {
            "temperature": 0,
            "num_predict" : kwargs.get("max_tokens", None),
        },
        "stream": False,
    }

    # We cannot use num_ctx using openai's parameter so in order to change the default context length of 2048,
    # we need to use the extra parameter in the Gai's client_config.
    if client_config.extra and client_config.extra.get("num_ctx", None):
        kwargs["options"]["num_ctx"] = client_config.extra.get("num_ctx")

    # Convert pydantic BaseModel to json schema    
    if is_BaseModel(response_format):
        schema = response_format.model_json_schema()
        kwargs["format"] = schema
    elif type(response_format) is dict:
        if response_format.get("json_schema"):
            kwargs["format"] = response_format["json_schema"]["schema"]
        else:
            kwargs["format"] = response_format        
    else:
        raise Exception("completions.patched_parse: response_format must be a dict or a pydantic BaseModel")    
    
    # Call ollama
    
    response = chat(**kwargs)
        
    # Format ollama output to match openai output
    
    stream = kwargs["stream"]
    from gai.openai.ollama_response_builders.completions_factory import CompletionsFactory
    factory = CompletionsFactory()
    response = factory.message.build_content(response)
    response = attach_extractor(response,stream)
    return response

# gai_parse(): This function calls the gai TTTClient() function.

def gai_parse(client_config,response_format, **kwargs):
    from gai.ttt.client import TTTClient    
    
    # Map openai parameters to gai parameters
    kwargs = {
        "messages": kwargs.get("messages", None),
        "stream": False,
        "max_tokens": kwargs.get("max_tokens", None),
        "timeout": kwargs.get("timeout", None),
    }
    if is_BaseModel(response_format):
        schema = response_format.model_json_schema()
        kwargs["json_schema"] = schema
    elif type(response_format) is dict:
        if response_format.get("json_schema"):
            kwargs["json_schema"] = response_format["json_schema"]["schema"]
        else:
            kwargs["json_schema"] = response_format        
    else:
        raise Exception("completions.patched_parse: response_format must be a dict or a pydantic BaseModel")    

    ttt = TTTClient(client_config)
    response = ttt(**kwargs)
    return response

# This class is used by the monkey patch to override the openai's chat.completions.create() function.
# This is also the class responsible for for GAI's text-to-text completion.
# The main driver is the create() function that can be used to generate or stream completions as JSON output.
# The output from create() should be indisguishable from the output of openai's chat.completions.create() function.
#
# Example:
# from openai import OpenAI
# client = OpenAI()
# from gai.openai.patch import patch_chatcompletions
# openai=patch_chatcompletions(openai)
# openai.chat.completions.create(model="llama3.1", messages=[{"role": "system", "content": "You are a helpful assistant."}], max_tokens=100)

# override_get_client_from_model is meant to be used for unit testing
def patch_chatcompletions(openai_client:OpenAI, file_path:str=None, client_config: Optional[Union[GaiClientConfig|dict]]=None):

    # Step 1: During patch time, the client is patched with the following new functions.

    # a) Add get_client_config() function to the client.
    
    def get_client_config(model:str):
        nonlocal client_config, file_path
        
        if client_config and file_path:
            raise ValueError(f"__init__: config and path cannot be provided at the same time")

        # If model is an openai model, return "openai"
        if model in get_args(ChatModel):
            return GaiClientConfig(client_type="openai", model=model)
        
        # If it is not an openai model, then check client_config
        # There are two ways to provide the client_config:
        # 1. Provide the client_config directly
        # 2. Provide the file_path to the client_config
        # But both cannot be provided at the same time.

        if client_config:
            if isinstance(client_config, dict):
                # Load default config and patch with provided config
                client_config = GaiClientConfig.from_dict(client_config)
            elif not isinstance(client_config, GaiClientConfig):
                raise ValueError(f"__init__: Invalid config provided")
        else:
            # If not config is provided, load config from path
            client_config = GaiClientConfig.from_name(name=model,file_path=file_path)    
            
        return client_config
    
    openai_client.get_client_config = get_client_config
    
    # b) Add the openai_create() function to the client.

    openai_client.openai_create = openai_create
    
    # c) Add the ollama_create() function to the client.
    
    openai_client.ollama_create = ollama_create
    
    # d) Add the gai_create() function to the client.
    
    openai_client.gai_create = gai_create
    
    # e) Add the openai_parse() function to the client.
    
    openai_client.openai_parse = openai_parse
    
    # f) Add the ollama_parse() function to the client.
    
    openai_client.ollama_parse = ollama_parse
    
    # g) Add the gai_parse() function to the client.
    
    openai_client.gai_parse = gai_parse
    
    # Step 2a: Create the actual runtime logic that is used to select the client and call the appropriate create() function.

    def patched_create(**kwargs):
        nonlocal openai_client
        patched_client = openai_client
        model = kwargs.get("model")
        client_config = patched_client.get_client_config(model)
        client_type = client_config.client_type

        if client_type == "openai":
            return patched_client.openai_create(patched_client, **kwargs)    
        
        if client_type == "ollama":
            return patched_client.ollama_create(client_config, **kwargs)
        
        if client_type == "gai":
            return patched_client.gai_create(client_config, **kwargs)
        
        error_message = f"patched_create: Invalid client type: {client_type}"
        logger.error(error_message)
        raise Exception(error_message)

    # Step 2b: Create the actual runtime logic that is used to select the client and call the appropriate parse() function.
    
    def patched_parse(**kwargs):

        nonlocal openai_client
        patched_client = openai_client
        model = kwargs.get("model")
        client_config = patched_client.get_client_config(model)
        client_type = client_config.client_type

        if client_type == "openai":
            return patched_client.openai_parse(patched_client, **kwargs)    
        
        if client_type == "ollama":
            return patched_client.ollama_parse(client_config, **kwargs)
        
        if client_type == "gai":
            return patched_client.gai_parse(client_config, **kwargs)
        
        error_message = f"patched_parse: Invalid client type: {client_type}"
        logger.error(error_message)
        raise Exception(error_message)
        
    # Step 3: Backup the original and patch the client with the patched_create() function.
    if not hasattr(openai_client.chat.completions, 'is_patched'):
        openai_client.chat.completions.original_openai_create = openai_client.chat.completions.create
        openai_client.chat.completions.create = patched_create
        openai_client.chat.completions.is_patched = True
    else:
        error_message = "patched_create: Attempted to re-patch the OpenAI client which is already patched."
        logger.error(error_message)
        raise Exception(error_message)

    if not hasattr(openai_client.beta.chat.completions.parse, 'is_patched'):      
        openai_client.beta.chat.completions.original_openai_parse = openai_client.beta.chat.completions.parse
        openai_client.beta.chat.completions.parse = patched_parse
        openai_client.beta.chat.completions.is_patched = True
        
    else:
        error_message = "patched_parse: Attempted to re-patch the OpenAI client which is already patched."
        logger.error(error_message)
        raise Exception(error_message)



        
    return openai_client