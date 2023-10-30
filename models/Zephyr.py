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


# zephyr interface
"""
Zephyr is a series of language models that are trained to act as helpful assistants. 
Zephyr-7B-β is the second model in the series, and is a fine-tuned version of mistralai/Mistral-7B-v0.1
 that was trained on on a mix of publicly available, 
 synthetic datasets using Direct Preference Optimization (DPO). 
 We found that removing the in-built alignment of these datasets boosted performance on 
 MT Bench and made the model more helpful. However, this means that model is likely to 
 generate problematic text when prompted to do so and should only be used for educational a
 nd research purposes. You can find more details in the technical report.

"""

class ZEPHYR(BaseLLM):
    

    #implement here
    def __init__ (self, **kwargs):

       
        # add values here directly or if kwargs are specified they are taken from the config file
        defaults  = {
            "class_name" : "ZEPHYR",
            "model" : "zephyr-7b-beta",
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
            return('zephyr response failed as {}'.format(e))
        
    
    
    def get_response(self, prompt: Prompt, taskid=None, convid = None):
        
        
        """Predict using a Large Language Model."""
        project_id = "zephyr"
        location = "us-central1"
        url = "http://54.187.10.199/zephyr/predict"
        
        """ Get credentials file set in the config, and set appropriate variables for your model """

        try:
            """ Call API """
            
            ## See if we can invoke importToDb
            headers = {"Content-Type" :  "application/json"}
            prmpt = prompt.get_string() + " , please return response in markdown format"
            
            
            # Chec if thread of conversation exists.. 
            messages=[]
            if convid:
                qa = super().get_conversation_history(convid,"ZEPHYR")
                for q,a in qa:
                    messages.append( {"role": "user", "content" : q})
                    messages.append( {"role": "assistant", "content" : a})
        
            messages.append( {"role": prompt.get_role(), "content" : prmpt } )
            if prompt.context:
                messages.append({"role": prompt.get_role(), "content" : prompt.get_context()})
        
            #values = {'question':  prmpt}
            values = {'question':  messages}

      
            resp = requests.post(url, data=json.dumps(values),headers=headers)
            print("zephyr-7b-beta Response: {0}" .format(resp.text))
            data = resp.json()
            content, is_code = self.get_content(data)
            
            content = content.replace(prmpt, "")
            extras = ['<s>', '</s>', '[INST]', '[/INST]' ]
            for extra in extras:          
                content = content.replace(extra, '')

            if content and taskid:
                self.publish_to_redis(content, taskid)
                
            return content, is_code
            
        except Exception as e:
            print('error calling zephyr: {0}' .format(str(e)))
            return('zephyr failed as {}'.format(e))
