# ==============================================================================
# Copyright 2023 VerifAI All Rights Reserved.
# https://www.verifai.ai
# License: 
#
# ==============================================================================


import os
import sys
import re

from transformers import AutoTokenizer

class Prompt(object):

    #format_string : str
    
    #class Prompt:
    def __init__(self, format_string, role=None, context=None):
        """format_string: "Something like this or {something_else}"
        We can then format this string using keyword args

        Args:
             format_string: a string to formated using curly braces {}
        
        """
        self.format_string = format_string
        self.role = role
        self.context = context

    def __call__(self, **kwargs):
        """__call__ for formatting the string

        Args:
            kwargs: Keyword args 

        """
        return self.format_string.format(**kwargs)

    def __str__(self):
        """__str__ for getting the string representation of the format string

        """
        return self.format_string

    def __repr__(self):
        """__repr__ for getting the objects representation

        """
        return f"Prompt('{self.format_string}')"

    def __len__(self):
        """__len__ for getting the unformatted string length (removes keywords and calculates)

        """
        unformatted_string = self.format_string.replace('{', '').replace('}', '')
        return len(unformatted_string)

    def tokens_used(self, tokenizer_name="gpt2", kwargs=None):
        """Returns the number of tokens used from the unformatted string

        Args:
            tokenizer_name: The name of the tokenizer we want to use
            kwargs: The keywords we want to optionally format and get the tokenized length of
   
        Returns:
            The token count
        """
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        if not kwargs:
            unformatted_string = self.format_string.replace('{', '').replace('}', '')
        else:
            unformatted_sring = self.format_string.format(**kwargs)
        tokens = tokenizer.tokenize(unformatted_string)
        return len(tokens)

    def get_keywords(self):
        """Returns a list of keywords from the prompt format_string body

        Args:
            None

        Returns:
            A list of keywords
        """
        pattern = r"{(.*?)}"
        return re.findall(pattern, self.format_string)

    def get_string(self):
        """Returns the formatted_string variable 

        Args:
            None

        Returns:
        formatted_string : String
        """
        return(self.format_string)


    def get_role(self):
        """Returns the role variable

        Args:
            None

        Returns:
        role: String
        """
        return(self.role)



    def get_context(self):
        """Returns the context string
        
        Args:
            None
        
        Returns:
        context: String
        """
        return(self.context)
