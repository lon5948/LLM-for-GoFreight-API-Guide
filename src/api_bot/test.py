openapi_data = {
    "paths": {
    "/api/v1/offices": {
      "get": {
        "operationId": "GetOffices",
        "summary": "Get Offices",
        "security": [
          {
            "apiKeyAuth": []
          }
        ],
        "tags": [
          "Office"
        ],
        "parameters": [],
        "responses": {
          "200": {
            "description": "Successful response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "required": [
                    "meta",
                    "data"
                  ],
                  "properties": {
                    "meta": {
                      "nullable": False,
                      "type": "object",
                      "required": [
                        "total"
                      ],
                      "properties": {
                        "total": {
                          "type": "integer",
                          "nullable": False,
                          "description": "The total number of offices"
                        }
                      }
                    },
                    "data": {
                      "type": "array",
                      "nullable": False,
                      "items": {
                        "type": "object",
                        "required": [
                          "ref",
                          "short_name",
                          "full_name",
                          "local_name",
                          "description",
                          "is_active",
                          "country_code",
                          "state_code",
                          "city_name",
                          "zip_code",
                          "address",
                          "local_address",
                          "phone",
                          "fax",
                          "email",
                          "direct_line",
                          "url"
                        ],
                        "properties": {
                          "ref": {
                            "type": "string",
                            "nullable": False,
                            "description": "The ref. of the office"
                          },
                          "short_name": {
                            "type": "string",
                            "nullable": False,
                            "description": "The short name of the office"
                          },
                          "full_name": {
                            "type": "string",
                            "nullable": False,
                            "description": "The full name of the office"
                          },
                          "local_name": {
                            "type": "string",
                            "nullable": True,
                            "description": "The local name of the office"
                          },
                          "description": {
                            "type": "string",
                            "nullable": True,
                            "description": "The description of the office"
                          },
                          "is_active": {
                            "type": "boolean",
                            "nullable": False,
                            "description": "The flag that indicates if the office is active"
                          },
                          "country_code": {
                            "type": "string",
                            "nullable": True,
                            "description": "The country code of the office"
                          },
                          "state_code": {
                            "type": "string",
                            "nullable": True,
                            "description": "The state code of the office"
                          },
                          "city_name": {
                            "type": "string",
                            "nullable": True,
                            "description": "The city name of the office"
                          },
                          "zip_code": {
                            "type": "string",
                            "nullable": True,
                            "description": "The zip code of the office"
                          },
                          "address": {
                            "type": "string",
                            "nullable": True,
                            "description": "The address of the office"
                          },
                          "local_address": {
                            "type": "string",
                            "nullable": True,
                            "description": "The local address of the office"
                          },
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "400": {
            "$ref": "#/components/responses/BadRequest"
          },
          "401": {
            "$ref": "#/components/responses/UnauthorizedError"
          }
        }
      }
    },
    }
}

schema_prefix = "#/components/schemas/"

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
            response_content_type, response_content_content = list(success_response.get("content").items())[0]
            response_content_schema = response_content_content.get("schema")
            print(response_content_schema)
        else:
            response_content_type = None
            response_content_content = None
            response_content_schema = None