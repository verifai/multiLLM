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


def extract_rank_info(GPT_code_quality_score, GPT_extensibility_score, 
    GPT_maintainability_score, GPT_readability_score,
    GPT_clarity_score, GPT_space_time_efficiency_score,GPT_code_quality_exp, 
    GPT_extensibility_exp, GPT_maintainability_exp, GPT_readability_exp,GPT_clarity_exp,
    GPT_space_time_efficiency_exp,BARD_code_quality_score, BARD_extensibility_score, 
    BARD_maintainability_score, BARD_readability_score,BARD_clarity_score, 
    BARD_space_time_efficiency_score,BARD_code_quality_exp, BARD_extensibility_exp,
    BARD_maintainability_exp, BARD_readability_exp,BARD_clarity_exp, 
    BARD_space_time_efficiency_exp):
    '''
    Prints basic "ranking" metrics and information

    Inputs:
        -GPT_code_quality_score (str): Code Quality Score out of 10 of GPT response
        -GPT_extensibility_score (str): extensibility Score out of 10 of GPT response
        -GPT_maintainability_score (str): maintainability Score out of 10 of GPT response
        -GPT_code_readability_score (str): readability Score out of 10 of GPT response
        -GPT_clarity_score (str): clarity Score out of 10 of GPT response
        -GPT_space_time_efficiency_score (str): space_time_efficiency Score out of 10 of GPT response
        -GPT_code_quality_exp (str): Code Quality short explanation of GPT response
        -GPT_extensibility_exp (str): extensibility short explanation of GPT response
        -GPT_maintainability_exp (str): maintainability short explanation of GPT response
        -GPT_code_readability_exp (str): readability short explanation of GPT response
        -GPT_clarity_exp (str): clarity short explanation of GPT response
        -GPT_space_time_efficiency_exp (str): space_time_efficiency short explanation of GPT response
        -BARD_code_quality_score (str): Code Quality Score out of 10 of BARD response
        -BARD_extensibility_score (str): extensibility Score out of 10 of BARD response
        -BARD_maintainability_score (str): maintainability Score out of 10 of BARD response
        -BARD_code_readability_score (str): readability Score out of 10 of BARD response
        -BARD_clarity_score (str): clarity Score out of 10 of BARD response
        -BARD_space_time_efficiency_score (str): space_time_efficiency Score out of 10 of BARD response
        -BARD_code_quality_exp (str): Code Quality short explanation of BARD response
        -BARD_extensibility_exp (str): extensibility short explanation of BARD response
        -BARD_maintainability_exp (str): maintainability short explanation of BARD response
        -BARD_code_readability_exp (str): readability short explanation of BARD response
        -BARD_clarity_exp (str): clarity short explanation of BARD response
        -BARD_space_time_efficiency_exp (str): space_time_efficiency short explanation of BARD response
      
    '''

    return GPT_code_quality_score, GPT_extensibility_score, GPT_maintainability_score, GPT_readability_score,GPT_clarity_score, GPT_space_time_efficiency_score,GPT_code_quality_exp, GPT_extensibility_exp, GPT_maintainability_exp, GPT_readability_exp,GPT_clarity_exp, GPT_space_time_efficiency_exp,BARD_code_quality_score, BARD_extensibility_score, BARD_maintainability_score, BARD_readability_score,BARD_clarity_score, BARD_space_time_efficiency_score,BARD_code_quality_exp, BARD_extensibility_exp, BARD_maintainability_exp, BARD_readability_exp,BARD_clarity_exp, BARD_space_time_efficiency_exp

def return_ranking_result(args_dict):
    # Loop through the scores and calculate the sum and count for each category
    bard_sum = 0
    bard_count = 0
    gpt_sum = 0
    gpt_count = 0
    for key, value in args_dict.items():
        if key.startswith("BARD") and key.endswith("score"):
            bard_sum += float(value)
            bard_count += 1
        elif key.startswith("GPT") and key.endswith("score"):
            gpt_sum += float(value)
            gpt_count += 1
    # Calculate the average scores
    average_gpt_score = gpt_sum / gpt_count
    average_bard_score = bard_sum / bard_count
    args_dict["GPT_avg_score"] = average_gpt_score
    args_dict["BARD_avg_score"] = average_bard_score

    print("Average GPT score:", average_gpt_score)
    print("Average BARD score:", average_bard_score)
    return args_dict

