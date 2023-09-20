# ==============================================================================
# Copyright 2023 VerifAI All Rights Reserved.
# https://www.verifai.ai
# License: 
#
# ==============================================================================

import sys, os
from Action import *
import importlib
import json

class Rank(Action):
    """
    Rank class, which is instantiated with a callback function
    which itself will take in a single input and output a single output
    """
    def __init__(self, config=None):
        """
        init function
        """
        self.is_code = None

        if config:
            try:
                with open(config) as f:
                    conf_data = json.load(f)
                    callback_file = conf_data["Config"]["MultiLLM"]["rank_callback_file"]
                    if not os.path.exists(callback_file):
                        # Check if relative file path works.
                        rel_path, cfile = script_path = os.path.split(os.path.abspath(__file__))
                        callback_file_path = os.path.join(rel_path, callback_file)
                    else:
                        callback_file_path = callback_file
                    
            except Exception as e:
                print('(Rank) ERROR: no rank_callback_file : {0}' .format(str(e)))
                callback_file_path = None
                return None
                
        if callback_file_path:
            head , tail = os.path.split(os.path.abspath(callback_file_path))

            #head , tail = os.path.split(os.path.abspath(callback_file))
            sys.path.append(head)
            mfile = os.path.splitext(tail)[0]
            print("(Rank) loading rank_callback_file: {0}" .format(callback_file_path))
            rank_module = importlib.import_module(mfile)
        
        self.rank_module = rank_module

        
    def set_cb_funct(self) :   # invoke rank_CB
            if self.is_code:
                super().__init__(self.rank_module.rank_CB)
            else:
                super().__init__(self.rank_module.rank_CB_no_code)

    def set_is_code(self, val):
        self.is_code = val



