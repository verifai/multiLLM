# ==============================================================================
# Copyright 2023 VerifAI All Rights Reserved.
# https://www.verifai.ai
# License: 
#
# ==============================================================================
import os,sys
import json
import requests
from multillm.BaseLLM import BaseLLM
from multillm.Prompt import Prompt

""" Google vertexai imports """
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.language_models import ChatModel, InputOutputTextPair


# mistral interface
"""
The Mistral-7B-v0.1 Large Language Model (LLM) is a pretrained generative text model with 7 billion parameters. Mistral-7B-v0.1 outperforms Llama 2 13B on all benchmarks we tested.

For full details of this model please read our Release blog post:
https://mistral.ai/news/announcing-mistral-7b/

Model Architecture
Mistral-7B-v0.1 is a transformer model, with the following architecture choices:

Grouped-Query Attention
Sliding-Window Attention
Byte-fallback BPE tokenizer

"""

class MISTRAL(BaseLLM):
    

    #implement here
    def __init__ (self, **kwargs):

       
        # add values here directly or if kwargs are specified they are taken from the config file
        defaults  = {
            "class_name" : "mistral",
            "model" : "mistralai/Mistral-7B-v0.1",
            "credentials" : "key.json"
        }
       
        
    
    # Get Text
    def get_content(self, response):
    
        """ Get the text from the response of an LLM """
        try:
            resp = response
        except Exception as e:
            #print("error is_code() {0}" .format(str(e)))
            return('your prompt returned no response  as {}'.format(e))

        try:
            if self.is_code(resp):
                print("{0} response: {1}" .format(self.__class__.__name__,str(resp)))
                return str(resp), True
            else:
                return str(resp), False
        except Exception as e:
            #print("error is_code() {0}" .format(str(e)))
            return('mistral response failed as {}'.format(e))
        
    
    
    def get_response(self, prompt: Prompt, taskid=None, convid = None):
        
        
        """Predict using a Large Language Model."""
        project_id = "mistral"
        location = "us-central1"
        url = "http://54.187.10.199/mistral/predict"
        
        """ Get credentials file set in the config, and set appropriate variables for your model """

        try:
            """ Call API """
            
            ## See if we can invoke importToDb
            headers = {"Content-Type" :  "application/json"}
            prmpt = prompt.get_string() + " , please return response in markdown format"
            
            
            # Chec if thread of conversation exists.. 
            messages=[]
            if convid:
                qa = super().get_conversation_history(convid,"MISTRAL")
                for q,a in qa:
                    messages.append( {"role": "user", "content" : q})
                    messages.append( {"role": "assistant", "content" : a})
        
            messages.append( {"role": prompt.get_role(), "content" : prmpt } )
            if prompt.context:
                messages.append({"role": prompt.get_role(), "content" : prompt.get_context()})
        
            #values = {'question':  prmpt}
            values = {'question':  messages}

      
            resp = requests.post(url, data=json.dumps(values),headers=headers)
            print("mistral Response: {0}" .format(resp.text))
            data = resp.json()
            #print("mistral JSON Response: {0}" .format(data))
            content, is_code = self.get_content(data)
            #print("mistral here: {0}" .format(content))
            content = content.replace(prmpt, "")
            extras = ['<s>', '</s>', '[INST]', '[/INST]' ]
            for extra in extras:          
                content = content.replace(extra, '')

            if content and taskid:
                self.publish_to_redis(content, taskid)
                
            return content, is_code
            
        except Exception as e:
            print('error calling mistral: {0}' .format(str(e)))
            return('mistral failed as {}'.format(e))
