import os,sys
import openai
import json
from BaseLLM import BaseLLM
import Prompt


# Openai gpt interface
"""
The GPT class extends the BaseModel class and overrides the get_response() method, providing an implementation.
The get_response() method takes a response parameter and returns the content of the first response in the given response object.
"""
class GPT(BaseLLM):
    

    #implement here
    def __init__ (self, **kwargs):

       
        # add values here directly or if kwargs are specified they are taken from the config file
        defaults  = {
            "class_name" : "GPT",
            "model" : "gpt-3.5-turbo",
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
        return response["choices"][0]["message"]["content"]
    
    
    def get_response(self, prompt):
        
        # setup prompt for API call
        messages=[]
        
        messages.append( {"role": prompt.get_role(), "content" : prompt.get_string()})
        if prompt.context:
            messages.append({"role": prompt.get_role(), "content" : prompt.get_context()})
        
        # Setup Credentials
        
        """ or seet an Env Variable to be more secure
        self.credentials = os.getenv('OPENAI_APPLICATION_CREDENTIALS')
        """
    
        if not os.path.exists(self.credentials):
            print('error (multi_llm): could not find openai_credentials: {0}' .format(self.credentials))
            return 
        

        # Open the file for reading
        try:
            with open(self.credentials, 'r') as file:
                # Load the JSON data from the file
                data = json.load(file)
                openai.organization = data['organization']
                openai.api_key = data['api_key'] 

        except Exception as e:
            print('(multi_llm) error: could not load credentials {0} : {1}' .format(self.credentials,str(e)))
            return
                    
        # do API call
        response = openai.ChatCompletion.create(
            model = self.model,
            messages=messages
        )
        
        # return response
        #print("response {0}" .format(response))
        if response:
            return(self.get_content(response))
        else:
            return response
