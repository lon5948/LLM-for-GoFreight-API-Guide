# LLM-for-GoFreight-API-Guide

LLM-for-GoFreight-API-Guide is an innovative tool designed to simplify the way developers interact with API documentation. It harnesses the power of OpenAI's GPT-3.5 language model to provide users with intuitive guidance on using their APIs effectively. By feeding the `openapi.json` file into this tool, developers can obtain clear instructions on how to execute API calls, understand the functionality of various endpoints, and troubleshoot common issues.

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.11 or higher installed on your system.
- an `openapi.json` file you wish to analyze.
- An API key from OpenAI.

## Installation

Ensure you have Poetry installed on your system. If you do not have Poetry installed, you can install it by following the instructions at the [Poetry documentation](https://python-poetry.org/docs/).

With Poetry installed, you can set up your project environment and install all required dependencies by running:

```bash
poetry install
```

## Run

To run the LLM-for-GoFreight-API-Guide tool, you need to configure it with your OpenAI API key, the path to your openapi.json file, and your API's base URL.

Run the tool using the following command:

```bash
python api_selector.py --openai-key <your-openai-key> --openapi-json <openapi-json-path> --base-url <your-base-url>
```

## How It Works

The LLM-for-GoFreight-API-Guide consists of several components that work together to provide an interactive experience for analyzing and understanding API documentation. Here's a breakdown of each file and its role:

#### OpenAPI Parser(`openapi_parser.py`)
The OpenAPI Parser is a bespoke component that ingests your `openapi.json` specification. Its primary function is to parse and extract essential details such as endpoints, parameters, and schema definitions, converting them into a structured format that the GPT-3.5 language model can process and interpret.

#### Entry Point Script (`api_selector.py`)
The `api_selector.py` file serves as the entry point for the tool. It accepts command-line arguments to initialize the application with user-provided details, including the OpenAI key, the path to the `openapi.json` file, and the API's base URL.

#### API Selection Manager (`main.py`)
The `main.py` file contains the `ApiSelector` class, which is responsible for API selection based on the given `openapi.json` file. It also oversees the initiation of the agent that handles the interaction between the user and the tool.

#### User Query Processor (`engine.py`)
Within `engine.py`, the `ProcessingEngine` class is defined. This class is tasked with the processing of user queries. It formulates the requests to the language model and interprets the responses to provide answers.

#### Chat Interface Handler (`chat.py`)
The `chat.py` file manages the chat interface. It is in charge of storing the conversation history and sending requests to the OpenAI API. 

#### Component Orchestrator (`agent.py`)
`agent.py` acts as the orchestrator for all the separate components. It is responsible for loading the system and user prompts and starting the chat and processing engines.

