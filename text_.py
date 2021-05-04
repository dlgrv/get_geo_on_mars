import emoji
import db
from info_from_wikipedia import get_info
from attractions import attractions

def first_start():
    return_text = f'{emoji.FLAG_RUSSIA}Выберите язык{emoji.ALIEN}\n\n'\
                  f'{emoji.FLAG_UNITED_STATES}Select language{emoji.ALIEN}'
    return return_text


def repeat_start():
    return_text = f'{emoji.FLAG_RUSSIA}Уже всё давно настроено.\n' \
                  f'Может быть ты захотел поменять язык?\n\n'\
                  f'{emoji.FLAG_UNITED_STATES}Everything works.\n'\
                  f'Maybe you wanted to change the language?'
    return return_text


def instruction(lang):
    if lang == 'rus':
        return_text = 'Круто!\n'\
                      'Теперь стоит объяснить что к чему.\n'\
                      'Ты кидаешь мне свою геопозицию, а я отправляю тебя в эту точку на Марсе!\n'\
                      'А еще расскажу какая Марсианская достопримечательность находится ближе всего к тебе и добавлю ее в твой личный список!'
        return return_text
    elif lang == 'eng':
        return_text = "Cool!\n"\
                      "Now it's worth explaining what's what.\n"\
                      "You throw me your geoposition, and I send you to this point on Mars!"\
                      "I'll also tell you which Martian attraction is closest to you and add it to your personal list!"
        return return_text

def info_about(lang, nearest_attraction_id):
    if lang == 'rus':
        type_attraction = attractions[lang][nearest_attraction_id][1]
        name_attraction = attractions[lang][nearest_attraction_id][0]
        info_about_attraction = get_info(lang, nearest_attraction_id)
        return_text = f'{emoji.ROUND_PUSHPIN}Ближайшее к вам место: {type_attraction} {name_attraction}\n\n' \
                      f'{emoji.SPIDER_WEB}Вот, что мы нашли о нем в Интернете:\n\n' \
                      f'{info_about_attraction}\n\n' \
                      f'{emoji.CHECK_MARK_BUTTON}Также, место добавлено в ваш список'
        return return_text
    elif lang == 'eng':
        type_attraction = attractions[lang][nearest_attraction_id][1]
        name_attraction = attractions[lang][nearest_attraction_id][0]
        info_about_attraction = get_info(lang, nearest_attraction_id)
        return_text = f"{emoji.ROUND_PUSHPIN}Nearest place to you: {type_attraction} {name_attraction}\n\n" \
                      f"{emoji.SPIDER_WEB}Here's what we found about him on the Internet:\n\n" \
                      f"{info_about_attraction}\n\n" \
                      f"{emoji.CHECK_MARK_BUTTON}Also, the place is added to your list"
        return return_text