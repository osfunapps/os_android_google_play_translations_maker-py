import os_translator.translator as translator
import os_android_google_play_translations_maker.modules.props_bank as props_bank


##############################################################################
# just a boiler plate code file for the json's translations maker
##############################################################################

# will check if the initial properties are legal
def check_source_language_props(app_title_src,
                                app_short_description_src,
                                app_full_description_src):
    if len(app_title_src) > props_bank.MAX_TITLE_LENGTH:
        raise_src_lang_length_error(props_bank.PROP_TITLE, props_bank.MAX_TITLE_LENGTH)
    elif len(app_short_description_src) > props_bank.MAX_SHORT_DESCRIPTION_LENGTH:
        raise_src_lang_length_error(props_bank.PROP_SHORT_DESCRIPTION, props_bank.MAX_SHORT_DESCRIPTION_LENGTH)
    elif len(app_full_description_src) > props_bank.MAX_FULL_DESCRIPTION_LENGTH:
        raise_src_lang_length_error(props_bank.PROP_FULL_DESCRIPTION, props_bank.MAX_FULL_DESCRIPTION_LENGTH)


# will be called if one of the source language properties is too long
def raise_src_lang_length_error(translation_type, max_chars):
    raise IndexError(f"Length error: your app's {translation_type} is too long! it should be max of {max_chars} chars")


# will build a legal translation to a specific type (title, short description etc...)
def build_legal_translation(service_account_json_path,
                            project_id,
                            language_initials_dest,
                            translation_type,
                            if_translation_too_long_function,
                            on_translation_made_function,
                            text_to_translate,
                            max_chars):
    print(f"translating {translation_type} to language '{language_initials_dest}'")
    translated_text = translator.translate_text(service_account_json_path,
                                                project_id,
                                                text_to_translate,
                                                language_initials_dest)

    # notify about translation made if needed
    if on_translation_made_function is not None:
        translated_text = on_translation_made_function(translation_type, text_to_translate, translated_text, language_initials_dest)

    # notify length of translated text is too long
    if len(translated_text) > max_chars:
        warning_msg = print_error_with_src(language_initials_dest, translation_type, props_bank.MAX_TITLE_LENGTH)
        if if_translation_too_long_function is None:
            raise TypeError(f"{warning_msg} but couldn't find one!")
        text_to_translate = if_translation_too_long_function(translation_type, text_to_translate, language_initials_dest)
        if text_to_translate is None or text_to_translate == "":
            raise TypeError(f"The new {translation_type} is empty!")

        translated_text = translator.translate_text(service_account_json_path,
                                                    project_id,
                                                    text_to_translate,
                                                    language_initials_dest)
        # notify about translation made if needed
        if on_translation_made_function is not None:
            translated_text = on_translation_made_function(translation_type, text_to_translate, translated_text, language_initials_dest)

        if len(translated_text) > max_chars:
            raise IndexError(f"Length error: the translation of the {translation_type} for language '{language_initials_dest}' is still bigger than {max_chars} chars,  even after using your backup function!")
    return translated_text


# will add the translated language to the list of languages
def append_lang_to_list(languages_translations_list, lang_dst, translated_title, translated_short_description, translated_full_description):
    languages_translations_list.append({props_bank.JSON_KEY_LANGUAGE: lang_dst,
                                        props_bank.JSON_KEY_TITLE: translated_title,
                                        props_bank.JSON_KEY_SHORT_DESCRIPTION: translated_short_description,
                                        props_bank.JSON_KEY_FULL_DESCRIPTION: translated_full_description
                                        })


# will print an error if there is a problem with one of the props in the source language
def print_error_with_src(language_initials, translation_type, max_chars):
    warning_msg = f"language '{language_initials}' {translation_type} translation is bigger then {max_chars} chars. Trying to translate with your if_translation_too_long_function function..."
    print(warning_msg)
    return warning_msg
