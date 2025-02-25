import logging
import openai
from ajent import LLMClient
from openai import OpenAI
from openai.types.chat import ChatCompletionChunk
from typing import Any, Dict, List, Generator
from ..response_serializer import ResponseSerializer


class OpenAIClient(LLMClient):
    def __init__(self, token: str):
        self._client = OpenAI(api_key=token)

    def send(self, messages: List[Dict], tools: List[Dict], model: str) -> Any:
        try:
            response = self._client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools
            )
            message = response.choices[0].message
            return self.serialize_response(message)
        except openai.APIError as e:
            logging.error(f"OpenAI API error: {e}")
            return {"error": "OpenAI API error", "details": str(e)}
        except openai.RateLimitError as e:
            logging.warning("Rate limit exceeded. Please slow down your requests.")
            return {"error": "Rate limit exceeded", "details": str(e)}
        except openai.InvalidRequestError as e:
            logging.error(f"Invalid request: {e}")
            return {"error": "Invalid request", "details": str(e)}
        except openai.AuthenticationError as e:
            logging.error(f"Authentication error: {e}")
            return {"error": "Authentication error", "details": str(e)}
        except openai.OpenAIError as e:
            logging.error(f"General OpenAI error: {e}")
            return {"error": "OpenAI error", "details": str(e)}
        except Exception as e:
            logging.exception("Unexpected error occurred")
            return {"error": "Unexpected error", "details": str(e)}
        
    def serialize_response(self, response: Any) -> Dict:
        return ResponseSerializer.serialize_message(response)

    def stream(self, messages: List[Dict], tools: List[Dict], model: str) -> Generator[Dict, None, None]:
        """
        Streaming version of the send function that yields chunks of the response.
        
        Args:
            messages: List of message dictionaries
            tools: List of tool dictionaries
            model: Model identifier string
        
        Yields:
            Dictionary containing either response chunks or error information
        """
        try:
            # Create streaming response
            stream = self._client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                stream=True  # Enable streaming
            )
            
            # Initialize variables to accumulate the response
            current_tool_calls = {}
            current_content = ""
            current_tool_call_id = None

            
            # Process each chunk
            for chunk in stream:
                if not isinstance(chunk, ChatCompletionChunk):
                    continue
                    
                delta = chunk.choices[0].delta
                
                # Handle tool calls
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        if tool_call.id:
                            current_tool_call_id = tool_call.id
                            print(f"Tool call id: {current_tool_call_id}")
                        else:
                            print("Tool call id not found, keep using the previous one")
                        
                        if current_tool_call_id not in current_tool_calls:
                            print(f"Tool call not found, creating new one. Tool call id: {current_tool_call_id}")
                            print( f"Existing tool calls: {current_tool_calls}")
                            current_tool_calls[current_tool_call_id] = {
                                "id": current_tool_call_id,
                                "type": "function",
                                "function": {"name": "", "arguments": ""}
                            }
                        
                        if tool_call.function.name:
                            print("Tool call function name found")
                            current_tool_calls[current_tool_call_id]["function"]["name"] = tool_call.function.name
                        if tool_call.function.arguments:
                            print("Tool call function arguments found")
                            current_tool_calls[current_tool_call_id]["function"]["arguments"] += tool_call.function.arguments
                            
                        yield {
                            "type": "tool_call",
                            "tool_call": current_tool_calls[current_tool_call_id]
                        }
                
                # Handle content
                if delta.content:
                    current_content += delta.content
                    yield {
                        "type": "content",
                        "content": delta.content
                    }
                    
                # Handle end of response
                if chunk.choices[0].finish_reason:
                    yield {
                        "type": "finish",
                        "finish_reason": chunk.choices[0].finish_reason,
                        "final_content": current_content,
                        "final_tool_calls": list(current_tool_calls.values()) if current_tool_calls else None
                    }
                    
        except openai.APIError as e:
            logging.error(f"OpenAI API error: {e}")
            yield {"error": "OpenAI API error", "details": str(e)}
        except openai.RateLimitError as e:
            logging.warning("Rate limit exceeded. Please slow down your requests.")
            yield {"error": "Rate limit exceeded", "details": str(e)}
        except openai.InvalidRequestError as e:
            logging.error(f"Invalid request: {e}")
            yield {"error": "Invalid request", "details": str(e)}
        except openai.AuthenticationError as e:
            logging.error(f"Authentication error: {e}")
            yield {"error": "Authentication error", "details": str(e)}
        except openai.OpenAIError as e:
            logging.error(f"General OpenAI error: {e}")
            yield {"error": "OpenAI error", "details": str(e)}
        except Exception as e:
            logging.exception("Unexpected error occurred")
            yield {"error": "Unexpected error", "details": str(e)}