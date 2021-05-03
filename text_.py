import emoji

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


