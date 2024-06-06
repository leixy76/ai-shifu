from .ernie import *
from .glm import *
import openai
from flask import Flask



client = openai.Client(api_key="sk-proj-TsOFXPGAkp6GZKt1AUinT3BlbkFJiFiJO0hAu7om7TOl4RRY") 



OPENAI_MODELS = [i.id for i in client.models.list().data]
ERNIE_MODELS = get_erine_models(Flask(__name__))
GLM_MODELS = get_zhipu_models(Flask(__name__))


print(OPENAI_MODELS)

class LLMStreamaUsage:
    def __init__(self,prompt_tokens,completion_tokens,total_tokens):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens=completion_tokens
        self.total_tokens=total_tokens
class LLMStreamResponse:
    def __init__(self,id,is_end,is_truncated,result,finish_reason,usage):
        self.id = id
    
        self.is_end = is_end
        self.is_truncated = is_truncated
        self.result = result
        self.finish_reason = finish_reason
        self.usage = LLMStreamaUsage(**usage) if usage else None


def invoke_llm(app:Flask,model,message,system=None,**kwargs)->Generator[LLMStreamResponse,None,None]:
    kwargs.update({"stream":True})  
    if model in OPENAI_MODELS:
        messages = []
        if system:
            messages.append({"content":system,"role":"system"})
        messages.append({"content":message,"role":"user"})
        response = client.chat.completions.create(model=model,messages=messages,**kwargs)
        for res in response:
            yield LLMStreamResponse(res.id,
                                    True if res.choices[0].finish_reason else False,
                                    False,res.choices[0].delta.content,
                                    res.choices[0].finish_reason,None)
    elif model in ERNIE_MODELS:
        if system:
            kwargs.update({"system":system})  
        response = get_chat_response(app,model,msg = message,**kwargs)
        for res in response:
            yield LLMStreamResponse(res.id,res.is_end,res.is_truncated,res.result,res.finish_reason,res.usage.__dict__)
    elif model in GLM_MODELS:
        response = invoke_glm(app,model,message,system,**kwargs)
        for res in response:
            yield LLMStreamResponse(res.id,
                                    True if res.choices[0].finish_reason else False,
                                    False,res.choices[0].delta.content,
                                    res.choices[0].finish_reason,None)    
    else:
        raise Exception("model not found")
