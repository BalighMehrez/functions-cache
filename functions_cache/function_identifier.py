class FunctionIdentifier:
    def __init__(self,function_name: str, function_args: tuple = (), function_kwargs: dict={}):
        self.function_name = function_name
        self.function_args = function_args
        self.function_kwargs = function_kwargs