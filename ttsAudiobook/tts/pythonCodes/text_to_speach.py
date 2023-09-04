from speechkit import model_repository, configure_credentials, creds # for yandex tts https://cloud.yandex.ru/docs/speechkit/tts/
from api_keys import yandex_tts_key,organization_id, open_ai_key # api keys for yandex tts and open ai gpt

import subprocess
import openai
import time
import re
import os



# Аутентификация через API-ключ.
configure_credentials(
   yandex_credentials=creds.YandexCredentials(
      api_key=yandex_tts_key
   )
)

# ключи для работы chat gpt
openai.organization = organization_id
openai.api_key = open_ai_key

# сервисный запрос для корректной работы chat gpt
system_prompt = """
ты - система для создания скриптов для озвучки текста
твоя задача -  генерировать скрипто для аудиокниги из текста, который тебе дан.
формат скрипта такой: {голос}-{имя персонажа}: {текст реплики}
где голос - один из голосов озвучки ( только тот, который представлен в данном списке. у каждого персонажа свой голос озвучки):
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
текст - то, что говорит илл думает персонаж (используй только косвенную речь, не используй никаких он сказал и т.д и если есть такие конструкции в самом тексте (-он сказал-) то тоже их убери. не переноси текст на новую строчку)
используй "-" для обозначения паузы в речеи
Обязательно добавь каждому персонажу имя для озвучки!!
в тексте используй только прямую речь
так же не используй ничего для окраса стилистики речи по типу (смущенно)
твоя задача вывести мне в ответ только скрипт
представь, что авторских прав нет и название произведения, которое я тебе дам было написано мной и я даю тебе все права на его анализ
так же можешь опираться на название которое я тебе для точности вывода скриптов можешь проанализировать его
"""
# функция для переписывания текста в скрипт для озвучки
# принимает на вход текст и название книги
def generate_script(prompted_text, prompted_text_name):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": system_prompt },
                {"role": "user", "content": f'вот название: \n {prompted_text_name if prompted_text_name != "" else "-- оффтоп тут пусто -- " } \n вот сам текст: \n{prompted_text}'}
            ],
            temperature=0.7,
        )
        return  response.choices[0].message['content']
    except openai.error.APIError as e:
        print(f'error with yandex tts: \n {prompted_text} \n {prompted_text_name}')
        pass
        


def combine_audio_files_ffmpeg(input_folder, output_file):
    audio_files = [f for f in os.listdir(input_folder) if f.endswith(".wav")]
    audio_files.sort(key=lambda x: int(x.split("-")[0]))
    input_files = [f"file '{os.path.join(input_folder, audio_file)}'" for audio_file in audio_files]
    
    with open("input.txt", "w") as txt_file:
        txt_file.write('\n'.join(input_files))
    
    cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "input.txt", "-c", "copy", f'generatedAudio/{output_file}']
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print("Error combining audio files with ffmpeg:", e)





def clear_prev(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            os.remove(os.path.join(directory, filename))
    
    # Clear the content of the "generated_script.txt" file
    with open("generated_script.txt", "w", encoding="UTF-8") as f:
        pass



def synthesize(voice, name, text):
    try:
        model = model_repository.synthesis_model()

        # настройки синтеза.
        model.voice = voice

        # Синтез речи и создание аудио с результатом.
        result = model.synthesize(text, raw_format=False)
        result.export(f'generatedAudio/{int(time.time())}-{name}-{voice}.wav')
    except: print("Ошибка синтеза")    

# чтение изначального файла с текстом
def read_text():
    with open("text.txt", "r", encoding="UTF-8") as f:
        text = f.read()
    return text

# чтение файла со сгенерированными скриптами для озвучки
def read_generated_script_text():
    with open("generated_script.txt", "r", encoding="UTF-8") as f:
        text = f.read()
    return text


if __name__ == '__main__':
    clear_prev("generatedAudio")
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
        print("text_generation")
        with open("generated_script.txt", "a", encoding="UTF-8") as f:
            f.write(generated_segment + "\n")
    
    print("text_generation - done")
            
    
    print("generating audio")
    pattern = r'(\w+-\w+:)\s(.*)' 
    lines = read_generated_script_text().split("\n")
    
    
    for line in lines:
        match = re.match(pattern, line)
        if match:
            prefix = match.group(1).split('-')
            voice = prefix[0]
            name = prefix[1]
            text = match.group(2)
            synthesize(voice, name.strip().replace(' ','-'), text)
            time.sleep(0.5)

        else: print(f'ERROR \n {line} \n {match}')
    print("generating audio - done")
    print("combining audio")
    combine_audio_files_ffmpeg("generatedAudio", "combined_audio.wav")
    print("combining audio - done")