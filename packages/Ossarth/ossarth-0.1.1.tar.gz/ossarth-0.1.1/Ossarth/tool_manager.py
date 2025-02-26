import os
from .templates.general_template import TOOL_TEMPLATE, FUNCTION_TEMPLATE

class CustomFunctionManager:
    def __init__(self, result_dir):
        self.result_dir = result_dir
        os.makedirs(self.result_dir, exist_ok=True)

    def create_custom_tool(self, func_name, description, params, args_doc, return_type, return_desc, body, filename=None):  
        function_code = TOOL_TEMPLATE.format(
            func_name=func_name,
            params=params,
            description=description,
            args_doc=args_doc,
            return_type=return_type,
            return_desc=return_desc,
            body=body
        )

        file_path = os.path.join(self.result_dir, f"{filename or func_name}.py")
        mode = "a" if filename and os.path.exists(file_path) else "w"

        with open(file_path, mode) as f:
            if mode == "a":
                f.write("\n\n")
            f.write(function_code)

        print(f"✅ Tool '{func_name}' has been {'appended to' if filename else 'saved at'} {file_path}")

    def create_custom_function(self, func_name, description, params, args_doc, return_type, return_desc, body, filename=None):
        function_code = FUNCTION_TEMPLATE.format(
            func_name=func_name,
            params=params,
            description=description,
            args_doc=args_doc,
            return_type=return_type,
            return_desc=return_desc,
            body=body
        )

        file_path = os.path.join(self.result_dir, f"{filename or func_name}.py")
        mode = "a" if filename and os.path.exists(file_path) else "w"

        with open(file_path, mode) as f:
            if mode == "a":
                f.write("\n\n")
            f.write(function_code)

        print(f"✅ Function '{func_name}' has been {'appended to' if filename else 'saved at'} {file_path}")