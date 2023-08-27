# ==============================================================================
# Copyright 2023 VerifAI All Rights Reserved.
# https://www.verifai.ai
# License: 
#
# ==============================================================================
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from Action import *


""" Add your callback function here """
## Rank operation definitions
# Rank Operation 1

import json
import openai
from multillm.MultiLLM import MultiLLM

def rank_CB(responses, config=None):
    """ rank_CB is called by Rank() class, with the arguments dict and config
    Args:
        responses: dictionary of key,value in the form of {"llm-name" : "response"}
        config: name of config file used during the multillm calls..
    Description:
        The purpose of this callback is to rank the responses of the various LLMs from the responses dictionary,
        and to return the result as a text string or markdown.
        For example: if responses = {"GPT" : gpt-response , "BARD" : bard-response}
        this callback will parse, analyze and rank the responses from "GPT" and "BARD" and return a ranked result"
    """
    
    """ Read Config Fild data"""
    conf_data = MultiLLM.read_config()
    if conf_data:
        """ Get the credentials for GPT LLM"""
        try:
            llms = conf_data["Config"]["MultiLLM"]["llms"]  
            for llm in llms:
                if llm['class_name'] == "GPT":
                    credentials = llm['credentials']
                    openai_auth_file = credentials
                    if not os.path.exists(openai_auth_file):
                        return ("(rank_CB) could not find GPT credentials: {0}" .format(openai_auth_file))
                    break
        except Exception as e:
            return ("(rank_CB) could not find GPT credentials: {0}" .format(str(e)))
    try:
        with open(openai_auth_file, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)
            try:
                openai.organization = data['organization']
                openai.api_key = data['api_key'] 
            except Exception as e:
                print('(LLM.check_key(): {0}' .format(str(e)))
                return ("(rank_CB) could not find GPT credentials: {0}" .format(str(e)))
    except Exception as e:
        print('(LLM.check_key(): {0}' .format(str(e)))
        return ("(rank_CB) could not find GPT credentials: {0}" .format(str(e)))
            
    messages = [
            {"role": "system", "content":"Given the following LLMs and their responses, rank them. Response only with a name and explanation in bullet points. Return the response in markdown format"}
            #{ "role": "system", "content":"You are an LLM tasked with ranking other LLMs, given the following LLMs and their responses, rank them. Response only with a name and explanation in a python list"}
    ]

    
    no_code = False
    for llm,response in responses.items():
        #print('llm: {0} Response {1}' .format(llm, response))
        if not response or "returned no code" in response:
            no_code = True
        messages.append({"role": "user", "content": f"{llm}: {response}"})

    if no_code:
        return('Sorry, we can only rank code at the moment!')
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response["choices"][0]["message"]["content"]
