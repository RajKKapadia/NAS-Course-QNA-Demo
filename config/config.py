import os

cwd = os.getcwd()

QNA_FILE_PATH = os.path.join(
    cwd,
    'data',
    'qna.json'
)

NUMB_QUE_TO_ASK = 5
DIFFICULTY_LEVELS = [1, 2, 3, 4, 5]
