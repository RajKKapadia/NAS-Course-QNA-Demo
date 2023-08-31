import json
from random import choices

from config import config

def format_dialogflow_response(messages: list[str], output_contexts: list[dict] = []) -> dict:
    response_data = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": messages
                }
            }
        ]
    }
    if len(output_contexts) > 0:
        response_data['outputContexts'] = output_contexts
    return response_data

def get_random_qna(difficulty_level: str) -> list[dict]:
    with open(config.QNA_FILE_PATH, 'r') as file:
        qna_data = json.loads(file.read())
    random_qna = choices(list(qna_data[str(difficulty_level)].values()), k=5)
    return random_qna

def get_context_parameters(body: dict) -> dict:
    output_contexts = body['queryResult']['outputContexts']
    parameters = {}
    for oc in output_contexts:
        name = oc['name']
        if 'session-vars' in name:
            parameters = oc['parameters']
    return parameters
