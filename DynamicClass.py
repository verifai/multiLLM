import types
import os,sys


class DynamicClass(object):

    def __init__(self, class_name):
        self.name = class_name
        
    def create_function_from_string(self, function_code, function_name):
        """Creates a function from a string."""

        locals_dict = {}
        exec(function_code, globals(), locals_dict)

        # Step 3: Retrieve the created function from the locals dictionary
        function = locals_dict[function_name]
        return function


    def create_class(self,class_name, class_dict):

        # Define the class attributes and methods in a dictionary
        #class_dict = {
        #    'class_variable': 123,        # A class-level variable
        #    'class_method': lambda self: "This is a class method!",  # A class-level method
        #    'dynamic_function': dynamic_function  # The dynamically added member function
        #    #'my_function' : my_function
        #}

        # Create the class dynamically using type()
        myClass = type(class_name, (), class_dict)
        return myClass

    def add_function_to_class(self, class_obj, function_name, function_code):
    
        my_function = self.create_function_from_string(function_code, function_name)
        class_method = types.MethodType(my_function, class_obj)
        setattr(class_obj, function_name, class_method)



    def create_class_from_config(self, class_name, llm_config=None):
        """ create a class from a config file description, of the llm section:
        e.g.: llm = [ 
         {
           "name": "llama",
           "model" : "meta-llama/Llama-2-7b-chat-hf",
           "role" : "user",
           "url" : "https://api.openai.com/v1/chat/completions",
           "context" : "gauss_elimination.py",
            "args" :
               {
                "key1" : "val1",
                "key2" : "val2"
               }
            },
        """

        # Convert the function to a class method and bind it to the class
        # Create Dynamic Functions

        function_name = "mult"

        class_dict = {
            'class_variable': 123,        # A class-level variable
            'class_method': lambda self: "This is a class method!"  # A class-level method
            #'dynamic_function': dynamic_function  # The dynamically added member function
        }

        function_code = """
def mult(self, {0}):
  return x * 2
    """.format("x")

        # Create an instance of the dynamically created class
        instance = self.create_class(class_name, class_dict)
        self.add_function_to_class(instance, function_name, function_code)

        # Access and call the dynamically added member function
        #result = instance.dynamic_function()
        #print(result)  # Output: "This is a dynamically added function!"
        
        # Access and call the dynamically added member function
        result = instance.mult(13)
        print(result)  # Output: "This is a dynamically added function!"
        
        # Access and use the class-level variable and method
        print(instance.class_variable)        # Output: 123
        #print(globals())
        #print(instance.class_method())            # Output: "This is a class method!"
    
        attrs = vars(instance)
        print(', '.join("%s: %s" % item for item in attrs.items()))


## Test Creating class , adding methods to the class and testing..
d = DynamicClass('CodeClass')
d.create_class_from_config('CodeClass')
