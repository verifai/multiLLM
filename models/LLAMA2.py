import os,sys
import json
import requests
from multillm.BaseLLM import BaseLLM
from multillm.Prompt import Prompt

""" Google vertexai imports """
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.language_models import ChatModel, InputOutputTextPair


# LLAMA-2 interface
"""
The LAMMA class extends the BaseModel class and overrides the get_response() method, providing an implementation.
The get_response() method takes a response parameter and returns the content of the first response in the given response object.
"""
class LLAMA2(BaseLLM):
    

    #implement here
    def __init__ (self, **kwargs):

       
        # add values here directly or if kwargs are specified they are taken from the config file
        defaults  = {
            "class_name" : "LLAMA2",
            "model" : "meta-llama/Llama-2-7b-chat-hf",
            "credentials" : "key.json"
        }
       
        
    
    # Get Text
    def get_content(self, response):
    
        """ Get the text from the response of an LLM """
        try:
            resp = response["generated_text"]
        except Exception as e:
            #print("error is_code() {0}" .format(str(e)))
            return('your prompt returned no response or code')

        try:
            if self.is_code(resp):
                print("{0} response: {1}" .format(self.__class__.__name__,str(resp)))
                return str(resp)
            else:
                return('your prompt returned no code')
        except Exception as e:
            #print("error is_code() {0}" .format(str(e)))
            return('your prompt returned no code')
        
    
    
    def get_response(self, prompt: Prompt, taskid=None):
        
        
        """Predict using a Large Language Model."""
        project_id = "llama2"
        location = "us-central1"
        url = "http://34.221.191.141/predict"
        
        """ Get credentials file set in the config, and set appropriate variables for your model """

        try:
            """ Call API """

            ## See if we can invoke importToDb
            headers = {"Content-Type" :  "application/json"}
            values = {'question':  prompt.get_string() + " , please return response in markdown format"}
      
            resp = requests.post(url, data=json.dumps(values),headers=headers)
            #print("LLAMA2 Response: {0}" .format(resp.text))
            data = resp.json()
            #print("LLAMA2 JSON Response: {0}" .format(data))
            content = self.get_content(data[0])
            if content and taskid:
                self.publish_to_redis(content, taskid)
            return (content)
            
        except Exception as e:
            #print('error calling llama2: {0}' .format(str(e)))
            return('your prompt returned no code')
