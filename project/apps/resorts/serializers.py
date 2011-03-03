import ast
import json

from django.conf import settings
from rest_framework import serializers

from apps.custom_user.serializers import UserSerializer
from apps.resorts.models import Area
from apps.resorts.models import DATETIME_FORMAT
from apps.resorts.models import LIVE
from apps.resorts.models import LOCATION_STATUS
from apps.resorts.models import MapType, Choice
from apps.resorts.models import PaperSize
from apps.resorts.models import Resort
from apps.resorts.models import ResortLocation
from apps.resorts.models import UnitType
from apps.resorts.models import UserResortMap
from helper_functions import construct_options
from helper_functions import replace_null

timezone = {'Africa_Abidjan': 'Africa/Abidjan',
            'Africa_Accra': 'Africa/Accra',
            'Africa_Addis_Ababa': 'Africa/Addis_Ababa',
            'Africa_Algiers': 'Africa/Algiers',
            'Africa_Asmara': 'Africa/Asmara',
            'Africa_Asmera': 'Africa/Asmera',
            'Africa_Bamako': 'Africa/Bamako',
            'Africa_Bangui': 'Africa/Bangui',
            'Africa_Banjul': 'Africa/Banjul',
            'Africa_Bissau': 'Africa/Bissau',
            'Africa_Blantyre': 'Africa/Blantyre',
            'Africa_Brazzaville': 'Africa/Brazzaville',
            'Africa_Bujumbura': 'Africa/Bujumbura',
            'Africa_Cairo': 'Africa/Cairo',
            'Africa_Casablanca': 'Africa/Casablanca',
            'Africa_Ceuta': 'Africa/Ceuta',
            'Africa_Conakry': 'Africa/Conakry',
            'Africa_Dakar': 'Africa/Dakar',
            'Africa_Dar_es_Salaam': 'Africa/Dar_es_Salaam',
            'Africa_Djibouti': 'Africa/Djibouti',
            'Africa_Douala': 'Africa/Douala',
            'Africa_El_Aaiun': 'Africa/El_Aaiun',
            'Africa_Freetown': 'Africa/Freetown',
            'Africa_Gaborone': 'Africa/Gaborone',
            'Africa_Harare': 'Africa/Harare',
            'Africa_Johannesburg': 'Africa/Johannesburg',
            'Africa_Juba': 'Africa/Juba',
            'Africa_Kampala': 'Africa/Kampala',
            'Africa_Khartoum': 'Africa/Khartoum',
            'Africa_Kigali': 'Africa/Kigali',
            'Africa_Kinshasa': 'Africa/Kinshasa',
            'Africa_Lagos': 'Africa/Lagos',
            'Africa_Libreville': 'Africa/Libreville',
            'Africa_Lome': 'Africa/Lome',
            'Africa_Luanda': 'Africa/Luanda',
            'Africa_Lubumbashi': 'Africa/Lubumbashi',
            'Africa_Lusaka': 'Africa/Lusaka',
            'Africa_Malabo': 'Africa/Malabo',
            'Africa_Maputo': 'Africa/Maputo',
            'Africa_Maseru': 'Africa/Maseru',
            'Africa_Mbabane': 'Africa/Mbabane',
            'Africa_Mogadishu': 'Africa/Mogadishu',
            'Africa_Monrovia': 'Africa/Monrovia',
            'Africa_Nairobi': 'Africa/Nairobi',
            'Africa_Ndjamena': 'Africa/Ndjamena',
            'Africa_Niamey': 'Africa/Niamey',
            'Africa_Nouakchott': 'Africa/Nouakchott',
            'Africa_Ouagadougou': 'Africa/Ouagadougou',
            'Africa_Porto_Novo': 'Africa/Porto-Novo',
            'Africa_Sao_Tome': 'Africa/Sao_Tome',
            'Africa_Timbuktu': 'Africa/Timbuktu',
            'Africa_Tripoli': 'Africa/Tripoli',
            'Africa_Tunis': 'Africa/Tunis',
            'Africa_Windhoek': 'Africa/Windhoek',
            'America_Adak': 'America/Adak',
            'America_Anchorage': 'America/Anchorage',
            'America_Anguilla': 'America/Anguilla',
            'America_Antigua': 'America/Antigua',
            'America_Araguaina': 'America/Araguaina',
            'America_Argentina_Buenos_Aires': 'America/Argentina/Buenos_Aires',
            'America_Argentina_Catamarca': 'America/Argentina/Catamarca',
            'America_Argentina_ComodRivadavia': 'America/Argentina/ComodRivadavia',
            'America_Argentina_Cordoba': 'America/Argentina/Cordoba',
            'America_Argentina_Jujuy': 'America/Argentina/Jujuy',
            'America_Argentina_La_Rioja': 'America/Argentina/La_Rioja',
            'America_Argentina_Mendoza': 'America/Argentina/Mendoza',
            'America_Argentina_Rio_Gallegos': 'America/Argentina/Rio_Gallegos',
            'America_Argentina_Salta': 'America/Argentina/Salta',
            'America_Argentina_San_Juan': 'America/Argentina/San_Juan',
            'America_Argentina_San_Luis': 'America/Argentina/San_Luis',
            'America_Argentina_Tucuman': 'America/Argentina/Tucuman',
            'America_Argentina_Ushuaia': 'America/Argentina/Ushuaia',
            'America_Aruba': 'America/Aruba',
            'America_Asuncion': 'America/Asuncion',
            'America_Atikokan': 'America/Atikokan',
            'America_Atka': 'America/Atka',
            'America_Bahia': 'America/Bahia',
            'America_Bahia_Banderas': 'America/Bahia_Banderas',
            'America_Barbados': 'America/Barbados',
            'America_Belem': 'America/Belem',
            'America_Belize': 'America/Belize',
            'America_Blanc_Sablon': 'America/Blanc-Sablon',
            'America_Boa_Vista': 'America/Boa_Vista',
            'America_Bogota': 'America/Bogota',
            'America_Boise': 'America/Boise',
            'America_Buenos_Aires': 'America/Buenos_Aires',
            'America_Cambridge_Bay': 'America/Cambridge_Bay',
            'America_Campo_Grande': 'America/Campo_Grande',
            'America_Cancun': 'America/Cancun',
            'America_Caracas': 'America/Caracas',
            'America_Catamarca': 'America/Catamarca',
            'America_Cayenne': 'America/Cayenne',
            'America_Cayman': 'America/Cayman',
            'America_Chicago': 'America/Chicago',
            'America_Chihuahua': 'America/Chihuahua',
            'America_Coral_Harbour': 'America/Coral_Harbour',
            'America_Cordoba': 'America/Cordoba',
            'America_Costa_Rica': 'America/Costa_Rica',
            'America_Creston': 'America/Creston',
            'America_Cuiaba': 'America/Cuiaba',
            'America_Curacao': 'America/Curacao',
            'America_Danmarkshavn': 'America/Danmarkshavn',
            'America_Dawson': 'America/Dawson',
            'America_Dawson_Creek': 'America/Dawson_Creek',
            'America_Denver': 'America/Denver',
            'America_Detroit': 'America/Detroit',
            'America_Dominica': 'America/Dominica',
            'America_Edmonton': 'America/Edmonton',
            'America_Eirunepe': 'America/Eirunepe',
            'America_El_Salvador': 'America/El_Salvador',
            'America_Ensenada': 'America/Ensenada',
            'America_Fort_Wayne': 'America/Fort_Wayne',
            'America_Fortaleza': 'America/Fortaleza',
            'America_Glace_Bay': 'America/Glace_Bay',
            'America_Godthab': 'America/Godthab',
            'America_Goose_Bay': 'America/Goose_Bay',
            'America_Grand_Turk': 'America/Grand_Turk',
            'America_Grenada': 'America/Grenada',
            'America_Guadeloupe': 'America/Guadeloupe',
            'America_Guatemala': 'America/Guatemala',
            'America_Guayaquil': 'America/Guayaquil',
            'America_Guyana': 'America/Guyana',
            'America_Halifax': 'America/Halifax',
            'America_Havana': 'America/Havana',
            'America_Hermosillo': 'America/Hermosillo',
            'America_Indiana_Indianapolis': 'America/Indiana/Indianapolis',
            'America_Indiana_Knox': 'America/Indiana/Knox',
            'America_Indiana_Marengo': 'America/Indiana/Marengo',
            'America_Indiana_Petersburg': 'America/Indiana/Petersburg',
            'America_Indiana_Tell_City': 'America/Indiana/Tell_City',
            'America_Indiana_Vevay': 'America/Indiana/Vevay',
            'America_Indiana_Vincennes': 'America/Indiana/Vincennes',
            'America_Indiana_Winamac': 'America/Indiana/Winamac',
            'America_Indianapolis': 'America/Indianapolis',
            'America_Inuvik': 'America/Inuvik',
            'America_Iqaluit': 'America/Iqaluit',
            'America_Jamaica': 'America/Jamaica',
            'America_Jujuy': 'America/Jujuy',
            'America_Juneau': 'America/Juneau',
            'America_Kentucky_Louisville': 'America/Kentucky/Louisville',
            'America_Kentucky_Monticello': 'America/Kentucky/Monticello',
            'America_Knox_IN': 'America/Knox_IN',
            'America_Kralendijk': 'America/Kralendijk',
            'America_La_Paz': 'America/La_Paz',
            'America_Lima': 'America/Lima',
            'America_Los_Angeles': 'America/Los_Angeles',
            'America_Louisville': 'America/Louisville',
            'America_Lower_Princes': 'America/Lower_Princes',
            'America_Maceio': 'America/Maceio',
            'America_Managua': 'America/Managua',
            'America_Manaus': 'America/Manaus',
            'America_Marigot': 'America/Marigot',
            'America_Martinique': 'America/Martinique',
            'America_Matamoros': 'America/Matamoros',
            'America_Mazatlan': 'America/Mazatlan',
            'America_Mendoza': 'America/Mendoza',
            'America_Menominee': 'America/Menominee',
            'America_Merida': 'America/Merida',
            'America_Metlakatla': 'America/Metlakatla',
            'America_Mexico_City': 'America/Mexico_City',
            'America_Miquelon': 'America/Miquelon',
            'America_Moncton': 'America/Moncton',
            'America_Monterrey': 'America/Monterrey',
            'America_Montevideo': 'America/Montevideo',
            'America_Montreal': 'America/Montreal',
            'America_Montserrat': 'America/Montserrat',
            'America_Nassau': 'America/Nassau',
            'America_New_York': 'America/New_York',
            'America_Nipigon': 'America/Nipigon',
            'America_Nome': 'America/Nome',
            'America_Noronha': 'America/Noronha',
            'America_North_Dakota_Beulah': 'America/North_Dakota/Beulah',
            'America_North_Dakota_Center': 'America/North_Dakota/Center',
            'America_North_Dakota_New_Salem': 'America/North_Dakota/New_Salem',
            'America_Ojinaga': 'America/Ojinaga',
            'America_Panama': 'America/Panama',
            'America_Pangnirtung': 'America/Pangnirtung',
            'America_Paramaribo': 'America/Paramaribo',
            'America_Phoenix': 'America/Phoenix',
            'America_Port_au_Prince': 'America/Port-au-Prince',
            'America_Port_of_Spain': 'America/Port_of_Spain',
            'America_Porto_Acre': 'America/Porto_Acre',
            'America_Porto_Velho': 'America/Porto_Velho',
            'America_Puerto_Rico': 'America/Puerto_Rico',
            'America_Rainy_River': 'America/Rainy_River',
            'America_Rankin_Inlet': 'America/Rankin_Inlet',
            'America_Recife': 'America/Recife',
            'America_Regina': 'America/Regina',
            'America_Resolute': 'America/Resolute',
            'America_Rio_Branco': 'America/Rio_Branco',
            'America_Rosario': 'America/Rosario',
            'America_Santa_Isabel': 'America/Santa_Isabel',
            'America_Santarem': 'America/Santarem',
            'America_Santiago': 'America/Santiago',
            'America_Santo_Domingo': 'America/Santo_Domingo',
            'America_Sao_Paulo': 'America/Sao_Paulo',
            'America_Scoresbysund': 'America/Scoresbysund',
            'America_Shiprock': 'America/Shiprock',
            'America_Sitka': 'America/Sitka',
            'America_St_Barthelemy': 'America/St_Barthelemy',
            'America_St_Johns': 'America/St_Johns',
            'America_St_Kitts': 'America/St_Kitts',
            'America_St_Lucia': 'America/St_Lucia',
            'America_St_Thomas': 'America/St_Thomas',
            'America_St_Vincent': 'America/St_Vincent',
            'America_Swift_Current': 'America/Swift_Current',
            'America_Tegucigalpa': 'America/Tegucigalpa',
            'America_Thule': 'America/Thule',
            'America_Thunder_Bay': 'America/Thunder_Bay',
            'America_Tijuana': 'America/Tijuana',
            'America_Toronto': 'America/Toronto',
            'America_Tortola': 'America/Tortola',
            'America_Vancouver': 'America/Vancouver',
            'America_Virgin': 'America/Virgin',
            'America_Whitehorse': 'America/Whitehorse',
            'America_Winnipeg': 'America/Winnipeg',
            'America_Yakutat': 'America/Yakutat',
            'America_Yellowknife': 'America/Yellowknife',
            'Antarctica_Casey': 'Antarctica/Casey',
            'Antarctica_Davis': 'Antarctica/Davis',
            'Antarctica_DumontDUrville': 'Antarctica/DumontDUrville',
            'Antarctica_Macquarie': 'Antarctica/Macquarie',
            'Antarctica_Mawson': 'Antarctica/Mawson',
            'Antarctica_McMurdo': 'Antarctica/McMurdo',
            'Antarctica_Palmer': 'Antarctica/Palmer',
            'Antarctica_Rothera': 'Antarctica/Rothera',
            'Antarctica_South_Pole': 'Antarctica/South_Pole',
            'Antarctica_Syowa': 'Antarctica/Syowa',
            'Antarctica_Troll': 'Antarctica/Troll',
            'Antarctica_Vostok': 'Antarctica/Vostok',
            'Arctic_Longyearbyen': 'Arctic/Longyearbyen',
            'Asia_Aden': 'Asia/Aden',
            'Asia_Almaty': 'Asia/Almaty',
            'Asia_Amman': 'Asia/Amman',
            'Asia_Anadyr': 'Asia/Anadyr',
            'Asia_Aqtau': 'Asia/Aqtau',
            'Asia_Aqtobe': 'Asia/Aqtobe',
            'Asia_Ashgabat': 'Asia/Ashgabat',
            'Asia_Ashkhabad': 'Asia/Ashkhabad',
            'Asia_Baghdad': 'Asia/Baghdad',
            'Asia_Bahrain': 'Asia/Bahrain',
            'Asia_Baku': 'Asia/Baku',
            'Asia_Bangkok': 'Asia/Bangkok',
            'Asia_Beirut': 'Asia/Beirut',
            'Asia_Bishkek': 'Asia/Bishkek',
            'Asia_Brunei': 'Asia/Brunei',
            'Asia_Calcutta': 'Asia/Calcutta',
            'Asia_Chita': 'Asia/Chita',
            'Asia_Choibalsan': 'Asia/Choibalsan',
            'Asia_Chongqing': 'Asia/Chongqing',
            'Asia_Chungking': 'Asia/Chungking',
            'Asia_Colombo': 'Asia/Colombo',
            'Asia_Dacca': 'Asia/Dacca',
            'Asia_Damascus': 'Asia/Damascus',
            'Asia_Dhaka': 'Asia/Dhaka',
            'Asia_Dili': 'Asia/Dili',
            'Asia_Dubai': 'Asia/Dubai',
            'Asia_Dushanbe': 'Asia/Dushanbe',
            'Asia_Gaza': 'Asia/Gaza',
            'Asia_Harbin': 'Asia/Harbin',
            'Asia_Hebron': 'Asia/Hebron',
            'Asia_Ho_Chi_Minh': 'Asia/Ho_Chi_Minh',
            'Asia_Hong_Kong': 'Asia/Hong_Kong',
            'Asia_Hovd': 'Asia/Hovd',
            'Asia_Irkutsk': 'Asia/Irkutsk',
            'Asia_Istanbul': 'Asia/Istanbul',
            'Asia_Jakarta': 'Asia/Jakarta',
            'Asia_Jayapura': 'Asia/Jayapura',
            'Asia_Jerusalem': 'Asia/Jerusalem',
            'Asia_Kabul': 'Asia/Kabul',
            'Asia_Kamchatka': 'Asia/Kamchatka',
            'Asia_Karachi': 'Asia/Karachi',
            'Asia_Kashgar': 'Asia/Kashgar',
            'Asia_Kathmandu': 'Asia/Kathmandu',
            'Asia_Katmandu': 'Asia/Katmandu',
            'Asia_Khandyga': 'Asia/Khandyga',
            'Asia_Kolkata': 'Asia/Kolkata',
            'Asia_Krasnoyarsk': 'Asia/Krasnoyarsk',
            'Asia_Kuala_Lumpur': 'Asia/Kuala_Lumpur',
            'Asia_Kuching': 'Asia/Kuching',
            'Asia_Kuwait': 'Asia/Kuwait',
            'Asia_Macao': 'Asia/Macao',
            'Asia_Macau': 'Asia/Macau',
            'Asia_Magadan': 'Asia/Magadan',
            'Asia_Makassar': 'Asia/Makassar',
            'Asia_Manila': 'Asia/Manila',
            'Asia_Muscat': 'Asia/Muscat',
            'Asia_Nicosia': 'Asia/Nicosia',
            'Asia_Novokuznetsk': 'Asia/Novokuznetsk',
            'Asia_Novosibirsk': 'Asia/Novosibirsk',
            'Asia_Omsk': 'Asia/Omsk',
            'Asia_Oral': 'Asia/Oral',
            'Asia_Phnom_Penh': 'Asia/Phnom_Penh',
            'Asia_Pontianak': 'Asia/Pontianak',
            'Asia_Pyongyang': 'Asia/Pyongyang',
            'Asia_Qatar': 'Asia/Qatar',
            'Asia_Qyzylorda': 'Asia/Qyzylorda',
            'Asia_Rangoon': 'Asia/Rangoon',
            'Asia_Riyadh': 'Asia/Riyadh',
            'Asia_Saigon': 'Asia/Saigon',
            'Asia_Sakhalin': 'Asia/Sakhalin',
            'Asia_Samarkand': 'Asia/Samarkand',
            'Asia_Seoul': 'Asia/Seoul',
            'Asia_Shanghai': 'Asia/Shanghai',
            'Asia_Singapore': 'Asia/Singapore',
            'Asia_Srednekolymsk': 'Asia/Srednekolymsk',
            'Asia_Taipei': 'Asia/Taipei',
            'Asia_Tashkent': 'Asia/Tashkent',
            'Asia_Tbilisi': 'Asia/Tbilisi',
            'Asia_Tehran': 'Asia/Tehran',
            'Asia_Tel_Aviv': 'Asia/Tel_Aviv',
            'Asia_Thimbu': 'Asia/Thimbu',
            'Asia_Thimphu': 'Asia/Thimphu',
            'Asia_Tokyo': 'Asia/Tokyo',
            'Asia_Ujung_Pandang': 'Asia/Ujung_Pandang',
            'Asia_Ulaanbaatar': 'Asia/Ulaanbaatar',
            'Asia_Ulan_Bator': 'Asia/Ulan_Bator',
            'Asia_Urumqi': 'Asia/Urumqi',
            'Asia_Ust_Nera': 'Asia/Ust-Nera',
            'Asia_Vientiane': 'Asia/Vientiane',
            'Asia_Vladivostok': 'Asia/Vladivostok',
            'Asia_Yakutsk': 'Asia/Yakutsk',
            'Asia_Yekaterinburg': 'Asia/Yekaterinburg',
            'Asia_Yerevan': 'Asia/Yerevan',
            'Atlantic_Azores': 'Atlantic/Azores',
            'Atlantic_Bermuda': 'Atlantic/Bermuda',
            'Atlantic_Canary': 'Atlantic/Canary',
            'Atlantic_Cape_Verde': 'Atlantic/Cape_Verde',
            'Atlantic_Faeroe': 'Atlantic/Faeroe',
            'Atlantic_Faroe': 'Atlantic/Faroe',
            'Atlantic_Jan_Mayen': 'Atlantic/Jan_Mayen',
            'Atlantic_Madeira': 'Atlantic/Madeira',
            'Atlantic_Reykjavik': 'Atlantic/Reykjavik',
            'Atlantic_South_Georgia': 'Atlantic/South_Georgia',
            'Atlantic_St_Helena': 'Atlantic/St_Helena',
            'Atlantic_Stanley': 'Atlantic/Stanley',
            'Australia_ACT': 'Australia/ACT',
            'Australia_Adelaide': 'Australia/Adelaide',
            'Australia_Brisbane': 'Australia/Brisbane',
            'Australia_Broken_Hill': 'Australia/Broken_Hill',
            'Australia_Canberra': 'Australia/Canberra',
            'Australia_Currie': 'Australia/Currie',
            'Australia_Darwin': 'Australia/Darwin',
            'Australia_Eucla': 'Australia/Eucla',
            'Australia_Hobart': 'Australia/Hobart',
            'Australia_LHI': 'Australia/LHI',
            'Australia_Lindeman': 'Australia/Lindeman',
            'Australia_Lord_Howe': 'Australia/Lord_Howe',
            'Australia_Melbourne': 'Australia/Melbourne',
            'Australia_NSW': 'Australia/NSW',
            'Australia_North': 'Australia/North',
            'Australia_Perth': 'Australia/Perth',
            'Australia_Queensland': 'Australia/Queensland',
            'Australia_South': 'Australia/South',
            'Australia_Sydney': 'Australia/Sydney',
            'Australia_Tasmania': 'Australia/Tasmania',
            'Australia_Victoria': 'Australia/Victoria',
            'Australia_West': 'Australia/West',
            'Australia_Yancowinna': 'Australia/Yancowinna',
            'Brazil_Acre': 'Brazil/Acre',
            'Brazil_DeNoronha': 'Brazil/DeNoronha',
            'Brazil_East': 'Brazil/East',
            'Brazil_West': 'Brazil/West',
            'CET': 'CET',
            'CST6CDT': 'CST6CDT',
            'Canada_Atlantic': 'Canada/Atlantic',
            'Canada_Central': 'Canada/Central',
            'Canada_East_Saskatchewan': 'Canada/East-Saskatchewan',
            'Canada_Eastern': 'Canada/Eastern',
            'Canada_Mountain': 'Canada/Mountain',
            'Canada_Newfoundland': 'Canada/Newfoundland',
            'Canada_Pacific': 'Canada/Pacific',
            'Canada_Saskatchewan': 'Canada/Saskatchewan',
            'Canada_Yukon': 'Canada/Yukon',
            'Chile_Continental': 'Chile/Continental',
            'Chile_EasterIsland': 'Chile/EasterIsland',
            'Cuba': 'Cuba',
            'EET': 'EET',
            'EST': 'EST',
            'EST5EDT': 'EST5EDT',
            'Egypt': 'Egypt',
            'Eire': 'Eire',
            'Etc_GMT': 'Etc/GMT',
            'Etc_GMT+0': 'Etc/GMT+0',
            'Etc_GMT+1': 'Etc/GMT+1',
            'Etc_GMT+10': 'Etc/GMT+10',
            'Etc_GMT+11': 'Etc/GMT+11',
            'Etc_GMT+12': 'Etc/GMT+12',
            'Etc_GMT+2': 'Etc/GMT+2',
            'Etc_GMT+3': 'Etc/GMT+3',
            'Etc_GMT+4': 'Etc/GMT+4',
            'Etc_GMT+5': 'Etc/GMT+5',
            'Etc_GMT+6': 'Etc/GMT+6',
            'Etc_GMT+7': 'Etc/GMT+7',
            'Etc_GMT+8': 'Etc/GMT+8',
            'Etc_GMT+9': 'Etc/GMT+9',
            'Etc_GMT0': 'Etc/GMT0',
            'Etc_GMT_0': 'Etc/GMT-0',
            'Etc_GMT_1': 'Etc/GMT-1',
            'Etc_GMT_10': 'Etc/GMT-10',
            'Etc_GMT_11': 'Etc/GMT-11',
            'Etc_GMT_12': 'Etc/GMT-12',
            'Etc_GMT_13': 'Etc/GMT-13',
            'Etc_GMT_14': 'Etc/GMT-14',
            'Etc_GMT_2': 'Etc/GMT-2',
            'Etc_GMT_3': 'Etc/GMT-3',
            'Etc_GMT_4': 'Etc/GMT-4',
            'Etc_GMT_5': 'Etc/GMT-5',
            'Etc_GMT_6': 'Etc/GMT-6',
            'Etc_GMT_7': 'Etc/GMT-7',
            'Etc_GMT_8': 'Etc/GMT-8',
            'Etc_GMT_9': 'Etc/GMT-9',
            'Etc_Greenwich': 'Etc/Greenwich',
            'Etc_UCT': 'Etc/UCT',
            'Etc_UTC': 'Etc/UTC',
            'Etc_Universal': 'Etc/Universal',
            'Etc_Zulu': 'Etc/Zulu',
            'Europe_Amsterdam': 'Europe/Amsterdam',
            'Europe_Andorra': 'Europe/Andorra',
            'Europe_Athens': 'Europe/Athens',
            'Europe_Belfast': 'Europe/Belfast',
            'Europe_Belgrade': 'Europe/Belgrade',
            'Europe_Berlin': 'Europe/Berlin',
            'Europe_Bratislava': 'Europe/Bratislava',
            'Europe_Brussels': 'Europe/Brussels',
            'Europe_Bucharest': 'Europe/Bucharest',
            'Europe_Budapest': 'Europe/Budapest',
            'Europe_Busingen': 'Europe/Busingen',
            'Europe_Chisinau': 'Europe/Chisinau',
            'Europe_Copenhagen': 'Europe/Copenhagen',
            'Europe_Dublin': 'Europe/Dublin',
            'Europe_Gibraltar': 'Europe/Gibraltar',
            'Europe_Guernsey': 'Europe/Guernsey',
            'Europe_Helsinki': 'Europe/Helsinki',
            'Europe_Isle_of_Man': 'Europe/Isle_of_Man',
            'Europe_Istanbul': 'Europe/Istanbul',
            'Europe_Jersey': 'Europe/Jersey',
            'Europe_Kaliningrad': 'Europe/Kaliningrad',
            'Europe_Kiev': 'Europe/Kiev',
            'Europe_Lisbon': 'Europe/Lisbon',
            'Europe_Ljubljana': 'Europe/Ljubljana',
            'Europe_London': 'Europe/London',
            'Europe_Luxembourg': 'Europe/Luxembourg',
            'Europe_Madrid': 'Europe/Madrid',
            'Europe_Malta': 'Europe/Malta',
            'Europe_Mariehamn': 'Europe/Mariehamn',
            'Europe_Minsk': 'Europe/Minsk',
            'Europe_Monaco': 'Europe/Monaco',
            'Europe_Moscow': 'Europe/Moscow',
            'Europe_Nicosia': 'Europe/Nicosia',
            'Europe_Oslo': 'Europe/Oslo',
            'Europe_Paris': 'Europe/Paris',
            'Europe_Podgorica': 'Europe/Podgorica',
            'Europe_Prague': 'Europe/Prague',
            'Europe_Riga': 'Europe/Riga',
            'Europe_Rome': 'Europe/Rome',
            'Europe_Samara': 'Europe/Samara',
            'Europe_San_Marino': 'Europe/San_Marino',
            'Europe_Sarajevo': 'Europe/Sarajevo',
            'Europe_Simferopol': 'Europe/Simferopol',
            'Europe_Skopje': 'Europe/Skopje',
            'Europe_Sofia': 'Europe/Sofia',
            'Europe_Stockholm': 'Europe/Stockholm',
            'Europe_Tallinn': 'Europe/Tallinn',
            'Europe_Tirane': 'Europe/Tirane',
            'Europe_Tiraspol': 'Europe/Tiraspol',
            'Europe_Uzhgorod': 'Europe/Uzhgorod',
            'Europe_Vaduz': 'Europe/Vaduz',
            'Europe_Vatican': 'Europe/Vatican',
            'Europe_Vienna': 'Europe/Vienna',
            'Europe_Vilnius': 'Europe/Vilnius',
            'Europe_Volgograd': 'Europe/Volgograd',
            'Europe_Warsaw': 'Europe/Warsaw',
            'Europe_Zagreb': 'Europe/Zagreb',
            'Europe_Zaporozhye': 'Europe/Zaporozhye',
            'Europe_Zurich': 'Europe/Zurich',
            'GB': 'GB',
            'GB_Eire': 'GB-Eire',
            'GMT': 'GMT',
            'GMT+0': 'GMT+0',
            'GMT0': 'GMT0',
            'GMT_0': 'GMT-0',
            'Greenwich': 'Greenwich',
            'HST': 'HST',
            'Hongkong': 'Hongkong',
            'Iceland': 'Iceland',
            'Indian_Antananarivo': 'Indian/Antananarivo',
            'Indian_Chagos': 'Indian/Chagos',
            'Indian_Christmas': 'Indian/Christmas',
            'Indian_Cocos': 'Indian/Cocos',
            'Indian_Comoro': 'Indian/Comoro',
            'Indian_Kerguelen': 'Indian/Kerguelen',
            'Indian_Mahe': 'Indian/Mahe',
            'Indian_Maldives': 'Indian/Maldives',
            'Indian_Mauritius': 'Indian/Mauritius',
            'Indian_Mayotte': 'Indian/Mayotte',
            'Indian_Reunion': 'Indian/Reunion',
            'Iran': 'Iran',
            'Israel': 'Israel',
            'Jamaica': 'Jamaica',
            'Japan': 'Japan',
            'Kwajalein': 'Kwajalein',
            'Libya': 'Libya',
            'MET': 'MET',
            'MST': 'MST',
            'MST7MDT': 'MST7MDT',
            'Mexico_BajaNorte': 'Mexico/BajaNorte',
            'Mexico_BajaSur': 'Mexico/BajaSur',
            'Mexico_General': 'Mexico/General',
            'NZ': 'NZ',
            'NZ_CHAT': 'NZ-CHAT',
            'Navajo': 'Navajo',
            'PRC': 'PRC',
            'PST8PDT': 'PST8PDT',
            'Pacific_Apia': 'Pacific/Apia',
            'Pacific_Auckland': 'Pacific/Auckland',
            'Pacific_Bougainville': 'Pacific/Bougainville',
            'Pacific_Chatham': 'Pacific/Chatham',
            'Pacific_Chuuk': 'Pacific/Chuuk',
            'Pacific_Easter': 'Pacific/Easter',
            'Pacific_Efate': 'Pacific/Efate',
            'Pacific_Enderbury': 'Pacific/Enderbury',
            'Pacific_Fakaofo': 'Pacific/Fakaofo',
            'Pacific_Fiji': 'Pacific/Fiji',
            'Pacific_Funafuti': 'Pacific/Funafuti',
            'Pacific_Galapagos': 'Pacific/Galapagos',
            'Pacific_Gambier': 'Pacific/Gambier',
            'Pacific_Guadalcanal': 'Pacific/Guadalcanal',
            'Pacific_Guam': 'Pacific/Guam',
            'Pacific_Honolulu': 'Pacific/Honolulu',
            'Pacific_Johnston': 'Pacific/Johnston',
            'Pacific_Kiritimati': 'Pacific/Kiritimati',
            'Pacific_Kosrae': 'Pacific/Kosrae',
            'Pacific_Kwajalein': 'Pacific/Kwajalein',
            'Pacific_Majuro': 'Pacific/Majuro',
            'Pacific_Marquesas': 'Pacific/Marquesas',
            'Pacific_Midway': 'Pacific/Midway',
            'Pacific_Nauru': 'Pacific/Nauru',
            'Pacific_Niue': 'Pacific/Niue',
            'Pacific_Norfolk': 'Pacific/Norfolk',
            'Pacific_Noumea': 'Pacific/Noumea',
            'Pacific_Pago_Pago': 'Pacific/Pago_Pago',
            'Pacific_Palau': 'Pacific/Palau',
            'Pacific_Pitcairn': 'Pacific/Pitcairn',
            'Pacific_Pohnpei': 'Pacific/Pohnpei',
            'Pacific_Ponape': 'Pacific/Ponape',
            'Pacific_Port_Moresby': 'Pacific/Port_Moresby',
            'Pacific_Rarotonga': 'Pacific/Rarotonga',
            'Pacific_Saipan': 'Pacific/Saipan',
            'Pacific_Samoa': 'Pacific/Samoa',
            'Pacific_Tahiti': 'Pacific/Tahiti',
            'Pacific_Tarawa': 'Pacific/Tarawa',
            'Pacific_Tongatapu': 'Pacific/Tongatapu',
            'Pacific_Truk': 'Pacific/Truk',
            'Pacific_Wake': 'Pacific/Wake',
            'Pacific_Wallis': 'Pacific/Wallis',
            'Pacific_Yap': 'Pacific/Yap',
            'Poland': 'Poland',
            'Portugal': 'Portugal',
            'ROC': 'ROC',
            'ROK': 'ROK',
            'Singapore': 'Singapore',
            'Turkey': 'Turkey',
            'UCT': 'UCT',
            'US_Alaska': 'US/Alaska',
            'US_Aleutian': 'US/Aleutian',
            'US_Arizona': 'US/Arizona',
            'US_Central': 'US/Central',
            'US_East_Indiana': 'US/East-Indiana',
            'US_Eastern': 'US/Eastern',
            'US_Hawaii': 'US/Hawaii',
            'US_Indiana_Starke': 'US/Indiana-Starke',
            'US_Michigan': 'US/Michigan',
            'US_Mountain': 'US/Mountain',
            'US_Pacific': 'US/Pacific',
            'US_Pacific_New': 'US/Pacific-New',
            'US_Samoa': 'US/Samoa',
            'UTC': 'UTC',
            'Universal': 'Universal',
            'WET': 'WET',
            'W_SU': 'W-SU',
            'Zulu': 'Zulu'}


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class Base64FileField(serializers.FileField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_file')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            complete_file_name = "%s.%s" % (file_name, self.filetype,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64FileField, self).to_internal_value(data)

    def __init__(self, *args, **kwargs):
        filetype = kwargs.pop('filetype', None)
        super(Base64FileField, self).__init__(*args, **kwargs)
        self.filetype = filetype


class ResortSerializer(serializers.ModelSerializer):
    resort_logo = Base64ImageField(
        max_length=None, use_url=True, required=False
    )
    map_kml = Base64FileField(
        max_length=None, use_url=True, filetype='json',
        required=False
    )
    report_form = Base64FileField(
        max_length=None, use_url=True, filetype='html',
        required=False
    )

    class Meta:
        model = Resort

    def to_internal_value(self, data):
        timezone_val = data.get('timezone')
        if timezone_val is not None:
            if '/' not in timezone_val:
                data['timezone'] = timezone[timezone_val]
        ret = super(ResortSerializer, self).to_internal_value(data)

        dispatch_field_choice = ret.get('dispatch_field_choice')
        if dispatch_field_choice is not None:
            ret['dispatch_field_choice'] = ast.literal_eval(json.dumps(ast.literal_eval(dispatch_field_choice)))
        return ret

    def to_representation(self, instance):
        domain = instance.domain_id.domain
        ret = super(ResortSerializer, self).to_representation(instance)

        dispatch_field_choice = ret.get('dispatch_field_choice')
        if dispatch_field_choice is not None:
            ret['dispatch_field_choice'] = ast.literal_eval(dispatch_field_choice)

        map_kml = ret.get('map_kml')
        image = ret.get('resort_logo')
        # default_unit_distance = ret.get('default_unit_distance')
        map_type = ret.get('map_type')
        print_on_device = ret.get('print_on_device')
        # default_unit_temp = ret.get('default_unit_temp')
        # default_unit_length = ret.get('default_unit_length')
        # default_unit_weight = ret.get('default_unit_weight')
        report_form = ret.get('report_form')
        unit_format = ret.get('unit_format')
        default_unit_paper = ret.get('default_unit_paper')
        domain_id = ret.get('domain_id')
        datetime_format = ret.get('datetime_format')
        try:
            # if default_unit_distance is not None:
            #     ret['default_unit_distance'] = construct_options(DistanceUnit, default_unit_distance)
            if map_type is not None:
                ret['map_type'] = construct_options(MapType, map_type)
            if print_on_device is not None:
                ret['print_on_device'] = construct_options(Choice, print_on_device)
            # if default_unit_temp is not None:
            #     ret['default_unit_temp'] = construct_options(TemperatureUnit, default_unit_temp)
            # if default_unit_length is not None:
            #     ret['default_unit_length'] = construct_options(LengthUnit, default_unit_length)
            # if default_unit_distance is not None:
            #     ret['default_unit_distance'] = construct_options(DistanceUnit, default_unit_distance)
            # if default_unit_weight is not None:
            #     ret['default_unit_weight'] = construct_options(WeightUnit, default_unit_weight)
            # if map_kml is not None and map_kml:
            #     ret['map_kml'] = settings.SCHEME + domain + '/static' + ret['map_kml'].split('static')[1]
            # if image is not None and image:
            #     ret['resort_logo'] = settings.SCHEME + domain + '/static' + ret['resort_logo'].split('static')[1]
            # if report_form is not None and report_form:
            #     ret['report_form'] = settings.SCHEME + domain + '/static' + ret['report_form'].split('static')[1]
            if unit_format is not None:
                ret['unit_format'] = construct_options(UnitType, unit_format)
            if default_unit_paper is not None:
                ret['default_unit_paper'] = construct_options(PaperSize, default_unit_paper)
            if datetime_format is not None:
                ret['datetime_format'] = construct_options(DATETIME_FORMAT, datetime_format)
            if domain_id is not None:
                ret['domain_id'] = domain
        except:
            pass
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(ResortSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserResortMapSerializer(serializers.ModelSerializer):
    user = UserSerializer(fields=('user_id', 'name'))

    def to_representation(self, instance):
        from apps.custom_user.utils import userrole_option
        ret = super(UserResortMapSerializer, self).to_representation(instance)
        ret['role'] = userrole_option(int(ret['role']))
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(UserResortMapSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = UserResortMap


class UserResortListSerializer(serializers.ModelSerializer):
    user = UserSerializer(fields=('user_id', 'name', 'email'))

    def to_representation(self, instance):
        from apps.custom_user.utils import userrole_option
        ret = super(UserResortListSerializer, self).to_representation(instance)
        ret['role'] = userrole_option(int(ret['role']))
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(UserResortListSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = UserResortMap


class AreaSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        ret = super(AreaSerializer, self).to_internal_value(data)
        return ret

    def to_representation(self, instance):
        ret = super(AreaSerializer, self).to_representation(instance)
        if 'location_count' in self.context:
            ret['location_count'] = ResortLocation.objects.filter(resort=self.context['resort'], area=instance,
                                                                  location_status=LIVE).count()
        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(AreaSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Area


class LocationSerializer(serializers.ModelSerializer):
    area = AreaSerializer(fields=('area_id', 'area_name'))

    def to_internal_value(self, data):
        data.pop('area_id', None)
        ret = super(LocationSerializer, self).to_internal_value(data)
        return ret

    def to_representation(self, instance):
        ret = super(LocationSerializer, self).to_representation(instance)
        location_status = ret.get('location_status')

        if location_status is not None:
            try:
                ret['location_status'] = construct_options(LOCATION_STATUS, location_status)
            except:
                pass

        return replace_null(ret)

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(LocationSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = ResortLocation
        exclude = ('resort', 'location_pk')
