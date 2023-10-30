

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from Action import *

# print("LLMs in rank is {}".format(llms))
# sys.exit()


""" Add your callback function here """
## Rank operation definitions
# Rank Operation 1

import json
import openai
from multillm.MultiLLM import MultiLLM


# Define the list of LLM names
#LLM = ["GPT", "BARD","LLAMA2"]

# Modify the extract_rank_info function







def extract_rank_info(*args):
    '''
    Prints basic "ranking" metrics and information

    Inputs:
        - args (tuple): Tuple of input arguments, including score and explanation for each LLM response.
      
verifai-ai/src/verifai/llm/multi_llm/multillm/example_rank_callback3_scaled.py    '''
    return args

my_custom_functions = [
    {
        'name': 'extract_rank_info',
        'description': 'Get scores out of 10 followed by short explanation for various metrics  from the GPT responses',
        'parameters': {
            'type': 'object',
            'properties': {}
        }
    }
]
my_custom_functions_no_code = [
    {
        'name': 'extract_rank_info',
        'description': 'Get scores out of 10 followed by short explanation for various metrics  from the GPT responses',
        'parameters': {
            'type': 'object',
            'properties': {}
        }
    }
]




# Dynamically generate the properties for each item in LLM


#print(my_custom_functions)


def gen_schema(llm_list, is_code = True):
    if is_code:
        for item in llm_list:
            item_properties = {
                f'{item}_code_quality_score': {
                    'type': 'string',
                    'description': f'Code Quality Score out of 10 of {item} response'
                },
                f'{item}_space_time_efficiency_score': {
                    'type': 'string',
                    'description': f'space_time_efficiency Score out of 10 of {item} response'
                },
                f'{item}_code_quality_exp': {
                    'type': 'string',
                    'description': f'Code Quality explanation of {item} response right after score in response'
                },
                f'{item}_space_time_efficiency_exp': {
                    'type': 'string',
                    'description': f'space_time_efficiency explanation of {item} response right after score in response'
                }
            }
            
            my_custom_functions[0]['parameters']['properties'].update(item_properties)

    else:
        for item in llm_list:
            item_properties_no_code = {
                f'{item}_accuracy_score': {
                    'type': 'string',
                    'description': f'Accuracy Score out of 10 of {item} response'
                },
                f'{item}_completeness_score': {
                    'type': 'string',
                    'description': f'Completeness Score out of 10 of {item} response'
                },
                f'{item}_accuracy_exp': {
                    'type': 'string',
                    'description': f'accuracy explanation of {item} response right after score in response'
                },
                f'{item}_completeness_exp': {
                    'type': 'string',
                    'description': f'completeness explanation of {item} response right after score in response'
                }
            }
    
            my_custom_functions_no_code[0]['parameters']['properties'].update(item_properties_no_code)


# Modify the return_ranking_result function
def return_ranking_result(args_dict, llm_list):
    # Loop through the scores and calculate the sum and count for each LLM

    scores_sum = {llm: 0 for llm in llm_list}
    scores_count = {llm: 0 for llm in llm_list}

    for key, value in args_dict.items():
        for llm in llm_list:
            if key.startswith(llm) and key.endswith("score"):
                scores_sum[llm] += float(value)
                scores_count[llm] += 1

    # Calculate the average scores for each LLM
    average_scores = {llm: scores_sum[llm] / scores_count[llm] for llm in llm_list}
    
    for llm in llm_list:
        args_dict[f"{llm}_avg_score"] = average_scores[llm]

    # Print average scores
    for llm in llm_list:
        print(f"Average {llm} score:", average_scores[llm])

    return args_dict


def transform_json(input_json):
    output_json = {}
    for key in input_json:
        # Split the key using '_' as a separator
        parts = key.split('_')

        # Extract the first part as the group name and the second part as the field name
        group_name = parts[0]
        field_name = '_'.join(parts[1:])

        # Create a dictionary for the group if it doesn't exist
        if group_name not in output_json:
            output_json[group_name] = {}

        # Add the field to the group dictionary with the corresponding value from the input JSON
        output_json[group_name][field_name] = input_json[key]
    return output_json


