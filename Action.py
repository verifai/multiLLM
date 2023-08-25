# ==============================================================================
# Copyright 2023 VerifAI All Rights Reserved.
# https://www.verifai.ai
# License: The MIT License
# Copyright (c) VerifAI Inc, https://www.verifai.ai
#
# ==============================================================================


class Action:
    """
    Action class, which is instantiated with a callback function
    which itself will take in a single input and output a single output
    """
    def __init__(self, operation=None):
        """
        init function
        """
        self.operation = operation

    def process(self, data):
        """
        process function that actually runs the apply function
        """
        if self.operation is not None:
            return self.operation(data)
        else:
            return data

    def apply(self, data):
        """
        Simple wrapped for process
        """
        return self.process(data)

    def then(self, next_action):
        """
        Used to chain together functions
        """
        if not isinstance(next_action, Action):
            raise ValueError("next_action must be an instance of the Action class.")
        return ChainedAction(self, next_action)


class ChainedAction(Action):
    """
    Helper class to implement Action.then() so it can use it with multiprocessing
    """
    def __init__(self, action1, action2):
        self.action1 = action1
        self.action2 = action2

    def apply(self, data):
        """
        apply function used to run the Action.then()
        """
        intermediate_result = self.action1.apply(data)
        return self.action2.apply(intermediate_result)


"""
Example code
# Operation 1: Convert the words to lowercase.
def to_lowercase(data):
    return [word.lower() for word in data]

# Operation 2: Remove stopwords from the list of words.
def remove_stopwords(data):
    stopwords = ["a", "an", "the", "is", "and", "in", "on", "of"]
    return [word for word in data if word not in stopwords]

# Operation 3: Join the list of words back to a sentence.
def join_to_sentence(data):
    return " ".join(data)

# Create the Action instances for each operation.
action1 = Action(operation=to_lowercase)
action2 = Action(operation=remove_stopwords)
action3 = Action(operation=join_to_sentence)

# Chain the actions together to form a pipeline.
pipeline = action1.then(action2).then(action3)

# Sample input from the language model.
output_from_llm = ["This", "is", "a", "Sample", "Sentence", "for", "Processing"]

# Process the output using the pipeline.
result = pipeline.apply(output_from_llm)
print(result)
"""
