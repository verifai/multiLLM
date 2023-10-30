import os,sys
import json
from multillm.BaseLLM import BaseLLM
from multillm.Prompt import Prompt

""" Google vertexai imports """
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.language_models import ChatModel, InputOutputTextPair


# Google BARD interface
"""
The BARD class extends the BaseModel class and overrides the get_response() method, providing an implementation.
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
                return str(response), True
            else:
                #print('BARD is not code')
                print("{0} response: {1}" .format(self.__class__.__name__,str(response)))
                return str(response), False
        except Exception as e:
            #print("error is_code() {0}" .format(str(e)))
            return('Bard response failed {}'.format(e))


    def get_response1(self, prompt: Prompt, taskid=None, convid = None):
    
    
        """Predict using a Large Language Model."""
        project_id = "verifai-ml-training"
        location = "us-central1"
        
        """ Get credentials file set in the config, and set appropriate variables for your model """
        if not os.path.exists(self.credentials):
            print("({0}) error:  credential file doesn't exist" .format(self.__class__.__name__))
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials
        """
        vertexai.init(project=project_id, location=location)
        print('model {0}' .format(self.model))
        chat_model = ChatModel.from_pretrained(self.model)
        
        """ 
        "client_id" =  "xxxxxx",
        "client_secret": "xxxx",
        "quota_project_id": "verifai-ml-training",
        "refresh_token": "1//06LRKjz4n1BBHCgYIARAAGAYSNgF-L9Ir2oB1-gO0hIjXcbMVVgrpYLSTtoxGLhT8DB7MsfmOkSNsh1gcaLkKP9PxBVxOJmT1pw",
        "type": "authorized_user"
        try:
            with open(self.credentials, 'r') as file:
                # Load the JSON data from the file
                cred = json.load(file)
            
        except Exception as e:
            print('(multi_llm) error: could not load credentials {0} : {1}' .format(self.credentials,str(e)))
            return
        
        parameters = {
            "max_output_tokens" :  1024,
            "top_p" :  0.8,
            "top_k" :  40,
            "temperature" : 0.2
        }
        urls = "https://us-central1-aiplatform.googleapis.com/v1/projects/" + cred.quota_project_id + "/locations/us-central1/publishers/google/models/chat-bison:predict"
        """ If context file exists, use it """
        context = ""
        if prompt.context:
            context = prompt.get_context()

        """ Create a Chat_model """        

        payload = {
        "instances": [{
            "context":  context,
            
            "messages": [
            { 
                "author": "user",
                "content": prompt.get_string(),
            }],
        }],
        "parameters": parameters
        }

        try:
            """ Call API """
            headers = {"Authorization": "Bearer " + cred.refresh_token, "Content-Type" :  "application/json", 'accept': "application/json"}
            

            resp = requests.post(url, data=json.dumps(payload),headers=headers)
            print("Bard Response: {0}" .format(resp.text))
            data = resp.json()
            
        except Exception as e:
            print('error calling bard: {0}' .format(str(e)))

        if not response:
            return response
        else: 
            content, is_code = self.get_content(response)
            if content and taskid:
                self.publish_to_redis(content, taskid)
            return(content), is_code 

    


    def get_response1(self, prompt: Prompt, taskid=None, convid = None):
        
        
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

        """ If context file exists, use it """
        context = ""
        if prompt.context:
            context = prompt.get_context()
    
        """ Create a Chat_model """        
        chat = chat_model.start_chat(context=context,
                                     examples=[] )
        try:
            """ Call API """
            response=chat.send_message( prompt.get_string(), **parameters)
            
        except Exception as e:
            print('error calling bard: {0}' .format(str(e)))

        if not response:
            return response
        else: 
            content, is_code = self.get_content(response)
            if content and taskid:
                self.publish_to_redis(content, taskid)
            return(content), is_code

