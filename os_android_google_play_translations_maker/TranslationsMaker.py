import os_translator.translator as translator
import os_tools.file_handler as fh
import json
import os_android_google_play_translations_maker.modules.translations_maker_boilerplate as bp
import os_android_google_play_translations_maker.modules.props_bank as props_bank

##############################################################################
# this module aim is to translate a string to a desired languages and save
# the output in a json file, suitable for uploaded directly to the Google Play
##############################################################################

GOOGLE_PLAY_LANGUAGES_INITIALS = ['af', 'am', 'ar', 'hy-AM', 'az-AZ', 'bn-BD', 'eu-ES', 'be', 'bg', 'my-MM', 'ca', 'zh-HK', 'zh-CN', 'zh-TW', 'hr', 'cs-CZ', 'da-DK', 'nl-NL', 'et', 'fil', 'fi-FI', 'fr-FR', 'fr-CA', 'gl-ES', 'ka-GE', 'de-DE', 'el-GR', 'hi-IN', 'hu-HU', 'is-IS', 'id', 'it-IT', 'ja-JP', 'kn-IN', 'km-KH', 'ko-KR', 'ky-KG', 'lo-LA', 'lv', 'lt', 'mk-MK', 'ms', 'ml-IN', 'mr-IN', 'mn-MN', 'ne-NP', 'no-NO', 'fa', 'pl-PL', 'pt-BR', 'pt-PT', 'ro', 'ru-RU', 'sr', 'si-LK', 'sk', 'sl',
                                  'es-419', 'es-ES', 'es-US', 'en-US', 'sw', 'sv-SE', 'ta-IN', 'te-IN', 'th', 'tr-TR', 'uk', 'vi', 'zu']


class TranslationMaker:

    def __init__(self,
                 service_account_json_path,
                 project_id):
        self.languages_translations_list = []
        self.service_account_json_path = service_account_json_path
        self.project_id = project_id

    def translate_to_json(self,
                          app_title_src,
                          app_short_description_src,
                          app_full_description_src,
                          output_json_path,
                          if_translation_too_long_callback=None,
                          on_translation_made_successfully_callback=None,
                          app_keywords=None,
                          dest_languages_initials_list=GOOGLE_PLAY_LANGUAGES_INITIALS,
                          language_initials_src='en-US'
                          ):
        """Will translate a text to a given languages and save the results in a nice excel file.

       Parameters:
       :param app_title_src: the desired name for the app in the Google Play, in the source language
       :param app_short_description_src: the desired short description for the app in the Google Play, in the source language
       :param app_full_description_src: the desired full description for the app in the Google Play, in the source language
       :param output_json_path: the output path for the json file
       :param if_translation_too_long_callback: add a callback if you wan't to get notified about each translation made
       :param on_translation_made_successfully_callback: add a callback to specifically handle any length problem of the translated text
       :param app_keywords: these added keywords will be added to the description end
       :param dest_languages_initials_list: the initials of the languages you want to translate to
       :param language_initials_src: the initials of the sources language (usually 'en-US')

       NOTICE:
           If there are substrings you don't want to translate, write KEEP before them. Example: "The boy looks KEEPWord".
       """

        # set source language props
        app_title_src_translated = app_title_src
        app_short_description_src_translated = app_short_description_src
        app_full_description_src_translated = app_full_description_src
        if on_translation_made_successfully_callback is not None:
            app_title_src_translated = on_translation_made_successfully_callback(props_bank.PROP_TITLE, app_title_src, app_title_src, language_initials_src)
            app_short_description_src_translated = on_translation_made_successfully_callback(props_bank.PROP_SHORT_DESCRIPTION, app_short_description_src, app_short_description_src, language_initials_src)
            app_full_description_src_translated = on_translation_made_successfully_callback(props_bank.PROP_FULL_DESCRIPTION, app_full_description_src, app_full_description_src, language_initials_src)

        # check if src language props are legal
        bp.check_source_language_props(app_title_src, app_short_description_src, app_full_description_src)

        # clear languages array
        self.languages_translations_list.clear()

        # remove the src language from the list of languages if exists
        if language_initials_src in dest_languages_initials_list:
            dest_languages_initials_list.remove(language_initials_src)

        # append keywords to description
        if app_keywords is not None:
            app_full_description_src += f'\n{app_keywords}'

        # add src language
        bp.append_lang_to_list(self.languages_translations_list,
                               language_initials_src,
                               app_title_src_translated,
                               app_short_description_src_translated,
                               app_full_description_src_translated)

        # run on all of the languages and translate them all
        for lang_dst in dest_languages_initials_list:
            translated_title = bp.build_legal_translation(self.service_account_json_path, self.project_id, lang_dst, props_bank.PROP_TITLE, if_translation_too_long_callback, on_translation_made_successfully_callback, app_title_src, props_bank.MAX_TITLE_LENGTH)
            translated_short_description = bp.build_legal_translation(self.service_account_json_path, self.project_id, lang_dst, props_bank.PROP_SHORT_DESCRIPTION, if_translation_too_long_callback, on_translation_made_successfully_callback, app_short_description_src, props_bank.MAX_SHORT_DESCRIPTION_LENGTH)
            translated_full_description = bp.build_legal_translation(self.service_account_json_path, self.project_id, lang_dst, props_bank.PROP_FULL_DESCRIPTION, if_translation_too_long_callback, on_translation_made_successfully_callback, app_full_description_src, props_bank.MAX_FULL_DESCRIPTION_LENGTH)

            # append the translated language props to the list of languages
            bp.append_lang_to_list(self.languages_translations_list, lang_dst, translated_title, translated_short_description, translated_full_description)

        # save the output into a json file
        print("done. saving json...")
        output_dict = {"languages": self.languages_translations_list,
                       "updated": False
                       }
        output_json = json.dumps(output_dict, ensure_ascii=False)
        fh.create_file(output_json_path, output_json)
