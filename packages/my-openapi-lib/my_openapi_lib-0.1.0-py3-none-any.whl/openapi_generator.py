import os
import ast
import json
from typing import Dict, List

def find_important_py_files(folder_path: str) -> List[str]:
    """
    Traverse the given folder to find important Python (.py) files.

    Important files are defined as:
    - Files that contain functions, classes, or "import" statements.
    - Files with non-trivial size (not empty or very small).
    """
    important_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if is_important_file(file_path):
                    important_files.append(file_path)

    return important_files

def is_important_file(file_path: str) -> bool:
    """
    Determine if a .py file is important based on its content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for functions, classes, or imports
        if any(keyword in content for keyword in ["def ", "class ", "import "]):
            return True

        # Check for file size (non-empty files)
        if os.path.getsize(file_path) > 0:
            return True

    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return False

def extract_routes_and_models(py_files: List[str]) -> Dict:
    """
    Extract detailed route information and Pydantic models from Python files.
    """
    data = {"routes": {}, "models": {}}

    for file_path in py_files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                tree = ast.parse(content)
               
                
                # Extract routes and models
                routes_in_file = find_routes_in_ast(tree, file_path)
                models_in_file = find_models_in_ast(tree)

                if routes_in_file:
                    data["routes"][file_path] = routes_in_file
                if models_in_file:
                    data["models"][file_path] = models_in_file

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return data

def find_routes_in_ast(tree: ast.AST, file_path: str) -> List[Dict]:
    """
    Dynamically extract route definitions, including prefixes and tags.
    """
    routes = []   # Store route details (e.g., method, path, tags)
    routers = {}  # Map router variable names to their metadata (prefix, tags) (e.g., `router = APIRouter(...)`).

    class RouteVisitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            """
            Detect router definitions and extract their metadata.
            """
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                if node.value.func.id == "APIRouter":
                    router_name = node.targets[0].id  # The variable name assigned to APIRouter
                    metadata = {"prefix": "", "tags": ["Default"]}  # Default values
                    for kw in node.value.keywords:
                        if kw.arg == "prefix" and isinstance(kw.value, ast.Constant):
                            metadata["prefix"] = kw.value.value
                        if kw.arg == "tags" and isinstance(kw.value, ast.List):
                            metadata["tags"] = [
                                elt.value for elt in kw.value.elts if isinstance(elt, ast.Constant)
                            ]
                    routers[router_name] = metadata

        def visit_FunctionDef(self, node):
            """
            Extract route metadata from synchronous function decorators.
            """
            self._process_function(node)

        def visit_AsyncFunctionDef(self, node):
            """
            Extract route metadata from asynchronous function decorators.
            """
            self._process_function(node)

        def _process_function(self, node):
            """
            Common processing logic for FunctionDef and AsyncFunctionDef.
            """
            method = None  
            router_name = None  
            full_path = None  
            parameters = []  
            body_schema = None  

            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                    method = decorator.func.attr.upper()  # HTTP method (e.g., GET, POST)
                    relative_path = None
                    router_name = decorator.func.value.id if isinstance(decorator.func.value, ast.Name) else None

                    if (
                        decorator.args
                        and isinstance(decorator.args[0], ast.Constant)
                        and isinstance(decorator.args[0].value, str)
                    ):
                        relative_path = decorator.args[0].value

                    prefix = routers.get(router_name, {}).get("prefix", "")
                    full_path = f"{prefix}{relative_path}" if prefix else relative_path

            if method is None:
                method = "GET"  

            if full_path is None:
                return  

            # Extract parameters dynamically
            for i, arg in enumerate(node.args.args):
                param_name = arg.arg
                param_type = "default"
                param_location = "query"

                # Skip Dependencies like db: Session = Depends(get_db)
                if i < len(node.args.defaults):
                    default_value_node = node.args.defaults[i]

                    if (
                        isinstance(default_value_node, ast.Call)
                        and isinstance(default_value_node.func, ast.Name)
                        and default_value_node.func.id == "Depends"
                    ):
                        continue  

                if full_path and f"{{{param_name}}}" in full_path:
                    param_location = "path"
                elif method in {"POST", "PUT"} and param_name not in ["self", "request"]:
                    param_location = "body"
                    body_schema = param_name

                # Extract type hints for parameters
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        param_type = arg.annotation.id
                    elif isinstance(arg.annotation, ast.Subscript):
                        param_type = getattr(arg.annotation.value, "id", "string")

                schema = {
                    "type": param_type,
                    "minimum": None,
                    "maximum": None,
                    "default": None,
                    "title": param_name.capitalize(),
                }

                if i < len(node.args.defaults):
                    default_value_node = node.args.defaults[i]

                    if isinstance(default_value_node, ast.Call):
                        if default_value_node.args:
                            first_arg = default_value_node.args[0]
                            if isinstance(first_arg, ast.Constant):
                                schema["default"] = first_arg.value
                            elif isinstance(first_arg, ast.Name):
                                schema["default"] = first_arg.id  

                        for keyword in default_value_node.keywords:
                            if keyword.arg == "ge":
                                schema["minimum"] = keyword.value.value
                            elif keyword.arg == "le":
                                schema["maximum"] = keyword.value.value
                            elif keyword.arg == "title":
                                schema["title"] = keyword.value.value
                            elif keyword.arg == "description":
                                description = keyword.value.value

                schema = {k: v for k, v in schema.items() if v is not None}

                if param_location != "body":
                    parameters.append({
                        "name": param_name,
                        "in": param_location,
                        "required": param_location == "path",
                        "schema": schema,
                        "description": description if 'description' in locals() else None
                    })

            tags = routers.get(router_name, {}).get("tags", ["Default"])

            docstring = ast.get_docstring(node) or ""
            summary = docstring.split("\n")[0] if docstring else node.name
            description = docstring

            routes.append({
                "method": method,
                "path": full_path,
                "summary": summary,
                "description": description,
                "parameters": parameters,
                "tag": tags,
                "body_schema": body_schema,
            })


    # Visit the AST nodes
    RouteVisitor().visit(tree)
    return routes


def find_models_in_ast(tree: ast.AST) -> List[Dict]:
    """
    Extract Pydantic models from the AST.
    """
    models = []

    class ModelVisitor(ast.NodeVisitor):
        def visit_ClassDef(self, node):
            if any(base.id == "BaseModel" for base in node.bases if isinstance(base, ast.Name)):
                properties = {}
                required_fields = []

                for body_item in node.body:
                    if isinstance(body_item, ast.AnnAssign):  # Field type hints
                        field_name = body_item.target.id
                        field_type = extract_python_type(body_item.annotation)

                        # Track required fields (no default value)
                        if not hasattr(body_item, "value"):
                            required_fields.append(field_name)

                        # Add the field to properties
                        properties[field_name] = field_type

                    elif isinstance(body_item, ast.Assign):  # Direct assignments
                        for target in body_item.targets:
                            if isinstance(target, ast.Name):
                                field_name = target.id
                                properties[field_name] = {"type": "string"}  # Default to string

                models.append({
                    "name": node.name,
                    "properties": properties,
                    "required": required_fields,
                })

    ModelVisitor().visit(tree)
    return models


def extract_python_type(node):
    """
    Convert Python type hints to OpenAPI types.
    Handles Optional, List, and datetime properly.
    """
    if isinstance(node, ast.Name):
        return map_python_type_to_openapi(node.id)

    elif isinstance(node, ast.Subscript):  # Handles List[str], Optional[int], etc.
        base_type = node.value.id if isinstance(node.value, ast.Name) else "string"
        
        if base_type == "List":
            return {"type": "array", "items": map_python_type_to_openapi(node.slice.id)}

        elif base_type == "Optional":
            return {"anyOf": [{"type": map_python_type_to_openapi(node.slice.id)}, {"type": "null"}]}

    return {"type": "string"}  # Default fallback

def map_python_type_to_openapi(python_type):
    """Maps Python types to OpenAPI-compatible types."""
    mapping = {
        "int": "integer",
        "float": "number",
        "bool": "boolean",
        "str": "string",
        "datetime": {"type": "string", "format": "date-time"},
        "list": {"type": "array", "items": {"type": "string"}},
    }
    return mapping.get(python_type, {"type": "string"})



def map_python_type_to_openapi(python_type):
    """Maps Python types to OpenAPI-compatible types."""
    mapping = {
        "int": "integer",
        "float": "number",
        "bool": "boolean",
        "str": "string",
        "datetime": "string",  # Add format datetime if detected
        "list": "array",
        "Optional": "string",
    }
    return mapping.get(python_type, "string")



def generate_openapi_spec(data: Dict, title: str = "E-commerce API", version: str = "1.0.0") -> Dict:
    """
    Generate a refined OpenAPI spec using extracted route data.
    """
    spec = {
        "openapi": "3.1.0",
        "info": {
            "title": title,
            "description": """
            Welcome to the E-commerce API! 🚀
            This API provides comprehensive functionalities for managing your e-commerce platform.
            """,
            "contact": {
                "name": "Developer Support",
                "url": "https://github.com/your-repo",
                "email": "support@ecommerce.com"
            },
            "version": version
        },
        "paths": {},
        "components": {
            "schemas": {},
            "securitySchemes": {
                "HTTPBearer": {
                    "type": "http",
                    "scheme": "bearer"
                }
            }
        }
    }


    for file_path, routes in data.get("routes", {}).items():
        for route in routes:
            path = route.get("path")
            if not path:
                print(f"Warning: Found a route with a missing path in {file_path}. Skipping...")
                continue  # Skip this route

            method = route["method"].lower()
            tag = route.get("tag", "Default")
            summary = route.get("summary", f"{method.capitalize()} {path}")
            description = route.get("description", f"Endpoint for {method} {path}")
            parameters = route.get("parameters", [])
            body_schema = route.get("body_schema")
            auth_required = route.get("auth_required", False)  # Flag to check if security is needed

            # Initialize path if not already in the spec
            if path not in spec["paths"]:
                spec["paths"][path] = {}

            # Determine the response schema based on method type
            response_schemas = {
                "get": "#/components/schemas/ProductsOut",
                "post": "#/components/schemas/ProductOut",
                "put": "#/components/schemas/ProductOut",
                "delete": "#/components/schemas/ProductOutDelete"
            }

            # Define appropriate response codes based on method
            responses = {}

            if method == "get":
                responses["200"] = {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": response_schemas["get"]}
                        }
                    }
                }
                responses["404"] = {
                    "description": "Resource Not Found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/HTTPValidationError"}
                        }
                    }
                }
            elif method == "post":
                responses["201"] = {
                    "description": "Resource Created",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": response_schemas["post"]}
                        }
                    }
                }
            elif method == "put":
                responses["200"] = {
                    "description": "Resource Updated",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": response_schemas["put"]}
                        }
                    }
                }
            elif method == "delete":
                responses["200"] = {  # FastAPI returns 200 for delete, not 204
                    "description": "Resource Deleted",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": response_schemas["delete"]}
                        }
                    }
                }

            # Add common validation error for all methods
            responses["422"] = {
                "description": "Validation Error",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/HTTPValidationError"}
                    }
                }
            }

            # Construct operation data
            operation_data = {
                "tags": [tag],
                "summary": summary,
                "description": description,
                "operationId": f"{method}_{path.replace('/', '_')}".strip('_'),
                "parameters": parameters,
                "responses": responses,
            }

            # Add security if authentication is required
            if auth_required and method in ["post", "put", "delete"]:
                operation_data["security"] = [{"HTTPBearer": []}]

            # Add request body schema for methods that require it
            if body_schema and method in ["post", "put"]:
                operation_data["requestBody"] = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{body_schema}"}
                        }
                    }
                }

            spec["paths"][path][method] = operation_data

            

            # Populate schemas
            for file_path, models in data.get("models", {}).items():
                for model in models:
                    model_name = model["name"]
                    properties = model["properties"]
                    required_fields = model.get("required", [])

                    formatted_properties = {}
                    for prop_name, prop_type in properties.items():
                        prop_data = {"title": prop_name.replace("_", " ").title()}  # Fix title casing

                        # Detect Class References
                        if isinstance(prop_type, str):
                            if prop_type[0].isupper():  # Likely a referenced model
                                prop_data = {"$ref": f"#/components/schemas/{prop_type}"} 
                            else:
                                prop_data["type"] = prop_type  # Normal primitive type (int, str, etc.)

                        elif isinstance(prop_type, dict):
                            # Assign `type` only if present
                            if "type" in prop_type:
                                prop_data["type"] = prop_type["type"]

                            # Handle `anyOf` for nullable fields
                            if "anyOf" in prop_type:
                                prop_data["anyOf"] = prop_type["anyOf"]

                            # Automatically detect referenced schemas ($ref)
                            if "items" in prop_type and isinstance(prop_type["items"], str):
                                prop_data["items"] = {"type": prop_type["items"]}

                            # Detect and set "$ref" for related models
                            if prop_type.get("type") == "object" and "title" in prop_type:
                                prop_data = {"$ref": f"#/components/schemas/{prop_type['title']}"}

                            # Ensure "format: date-time" for datetime fields
                            if "format" in prop_type:
                                prop_data["format"] = prop_type["format"]

                        formatted_properties[prop_name] = prop_data  # Store final property

                    schema_data = {
                        "type": "object",
                        "title": model_name,
                        "properties": formatted_properties,
                    }

                    # Only include "required" if not empty
                    if required_fields:
                        schema_data["required"] = required_fields

                    spec["components"]["schemas"][model_name] = schema_data



    return spec


def save_spec_to_file(spec: Dict, output_file: str) -> None:
    """
    Save the OpenAPI spec to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)
    print(f"OpenAPI spec saved to {output_file}")


# Allow the script to be used as a standalone tool and as a library
def main(folder_to_scan: str, output_file: str = "openapi_spec.json"):
    """Main function to generate OpenAPI spec."""
    print(f"Scanning folder: {folder_to_scan}")
    important_files = find_important_py_files(folder_to_scan)

    if important_files:
        extracted_data = extract_routes_and_models(important_files)
        openapi_spec = generate_openapi_spec(extracted_data)
        save_spec_to_file(openapi_spec, output_file)
    else:
        print("No important Python files found.")