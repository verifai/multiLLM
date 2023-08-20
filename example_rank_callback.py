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

def rank_CB(dictionary):
    
    

    openai_auth_file = os.getenv('OPENAI_APPLICATION_CREDENTIALS')
    if not os.path.exists(openai_auth_file):
        sys.exit()
    try:
        with open(openai_auth_file, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)
            try:
                openai.organization = data['organization']
                openai.api_key = data['api_key'] 
            except Exception as e:
                print('(LLM.check_key(): {0}' .format(str(e)))
                sys.exit()
    except Exception as e:
        print('(LLM.check_key(): {0}' .format(str(e)))
        sys.exit()
            
    messages = [
        { "role": "system", "content":"You are an LLM tasked with ranking other LLMs, given the following LLMs and their responses, rank them. Response only with a name and explanation in a python list"}
    ]
    for llm,response in dictionary.items():
        messages.append({"role": "user", "content": f"{llm}: {response}"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response["choices"][0]["message"]["content"]
