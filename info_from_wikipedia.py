import wikipedia
import db
from attractions import attractions

def get_info(uid, nearest_attraction_id):
    lang = db.get_language(uid)[0]
    lang = 'ru' if lang == 'rus' else 'en'
    wikipedia.set_lang('lang')