# Modify the rank_CB function
def rank_CB(responses, config=None):
    # ... (Previous code)
    """ rank_CB is called by Rank() class, with the arguments dict and config
    Args:
        responses: dictionary of key,value in the form of {"llm-name" : "response"}
        config: name of config file used during the multillm calls..
    Description:
        The purpose of this callback is to rank the responses of the various LLMs from the responses dictionary,
        and to return the result as a text string or markdown.
        For example: if responses = {"LLM1" : llm1-response , "LLM2" : llm2-response}
        this callback will parse, analyze and rank the responses from "LLM1" and "LLM2" and return a ranked result"
    """
    
    """ Read Config Fild data"""
    print("Responses are:\n\n")
    print(responses)
    llm_list = []
    for llm, response in responses.items():
        llm_list.append(llm)

    
    gen_schema(llm_list)
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
        {"role": "system", "content": "Given the following LLMs {} and their responses, give each code a score out of 10 for the following 2 metrics for each LLM response. Code quality and space-time efficiency with a short explanation for each. Return these scores and explanations for the responses.total of {} scores and {} explanations".format(str(llm_list), 2*len(llm_list),2*len(llm_list))}
    ]

    no_code_count = 0
    responses_count = len(responses.items())

    for llm, response in responses.items():
        if not response or "returned no code" in response:
            no_code_count += 1
        messages.append({"role": "user", "content": f"{llm}: {response}"})

    if no_code_count == responses_count:
        return 'Sorry, we can only rank code at the moment!'

    exit = False

    while not exit:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=my_custom_functions,
            function_call='auto'
        )

        func_args = response["choices"][0]["message"]["function_call"]["arguments"]
        print(response["choices"][0]["message"])
        print(func_args)

        func_args_json = json.loads(func_args)
        if len(func_args_json) == len(llm_list)*4:
            exit = True
        else:
            print("Rerunning LLM ranking")

    updated_func_args_json = return_ranking_result(func_args_json, llm_list)
    updated_func_args_json = transform_json(updated_func_args_json)

    return updated_func_args_json

# ... (Rest of the code)

def rank_CB_no_code(responses, config=None):
    # ... (Previous code)
    """ rank_CB is called by Rank() class, with the arguments dict and config
    Args:
        responses: dictionary of key,value in the form of {"llm-name" : "response"}
        config: name of config file used during the multillm calls..
    Description:
        The purpose of this callback is to rank the responses of the various LLMs from the responses dictionary,
        and to return the result as a text string or markdown.
        For example: if responses = {"LLM1" : llm1-response , "LLM2" : llm2-response}
        this callback will parse, analyze and rank the responses from "LLM1" and "LLM2" and return a ranked result"
    """
    
    """ Read Config Fild data"""
    print("Responses are:\n\n")
    print(responses)
    conf_data = MultiLLM.read_config()

    llm_list = []
    for llm, response in responses.items():
        llm_list.append(llm)

    
    gen_schema(llm_list, is_code = False)
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
        {"role": "system", "content": "Given the following LLMs {} and their responses, give each code a score out of 10 for the following 2 metrics for each LLM response. Accuracy and completeness with a short explanation for each. Return these scores and explanations for the responses.total of {} scores and {} explanations".format(str(llm_list), 2*len(llm_list),2*len(llm_list))}
    ]

    responses_count = len(responses.items())

    for llm, response in responses.items():
        messages.append({"role": "user", "content": f"{llm}: {response}"})

    

    exit = False

    while not exit:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=my_custom_functions_no_code,
            function_call='auto'
        )

        func_args = response["choices"][0]["message"]["function_call"]["arguments"]
        print(response["choices"][0]["message"])
        print(func_args)

        func_args_json = json.loads(func_args)
        if len(func_args_json) == len(llm_list)*4:
            exit = True
        else:
            print("Rerunning LLM ranking")

    updated_func_args_json = return_ranking_result(func_args_json, llm_list)
    updated_func_args_json = transform_json(updated_func_args_json)

    return updated_func_args_json

