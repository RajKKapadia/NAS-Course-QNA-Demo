# import json
# from random import choices

# difficulty_level = 5

# with open('qna_chatbot/data/qna.json', 'r') as file:
#     qna_data = json.loads(file.read())

# random_qna = choices(list(qna_data[str(difficulty_level)].values()), k=5)
# print(random_qna)

from qna_chatbot.utils.helper_functions import get_random_qna

random_qna = get_random_qna('3')
print(random_qna)