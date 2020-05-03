import os

import os_tools.tools as tools
import os_tools.file_handler as fh
import os_tools.xml_file_handler as xh
import ast


# countries_list = ['China', 'India', 'Brasil', 'Hong Kong', 'Germany', 'Austria', 'Spain', 'Israel', 'USA', 'Argentina', 'Russia', 'Saudi Arabia', 'Egypt', 'Hungary', 'Canada']

class App:

    def __init__(self, package_name, country, stock_exchanges):
        self.package_name = package_name
        self.country = country
        self.stock_exchanges = stock_exchanges


def parse_translation(app_dir):
    # fetch app name from the strings.xml file
    package_name = fh.get_dir_name(app_dir)

    # open dynamic_strings.xml
    dyn_strings_xml = xh.read_xml_file(os.path.join(app_dir, 'dynamic_strings.xml'))

    # take the google_play_app_name
    play_name_node = xh.get_nodes(dyn_strings_xml, 'string', 'name', 'google_play_app_name')[0]
    name_in_google_play = xh.get_text_from_node(play_name_node)

    # take the keywords
    keywords_node = xh.get_nodes(dyn_strings_xml, 'string', 'name', 'google_play_keywords')[0]
    keywords = xh.get_text_from_node(keywords_node)

    # take the country
    country_start_idx = package_name.find('oky.') + 4
    country_end_idx = package_name.find('_stock')
    country = package_name[country_start_idx: country_end_idx]
    country = country.replace('_', ' ').title()

    # get the stock exchanges
    dash_idx = name_in_google_play.find(' - ')
    str_to_translate = name_in_google_play
    str_to_add_later = None

    # if there is dash in the name, we would take the string before the dash and add it later (without translating it).
    # we would also remove this part from the google play's app name
    if dash_idx != -1:
        str_to_add_later = name_in_google_play[:dash_idx]
        str_to_translate = name_in_google_play[dash_idx + 3:]
        # str_to_add_later = str_to_add_later.replace(',', '')  # remove commas (',')
        # str_to_add_later = str_to_add_later.split(' ')

    # if len(stock_exchanges) > 4:
    #     app_dir.stock_exchanges = tools.ask_for_input(f'{stock_exchanges}\n'
    #                                                   f'too many stock exchanges. write the relevant ones from the above: ')
    #     stock_exchanges = ast.literal_eval(stock_exchanges)
    #     # parse_translation(app)
    #     # return
    #
    # build resources
    xlsx_file_path = os.path.join(app_dir, f'{package_name}.xlsx')

    print("**********************************************************************")
    print('package name: ' + package_name)
    print('country: ' + country)
    print('string to translate: ' + str_to_translate)
    if str_to_add_later is not None:
        print('string to add later: ' + str_to_add_later)
    print('xlsx file path: ' + xlsx_file_path)
    if country == "Nasdaq First North":
        country = 'Nasdaq North'
    # excelTranslator.translate_to_excel(xlsx_file_path,
    #                                    "/Users/home/Programming/service_keys/remotes-firebase_service_account.json",
    #                                    "remotes-7c523",  # one of my projects name
    #                                    'en-US',  # base language
    #                                    [str_to_translate,
    #                                     f'Mobile Tracking Trading App for {country}.',  # app's summary
    #                                     f'An app for traders who looks for simplicity. All of {country} markets in one place! Updated stock prices and historic stock prices. Easy separation into interesting stocks in different sectors and categories. '
    #                                     f'This app supports data from {keywords}, Stock Exchange'],
    #                                    str_to_add_later,
    #                                    # ['af', 'am']
    #                                    # ['mk-MK']
    #                                    ['af', 'am', 'ar', 'hy-AM', 'az-AZ', 'bn-BD', 'eu-ES', 'be', 'bg', 'my-MM', 'ca', 'zh-HK', 'zh-CN', 'zh-TW', 'hr', 'cs-CZ', 'da-DK', 'nl-NL', 'et', 'fil', 'fi-FI', 'fr-FR', 'fr-CA', 'gl-ES', 'ka-GE', 'de-DE', 'el-GR', 'hi-IN', 'hu-HU', 'is-IS', 'id', 'it-IT', 'ja-JP', 'kn-IN', 'km-KH', 'ko-KR', 'ky-KG', 'lo-LA', 'lv', 'lt', 'mk-MK', 'ms', 'ml-IN', 'mr-IN', 'mn-MN', 'ne-NP', 'no-NO', 'fa', 'pl-PL', 'pt-BR',
    #                                     'pt-PT', 'ro', 'ru-RU', 'sr', 'si-LK', 'sk', 'sl', 'es-419', 'es-ES', 'es-US', 'sw', 'sv-SE', 'ta-IN', 'te-IN', 'th', 'tr-TR', 'uk', 'vi', 'zu']
    #                                    #
    #                                    )
    #
    # os.rename(app_dir, f'{app_dir}_completed')


def run_main():
    dir_list = fh.get_dir_content('/Users/home/Desktop/stock_exchange/20_apr/work', False, True, False)
    dir_list.sort()
    for app_dir in dir_list:
        # build_dir(app)
        parse_translation(app_dir)


run_main()
