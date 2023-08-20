import os,sys
import json
from BaseLLM import BaseLLM
import Prompt

""" Google vertexai imports """
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.language_models import ChatModel, InputOutputTextPair


# Google BARD gpt interface
"""
The GPT class extends the BaseModel class and overrides the get_response() method, providing an implementation.
The get_response() method takes a response parameter and returns the content of the first response in the given response object.
"""
class BARD(BaseLLM):
    

    #implement here
    def __init__ (self, **kwargs):

       
        # add values here directly or if kwargs are specified they are taken from the config file
        defaults  = {
            "class_name" : "BARD",
            "model" : "chat-bison@001",
            "credentials" : "key.json"
        }
        #if kwargs:
        # super().__init__(kwargs)
        #else:
        #    super().__init__(defaults)

        
    
    # Get Text
    def get_content(self, response):
    
        """ Get the text from the response of an LLM
        e.g.: openai returns the following response, this method should return the 'content'.
        {
          "choices":
             [{
                 {
               "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "from datetime import date\ntoday = date.today()\nprint(\"Today's date is:\", today)",
                    "role": "assistant"
                }
                 }}]
        }
        """
        """ return content """
        return str(response)
    
    
    def get_response(self, prompt: Prompt):
        
        
        """Predict using a Large Language Model."""
        project_id = "verifai-ml-training"
        location = "us-central1"

        vertexai.init(project=project_id, location=location)
        print('model {0}' .format(self.model))
        chat_model = ChatModel.from_pretrained(self.model)
        
        parameters = {
             "max_output_tokens" :  1024,
             "top_p" :  0.8,
             "top_k" :  40,
            "temperature" : 0.2
        }

        chat = chat_model.start_chat(context="",
                                     examples=[]
                                     
        )
        try:
            """ Call API """
            response=chat.send_message( prompt.get_string(), **parameters)
            print('bard response {0}' .format(response))
        except Exception as e:
            print('error calling bard: {0}' .format(str(e)))

        if not response:
            return response
        else:
            return self.get_content(response)
