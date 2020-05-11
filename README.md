Introduction
------------

This script will translate an app name, short description and full description and create a json file suitable to upload to Google Play as a new/updated translation for an apk.

Notice: you would need a service account key from your firebase project to translate the texts.

## Installation
Install via pip:

    pip install os-android-google-play-translations-maker

## Usage       

    from os_android_google_play_translations_maker.TranslationsMaker import TranslationMaker
    
    # set the path to your firebase service account key (needed for the translation process)
    tm = TranslationMaker(service_account_json_path="/path/to/your/project-firebase_service_account.json",
                          project_id="my_project_id-7c220")
    
    # the call to make the json
    tm.translate_to_json(app_title_src="My App Name",
                         app_short_description_src="This is the short description",
                         app_full_description_src="This is the app full description",
                         output_json_path='/path/to/com.osapps.myApp.json',
                         if_translation_too_long_callback=translation_too_long_callback,
                         on_translation_made_successfully_callback=on_translation_made_callback,
                         app_keywords="one two three four keywords",
                         dest_languages_initials_list=['af', 'am', 'ar', 'hy-AM'])


## Optional callbacks

    
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
    
# output

    {
      "languages": [
        {
          "lang": "en-US",
          "title": "My App Name no translate str",
          "shortDescription": "This is the short description",
          "fullDescription": "This is the app full description",
          "updated": false
        },
        {
          "lang": "af",
          "title": "My programnaam no translate str",
          "shortDescription": "Dit is die kort beskrywing",
          "fullDescription": "Dit is die volledige beskrywing van die app\neen twee drie vier sleutelwoorde",
          "updated": false
        },
        {
          "lang": "am",
          "title": "የእኔ መተግበሪያ ስም no translate str",
          "shortDescription": "ይህ አጭር መግለጫው ነው",
          "fullDescription": "ይህ የመተግበሪያው ሙሉ መግለጫ ነው\nአንድ ሁለት ሶስት አራት ቁልፍ ቃላት",
          "updated": false
        },
        {
          "lang": "ar",
          "title": "اسم التطبيق الخاص بي no translate str",
          "shortDescription": "هذا هو الوصف المختصر",
          "fullDescription": "هذا هو الوصف الكامل للتطبيق\nواحدة أو ثلاث أو أربع كلمات رئيسية",
          "updated": false
        },
        {
          "lang": "hy-AM",
          "title": "Իմ ծրագրի անունը no translate str",
          "shortDescription": "Սա կարճ նկարագրությունն է",
          "fullDescription": "Սա հավելվածի ամբողջական նկարագրությունն է\nմեկ երկու երեք չորս հիմնաբառ",
          "updated": false
        }
      ],
      
      "updated": false
    }
## Function Signature
    def translate_to_json(self,
                          app_title_src,
                          app_short_description_src,
                          app_full_description_src,
                          output_json_path,
                          if_translation_too_long_callback=None,
                          on_translation_made_successfully_callback=None,
                          app_keywords=None,
                          dest_languages_initials_list=GOOGLE_PLAY_LANGUAGES_INITIALS,
                          language_initials_src='en-US',
                          )
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


## Licence
MIT