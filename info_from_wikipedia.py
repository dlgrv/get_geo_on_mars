import wikipedia
import db
from attractions import attractions
import emoji

def get_info(lang, nearest_attraction_id):
    wiki_lang = 'ru' if lang == 'rus' else 'en'
    wikipedia.set_lang(wiki_lang)
    attraction_name = attractions[lang][nearest_attraction_id][0]
    attraction_type = attractions[lang][nearest_attraction_id][1]
    return_info = None
    try:
        return_info = emoji.MAN_TIPPING_HAND_LIGHT_SKIN_TONE + wikipedia.summary(f'{attraction_type} {attraction_name}')
    except Exception as e1:
        try:
            return_info = emoji.MAN_TIPPING_HAND_LIGHT_SKIN_TONE + wikipedia.summary(
                f'{attraction_type}_{attraction_name}')
        except Exception as e2:
            try:
                return_info = emoji.MAN_TIPPING_HAND_LIGHT_SKIN_TONE + wikipedia.summary(
                    f'{attraction_name} {attraction_type}')
            except Exception as e3:
                try:
                    return_info = emoji.MAN_TIPPING_HAND_LIGHT_SKIN_TONE + wikipedia.summary(
                        f'{attraction_name}_{attraction_type}')
                except Exception as e4:
                    if lang == 'rus':
                        return_info = f'{emoji.MAN_SHRUGGING_LIGHT_SKIN_TONE}Информация не найдена'
                    elif lang == 'eng':
                        return_info = f'{emoji.MAN_SHRUGGING_LIGHT_SKIN_TONE}Information not found'
    return return_info