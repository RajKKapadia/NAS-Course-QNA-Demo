from qna_chatbot.utils.helper_functions import format_dialogflow_response, get_random_qna, get_context_parameters
from config import config


def user_provide_difficulty_level(body: dict) -> dict:
    '''TODO
    [x] get the difficulty level
    [x] generate 5 random questions
    [x] ask first question in the response
    '''
    session = body['session']
    parameters = get_context_parameters(body)
    difficulty_level = parameters['difficulty-level']
    if difficulty_level not in config.DIFFICULTY_LEVELS:
        output_contexts = [
            {
                'name': f'{session}/contexts/await-difficulty',
                'lifespanCount': 1
            }
        ]
        response_data = format_dialogflow_response(
            [
                f'Please choose difficulty level of the question between a number {min(config.DIFFICULTY_LEVELS)} to {max(config.DIFFICULTY_LEVELS)}.'
            ],
            output_contexts
        )
        return response_data
    random_qna = get_random_qna(str(int(difficulty_level)))
    output_contexts = [
        {
            'name': f'{session}/contexts/await-answer',
            'lifespanCount': 1
        },
        {
            'name': f'{session}/contexts/session-vars',
            'lifespanCount': 100,
            'parameters': {
                'counter': 0,
                'score': 0,
                'random_qna': random_qna
            }
        }
    ]
    response_data = format_dialogflow_response(
        [
            'Here is your first question.'
            f'{random_qna[0]["question"][0]}'
        ],
        output_contexts
    )
    return response_data


def default_welcome_intent(body: dict) -> dict:
    session = body['session']
    output_contexts = [
        {
            'name': f'{session}/contexts/await-difficulty',
            'lifespanCount': 1
        },
        {
            'name': f'{session}/contexts/session-vars',
            'lifespanCount': 100
        }
    ]
    response_data = format_dialogflow_response(
        [
            'Welcome to the Qizebot.',
            'Please select a difficulty level between a number 1 to 5.'
        ],
        output_contexts
    )
    return response_data


def user_provides_answer(body: dict) -> dict:
    '''TODO
    [x] get the answer
    [x] get the correct answer
    [x] calculate score
    [x] return the correctness and ask next question
    [X] set the context
    '''
    session = body['session']
    parameters = get_context_parameters(body)
    user_answer = parameters['answer']
    random_qna = parameters['random_qna']
    counter = int(parameters['counter'])
    score = int(parameters['score'])
    correct_answer = random_qna[counter]['prefferedAnswer'][0]
    '''Get the correct answer, calculate score, and increment the counter.
    For correct answer set the answer_flag
    '''
    answer_flag = False
    correct_answer = random_qna[counter]['prefferedAnswer'][0]
    if user_answer in random_qna[counter]['prefferedAnswer'] or user_answer in random_qna[counter]['alternateAnswers']:
        score += 1
        answer_flag = True
    counter += 1
    '''Check if the counter is greater than number of questions to ask.
        '''
    if counter > (config.NUMB_QUE_TO_ASK - 1):
        if answer_flag:
            output_contexts = [
                {
                    'name': f'{session}/contexts/await-difficulty',
                    'lifespanCount': 1
                }
            ]
            response_data = format_dialogflow_response(
                [
                    f'Great, that is a right answer. High five!.',
                    f'Your score is {score} out of {config.NUMB_QUE_TO_ASK}.',
                    f'To start the quiz again please choose difficulty level of the question between a number {min(config.DIFFICULTY_LEVELS)} to {max(config.DIFFICULTY_LEVELS)}.'
                ],
                output_contexts
            )
            return response_data
        # Answer is wrong
        output_contexts = [
            {
                'name': f'{session}/contexts/await-difficulty',
                'lifespanCount': 1
            }
        ]
        response_data = format_dialogflow_response(
            [
                f'Oops, that is a wrong answer.\nThe correct answer is {correct_answer}.',
                f'Your score is {score} out of {config.NUMB_QUE_TO_ASK}.',
                f'To start the quiz again please choose difficulty level of the question between a number {min(config.DIFFICULTY_LEVELS)} to {max(config.DIFFICULTY_LEVELS)}.'
            ],
            output_contexts
        )
        return response_data
    output_contexts = [
        {
            'name': f'{session}/contexts/await-answer',
            'lifespanCount': 1
        },
        {
            'name': f'{session}/contexts/session-vars',
            'lifespanCount': 20,
            'parameters': {
                'counter': counter,
                'score': score
            }
        }
    ]
    if answer_flag:
        response_data = format_dialogflow_response(
            [
                f'Great, that is a right answer. Here is your next question.',
                f'({counter + 1}) {random_qna[counter]["question"][0]}'
            ],
            output_contexts
        )
        return response_data
    response_data = format_dialogflow_response(
        [
            f'Oops, that is a wrong answer. The correct answe is {correct_answer}.',
            'Here is your next question.',
            f'({counter + 1}) {random_qna[counter]["question"][0]}'
        ],
        output_contexts
    )
    return response_data
