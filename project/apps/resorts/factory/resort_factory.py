import factory
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.custom_user.factory.user_factory import UserRolesFactory, UserFactory
from apps.incidents.models import IncidentTemplate
from apps.resorts.models import Resort
from apps.resorts.models import UserResortMap
from apps.routing.factory.routing_factory import DomainFactory


class ResortFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resort
        django_get_or_create = ('resort_name',)

    resort_name = "Toggenburg"
    map_type = 0
    print_on_device = 0
    map_lat = -37.71411
    map_lng = 144.96328
    domain_id = DomainFactory(domain='localhost')
    network_key = "ZmY4YzZm"
    license_expiry_date = "2018-04-01T00:00:00"
    licenses = "10"
    website = "http://www.summit.com"
    timezone = "America/New_York"
    report_form = SimpleUploadedFile(name="report.html", content=open(
        "apps/resorts/factory/test_files/Perisher_report_tyvSnBC.html").read(), content_type='text/html')


class IncidentTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IncidentTemplate
        django_get_or_create = ('json',)

    json = {
        "DashboardItems": {
            "field_52ca41c50a16f": {
                "Order": 3,
                "Questions": {
                    "field_530fc1a1b12d0": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "location_details",
                        "Values": "",
                        "Type": "message",
                        "Order": 10
                    },
                    "field_551c8bbb3d785": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "run_name",
                        "Values": "",
                        "Type": "text",
                        "Order": 50
                    },
                    "field_554f7cbb3d784": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "area_name",
                        "Values": "",
                        "Type": "text",
                        "Order": 40
                    },
                    "field_551c8aaa3d786": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "location_info",
                        "Values": "",
                        "Type": "text",
                        "Order": 60
                    },
                    "field_52ca456962ba8": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "location",
                        "Values": "",
                        "Type": "google_map",
                        "Order": 70
                    },
                    "field_52ca451a62ba5": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "rating",
                        "Values": [
                            {
                                "57": "beginner"
                            },
                            {
                                "58": "easier"
                            },
                            {
                                "59": "more_difficult"
                            },
                            {
                                "60": "hard"
                            },
                            {
                                "61": "expert"
                            }
                        ],
                        "Type": "select",
                        "Order": 20
                    },
                    "field_52ca453862ba6": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "type",
                        "Values": [
                            {
                                "122": "on_piste"
                            },
                            {
                                "123": "off_piste"
                            },
                            {
                                "48": "lift"
                            },
                            {
                                "118": "terrain_park"
                            },
                            {
                                "119": "slope_style_course"
                            },
                            {
                                "121": "half_pipe"
                            },
                            {
                                "124": "big_air_site"
                            },
                            {
                                "125": "race_course"
                            },
                            {
                                "126": "event_course"
                            },
                            {
                                "1066": "tube_park"
                            },
                            {
                                "1067": "toboggan_slope"
                            },
                            {
                                "127": "premises"
                            },
                            {
                                "1063": "car_park"
                            },
                            {
                                "1064": "bridge"
                            },
                            {
                                "1431": "xc_trail"
                            },
                            {
                                "1065": "road"
                            },
                            {
                                "202": "rail"
                            }
                        ],
                        "Type": "select",
                        "Order": 30
                    }
                },
                "Label": "location"
            },
            "field_52d47a654d1aa": {
                "RepeatingQuestions": {
                    "photo": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "photo",
                        "Values": "",
                        "Type": "image",
                        "Order": 0
                    },
                    "photo_date_taken": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "photo_date_taken",
                        "Values": "",
                        "Type": "date_time_picker",
                        "Order": 1
                    }
                },
                "Required": "false",
                "Order": 8,
                "Label": "photos"
            },
            "field_52d47b5fdda86": {
                "RepeatingQuestions": {
                    "witness_type": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "statement_from",
                        "Values": [
                            {
                                "79": "staff"
                            },
                            {
                                "510": "witness"
                            },
                            {
                                "529": "casualty"
                            },
                            {
                                "1424": "parent"
                            }
                        ],
                        "Type": "select",
                        "Order": 4
                    },
                    "witness_relationship": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "witness_relationship",
                        "Values": "",
                        "Type": "text",
                        "Order": 2
                    },
                    "witness_phone": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "witness_phone",
                        "Values": "",
                        "Type": "text",
                        "Order": 1
                    },
                    "time_of_witness_statement": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "time_of_witness_statement",
                        "Values": "",
                        "Type": "date_time_picker",
                        "Order": 6
                    },
                    "witness_statement_recording": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "witness_statement_recording",
                        "Values": "",
                        "Type": "file",
                        "Order": 5
                    },
                    "witness_name": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "witness_name",
                        "Values": "",
                        "Type": "text",
                        "Order": 0
                    },
                    "witness_date_of_birth": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "witness_date_of_birth",
                        "Values": "",
                        "Type": "date_picker",
                        "Order": 3
                    }
                },
                "Required": "false",
                "Order": 10,
                "Label": "statements"
            },
            "notes": {
                "RepeatingQuestions": {
                    "field_52ca448dg94ja5": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "user",
                        "Values": "",
                        "Type": "hidden",
                        "Order": 30,
                        "Append": ""
                    },
                    "field_52ca448dg94ja4": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "note_date_time",
                        "Values": "",
                        "Type": "date_time_picker",
                        "Order": 20,
                        "Append": ""
                    },
                    "field_52ca448dg94ja3": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "note",
                        "Values": "",
                        "Type": "text",
                        "Order": 10,
                        "Append": ""
                    }
                },
                "Placeholder": "",
                "Required": "false",
                "Label": "notes",
                "Values": "",
                "Type": "repeater",
                "Order": 9999
            },
            "field_52ca42770a179": {
                "Order": 97,
                "Questions": {
                    "field_52d48077a16be": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "referred_to",
                        "Values": [
                            {
                                "195": "hospital"
                            },
                            {
                                "196": "doctor"
                            },
                            {
                                "197": "medical_centre"
                            },
                            {
                                "1096": "patroller_not_required"
                            },
                            {
                                "1097": "no_incident_found"
                            }
                        ],
                        "Type": "select",
                        "Order": 10
                    },
                    "field_5331c532e16df": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "grooming",
                        "Values": [
                            {
                                "1105": "overnight"
                            },
                            {
                                "1106": "flat_surface"
                            },
                            {
                                "1107": "ungroomed"
                            }
                        ],
                        "Type": "select",
                        "Order": 50
                    },
                    "field_53311c532e23a": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "patroller_sign_off",
                        "Values": "",
                        "Type": "message",
                        "Order": 30
                    },
                    "field_5331c865e16df": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "snowmaking",
                        "Values": [
                            {
                                "1108": "overnight"
                            },
                            {
                                "1109": "in_progress"
                            },
                            {
                                "1110": "none"
                            }
                        ],
                        "Type": "select",
                        "Order": 60
                    },
                    "field_52d48117a16bf": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "referrer_name",
                        "Values": "",
                        "Type": "text",
                        "Order": 20
                    },
                    "field_52d47de5edbdf": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "patroller_signature",
                        "Values": "",
                        "Type": "signature",
                        "Order": 100
                    },
                    "field_5331c532e16be": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "skier_traffic",
                        "Values": [
                            {
                                "1104": "low"
                            },
                            {
                                "1103": "medium"
                            },
                            {
                                "1102": "high"
                            }
                        ],
                        "Type": "select",
                        "Order": 40
                    },
                    "field_52d47e4cedbe2": {
                        "Placeholder": "enter_any_notes_you_may_think_are_relevant_to_this_incident",
                        "Required": "false",
                        "Label": "patroller_notes",
                        "Values": "",
                        "Type": "textarea",
                        "Order": 90
                    },
                    "field_863458b37814f": {
                        "ShowIf": {
                            "field_863458b37814e": "yes"
                        },
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "relevant_signage_comment",
                        "Values": "",
                        "Type": "text",
                        "Order": 80
                    },
                    "field_863458b37814e": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "relevant_signage",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 70
                    }
                },
                "Label": "close_case"
            },
            "field_52ca42550a175": {
                "Order": 80,
                "Questions": {
                    "field_54b0805ff5b3f": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "wind",
                        "Values": [
                            {
                                "1430": "none"
                            },
                            {
                                "1427": "light"
                            },
                            {
                                "1426": "moderate"
                            },
                            {
                                "1425": "strong"
                            },
                            {
                                "1429": "very_strong"
                            }
                        ],
                        "Type": "select",
                        "Order": 70
                    },
                    "field_52ca4637cc0fe": {
                        "Placeholder": "visible_distance",
                        "Required": "false",
                        "Label": "visible_distance",
                        "Values": "",
                        "Type": "decimal",
                        "Order": 60,
                        "Append": "m"
                    },
                    "field_52ca461ccc0fd": {
                        "Placeholder": "temperature",
                        "Required": "false",
                        "Label": "temperature",
                        "Values": "",
                        "Type": "temperature",
                        "Order": 50,
                        "Append": "c"
                    },
                    "field_52ca45fbcc0fc": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "visibility",
                        "Values": [
                            {
                                "55": "clear"
                            },
                            {
                                "56": "fog"
                            },
                            {
                                "110": "fair"
                            },
                            {
                                "111": "poor"
                            },
                            {
                                "221": "sharp_light"
                            },
                            {
                                "114": "whiteout"
                            },
                            {
                                "222": "flat_light"
                            },
                            {
                                "504": "flood_lights"
                            },
                            {
                                "114": "whiteout"
                            },
                            {
                                "505": "dark"
                            },
                            {
                                "1077": "inside"
                            }
                        ],
                        "Type": "select",
                        "Order": 40
                    },
                    "field_52ca45d6cc0fb": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "snow_conditions",
                        "Values": [
                            {
                                "52": "icy"
                            },
                            {
                                "53": "powder"
                            },
                            {
                                "104": "wet"
                            },
                            {
                                "105": "crust"
                            },
                            {
                                "107": "man_made"
                            },
                            {
                                "1082": "moguls"
                            },
                            {
                                "109": "granulated"
                            },
                            {
                                "106": "groomed"
                            },
                            {
                                "1077": "inside"
                            },
                            {
                                "1078": "off_snow"
                            },
                            {
                                "1079": "new_snow"
                            },
                            {
                                "108": "hard_packed"
                            },
                            {
                                "1080": "heavy_snow"
                            },
                            {
                                "54": "soft"
                            },
                            {
                                "1081": "spring_snow"
                            },
                            {
                                "1077": "inside"
                            },
                            {
                                "1078": "off_snow"
                            }
                        ],
                        "Type": "multi_select",
                        "Order": 20
                    },
                    "field_5386e82f7e637": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "weather",
                        "Values": [
                            {
                                "112": "raining"
                            },
                            {
                                "113": "snowing"
                            },
                            {
                                "56": "fog"
                            },
                            {
                                "115": "overcast"
                            },
                            {
                                "116": "fine"
                            },
                            {
                                "1085": "partly_cloudy"
                            },
                            {
                                "1086": "snowmaking"
                            },
                            {
                                "1089": "inside"
                            }
                        ],
                        "Type": "multi_select",
                        "Order": 10
                    }
                },
                "Label": "conditions"
            },
            "user_info": {
                "Order": 11,
                "Questions": {
                    "patient_age": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "age",
                        "Values": "",
                        "Type": "patient_age",
                        "Order": 111
                    },
                    "name": {
                        "Placeholder": "firstname_lastname",
                        "Required": "true",
                        "Label": "name",
                        "Values": "",
                        "Type": "text",
                        "Order": 20
                    },
                    "suburb": {
                        "Placeholder": "city___suburb",
                        "Required": "true",
                        "Label": "suburb",
                        "Values": "",
                        "Type": "text",
                        "Order": 40
                    },
                    "dob": {
                        "Type": "date_picker",
                        "Required": "true",
                        "Values": "",
                        "Order": 110,
                        "Label": "Date of Birth"
                    },
                    "country": {
                        "Type": "select",
                        "Required": "true",
                        "Values": [
                            {
                                "Afghanistan": "afghanistan"
                            },
                            {
                                "Albania": "albania"
                            },
                            {
                                "Algeria": "algeria"
                            },
                            {
                                "American Samoa": "american_samoa"
                            },
                            {
                                "Angola": "angola"
                            },
                            {
                                "Anguilla": "anguilla"
                            },
                            {
                                "Antarctica": "antarctica"
                            },
                            {
                                "Antigua and Barbuda": "antigua_and_barbuda"
                            },
                            {
                                "Argentina": "argentina"
                            },
                            {
                                "Armenia": "armenia"
                            },
                            {
                                "Aruba": "aruba"
                            },
                            {
                                "Ashmore and Cartier Island": "ashmore_and_cartier_island"
                            },
                            {
                                "Australia": "australia"
                            },
                            {
                                "Austria": "austria"
                            },
                            {
                                "Azerbaijan": "azerbaijan"
                            },
                            {
                                "Bahamas": "the_bahamas"
                            },
                            {
                                "Bahrain": "bahrain"
                            },
                            {
                                "Bangladesh": "bangladesh"
                            },
                            {
                                "Barbados": "barbados"
                            },
                            {
                                "Belarus": "belarus"
                            },
                            {
                                "Belgium": "belgium"
                            },
                            {
                                "Belize": "belize"
                            },
                            {
                                "Benin": "benin"
                            },
                            {
                                "Bermuda": "bermuda"
                            },
                            {
                                "Bhutan": "bhutan"
                            },
                            {
                                "Bolivia": "bolivia"
                            },
                            {
                                "Bosnia and Herzegovina": "bosnia_and_herzegovina"
                            },
                            {
                                "Botswana": "botswana"
                            },
                            {
                                "Brazil": "brazil"
                            },
                            {
                                "British Virgin Islands": "british_virgin_islands"
                            },
                            {
                                "Brunei": "brunei"
                            },
                            {
                                "Bulgaria": "bulgaria"
                            },
                            {
                                "Burkina Faso": "burkina_faso"
                            },
                            {
                                "Burma": "Burma"
                            },
                            {
                                "Burundi": "burundi"
                            },
                            {
                                "Cambodia": "cambodia"
                            },
                            {
                                "Cameroon": "cameroon"
                            },
                            {
                                "Canada": "canada"
                            },
                            {
                                "Cape Verde": "cape_verde"
                            },
                            {
                                "Cayman Islands": "cayman_islands"
                            },
                            {
                                "Central African Republic": "central_african_republic"
                            },
                            {
                                "Chad": "chad"
                            },
                            {
                                "Chile": "chile"
                            },
                            {
                                "China": "china"
                            },
                            {
                                "Christmas Island": "christmas_island"
                            },
                            {
                                "Clipperton Island": "clipperton_island"
                            },
                            {
                                "Cocos (Keeling) Islands": "cocos_keeling_islands"
                            },
                            {
                                "Colombia": "colombia"
                            },
                            {
                                "Comoros": "comoros"
                            },
                            {
                                "Democratic Republic of the Congo": "democratic_republic_of_the_congo"
                            },
                            {
                                "Congo": "congo"
                            },
                            {
                                "Cook Islands": "cook_islands"
                            },
                            {
                                "Costa Rica": "costa_rica"
                            },
                            {
                                "Cote d'Ivoire": "cote_divoire"
                            },
                            {
                                "Croatia": "croatia"
                            },
                            {
                                "Cuba": "cuba"
                            },
                            {
                                "Cyprus": "cyprus"
                            },
                            {
                                "Czeck Republic": "czech_republic"
                            },
                            {
                                "Denmark": "denmark"
                            },
                            {
                                "Djibouti": "djibouti"
                            },
                            {
                                "Dominica": "dominica"
                            },
                            {
                                "Dominican Republic": "dominican_republic"
                            },
                            {
                                "Ecuador": "ecuador"
                            },
                            {
                                "Egypt": "egypt"
                            },
                            {
                                "El Salvador": "el_salvador"
                            },
                            {
                                "Equatorial Guinea": "equatorial_guinea"
                            },
                            {
                                "Eritrea": "eritrea"
                            },
                            {
                                "Estonia": "estonia"
                            },
                            {
                                "Ethiopia": "ethiopia"
                            },
                            {
                                "Europa Island": "europa_island"
                            },
                            {
                                "Falkland Islands (Islas Malvinas)": "falkland_islands_islas_malvinas"
                            },
                            {
                                "Faroe Islands": "faeroe_islands"
                            },
                            {
                                "Fiji": "fiji"
                            },
                            {
                                "Finland": "finland"
                            },
                            {
                                "France": "france"
                            },
                            {
                                "French Guiana": "french_guiana"
                            },
                            {
                                "French Polynesia": "french_polynesia"
                            },
                            {
                                "French Southern and Antarctic Lands": "french_southern_and_antarctic_lands"
                            },
                            {
                                "Gabon": "gabon"
                            },
                            {
                                "The Gambia": "the_gambia"
                            },
                            {
                                "Gaza Strip": "gaza_strip"
                            },
                            {
                                "Georgia": "georgia"
                            },
                            {
                                "Germany": "germany"
                            },
                            {
                                "Ghana": "ghana"
                            },
                            {
                                "Gibraltar": "gibraltar"
                            },
                            {
                                "Glorioso Islands": "glorioso_islands"
                            },
                            {
                                "Greece": "greece"
                            },
                            {
                                "Greenland": "greenland"
                            },
                            {
                                "Grenada": "grenada"
                            },
                            {
                                "Guadeloupe": "guadeloupe"
                            },
                            {
                                "Guam": "guam"
                            },
                            {
                                "Guatemala": "guatemala"
                            },
                            {
                                "Guernsey": "Guernsey"
                            },
                            {
                                "Guinea": "guinea"
                            },
                            {
                                "Guinea-Bissau": "guinea_bissau"
                            },
                            {
                                "Guyana": "guyana"
                            },
                            {
                                "Haiti": "haiti"
                            },
                            {
                                "Heard Island and McDonald Islands": "heard_island_and_mcdonald_islands"
                            },
                            {
                                "Honduras": "honduras"
                            },
                            {
                                "Hong Kong": "hong_kong"
                            },
                            {
                                "Howland Island": "howland_island"
                            },
                            {
                                "Hungary": "hungary"
                            },
                            {
                                "Iceland": "iceland"
                            },
                            {
                                "India": "india"
                            },
                            {
                                "Indonesia": "indonesia"
                            },
                            {
                                "Iran": "iran"
                            },
                            {
                                "Iraq": "iraq"
                            },
                            {
                                "Ireland": "ireland"
                            },
                            {
                                "Northern Ireland": "Northern Ireland"
                            },
                            {
                                "Israel": "israel"
                            },
                            {
                                "Italy": "italy"
                            },
                            {
                                "Jamaica": "jamaica"
                            },
                            {
                                "Jan Mayen": "jan_mayen"
                            },
                            {
                                "Japan": "japan"
                            },
                            {
                                "Jarvis Island": "jarvis_island"
                            },
                            {
                                "Jersey": "Jersey"
                            },
                            {
                                "Johnston Atoll": "johnston_atoll"
                            },
                            {
                                "Jordan": "jordan"
                            },
                            {
                                "Juan de Nova Island": "juan_de_nova_island"
                            },
                            {
                                "Kazakhstan": "kazakhstan"
                            },
                            {
                                "Kenya": "kenya"
                            },
                            {
                                "Kiribati": "kiribati"
                            },
                            {
                                "North Korea": "north_korea"
                            },
                            {
                                "South Korea": "south_korea"
                            },
                            {
                                "Kuwait": "kuwait"
                            },
                            {
                                "Kyrgyzstan": "kyrgyzstan"
                            },
                            {
                                "Laos": "laos"
                            },
                            {
                                "Latvia": "latvia"
                            },
                            {
                                "Lebanon": "lebanon"
                            },
                            {
                                "Lesotho": "lesotho"
                            },
                            {
                                "Liberia": "liberia"
                            },
                            {
                                "Libya": "libya"
                            },
                            {
                                "Liechtenstein": "liechtenstein"
                            },
                            {
                                "Lithuania": "lithuania"
                            },
                            {
                                "Luxembourg": "luxembourg"
                            },
                            {
                                "Macau": "macau"
                            },
                            {
                                "Former Yugoslav Republic of Macedonia": "former_yugoslav_republic_of_macedonia"
                            },
                            {
                                "Madagascar": "madagascar"
                            },
                            {
                                "Malawi": "malawi"
                            },
                            {
                                "Malaysia": "malaysia"
                            },
                            {
                                "Maldives": "maldives"
                            },
                            {
                                "Mali": "mali"
                            },
                            {
                                "Malta": "malta"
                            },
                            {
                                "Isle of Man": "isle_of_man"
                            },
                            {
                                "Marshall Islands": "marshall_islands"
                            },
                            {
                                "Martinique": "martinique"
                            },
                            {
                                "Mauritania": "mauritania"
                            },
                            {
                                "Mauritius": "mauritius"
                            },
                            {
                                "Mayotte": "mayotte"
                            },
                            {
                                "Mexico": "mexico"
                            },
                            {
                                "Micronesia": "micronesia"
                            },
                            {
                                "Midway Islands": "midway_islands"
                            },
                            {
                                "Moldova": "moldova"
                            },
                            {
                                "Monaco": "monaco"
                            },
                            {
                                "Mongolia": "mongolia"
                            },
                            {
                                "Montserrat": "montserrat"
                            },
                            {
                                "Morocco": "morocco"
                            },
                            {
                                "Mozambique": "mozambique"
                            },
                            {
                                "Namibia": "namibia"
                            },
                            {
                                "Nauru": "nauru"
                            },
                            {
                                "Nepal": "nepal"
                            },
                            {
                                "Netherlands": "netherlands"
                            },
                            {
                                "Netherlands Antilles": "netherlands_antilles"
                            },
                            {
                                "New Caledonia": "new_caledonia"
                            },
                            {
                                "New Zealand": "new_zealand"
                            },
                            {
                                "Nicaragua": "nicaragua"
                            },
                            {
                                "Niger": "niger"
                            },
                            {
                                "Nigeria": "nigeria"
                            },
                            {
                                "Niue": "niue"
                            },
                            {
                                "Norfolk Island": "norfolk_island"
                            },
                            {
                                "Northern Mariana Islands": "northern_mariana_islands"
                            },
                            {
                                "Norway": "norway"
                            },
                            {
                                "Oman": "oman"
                            },
                            {
                                "Pakistan": "pakistan"
                            },
                            {
                                "Palau": "palau"
                            },
                            {
                                "Panama": "panama"
                            },
                            {
                                "Papua New Guinea": "papua_new_guinea"
                            },
                            {
                                "Paraguay": "paraguay"
                            },
                            {
                                "Peru": "peru"
                            },
                            {
                                "Philippines": "philippines"
                            },
                            {
                                "Pitcairn Islands": "pitcairn_islands"
                            },
                            {
                                "Poland": "poland"
                            },
                            {
                                "Portugal": "portugal"
                            },
                            {
                                "Puerto Rico": "puerto_rico"
                            },
                            {
                                "Qatar": "qatar"
                            },
                            {
                                "Reunion": "reunion"
                            },
                            {
                                "Romania": "romania"
                            },
                            {
                                "Russia": "russia"
                            },
                            {
                                "Rwanda": "rwanda"
                            },
                            {
                                "Saint Helena": "saint_helena"
                            },
                            {
                                "Saint Kitts and Nevis": "saint_kitts_and_nevis"
                            },
                            {
                                "Saint Lucia": "saint_lucia"
                            },
                            {
                                "Saint Pierre and Miquelon": "saint_pierre_and_miquelon"
                            },
                            {
                                "Saint Vincent and the Grenadines": "saint_vincent_and_the_grenadines"
                            },
                            {
                                "Samoa": "samoa"
                            },
                            {
                                "San Marino": "san_marino"
                            },
                            {
                                "Sao Tome and Principe": "sao_tome_and_principe"
                            },
                            {
                                "Saudi Arabia": "saudi_arabia"
                            },
                            {
                                "Scotland": "scotland"
                            },
                            {
                                "Senegal": "senegal"
                            },
                            {
                                "Seychelles": "seychelles"
                            },
                            {
                                "Sierra Leone": "sierra_leone"
                            },
                            {
                                "Singapore": "singapore"
                            },
                            {
                                "Slovakia": "slovakia"
                            },
                            {
                                "Slovenia": "slovenia"
                            },
                            {
                                "Solomon Islands": "solomon_islands"
                            },
                            {
                                "Somalia": "somalia"
                            },
                            {
                                "South Africa": "south_africa"
                            },
                            {
                                "South Georgia and the South Sandwich Islands": "south_georgia_and_the_south_sandwich_islands"
                            },
                            {
                                "Spain": "spain"
                            },
                            {
                                "Spratly Islands": "spratly_islands"
                            },
                            {
                                "Sri Lanka": "sri_lanka"
                            },
                            {
                                "Sudan": "sudan"
                            },
                            {
                                "Suriname": "suriname"
                            },
                            {
                                "Svalbard": "svalbard"
                            },
                            {
                                "Swaziland": "swaziland"
                            },
                            {
                                "Sweden": "sweden"
                            },
                            {
                                "Switzerland": "switzerland"
                            },
                            {
                                "Syria": "syria"
                            },
                            {
                                "Taiwan": "taiwan"
                            },
                            {
                                "Tajikistan": "tajikistan"
                            },
                            {
                                "Tanzania": "tanzania"
                            },
                            {
                                "Thailand": "thailand"
                            },
                            {
                                "Toga": "toga"
                            },
                            {
                                "Tokelau": "tokelau"
                            },
                            {
                                "Tonga": "tonga"
                            },
                            {
                                "Trinidad and Tobadi": "trinidad_and_tobago"
                            },
                            {
                                "Tunisia": "tunisia"
                            },
                            {
                                "Turkey": "turkey"
                            },
                            {
                                "Turkmenistan": "turkmenistan"
                            },
                            {
                                "Tuvalu": "tuvalu"
                            },
                            {
                                "Uganda": "uganda"
                            },
                            {
                                "Ukraine": "ukraine"
                            },
                            {
                                "United Arab Emirates": "united_arab_emirates"
                            },
                            {
                                "United Kingdom": "united_kingdom"
                            },
                            {
                                "Uruguay": "uruguay"
                            },
                            {
                                "USA": "USA"
                            },
                            {
                                "Uzbekistan": "uzbekistan"
                            },
                            {
                                "Vanuatu": "vanuatu"
                            },
                            {
                                "Venezuela": "venezuela"
                            },
                            {
                                "Vietnam": "vietnam"
                            },
                            {
                                "US Virgin Islands": "us_virgin_islands"
                            },
                            {
                                "Wales": "wales"
                            },
                            {
                                "Wallis and Futuna": "wallis_and_futuna"
                            },
                            {
                                "West Bank": "west_bank"
                            },
                            {
                                "Western Sahara": "western_sahara"
                            },
                            {
                                "Yemen": "yemen"
                            },
                            {
                                "Yugoslavia": "yugoslavia"
                            },
                            {
                                "Zambia": "zambia"
                            },
                            {
                                "Zimbabwe": "zimbabwe"
                            }
                        ],
                        "Order": 70,
                        "Label": "country"
                    },
                    "sex": {
                        "Type": "gender",
                        "Required": "true",
                        "Values": [
                            {
                                "male": "male"
                            },
                            {
                                "female": "female"
                            }
                        ],
                        "Order": 10,
                        "Label": "sex"
                    },
                    "phone": {
                        "Placeholder": "phone",
                        "Required": "true",
                        "Label": "phone",
                        "Values": "",
                        "Type": "text",
                        "Order": 90
                    },
                    "state": {
                        "Placeholder": "state___province",
                        "Required": "true",
                        "Label": "state",
                        "Values": "",
                        "Type": "text",
                        "Order": 50
                    },
                    "postcode": {
                        "Placeholder": "postcode___zip_code",
                        "Required": "false",
                        "Label": "postcode___zip_code",
                        "Values": "",
                        "Type": "text",
                        "Order": 60
                    },
                    "address": {
                        "Placeholder": "no__street",
                        "Required": "true",
                        "Label": "address",
                        "Values": "",
                        "Type": "text",
                        "Order": 30
                    },
                    "local_accommodation": {
                        "Placeholder": "local_accommodation_info",
                        "Required": "false",
                        "Label": "local_accommodation",
                        "Values": "",
                        "Type": "text",
                        "Order": 120
                    },
                    "email": {
                        "Placeholder": "email",
                        "Required": "true",
                        "Label": "email",
                        "Values": "",
                        "Type": "email",
                        "Order": 80
                    },
                    "occupation": {
                        "Placeholder": "patient_occupation",
                        "Required": "false",
                        "Label": "occupation",
                        "Values": "",
                        "Type": "text",
                        "Order": 100
                    }
                },
                "Label": "patient_details"
            },
            "field_52d4798f6d229": {
                "Required": "false",
                "Order": 68,
                "Questions": {
                    "field_52d4798f6d227": {
                        "RepeatingQuestions": {
                            "preexisting_injury": {
                                "Placeholder": "",
                                "Required": "false",
                                "Label": "pre_existing_injury",
                                "Values": [
                                    {
                                        "234": "no"
                                    },
                                    {
                                        "817": "not_activity_related"
                                    },
                                    {
                                        "818": "activity_related"
                                    }
                                ],
                                "Type": "select",
                                "Order": 3
                            },
                            "body_part": {
                                "Placeholder": "",
                                "Required": "true",
                                "Label": "body_part",
                                "Values": [
                                    {
                                        "19": "head"
                                    },
                                    {
                                        "129": "face"
                                    },
                                    {
                                        "148": "teeth"
                                    },
                                    {
                                        "20": "neck"
                                    },
                                    {
                                        "1428": "clavicle"
                                    },
                                    {
                                        "130": "shoulder"
                                    },
                                    {
                                        "21": "upper_back"
                                    },
                                    {
                                        "131": "chest"
                                    },
                                    {
                                        "145": "ribs"
                                    },
                                    {
                                        "132": "upper_arm"
                                    },
                                    {
                                        "143": "elbow"
                                    },
                                    {
                                        "146": "forearm"
                                    },
                                    {
                                        "133": "lower_arm"
                                    },
                                    {
                                        "135": "wrist"
                                    },
                                    {
                                        "134": "hand"
                                    },
                                    {
                                        "151": "fingers"
                                    },
                                    {
                                        "150": "thumb"
                                    },
                                    {
                                        "149": "lower_back"
                                    },
                                    {
                                        "136": "abdomen"
                                    },
                                    {
                                        "144": "groin___pelvis"
                                    },
                                    {
                                        "137": "hip"
                                    },
                                    {
                                        "141": "buttock"
                                    },
                                    {
                                        "138": "upper_leg"
                                    },
                                    {
                                        "140": "knee"
                                    },
                                    {
                                        "139": "lower_leg"
                                    },
                                    {
                                        "142": "ankle"
                                    },
                                    {
                                        "147": "foot"
                                    }
                                ],
                                "Type": "select",
                                "Order": 1
                            },
                            "injury_location": {
                                "Placeholder": "",
                                "Required": "true",
                                "Label": "injury_location",
                                "Values": [
                                    {
                                        "152": "front"
                                    },
                                    {
                                        "153": "left"
                                    },
                                    {
                                        "154": "right"
                                    },
                                    {
                                        "155": "back"
                                    }
                                ],
                                "Type": "arrows",
                                "Order": 0
                            },
                            "injury_type": {
                                "Placeholder": "",
                                "Required": "true",
                                "Label": "injury_type",
                                "Values": [
                                    {
                                        "157": "sprain"
                                    },
                                    {
                                        "158": "strain"
                                    },
                                    {
                                        "41": "open_fracture"
                                    },
                                    {
                                        "42": "closed_fracture"
                                    },
                                    {
                                        "39": "dislocation"
                                    },
                                    {
                                        "33": "pain"
                                    },
                                    {
                                        "34": "swelling"
                                    },
                                    {
                                        "35": "bruising"
                                    },
                                    {
                                        "161": "tenderness"
                                    },
                                    {
                                        "36": "laceration"
                                    },
                                    {
                                        "159": "abrasion"
                                    },
                                    {
                                        "166": "concussion"
                                    },
                                    {
                                        "165": "unconscious"
                                    },
                                    {
                                        "163": "difficulty_breathing"
                                    },
                                    {
                                        "164": "heart"
                                    },
                                    {
                                        "169": "asthma"
                                    },
                                    {
                                        "168": "hypoglycaemia"
                                    },
                                    {
                                        "160": "hypothermia"
                                    },
                                    {
                                        "38": "shock"
                                    },
                                    {
                                        "162": "nausea"
                                    },
                                    {
                                        "37": "burns"
                                    },
                                    {
                                        "1090": "epilepsy_convulsion"
                                    }
                                ],
                                "Type": "select",
                                "Order": 2
                            }
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "injuries",
                        "Values": "",
                        "Type": "repeater",
                        "Order": 30
                    },
                    "field_52ca445d62ba6": {
                        "Placeholder": "symptoms_hint",
                        "Required": "false",
                        "Label": "symptoms",
                        "Values": "",
                        "Type": "text",
                        "Order": 20
                    },
                    "field_52ca445d62bb6": {
                        "Placeholder": "signs_hint",
                        "Required": "false",
                        "Label": "signs",
                        "Values": "",
                        "Type": "text",
                        "Order": 10
                    }
                },
                "Label": "injuries"
            },
            "field_52d4767cde30d": {
                "RepeatingQuestions": {
                    "vitals_timer": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "timer",
                        "Values": "",
                        "Type": "timer",
                        "Order": 5
                    },
                    "pain_score": {
                        "Type": "number",
                        "Min": 1,
                        "Max": 10,
                        "Required": "true",
                        "Label": "pain_score",
                        "Values": "",
                        "Placeholder": "pain_out_of_10",
                        "Order": 10,
                        "Append": ""
                    },
                    "respiration_rate": {
                        "Type": "number",
                        "Min": 0,
                        "Max": 200,
                        "Required": "true",
                        "Label": "breathing",
                        "Values": "",
                        "Placeholder": "RPM",
                        "Order": 7,
                        "Append": ""
                    },
                    "gcs_eye": {
                        "Type": "range",
                        "Min": 1,
                        "Max": 4,
                        "Required": "true",
                        "Label": "gcs_eyes",
                        "Values": "",
                        "Increment": 1,
                        "Placeholder": "",
                        "Order": 1
                    },
                    "skin_colour": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "skin_colour",
                        "Values": "",
                        "Type": "text",
                        "Order": 11
                    },
                    "blood_pressure": {
                        "Placeholder": "sys_dia",
                        "Required": "false",
                        "Label": "blood_pressure",
                        "Values": "",
                        "Type": "text",
                        "Order": 9
                    },
                    "gcs": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "gcs",
                        "Values": "",
                        "Type": "message",
                        "Order": 0
                    },
                    "heart_rate": {
                        "Type": "number",
                        "Min": 0,
                        "Max": 217,
                        "Required": "true",
                        "Label": "pulse",
                        "Values": "",
                        "Placeholder": "BPM",
                        "Order": 6,
                        "Append": ""
                    },
                    "gcs_verbal": {
                        "Type": "range",
                        "Min": 1,
                        "Max": 5,
                        "Required": "true",
                        "Label": "gcs_verbal",
                        "Values": "",
                        "Increment": 1,
                        "Placeholder": "",
                        "Order": 3
                    },
                    "sp02": {
                        "Placeholder": "%",
                        "Required": "false",
                        "Label": "sp02",
                        "Values": "",
                        "Type": "number",
                        "Order": 8,
                        "Append": "%"
                    },
                    "date_added": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "date_added",
                        "Values": "",
                        "Type": "date_time_picker",
                        "Order": 12
                    },
                    "pulse_breathing": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "pulse__breathing",
                        "Values": "",
                        "Type": "message",
                        "Order": 4
                    },
                    "gcs_motor": {
                        "Type": "range",
                        "Min": 1,
                        "Max": 6,
                        "Required": "true",
                        "Label": "gcs_motor",
                        "Values": "",
                        "Increment": 1,
                        "Placeholder": "",
                        "Order": 2
                    }
                },
                "Required": "false",
                "Order": 62,
                "Label": "vitals"
            },
            "field_52d47aac9bd13": {
                "RepeatingQuestions": {
                    "incident_role": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "Incident Role",
                        "Values": [
                            {
                                "170": "first_responder"
                            },
                            {
                                "171": "secondary"
                            },
                            {
                                "172": "assistant"
                            },
                            {
                                "173": "transport_assist"
                            },
                            {
                                "174": "base_assist"
                            }
                        ],
                        "Type": "select",
                        "Order": 1
                    },
                    "patroller": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "Patroller",
                        "Values": [
                            {
                                "e439c04a-bc53-43fb-92a1-3cdc3eed17f0": "Duncan Isac"
                            },
                            {
                                "ac1dfe9f-d067-4d09-94c5-dbad0db0f513": "Fake Patroller"
                            },
                            {
                                "f7409e6b-64d7-440e-b4b8-5c34c0586ff2": "Mr Roberts"
                            },
                            {
                                "58595bfa-04f9-474c-a0ed-7112cbef41fb": "Jimit Shah"
                            },
                            {
                                "a691e551-adbb-48d1-baa6-6dc0f0a2e7e3": "Jim geek"
                            },
                            {
                                "9f344a80-4987-4b87-90e5-c0611b9342ed": "Jimit Shah"
                            },
                            {
                                "186c8bca-7980-45f9-88b0-e852c62dd829": "Jim"
                            },
                            {
                                "aaba3d9b-9830-45cb-9c08-336d893552b9": "Jimi"
                            },
                            {
                                "b26ea016-0ca5-4e5a-a86d-9318048049f4": "dfds"
                            }
                        ],
                        "Type": "select",
                        "Order": 0
                    }
                },
                "Required": "false",
                "Order": 84,
                "Label": "Patrollers"
            },
            "field_52ca419f0a16e": {
                "Order": 67,
                "Questions": {
                    "field_52dabradbe4": {
                        "ShowIf": {
                            "field_52dabradbe2": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "lift_area",
                        "Values": [
                            {
                                "1111": "load"
                            },
                            {
                                "1112": "unload"
                            },
                            {
                                "1113": "lift_line"
                            },
                            {
                                "85": "lift_riding"
                            }
                        ],
                        "Type": "select",
                        "Order": 62
                    },
                    "field_52dabradbe2": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "lift_related",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 60
                    },
                    "field_52dabradbe3": {
                        "ShowIf": {
                            "field_52dabradbe2": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "lift_name",
                        "Values": "",
                        "Type": "text",
                        "Order": 61
                    },
                    "field_84d435ysr6dbe2": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "walk_in",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 20
                    },
                    "field_52d47eer6dbe2": {
                        "Placeholder": "enter_patients_description_of_incident",
                        "Required": "false",
                        "Label": "patient_description",
                        "Values": "",
                        "Type": "textarea",
                        "Order": 30
                    },
                    "field_52d435ysr6dbe4": {
                        "ShowIf": {
                            "field_52d435ysr6dbe2": "yes"
                        },
                        "Placeholder": "anyone_else_or_thing",
                        "Required": "false",
                        "Label": "what_who",
                        "Values": "",
                        "Type": "text",
                        "Order": 51
                    },
                    "field_52d435ysr6dbe2": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "other_involved",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 50
                    },
                    "field_52ca447762ba2": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "type",
                        "Values": [
                            {
                                "64": "loss_of_control"
                            },
                            {
                                "65": "fall_on_surface"
                            },
                            {
                                "66": "collision_w__man_made_object"
                            },
                            {
                                "87": "collision_w__natural_object"
                            },
                            {
                                "67": "collision_with_person"
                            },
                            {
                                "1114": "collision_with_snowboarder"
                            },
                            {
                                "1115": "collision_with_skier"
                            },
                            {
                                "89": "collision_w__lift"
                            },
                            {
                                "90": "collision_riding_tbar_button_lift"
                            },
                            {
                                "92": "collision_skidoo"
                            },
                            {
                                "93": "collision_oversnow_vehicle"
                            },
                            {
                                "88": "other_person_not_a_collision"
                            },
                            {
                                "81": "kids_ski_school"
                            },
                            {
                                "82": "jump"
                            },
                            {
                                "86": "poor_visibility"
                            },
                            {
                                "91": "medical"
                            },
                            {
                                "213": "inadvertent_binding_release"
                            },
                            {
                                "214": "impact_with_snow_ice"
                            },
                            {
                                "1068": "slip_trip_or_fall"
                            },
                            {
                                "1116": "twisting_fall"
                            },
                            {
                                "1098": "catching_edge"
                            },
                            {
                                "1099": "surface_change"
                            },
                            {
                                "1117": "other"
                            }
                        ],
                        "Type": "multi_select",
                        "Order": 10
                    },
                    "field_52d53eer6dbe2": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "speed",
                        "Values": [
                            {
                                "1082": "slow"
                            },
                            {
                                "1083": "medium"
                            },
                            {
                                "1084": "fast"
                            }
                        ],
                        "Type": "select",
                        "Order": 40
                    }
                },
                "Label": "incident"
            },
            "field_52ca426c0a178": {
                "Order": 86,
                "Questions": {
                    "field_52d47da6edbde": {
                        "ShowIf": {
                            "field_52d47d7fedbdd": "yes"
                        },
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "guardian_name",
                        "Values": "",
                        "Type": "text",
                        "Order": 30
                    },
                    "field_539158b37814e": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "did_you_purchase_ticket",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            },
                            {
                                "unknown": "unknown"
                            }
                        ],
                        "Type": "radio_button",
                        "Default": "unknown",
                        "Order": 70
                    },
                    "field_539158b37814f": {
                        "ShowIf": {
                            "field_539158b37814e": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "ticket_purchase_point",
                        "Values": [
                            {
                                "1395": "online"
                            },
                            {
                                "1396": "recharge"
                            },
                            {
                                "1397": "point_of_sale"
                            },
                            {
                                "1398": "third_party"
                            }
                        ],
                        "Type": "select",
                        "Order": 80
                    },
                    "field_52dd8a24e95a6": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "has_insurance",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            },
                            {
                                "unknown": "unknown"
                            }
                        ],
                        "Type": "radio_button",
                        "Default": "unknown",
                        "Order": 60
                    },
                    "field_52d47d6aedbdc": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "patient___guardian_signature",
                        "Values": "",
                        "Type": "signature",
                        "Order": 10
                    },
                    "field_52d47d7fedbdd": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "patient_under_18",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 20
                    },
                    "field_539158b37754f": {
                        "ShowIf": {
                            "field_539158b37814e": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "third_party_name",
                        "Values": "",
                        "Type": "text",
                        "Order": 90
                    },
                    "field_53c386190a2dd": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "know_the_arc",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            },
                            {
                                "unknown": "unknown"
                            }
                        ],
                        "Type": "radio_button",
                        "Default": "unknown",
                        "Order": 50
                    },
                    "field_5334b101c8779": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "privacy_statement_given",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            },
                            {
                                "unknown": "unknown"
                            }
                        ],
                        "Type": "radio_button",
                        "Default": "unknown",
                        "Order": 40
                    }
                },
                "Label": "signature"
            },
            "field_52ca425e0a176": {
                "Order": 81,
                "Questions": {
                    "field_89175a06a08f6": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "destination",
                        "Values": [
                            {
                                "1091": "home"
                            },
                            {
                                "1092": "village"
                            },
                            {
                                "1093": "local_accommodation"
                            },
                            {
                                "1094": "doctor"
                            },
                            {
                                "1095": "hospital"
                            }
                        ],
                        "Type": "select",
                        "Order": 40
                    },
                    "field_539158987517d": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "courtesy_transport",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 10
                    },
                    "field_53915a06a08f6": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "from_base",
                        "Values": [
                            {
                                "513": "company_vehicle"
                            },
                            {
                                "512": "taxi"
                            },
                            {
                                "511": "private_car"
                            },
                            {
                                "45": "ambulance"
                            },
                            {
                                "47": "helicopter"
                            },
                            {
                                "198": "bus"
                            },
                            {
                                "501": "unknown"
                            },
                            {
                                "820": "walk_or_ski_away"
                            },
                            {
                                "821": "walk_away"
                            }
                        ],
                        "Type": "multi_select",
                        "Order": 30
                    },
                    "field_52ca4c34ef1a1": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "to_first_aid",
                        "Values": [
                            {
                                "44": "akja_cascade_sled"
                            },
                            {
                                "45": "ambulance"
                            },
                            {
                                "46": "groomer"
                            },
                            {
                                "47": "helicopter"
                            },
                            {
                                "48": "lift"
                            },
                            {
                                "49": "self"
                            },
                            {
                                "50": "ski_patrol_vehicle"
                            },
                            {
                                "51": "skidoo_trailer_akja"
                            },
                            {
                                "198": "bus"
                            },
                            {
                                "223": "funicular"
                            },
                            {
                                "224": "gondola"
                            },
                            {
                                "225": "argo"
                            },
                            {
                                "226": "skidoo_no_trailer"
                            },
                            {
                                "1075": "company_vehicle"
                            },
                            {
                                "1076": "oversnow_ambulance"
                            },
                            {
                                "1418": "fourwd_vehicle"
                            },
                            {
                                "1419": "oversnow_tracked_vehicle"
                            },
                            {
                                "1420": "train"
                            },
                            {
                                "1421": "wheelchair"
                            },
                            {
                                "1422": "gurney"
                            }
                        ],
                        "Type": "multi_select",
                        "Order": 20
                    }
                },
                "Label": "transport"
            },
            "field_52ca41790a16c": {
                "Order": 12,
                "Questions": {
                    "field_52dd8c049b005": {
                        "Type": "weight",
                        "Min": 1,
                        "Max": 400,
                        "Required": "false",
                        "Label": "weight",
                        "Values": "",
                        "Placeholder": "",
                        "Order": 105
                    },
                    "field_52ca3fe959d2a": {
                        "ShowIf": {
                            "field_52ca3fcc59d29": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "alcohol_when",
                        "Values": "",
                        "Type": "text",
                        "Order": 490
                    },
                    "field_52ca3f8c59d26": {
                        "Type": "decimal",
                        "Min": 1,
                        "Max": 20,
                        "Required": "false",
                        "Label": "back_right_din",
                        "Values": "",
                        "Placeholder": "back_right_din_placeholder",
                        "Order": 370,
                        "Append": ""
                    },
                    "field_52ca3dfcac438": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "ability",
                        "Values": [
                            {
                                "227": "first_day"
                            },
                            {
                                "228": "first_week"
                            },
                            {
                                "229": "one_to_four_weeks"
                            },
                            {
                                "230": "four_to_eight_weeks"
                            },
                            {
                                "231": "eight_weeks"
                            },
                            {
                                "63": "patroller"
                            },
                            {
                                "233": "instructor"
                            }
                        ],
                        "Type": "select",
                        "Order": 170
                    },
                    "field_52ca44c862ba4": {
                        "ShowIf": {
                            "field_52ca449b62ba3": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "instructor_name",
                        "Values": "",
                        "Type": "text",
                        "Order": 150
                    },
                    "field_52d84412ef10c": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "snowboard_bindings",
                        "Values": [
                            {
                                "210": "goofy"
                            },
                            {
                                "211": "regular"
                            }
                        ],
                        "Type": "select",
                        "Order": 330
                    },
                    "field_52ca42f362b99": {
                        "ShowIf": {
                            "field_54b0869fefc8c": "yes"
                        },
                        "Placeholder": "name_and_address",
                        "Required": "false",
                        "Label": "rental_shop",
                        "Values": "",
                        "Type": "text",
                        "Order": 390
                    },
                    "field_52dd8a0ce95a5": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "ski_bindings",
                        "Values": "",
                        "Type": "message",
                        "Order": 320
                    },
                    "field_532ff8dc99f5e": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "experience",
                        "Values": "",
                        "Type": "message",
                        "Order": 130
                    },
                    "field_52ca3dc8ac437": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "activity",
                        "Values": [
                            {
                                "69": "skiing"
                            },
                            {
                                "433": "snowboard"
                            },
                            {
                                "68": "toboganning"
                            },
                            {
                                "70": "telemark"
                            },
                            {
                                "71": "cross_country"
                            },
                            {
                                "72": "snow_shoe"
                            },
                            {
                                "73": "walking"
                            },
                            {
                                "128": "mountain_biking"
                            },
                            {
                                "434": "adaptive"
                            },
                            {
                                "199": "blades_no_release"
                            },
                            {
                                "200": "blades_with_release"
                            }
                        ],
                        "Type": "select",
                        "Order": 120
                    },
                    "field_54b083c3ac7a9": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "binding_model",
                        "Values": "",
                        "Type": "text",
                        "Order": 300
                    },
                    "field_52ca449b62ba3": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "ski_school",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 140
                    },
                    "field_52ca3f8e59d28": {
                        "Type": "decimal",
                        "Min": 1,
                        "Max": 20,
                        "Required": "false",
                        "Label": "back_left_din",
                        "Values": "",
                        "Placeholder": "back_left_din_placeholder",
                        "Order": 350,
                        "Append": ""
                    },
                    "field_52d4888a5b643": {
                        "Type": "number",
                        "Min": 1,
                        "Max": 12,
                        "Required": "true",
                        "Label": "hours_today",
                        "Values": "",
                        "Placeholder": "eg_2",
                        "Order": 200,
                        "Append": "hours"
                    },
                    "field_52ca999b62ba3": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "familiar_with_this_run",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 180
                    },
                    "field_54b083b2ac7a8": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "binding_make",
                        "Values": "",
                        "Type": "text",
                        "Order": 290
                    },
                    "field_52ca43f362ba0": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "glasses___lenses_required",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            },
                            {
                                "unknown": "unknown"
                            }
                        ],
                        "Type": "radio_button",
                        "Default": "unknown",
                        "Order": 590
                    },
                    "field_530fc0074291e": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "medical_history",
                        "Values": "",
                        "Type": "message",
                        "Order": 420
                    },
                    "field_54b087ef13f99": {
                        "ShowIf": {
                            "field_54b0869fefc8c": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "bootno",
                        "Values": "",
                        "Type": "text",
                        "Order": 410
                    },
                    "field_52ca43c462b9f": {
                        "ShowIf": {
                            "field_52ca43f362ba0": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "glasses___contact_lenses_worn",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 600
                    },
                    "field_5530f7ccd3d86": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "medic_alert",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 430
                    },
                    "field_52ca404059d2b": {
                        "ShowIf": {
                            "field_52ca3fcc59d29": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "alcohol_what",
                        "Values": "",
                        "Type": "text",
                        "Order": 480
                    },
                    "field_54b085452d256": {
                        "ShowIf": {
                            "field_52ca430462b9a": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "helmet_rental_no",
                        "Values": "",
                        "Type": "text",
                        "Order": 270
                    },
                    "field_5386e4e216667": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "pass_type",
                        "Values": [
                            {
                                "496": "day_ticket"
                            },
                            {
                                "497": "multi_day_ticket"
                            },
                            {
                                "498": "season_pass"
                            },
                            {
                                "499": "other_pass"
                            },
                            {
                                "500": "not_applicable"
                            },
                            {
                                "501": "unknown"
                            }
                        ],
                        "Type": "select",
                        "Order": 110
                    },
                    "field_52d488615b642": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "lessons",
                        "Values": [
                            {
                                "237": "none"
                            },
                            {
                                "238": "one_five_lessons"
                            },
                            {
                                "239": "six_ten_lessons"
                            },
                            {
                                "240": "ten_lessons"
                            }
                        ],
                        "Type": "select",
                        "Order": 160
                    },
                    "field_52d47f058205b": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "allergies",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 450
                    },
                    "field_52ca407959d2d": {
                        "ShowIf": {
                            "field_52ca405959d2c": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "medication_what",
                        "Values": "",
                        "Type": "text",
                        "Order": 540
                    },
                    "field_52dd8bee9b004": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "height",
                        "Values": "",
                        "Type": "height",
                        "Order": 106,
                        "Append": "cm"
                    },
                    "field_52ca430462b9a": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "helmet_worn",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            },
                            {
                                "unknown": "unknown"
                            }
                        ],
                        "Type": "radio_button",
                        "Default": "unknown",
                        "Order": 240
                    },
                    "field_52dd8a57e95a7": {
                        "ShowIf": {
                            "field_52ca430462b9a": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "helmet_brand",
                        "Values": "",
                        "Type": "text",
                        "Order": 250
                    },
                    "field_52d484ebef10b": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "removed_by",
                        "Values": [
                            {
                                "49": "self"
                            },
                            {
                                "62": "bystander"
                            },
                            {
                                "63": "patroller"
                            },
                            {
                                "203": "fall"
                            }
                        ],
                        "Type": "select",
                        "Order": 232
                    },
                    "field_52d155b6549d0": {
                        "Type": "number",
                        "Min": 1,
                        "Max": 100,
                        "Required": "true",
                        "Label": "years_experience",
                        "Values": "",
                        "Placeholder": "eg_20",
                        "Order": 225,
                        "Append": "years"
                    },
                    "field_52ca3e17ac439": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "source",
                        "Values": [
                            {
                                "77": "owned"
                            },
                            {
                                "76": "external_rental"
                            },
                            {
                                "201": "ski_area_rental"
                            },
                            {
                                "502": "ski_area_demo"
                            },
                            {
                                "503": "external_demo"
                            },
                            {
                                "78": "borrowed"
                            }
                        ],
                        "Type": "select",
                        "Order": 231
                    },
                    "field_52ca429c62b98": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "wristguards_worn",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            },
                            {
                                "unknown": "unknown"
                            }
                        ],
                        "Type": "radio_button",
                        "Default": "unknown",
                        "Order": 237
                    },
                    "field_52ca405959d2c": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "medication",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            },
                            {
                                "unknown": "unknown"
                            }
                        ],
                        "Type": "radio_button",
                        "Default": "unknown",
                        "Order": 530
                    },
                    "field_5530f7edd3d87": {
                        "ShowIf": {
                            "field_5530f7ccd3d86": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "medic_alert_details",
                        "Values": "",
                        "Type": "text",
                        "Order": 440
                    },
                    "field_52ca407a59d2e": {
                        "ShowIf": {
                            "field_52ca405959d2c": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "medication_when",
                        "Values": "",
                        "Type": "text",
                        "Order": 550
                    },
                    "field_52d488b6573b0": {
                        "Type": "number",
                        "Min": 1,
                        "Max": 365,
                        "Required": "true",
                        "Label": "season_days",
                        "Values": "",
                        "Placeholder": "eg_20",
                        "Order": 220,
                        "Append": "days"
                    },
                    "field_52ca438f62b9e": {
                        "ShowIf": {
                            "field_52ca437b62b9c": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "drugs_when",
                        "Values": "",
                        "Type": "text",
                        "Order": 520
                    },
                    "field_52ca3d31ac436": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "customer_type",
                        "Values": [
                            {
                                "79": "staff"
                            },
                            {
                                "80": "guest"
                            },
                            {
                                "103": "competitor"
                            },
                            {
                                "495": "staff_off_work"
                            }
                        ],
                        "Type": "select",
                        "Order": 100
                    },
                    "field_54b0869fefc8c": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "rental",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 380
                    },
                    "field_52d483dceb786": {
                        "ShowIf": {
                            "field_52ca429c62b98": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "wristguard_type",
                        "Values": [
                            {
                                "204": "short_guard"
                            },
                            {
                                "205": "long_guard"
                            },
                            {
                                "206": "palm_side"
                            },
                            {
                                "207": "back_of_wrist"
                            },
                            {
                                "208": "rigid"
                            },
                            {
                                "209": "flexible"
                            },
                            {
                                "212": "built_into_glove"
                            },
                            {
                                "1087": "on_top_of_glove"
                            },
                            {
                                "1088": "underneath_glove"
                            }
                        ],
                        "Type": "multi_select",
                        "Order": 238
                    },
                    "field_53f5cabe56646": {
                        "Type": "number",
                        "Min": 1,
                        "Max": 365,
                        "Required": "false",
                        "Label": "days_in_this_resort",
                        "Values": "",
                        "Placeholder": "eg_10",
                        "Order": 210,
                        "Append": "days"
                    },
                    "field_52d47ef08205a": {
                        "ShowIf": {
                            "field_52d47f058205b": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "allergies_what",
                        "Values": "",
                        "Type": "text",
                        "Order": 460
                    },
                    "field_52ca3f8d59d27": {
                        "Type": "number",
                        "Min": 1,
                        "Max": 20,
                        "Required": "false",
                        "Label": "front_right_din",
                        "Values": "",
                        "Placeholder": "front_right_din_placeholder",
                        "Order": 360,
                        "Append": ""
                    },
                    "field_530fbff54291d": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "equipment_details",
                        "Values": "",
                        "Type": "message",
                        "Order": 230
                    },
                    "field_52ca438e62b9d": {
                        "ShowIf": {
                            "field_52ca437b62b9c": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "drugs_what",
                        "Values": "",
                        "Type": "text",
                        "Order": 510
                    },
                    "field_52ca437b62b9c": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "drugs_taken",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            },
                            {
                                "unknown": "unknown"
                            }
                        ],
                        "Type": "radio_button",
                        "Default": "unknown",
                        "Order": 500
                    },
                    "field_52d48512ef10c": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "binding_releases",
                        "Values": [
                            {
                                "219": "left_yes"
                            },
                            {
                                "220": "left_no"
                            },
                            {
                                "217": "right_yes"
                            },
                            {
                                "218": "right_no"
                            },
                            {
                                "216": "snowblades"
                            }
                        ],
                        "Type": "multi_select",
                        "Order": 330
                    },
                    "field_52ca3fcc59d29": {
                        "Placeholder": "",
                        "Required": "true",
                        "Label": "alchohol",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            },
                            {
                                "unknown": "unknown"
                            }
                        ],
                        "Type": "radio_button",
                        "Default": "unknown",
                        "Order": 470
                    },
                    "field_54b087d913f98": {
                        "ShowIf": {
                            "field_54b0869fefc8c": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "ski___board_no",
                        "Values": "",
                        "Type": "text",
                        "Order": 400
                    },
                    "field_52ca407646d2d": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "medical_history",
                        "Values": "",
                        "Type": "text",
                        "Order": 560
                    },
                    "field_52ca3ef759d23": {
                        "Type": "number",
                        "Min": 1,
                        "Max": 20,
                        "Required": "false",
                        "Label": "front_left_din",
                        "Values": "",
                        "Placeholder": "front_left_din_placeholder",
                        "Order": 340,
                        "Append": ""
                    },
                    "field_52ca431e62b9b": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "body_armour_worn",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            },
                            {
                                "unknown": "unknown"
                            }
                        ],
                        "Type": "radio_button",
                        "Default": "unknown",
                        "Order": 280
                    },
                    "field_52cfg407646d2d": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "last_meal",
                        "Values": "",
                        "Type": "text",
                        "Order": 570
                    },
                    "field_54b084fb2d255": {
                        "ShowIf": {
                            "field_52ca430462b9a": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "helmet_area_rental",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 260
                    },
                    "field_52ca988b62ba3": {
                        "ShowIf": {
                            "field_52ca999b62ba3": "yes"
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "how_many_time_before",
                        "Values": "",
                        "Type": "text",
                        "Order": 190
                    }
                },
                "Label": "patient_history"
            },
            "field_52ca42230a171": {
                "Order": 69,
                "Questions": {
                    "field_52ca445d62ba1": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "treatments",
                        "Values": [
                            {
                                "22": "air_splint"
                            },
                            {
                                "23": "box_splint"
                            },
                            {
                                "102": "traction_splint"
                            },
                            {
                                "1073": "vacuum_splint"
                            },
                            {
                                "94": "angle_splint"
                            },
                            {
                                "98": "sam_splint"
                            },
                            {
                                "1069": "cascade_wrap"
                            },
                            {
                                "24": "defibrillator"
                            },
                            {
                                "1072": "code_crash_pack"
                            },
                            {
                                "27": "geudel_airway"
                            },
                            {
                                "25": "backboard"
                            },
                            {
                                "99": "scoop"
                            },
                            {
                                "26": "cervical_collar"
                            },
                            {
                                "28": "dressing"
                            },
                            {
                                "29": "elevate"
                            },
                            {
                                "30": "reassure"
                            },
                            {
                                "32": "ice"
                            },
                            {
                                "97": "pressure"
                            },
                            {
                                "101": "sling"
                            },
                            {
                                "1100": "blanket"
                            },
                            {
                                "1070": "guerney"
                            },
                            {
                                "100": "seek_medical_attention"
                            },
                            {
                                "1101": "no_treatment"
                            }
                        ],
                        "Type": "multi_select",
                        "Order": 20
                    },
                    "field_52d4800164f2e": {
                        "RepeatingQuestions": {
                            "drug_administered": {
                                "Placeholder": "",
                                "Required": "true",
                                "Label": "drug",
                                "Values": [
                                    {
                                        "31": "entonox"
                                    },
                                    {
                                        "95": "oxygen"
                                    },
                                    {
                                        "96": "penthrane"
                                    },
                                    {
                                        "1074": "ventolin"
                                    },
                                    {
                                        "1408": "asprin"
                                    }
                                ],
                                "Type": "select",
                                "Order": 0
                            },
                            "drug_time_administered": {
                                "Placeholder": "",
                                "Required": "false",
                                "Label": "time_administered",
                                "Values": "",
                                "Type": "date_time_picker",
                                "Order": 3
                            },
                            "drug_volume_administered": {
                                "Placeholder": "",
                                "Required": "true",
                                "Label": "volume",
                                "Values": [
                                    {
                                        "527": "miligrams_mg"
                                    },
                                    {
                                        "528": "litres_lt"
                                    },
                                    {
                                        "530": "millilitres_ml"
                                    }
                                ],
                                "Type": "select",
                                "Order": 2
                            },
                            "dose_administered": {
                                "Placeholder": "",
                                "Required": "true",
                                "Label": "dose",
                                "Values": "",
                                "Type": "number",
                                "Order": 1,
                                "Append": ""
                            }
                        },
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "drugs_administered",
                        "Values": "",
                        "Type": "repeater",
                        "Order": 30
                    },
                    "field_539158b37517e": {
                        "Placeholder": "",
                        "Required": "false",
                        "Label": "refused_care",
                        "Values": [
                            {
                                "yes": "yes"
                            },
                            {
                                "no": "no"
                            }
                        ],
                        "Type": "radio",
                        "Order": 10
                    }
                },
                "Label": "treatment"
            }
        }
    }


class UserResortMapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserResortMap
        django_get_or_create = ('user', 'resort')

    role_id = UserRolesFactory(key='dispatcher').role_id
    user = UserFactory()
    resort = ResortFactory()
