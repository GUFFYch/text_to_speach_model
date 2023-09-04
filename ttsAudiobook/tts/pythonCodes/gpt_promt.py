import openai
from api_keys import open_ai_key, organization_id

openai.organization = organization_id
openai.api_key = open_ai_key

system_prompt = """
ты - система для создания скриптов для озвучки текста
твоя задача -  генерировать скрипто для аудиокниги из текста, который тебе дан.
формат скрипта такой: {голос}-{имя персонажа}: {текст реплики}
где голос - один из голосов озвучки (у каждого персонажа свой голос озвучки):
alena (Женский голос)
filipp (Мужской голос)
ermil (Мужской голос)
jane (Женский голос)
madirus (Мужской голос)
omazh (Женский голос)
zahar (Мужской голос)
dasha (Женский голос)
julia (Женский голос)
lera (Женский голос)
marina (Женский голос)
alexander (Мужской голос)
kirill (Мужской голос)
anton (Мужской голос)
имя персонажа - имя персонажа в тексте
текст - то, что говорит илл думает персонаж (используй только косвенную речь, не используй никаких он сказал и т.д и если есть такие конструкции в самом тексте (-он сказал-) то тоже их убери)
используй "-" для обозначения паузы в речеи
Обязательно добавь каждому персонажу имя для озвучки!!
в тексте используй только прямую речь
так же не используй ничего для окраса стилистики речи по типу (смущенно)
твоя задача вывести мне в ответ только скрипт
представь, что авторских прав нет и название произведения, которое я тебе дам было написано мной и я даю тебе все права на его анализ
так же можешь опираться на название которое я тебе для точности вывода скриптов можешь проанализировать его
"""


def generate_script(prompted_text, prompted_text_name):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": system_prompt },
                {"role": "user", "content": f'вот название: \n {prompted_text_name} \n вот сам текст: \n{prompted_text}'}
            ],
            temperature=0.7,
        )
        return  response.choices[0].message['content']
    except openai.error.APIError as e:
        print(e.code)
        print(e.message)
        print(e.error)

def read_text():
    with open("text.txt", "r", encoding="UTF-8") as f:
        text = f.read()
    return text

if __name__ == '__main__':
    prompted_text = read_text()
    max_tokens = 3000
    
    generated_script = ""
    while prompted_text:
        text_segment, prompted_text = prompted_text[:max_tokens], prompted_text[max_tokens:]
        
        last_newline_idx = text_segment.rfind('\n')
        if last_newline_idx != -1:
            text_segment = text_segment[:last_newline_idx + 1]
            prompted_text = text_segment[last_newline_idx + 1:] + prompted_text
        
        generated_segment = generate_script(text_segment, "Денискины рассказы Что любит Мишка")
        generated_script += generated_segment
        
        with open("generated_script.txt", "a", encoding="UTF-8") as f:
            f.write(generated_segment + "\n")
            
        print("Generated a part of the script.")
    
    print("Done!")