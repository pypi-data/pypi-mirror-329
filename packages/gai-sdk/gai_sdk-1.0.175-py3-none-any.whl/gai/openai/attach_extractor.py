from openai.types.chat.chat_completion import ChatCompletion

"""
This is a convenient function for extracting the content of the response object.
Example:
- For generation.
use `response.extract()` instead of using `response.choices[0].message.content`.
- For stream.
    for chunk in response:
        if chunk:
            chunk.extract()
"""
def attach_extractor(response: ChatCompletion,is_stream:bool):

    if not is_stream:
        # return message content
        if response.choices[0].message.content:
            response.extract = lambda: {
                "type":"content",
                "content": response.choices[0].message.content
            }
            return response
        # return message toolcall
        if response.choices[0].message.tool_calls:
            response.extract = lambda: {
                "type":"function",
                "name": response.choices[0].message.tool_calls[0].function.name,
                "arguments": response.choices[0].message.tool_calls[0].function.arguments
            }
            return response
        raise Exception("completions.attach_extractor: Response is neither content nor toolcall. Please verify the API response.")
    
    def streamer():

        for chunk in response:
            if not chunk:
                continue

            if chunk.choices[0].delta.content or chunk.choices[0].delta.role:
                chunk.extract = lambda: chunk.choices[0].delta.content

            if chunk.choices[0].delta.tool_calls:

                if chunk.choices[0].delta.tool_calls[0].function.name:
                    chunk.extract = lambda: {
                        "type":"function",
                        "name": chunk.choices[0].delta.tool_calls[0].function.name,
                    }

                if chunk.choices[0].delta.tool_calls[0].function.arguments:
                    chunk.extract = lambda: {
                        "type":"function",
                        "arguments": chunk.choices[0].delta.tool_calls[0].function.arguments,
                    }

            if chunk.choices[0].finish_reason:
                chunk.extract = lambda: {
                    "type":"finish_reason",
                    "finish_reason": chunk.choices[0].finish_reason
                }

            if not hasattr(chunk,"extract") or not chunk.extract:
                chunk.extract = lambda: ""
                #raise Exception(f"completions.streamer: Chunk response contains unexpected data that cannot be processed. chunk: {chunk.__dict__}")
            yield chunk

    return (chunk for chunk in streamer())   