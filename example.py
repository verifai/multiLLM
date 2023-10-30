#!/usr/bin/env python
# ==============================================================================
# Copyright 2023 VerifAI All Rights Reserved.
# https://www.verifai.ai
# License:
#
# ==============================================================================

import sys
import os
import argparse
import ast
import re
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import concurrent.futures
import multiprocessing


from multillm.Prompt import Prompt
from multillm.BaseLLM import BaseLLM
from multillm.Action import Action
from multillm.Rank import Rank
from multillm.MultiLLM import MultiLLM


def main():
    

    global redisConnected

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        help="Path to config filename",
        metavar="STRING",
    )

    parser.add_argument(
        "-prompt",
        "--prompt",
        dest="prompt",
        help="Input prompt to LLM model",
        metavar="STRING",
    )

    parser.add_argument(
        "-src",
        "--source",
        dest="source",
        nargs="*",
        help="Specify a single or list of source files to pass to LLM (Default= None)",
        metavar="STRING",
    )

    parser.add_argument(
        "-llms",
        "--llms",
        dest="llms",
        nargs="*",
        help="Specify a list of LLMs to use (Default=All)",
        metavar="STRING",
    )

    parser.add_argument(
        "-taskid",
        "--taskid",
        dest="taskid",
        help="Specify a taskid to identify the process",
        metavar="STRING",
    )

    parser.add_argument(
        "-convid",
        "--conversationid",
        dest="convid",
        help="Specify a convid to identify if prompt is continuing a thread",
        metavar="STRING",
    )

    parser.add_argument(
        "-debug",
        "--debug",
        action="store_true", 
        dest="debug", 
        help = "Run multill in debug mode")
    
    """ Process command line arguments """
    args, unknown = parser.parse_known_args()

   
    # Disable printing to stdout temporarily
    if args.debug == False:
        sys.stdout = open(os.devnull, 'w')

    if args.convid:
        convid = args.convid
    else:
        convid = None

    """ make sure config file is specified """
    if not args.config_file:
        print("(MultiLLM) please specify a config file")
        sys.exit(0)

    """ make sure a promt is specified """
    if not args.prompt:
        print("(MultiLLM) please specify a prompt")
        sys.exit(0)



    """ create an instantce of the Prompt() class """
    p = Prompt(args.prompt)
    p.role = "user"


    """ If Context file is specified, use it 
      We support only one file at the moment
      """
    if args.source:

        src = args.source[0] 
        if not os.path.exists(src):
            print('(MultiLLM) Context file doesnot exist: {0}' .format(src))
        else:
            try:
                with open(src, 'r') as file:
                    p.context = file.read()
            except Exception as e:
                print('(MultiLLM) could not read context file: {0}: {1}' .format(src, str(e)))

    #If subset of LLMs is specified use it.
    if args.llms:
        llms = args.llms

    else:
        llms = []

    """ create an instance of the  Multi_LMM class """
    multi_llm = MultiLLM(args.config_file, model_names = llms)


    ## Action operation definitions
    # Action Operation 1: Extract code from the content
    def extract_code(data):
        def verify_code(code):
            try:
                import ast

                ast.parse(code)
            except SyntaxError as e:
                return False
            return True

        regex_pattern = r"```(?:[a-zA-Z]+)?(?:[a-zA-Z]+\n)?([^`]+)(?:```)?"

        import re

        matches = re.findall(regex_pattern, data)
        if not matches:
            # alert that there is no code, we must let gpt know that there is no code here
            print("No markdown matches, searching plain text...")
            attempt = verify_code(data)
            if attempt:
                # log.info("Matched plain text")
                return data
            else:
                print("Syntax error parsing code")
            print("No matches")
            return data
            #return "your prompt returned no code"

        else:
            return matches

    # Action Operation 2: Print the data
    def print_it(data):
        #print(f"Data extracted: {data}")
        return data

    # Create the Action instances for each operation.
    action1 = Action(operation=extract_code)
    action2 = Action(operation=print_it)

    # Chain the actions together to form a pipeline.
    action_chain = action1.then(action2)

    # Create the Rank instance
    # Check if rank_callback_file is specified
    try:
        rank = Rank(args.config_file) if convid is None else None
    except Exception as e:
        rank = None

    # Call the model
    r = multi_llm.run(p, action_chain, rank, args.taskid, convid)
    # Restore stdout and print
    res = {"result": r}
    sys.stdout = sys.__stdout__
    print(json.dumps(res))
    #print("multi llm response {0}".format(r))
