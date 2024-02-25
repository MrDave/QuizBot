import re


def assemble_questionnaire(text: str):

    questions = re.findall(r"Вопрос \d+:\s(.*?)\sОтвет", text, re.DOTALL)
    answers = re.findall(r"Ответ:\s(.*?)\.\s\s", text)

    questionnaire = list(zip(questions, answers))

    return questionnaire


def main():
    with open("quiz_questions/plehan17.txt", encoding="KOI8-R") as f:
        whole_text = f.read()

    questionnaire = assemble_questionnaire(whole_text)
    print(questionnaire)


if __name__ == '__main__':
    main()
