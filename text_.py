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
    type_attraction = attractions[lang][nearest_attraction_id][1]
    name_attraction = attractions[lang][nearest_attraction_id][0]
    info_about_attraction = get_info(lang, nearest_attraction_id)
    if lang == 'rus':
        return_text = f'{emoji.ROUND_PUSHPIN}Ближайшее к вам место: {type_attraction} {name_attraction}\n\n' \
                      f'{emoji.GLOBE_WITH_MERIDIANS}Вот, что мы нашли о нем в Интернете:\n\n' \
                      f'{info_about_attraction}\n\n' \
                      f'{emoji.CHECK_MARK_BUTTON}Место добавлено в ваш список'
        return return_text
    elif lang == 'eng':
        return_text = f"{emoji.ROUND_PUSHPIN}Nearest place to you: {type_attraction} {name_attraction}\n\n" \
                      f"{emoji.GLOBE_WITH_MERIDIANS}Here's what we found about him on the Internet:\n\n" \
                      f"{info_about_attraction}\n\n" \
                      f"{emoji.CHECK_MARK_BUTTON}Also, the place is added to your list"
        return return_text

def get_attractions_list(uid, lang):
    attractions_list = db.get_attractions(uid)[0].split()
    if lang == 'rus':
        return_text = f'{emoji.MEMO}Список ваших мест{emoji.BACKHAND_INDEX_POINTING_DOWN_LIGHT_SKIN_TONE}\n\n'
    elif lang == 'eng':
        return_text = f"{emoji.MEMO}List of your places{emoji.BACKHAND_INDEX_POINTING_DOWN_LIGHT_SKIN_TONE}\n\n"
    counter = 0
    if len(attractions_list) != 0:
        for attraction_id in attractions_list:
            attraction_id_int = int(attraction_id)
            return_text += f'{emoji.WHITE_SMALL_SQUARE}{attractions[lang][attraction_id_int][1]} ' \
                           f'{attractions[lang][attraction_id_int][0]}\n'
            counter += 1
    else:
        if lang == 'rus':
            return_text += f'{emoji.MAN_SHRUGGING_LIGHT_SKIN_TONE}Пусто.\n'
        elif lang == 'eng':
            return_text += f"{emoji.MAN_SHRUGGING_LIGHT_SKIN_TONE}Empty.\n"
    if lang == 'rus':
        return_text += f'\n{emoji.ABACUS}Всего: {counter}\n' \
                       f'\n{emoji.MAN_BOWING_LIGHT_SKIN_TONE}Некоторые места находятся слишком близко друг к другу, ' \
                       f'поэтому на вашей карте они могут быть обозначены одним пином'
    elif lang == 'eng':
        return_text += f"\n{emoji.ABACUS}In total: {counter}\n" \
                       f"\n{emoji.MAN_BOWING_LIGHT_SKIN_TONE}Some places are too close to each other, so they can be " \
                       f"marked with a single pin on your map"
    return return_text