import csv
from dataclasses import dataclass
from io import StringIO

def dict_to_csv(data: list[dict]) -> str:
    """
    Convert a dictionary to a CSV string.
    """
    # Use a StringIO object to simulate a file for CSV writer
    f = StringIO()
    writer = csv.writer(f)
    if not data: 
        return ""
    # Write the header row
    writer.writerow(data[0].keys())
    # Write the data rows
    for row in data:
        writer.writerow(row.values())
    # Get the CSV string
    csv_string = f.getvalue()
    f.close()
    return csv_string


@dataclass
class OpenApiGeneric:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        return self.__dict__
    
    def __str__(self) -> str:
        return str(self.to_dict())
    
    def __repr__(self) -> str:
        return str(self.to_dict())


@dataclass
class OpenApiGenericList:
    content: list[OpenApiGeneric]

    def __init__(self, content: list[OpenApiGeneric]) -> None:
        self.content = content

    def to_dict(self):
        return [item.to_dict() for item in self.content]
    
    def to_csv(self):
        return dict_to_csv(self.to_dict())


class OpenApiMethodDefinition(OpenApiGeneric):
    operation_id: str
    path: str
    method: str
    summary: str
    security: str
 
class OpenApiMethodDefinitionList(OpenApiGenericList):
    content: list[OpenApiMethodDefinition]

class OpenApiParameterDefinition(OpenApiGeneric):
    operation_id: str
    required: bool
    name: str
    in_: str
    parameter_type: str

class OpenApiParameterDefinitionList(OpenApiGenericList):
    content: list[OpenApiParameterDefinition]

class OpenApiRequestBodyDefinition(OpenApiGeneric):
    operation_id: str
    content_type: str
    schema_ref: str

class OpenApiRequestBodyDefinitionList(OpenApiGenericList):
    content: list[OpenApiRequestBodyDefinition]

class OpenApiSecurityDefinition(OpenApiGeneric):
    security_name: str
    security_type: str

class OpenApiSecurityDefinitionList(OpenApiGenericList):
    content: list[OpenApiSecurityDefinition]

@dataclass
class OpenApiParts:
    method_definitions: OpenApiMethodDefinitionList
    security_definitions: OpenApiSecurityDefinitionList

class OpenApiParser:
    def __init__(self, openapi_json: dict) -> None:
        self.openapi_json = openapi_json
        self.openapi_parts = OpenApiParts([], [])
        self.openapi_request = {}
        self.openapi_response = {}

    def parse(self) -> OpenApiParts:
        self._parse_paths()
        self._parse_components()
        return self.openapi_parts, self.openapi_request, self.openapi_response
    
    def _parse_paths(self):
        openapi_data = self.openapi_json
    
        method_definition_data = []
        parameter_list = []
        request_body_list = []

        for path, path_item in openapi_data["paths"].items():
            for method, operation in path_item.items():
                operation_id = operation["operationId"]
                security = None
                if "security" in operation:
                    security = list(operation["security"][0].keys())[0]
                responses = operation.get("responses")
                success_response = responses.get("200")
                if not success_response: 
                    success_response = list(responses.values())[0]
                if success_response.get("content"):
                    response_content_type, response_content = list(success_response.get("content").items())[0]
                    response_content_schema = response_content.get("schema")
                else:
                    response_content_type = None
                    response_content = None
                    response_content_schema = None

                if parameters := operation.get("parameters"):
                    for parameter in parameters:
                        parameter_type = parameter.get("schema").get("type")
                        if parameter_type == "array" and parameter.get("schema", {}).get("items"):
                            parameter_type_ref = parameter["schema"]['items'].get('type')
                            parameter_type = f"array[{parameter_type_ref}]"
                        parameter_list.append({
                            "operation_id": operation_id,
                            "required": parameter.get("required"),
                            "name": parameter.get("name"),
                            "in": parameter.get("in"),
                            "parameter_type": parameter_type,
                        })
                if request_body := operation.get("requestBody"):
                    for content_type, schema in request_body.get("content").items():
                        request_body_list.append({
                            "operation_id": operation_id,
                            "content_type": content_type,
                            "schema_ref": schema.get("schema")
                        })
                method_definition_data.append({
                    "operation_id": operation_id,
                    "path": path,
                    "method": method.upper(),
                    "summary": operation.get("summary", ""),
                    "security": security
                })
                self.openapi_request[operation_id] = {
                    "parameters": parameter_list,
                    "request_body": request_body_list
                }
                self.openapi_response[operation_id] = {
                    "response_type": response_content_type,
                    "response_schema": response_content_schema
                }
        self.openapi_parts.method_definitions = OpenApiMethodDefinitionList([OpenApiMethodDefinition(**d) for d in method_definition_data])

    def _parse_components(self):
        openapi_data = self.openapi_json

        security_data = []

        for path, path_item in openapi_data.get('components', {}).get("securitySchemes", {}).items():
            security_data.append({
                "security_name": path,
                "security_type": path_item.get("type")
            })

        self.openapi_parts.security_definitions = OpenApiSecurityDefinitionList([OpenApiSecurityDefinition(**d) for d in security_data])
