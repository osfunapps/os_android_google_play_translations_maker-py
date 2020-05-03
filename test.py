from os_android_google_play_translations_maker.TranslationsMaker import TranslationMaker

tm = TranslationMaker(service_account_json_path="/path/to/your/project-firebase_service_account.json",
                      project_id="my_project_id-7c220")


# a callback to return a new string to translate, if one of the properties is too long
def translation_too_long_callback(translation_type, text_to_translate, language_initials_dest):
    print(f'oops! too long translation for the language {language_initials_dest}')
    if translation_type == 'title':
        return 'new app title'
    elif translation_type == 'short description':
        return 'new app short description to translate'
    elif translation_type == 'full description':
        return 'new app full description to translate'


# just a callback to when the translation has been made successfully for a given type (title, short summary or full summary).
# you can add any text here, that you don't want to translate
def on_translation_made_callback(translation_type, text_to_translate, translated_text, language_initials_dest):
    print(f'just a callback here! translation made successfully for {translation_type}')
    if translation_type == 'title':
        return f'{translated_text} no translate str'

    return translated_text


# the call to make the json
tm.translate_to_json(app_title_src="My App Name",
                     app_short_description_src="This is the short description",
                     app_full_description_src="This is the app full description",
                     output_json_path='/Users/home/Desktop/stock_exchange/3.5/done/json.json',
                     if_translation_too_long_callback=translation_too_long_callback,
                     on_translation_made_successfully_callback=on_translation_made_callback,
                     app_keywords="one two three four keywords",
                     dest_languages_initials_list=['af', 'am', 'ar', 'hy-AM'])
