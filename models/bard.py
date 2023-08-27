import os,sys
import json
from multillm.BaseLLM import BaseLLM
from multillm.Prompt import Prompt

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
            return('your prompt returned no code')
        
    
    
    def get_response(self, prompt: Prompt):
        
        
        """Predict using a Large Language Model."""
        project_id = "verifai-ml-training"
        location = "us-central1"
        
        """ Get credentials file set in the config, and set appropriate variables for your model """
        if not os.path.exists(self.credentials):
            print("({0}) error:  credential file doesn't exist" .format(self.__class__.__name__))
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials

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
            
        except Exception as e:
            print('error calling bard: {0}' .format(str(e)))

        if not response:
            return response
        else: 
            return(self.get_content(response))

