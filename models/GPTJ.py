import os,sys
import json
from multillm.BaseLLM import BaseLLM
from multillm.Prompt import Prompt
from gpt4all import GPT4All

# GPT-J
"""
The GPT class extends the BaseModel class and overrides the get_response() method, providing an implementation.
The get_response() method takes a response parameter and returns the content of the first response in the given response object.
Model Description
This model has been finetuned from GPT-J

Developed by: Nomic AI
Model Type: A finetuned GPT-J model on assistant style interaction data
Language(s) (NLP): English
License: Apache-2
Finetuned from model [optional]: GPT-J

https://home.nomic.ai/


"""
class GPTJ(BaseLLM):
    

    #implement here
    def __init__ (self, **kwargs):

       
        # add values here directly or if kwargs are specified they are taken from the config file
        defaults  = {
            "class_name" : "GPTJ",
            "model" : "ggml-gpt4all-j-v1.3-groovy",
            "credentials" : None
        }
        #if kwargs:
        # super().__init__(kwargs)
        #else:
        #    super().__init__(defaults)

        
    
     # Get Text
    def get_content(self, response):
    
        """ Get the text from the response of an LLM """
        try:
            if self.is_code(str(response)):
                print("{0} response: {1}" .format(self.__class__.__name__,str(response)))
                return str(response)
            else:
                #print('BARD is not code')
                return('your prompt returned no code')
        except Exception as e:
            #print("error is_code() {0}" .format(str(e)))
            return('your prompt returned no code with error {}'.format(e))
    
           
    def get_response(self, prompt, taskid=None):
        
        # setup prompt for API call
       
        
        # Setup Credentials
        
        """ or seet an Env Variable to be more secure
        self.credentials = os.getenv('OPENAI_APPLICATION_CREDENTIALS')
        """
    
        

      
        print('model {0}' .format(self.model))
        # do API call
        gptj = GPT4All(self.model)
        response =gptj.generate(prompt.get_string())
        
        # return response
        #print("response {0}" .format(response))
        if not response:
            return response
        else: 
            content = self.get_content(response)
            if content and taskid:
                self.publish_to_redis(content, taskid)
            return (content)
            
          