my_custom_functions = [
    {
        'name': 'extract_rank_info',
        'description': 'Get scores out of 10 followed by short explanation for various metrics  from the GPT response',
        'parameters': {
            'type': 'object',
            'properties': {
                'GPT_code_quality_score': {
                    'type': 'string',
                    'description': 'Code Quality Score out of 10 of GPT response'
                },
                'GPT_extensibility_score': {
                    'type': 'string',
                    'description': 'extensibility Score out of 10 of GPT response'
                },
                'GPT_maintainability_score': {
                    'type': 'string',
                    'description': 'maintainabilit Score out of 10 of GPT response'
                },
                'GPT_readability_score': {
                    'type': 'string',
                    'description': 'readability Score out of 10 of GPT response'
                },
                'GPT_clarity_score': {
                    'type': 'string',
                    'description': 'clarity Score out of 10 of GPT response'
                },
                'GPT_space_time_efficiency_score': {
                    'type': 'string',
                    'description': 'space_time_efficiency Score out of 10 of GPT response'
                },
                'GPT_code_quality_exp': {
                    'type': 'string',
                    'description': 'Code Quality explanation of  GPT response right after score in response'
                },
                'GPT_extensibility_exp': {
                    'type': 'string',
                    'description': 'extensibility explanation of GPT response right after score in response'
                },
                'GPT_maintainability_exp': {
                    'type': 'string',
                    'description': 'maintainability explanation of GPT response right after score in response'
                },
                'GPT_readability_exp': {
                    'type': 'string',
                    'description': 'readability explanation of GPT response right after score in response'
                },
                'GPT_clarity_exp': {
                    'type': 'string',
                    'description': 'clarity explanation of GPT response right after score in response'
                },
                'GPT_space_time_efficiency_exp': {
                    'type': 'string',
                    'description': 'space_time_efficiency explanation of GPT response right after score in response'
                },
                'BARD_code_quality_score': {
                    'type': 'string',
                    'description': 'Code Quality Score out of 10 of BARD response'
                },
                'BARD_extensibility_score': {
                    'type': 'string',
                    'description': 'extensibility Score out of 10 of BARD response'
                },
                'BARD_maintainability_score': {
                    'type': 'string',
                    'description': 'maintainability Score out of 10 of BARD response'
                },
                'BARD_readability_score': {
                    'type': 'string',
                    'description': 'readability Score out of 10 of BARD response'
                },
                'BARD_clarity_score': {
                    'type': 'string',
                    'description': 'clarity Score out of 10 of BARD response'
                },
                'BARD_space_time_efficiency_score': {
                    'type': 'string',
                    'description': 'space_time_efficiency Score out of 10 of BARD response'
                },
                'BARD_code_quality_exp': {
                    'type': 'string',
                    'description': 'Code Quality explanation of  BARD response right after score in response'
                },
                'BARD_extensibility_exp': {
                    'type': 'string',
                    'description': 'extensibility explanation of BARD response right after score in response'
                },
                'BARD_maintainability_exp': {
                    'type': 'string',
                    'description': 'maintainability explanation of BARD response right after score in response'
                },
                'BARD_readability_exp': {
                    'type': 'string',
                    'description': 'readability explanation of BARD response right after score in response'
                },
                'BARD_clarity_exp': {
                    'type': 'string',
                    'description': 'clarity explanation of BARD response right after score in response'
                },
                'BARD_space_time_efficiency_exp': {
                    'type': 'string',
                    'description': 'space_time_efficiency explanation of BARD response right after score in response'
                }
            }
        }
    }
]

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
    print("Responses are:\n\n")
    print(responses)
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
            #{"role": "system", "content":"Given the following LLMs and their responses, rank them. Response only with a name and explanation in bullet points. Return the response in markdown format"}
            #{ "role": "system", "content":"Given the following LLMs and their responses,give each code a score out of 10 in code quality, extensibility, maintainability, readability, clarity and space time efficiency. Then based on the average of all these metrics rank them using integers. Return a nested dictionary object with the scores for each model with keys being the metric and value being the score."}
            #{ "role": "system", "content":"Given the following LLMs and their responses,give each code a score out of 10 for code quality, extensibility, maintainability, readability, clarity and space time efficiency with a short explanation for each.Then take an average of these scores and return average score for the model. Return these scores for the responses."}
            { "role": "system", "content":"Given the following LLMs and their responses,give each code a score out of 10 for following 6 metrics for the BARD key and GPT key.Code quality, extensibility, maintainability, readability, clarity and space time efficiency with a short explanation for each.Return these 12 scores for the responses, 6 scores for GPT and 6 scores for BARD."}


    ]

    
    no_code = False
    for llm,response in responses.items():
        #print('llm: {0} Response {1}' .format(llm, response))
        if not response or "returned no code" in response:
            no_code = True
        messages.append({"role": "user", "content": f"{llm}: {response}"})

    if no_code:
        return('Sorry, we can only rank code at the moment!')
    
    exit = False
    
    while not exit:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions = my_custom_functions,
            function_call = 'auto'

        )

   
        func_args = response["choices"][0]["message"]["function_call"]["arguments"]
        print(response["choices"][0]["message"])
        print(func_args)
    

        func_args_json = json.loads(func_args)
        if len(func_args_json) == 24:
            exit = True
        else:
            print("Rerunning LLM ranking")

    updated_func_args_json = return_ranking_result(func_args_json)
    
    return updated_func_args_json
