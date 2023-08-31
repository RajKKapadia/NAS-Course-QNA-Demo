from flask import Blueprint, jsonify, request

from qna_chatbot.utils.helper_functions import format_dialogflow_response
from qna_chatbot.utils.action_handler import user_provide_difficulty_level, default_welcome_intent, user_provides_answer

dialogflow = Blueprint(
    'dialogflow',
    __name__
)


@dialogflow.route('/webhook', methods=['POST'])
def handle_webhook():
    body = request.get_json()
    '''TODO
    [x] get the action name
    [ ] separate the request based on action name and generate response
    '''
    action = body['queryResult']['action']
    print(action)
    if action == 'userProvidesDifficultyLevel':
        response_data = user_provide_difficulty_level(body)
    elif action == 'defaultWelcomeIntent':
        response_data = default_welcome_intent(body)
    elif action == 'userProvidesAnswer':
        response_data = user_provides_answer(body)
    else:
        response_data = format_dialogflow_response(
            [
                f'No handler for the action {action}.'
            ]
        )
    return jsonify(response_data)
