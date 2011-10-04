'use strict';


angular.module('app')
    .controller('ConfirmRegenerateModalCtrl', ['$scope', '$modalInstance', function ($scope, $modalInstance) {

        $scope.ok = function () {
            $modalInstance.close(true);
        };

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
    }])
    .controller('ResortSettingsCtrl', ['$scope', '$location', '$state', '$rootScope', '$timeout', '$log', '$stateParams', '$intercom', 'ResortService', 'currentUser', 'growl', 'questions', '$translate', '$uimodal',  function ($scope, $location, $state, $rootScope, $timeout, $log, $stateParams, $intercom, ResortService, currentUser, growl, questions, $translate, $modal) {

        //$intercom.update({
        //    email: currentUser.email,
        //    name: currentUser.name,
        //    created_at: new Date(),
        //    user_id: currentUser.user_id,
        //    company: {
        //        id: currentUser.resorts[0].resort_id,
        //        name: currentUser.resorts[0].resort_name
        //    },
        //    role: currentUser.role_id[0].key,
        //    dashboard_feature_last_used: "Users"
        //});

        $scope.currentUser = currentUser;
        //$scope.showRole = false;
        //$scope.showPermissions = false;
        //$scope.showDeleteUser = false;

        var id = $stateParams.resortId;


        $scope.roles = [
            {key: 1, name: 'Patroller'},
            {key: 2, name: 'Dispatcher'},
            {key: 3, name: 'Manager'}
        ];

        $scope.paper_sizes = [
            {key: 0, name: 'A4'},
            {key: 1, name: 'US Paper'}
        ];

        $scope.unit_formats = [
            {key: 0, name: 'Imperial'},
            {key: 1, name: 'Metric'}
        ];

        $scope.datetime_formats = [
            {key: 0, name: 'MM/DD/YYYY'},
            {key: 1, name: 'DD/MM/YYYY'}
        ];

        $scope.timezones = [
            {key: 'Africa/Abidjan', name: 'Africa/Abidjan'},
            {key: 'Africa/Accra', name: 'Africa/Accra'},
            {key: 'Africa/Addis_Ababa', name: 'Africa/Addis_Ababa'},
            {key: 'Africa/Algiers', name: 'Africa/Algiers'},
            {key: 'Africa/Asmara', name: 'Africa/Asmara'},
            {key: 'Africa/Asmera', name: 'Africa/Asmera'},
            {key: 'Africa/Bamako', name: 'Africa/Bamako'},
            {key: 'Africa/Bangui', name: 'Africa/Bangui'},
            {key: 'Africa/Banjul', name: 'Africa/Banjul'},
            {key: 'Africa/Bissau', name: 'Africa/Bissau'},
            {key: 'Africa/Blantyre', name: 'Africa/Blantyre'},
            {key: 'Africa/Brazzaville', name: 'Africa/Brazzaville'},
            {key: 'Africa/Bujumbura', name: 'Africa/Bujumbura'},
            {key: 'Africa/Cairo', name: 'Africa/Cairo'},
            {key: 'Africa/Casablanca', name: 'Africa/Casablanca'},
            {key: 'Africa/Ceuta', name: 'Africa/Ceuta'},
            {key: 'Africa/Conakry', name: 'Africa/Conakry'},
            {key: 'Africa/Dakar', name: 'Africa/Dakar'},
            {key: 'Africa/Dar_es_Salaam', name: 'Africa/Dar_es_Salaam'},
            {key: 'Africa/Djibouti', name: 'Africa/Djibouti'},
            {key: 'Africa/Douala', name: 'Africa/Douala'},
            {key: 'Africa/El_Aaiun', name: 'Africa/El_Aaiun'},
            {key: 'Africa/Freetown', name: 'Africa/Freetown'},
            {key: 'Africa/Gaborone', name: 'Africa/Gaborone'},
            {key: 'Africa/Harare', name: 'Africa/Harare'},
            {key: 'Africa/Johannesburg', name: 'Africa/Johannesburg'},
            {key: 'Africa/Juba', name: 'Africa/Juba'},
            {key: 'Africa/Kampala', name: 'Africa/Kampala'},
            {key: 'Africa/Khartoum', name: 'Africa/Khartoum'},
            {key: 'Africa/Kigali', name: 'Africa/Kigali'},
            {key: 'Africa/Kinshasa', name: 'Africa/Kinshasa'},
            {key: 'Africa/Lagos', name: 'Africa/Lagos'},
            {key: 'Africa/Libreville', name: 'Africa/Libreville'},
            {key: 'Africa/Lome', name: 'Africa/Lome'},
            {key: 'Africa/Luanda', name: 'Africa/Luanda'},
            {key: 'Africa/Lubumbashi', name: 'Africa/Lubumbashi'},
            {key: 'Africa/Lusaka', name: 'Africa/Lusaka'},
            {key: 'Africa/Malabo', name: 'Africa/Malabo'},
            {key: 'Africa/Maputo', name: 'Africa/Maputo'},
            {key: 'Africa/Maseru', name: 'Africa/Maseru'},
            {key: 'Africa/Mbabane', name: 'Africa/Mbabane'},
            {key: 'Africa/Mogadishu', name: 'Africa/Mogadishu'},
            {key: 'Africa/Monrovia', name: 'Africa/Monrovia'},
            {key: 'Africa/Nairobi', name: 'Africa/Nairobi'},
            {key: 'Africa/Ndjamena', name: 'Africa/Ndjamena'},
            {key: 'Africa/Niamey', name: 'Africa/Niamey'},
            {key: 'Africa/Nouakchott', name: 'Africa/Nouakchott'},
            {key: 'Africa/Ouagadougou', name: 'Africa/Ouagadougou'},
            {key: 'Africa/Porto-Novo', name: 'Africa/Porto-Novo'},
            {key: 'Africa/Sao_Tome', name: 'Africa/Sao_Tome'},
            {key: 'Africa/Timbuktu', name: 'Africa/Timbuktu'},
            {key: 'Africa/Tripoli', name: 'Africa/Tripoli'},
            {key: 'Africa/Tunis', name: 'Africa/Tunis'},
            {key: 'Africa/Windhoek', name: 'Africa/Windhoek'},
            {key: 'America/Adak', name: 'America/Adak'},
            {key: 'America/Anchorage', name: 'America/Anchorage'},
            {key: 'America/Anguilla', name: 'America/Anguilla'},
            {key: 'America/Antigua', name: 'America/Antigua'},
            {key: 'America/Araguaina', name: 'America/Araguaina'},
            {key: 'America/Argentina/Buenos_Aires', name: 'America/Argentina/Buenos_Aires'},
            {key: 'America/Argentina/Catamarca', name: 'America/Argentina/Catamarca'},
            {key: 'America/Argentina/ComodRivadavia', name: 'America/Argentina/ComodRivadavia'},
            {key: 'America/Argentina/Cordoba', name: 'America/Argentina/Cordoba'},
            {key: 'America/Argentina/Jujuy', name: 'America/Argentina/Jujuy'},
            {key: 'America/Argentina/La_Rioja', name: 'America/Argentina/La_Rioja'},
            {key: 'America/Argentina/Mendoza', name: 'America/Argentina/Mendoza'},
            {key: 'America/Argentina/Rio_Gallegos', name: 'America/Argentina/Rio_Gallegos'},
            {key: 'America/Argentina/Salta', name: 'America/Argentina/Salta'},
            {key: 'America/Argentina/San_Juan', name: 'America/Argentina/San_Juan'},
            {key: 'America/Argentina/San_Luis', name: 'America/Argentina/San_Luis'},
            {key: 'America/Argentina/Tucuman', name: 'America/Argentina/Tucuman'},
            {key: 'America/Argentina/Ushuaia', name: 'America/Argentina/Ushuaia'},
            {key: 'America/Aruba', name: 'America/Aruba'},
            {key: 'America/Asuncion', name: 'America/Asuncion'},
            {key: 'America/Atikokan', name: 'America/Atikokan'},
            {key: 'America/Atka', name: 'America/Atka'},
            {key: 'America/Bahia', name: 'America/Bahia'},
            {key: 'America/Bahia_Banderas', name: 'America/Bahia_Banderas'},
            {key: 'America/Barbados', name: 'America/Barbados'},
            {key: 'America/Belem', name: 'America/Belem'},
            {key: 'America/Belize', name: 'America/Belize'},
            {key: 'America/Blanc-Sablon', name: 'America/Blanc-Sablon'},
            {key: 'America/Boa_Vista', name: 'America/Boa_Vista'},
            {key: 'America/Bogota', name: 'America/Bogota'},
            {key: 'America/Boise', name: 'America/Boise'},
            {key: 'America/Buenos_Aires', name: 'America/Buenos_Aires'},
            {key: 'America/Cambridge_Bay', name: 'America/Cambridge_Bay'},
            {key: 'America/Campo_Grande', name: 'America/Campo_Grande'},
            {key: 'America/Cancun', name: 'America/Cancun'},
            {key: 'America/Caracas', name: 'America/Caracas'},
            {key: 'America/Catamarca', name: 'America/Catamarca'},
            {key: 'America/Cayenne', name: 'America/Cayenne'},
            {key: 'America/Cayman', name: 'America/Cayman'},
            {key: 'America/Chicago', name: 'America/Chicago'},
            {key: 'America/Chihuahua', name: 'America/Chihuahua'},
            {key: 'America/Coral_Harbour', name: 'America/Coral_Harbour'},
            {key: 'America/Cordoba', name: 'America/Cordoba'},
            {key: 'America/Costa_Rica', name: 'America/Costa_Rica'},
            {key: 'America/Creston', name: 'America/Creston'},
            {key: 'America/Cuiaba', name: 'America/Cuiaba'},
            {key: 'America/Curacao', name: 'America/Curacao'},
            {key: 'America/Danmarkshavn', name: 'America/Danmarkshavn'},
            {key: 'America/Dawson', name: 'America/Dawson'},
            {key: 'America/Dawson_Creek', name: 'America/Dawson_Creek'},
            {key: 'America/Denver', name: 'America/Denver'},
            {key: 'America/Detroit', name: 'America/Detroit'},
            {key: 'America/Dominica', name: 'America/Dominica'},
            {key: 'America/Edmonton', name: 'America/Edmonton'},
            {key: 'America/Eirunepe', name: 'America/Eirunepe'},
            {key: 'America/El_Salvador', name: 'America/El_Salvador'},
            {key: 'America/Ensenada', name: 'America/Ensenada'},
            {key: 'America/Fort_Wayne', name: 'America/Fort_Wayne'},
            {key: 'America/Fortaleza', name: 'America/Fortaleza'},
            {key: 'America/Glace_Bay', name: 'America/Glace_Bay'},
            {key: 'America/Godthab', name: 'America/Godthab'},
            {key: 'America/Goose_Bay', name: 'America/Goose_Bay'},
            {key: 'America/Grand_Turk', name: 'America/Grand_Turk'},
            {key: 'America/Grenada', name: 'America/Grenada'},
            {key: 'America/Guadeloupe', name: 'America/Guadeloupe'},
            {key: 'America/Guatemala', name: 'America/Guatemala'},
            {key: 'America/Guayaquil', name: 'America/Guayaquil'},
            {key: 'America/Guyana', name: 'America/Guyana'},
            {key: 'America/Halifax', name: 'America/Halifax'},
            {key: 'America/Havana', name: 'America/Havana'},
            {key: 'America/Hermosillo', name: 'America/Hermosillo'},
            {key: 'America/Indiana/Indianapolis', name: 'America/Indiana/Indianapolis'},
            {key: 'America/Indiana/Knox', name: 'America/Indiana/Knox'},
            {key: 'America/Indiana/Marengo', name: 'America/Indiana/Marengo'},
            {key: 'America/Indiana/Petersburg', name: 'America/Indiana/Petersburg'},
            {key: 'America/Indiana/Tell_City', name: 'America/Indiana/Tell_City'},
            {key: 'America/Indiana/Vevay', name: 'America/Indiana/Vevay'},
            {key: 'America/Indiana/Vincennes', name: 'America/Indiana/Vincennes'},
            {key: 'America/Indiana/Winamac', name: 'America/Indiana/Winamac'},
            {key: 'America/Indianapolis', name: 'America/Indianapolis'},
            {key: 'America/Inuvik', name: 'America/Inuvik'},
            {key: 'America/Iqaluit', name: 'America/Iqaluit'},
            {key: 'America/Jamaica', name: 'America/Jamaica'},
            {key: 'America/Jujuy', name: 'America/Jujuy'},
            {key: 'America/Juneau', name: 'America/Juneau'},
            {key: 'America/Kentucky/Louisville', name: 'America/Kentucky/Louisville'},
            {key: 'America/Kentucky/Monticello', name: 'America/Kentucky/Monticello'},
            {key: 'America/Knox_IN', name: 'America/Knox_IN'},
            {key: 'America/Kralendijk', name: 'America/Kralendijk'},
            {key: 'America/La_Paz', name: 'America/La_Paz'},
            {key: 'America/Lima', name: 'America/Lima'},
            {key: 'America/Los_Angeles', name: 'America/Los_Angeles'},
            {key: 'America/Louisville', name: 'America/Louisville'},
            {key: 'America/Lower_Princes', name: 'America/Lower_Princes'},
            {key: 'America/Maceio', name: 'America/Maceio'},
            {key: 'America/Managua', name: 'America/Managua'},
            {key: 'America/Manaus', name: 'America/Manaus'},
            {key: 'America/Marigot', name: 'America/Marigot'},
            {key: 'America/Martinique', name: 'America/Martinique'},
            {key: 'America/Matamoros', name: 'America/Matamoros'},
            {key: 'America/Mazatlan', name: 'America/Mazatlan'},
            {key: 'America/Mendoza', name: 'America/Mendoza'},
            {key: 'America/Menominee', name: 'America/Menominee'},
            {key: 'America/Merida', name: 'America/Merida'},
            {key: 'America/Metlakatla', name: 'America/Metlakatla'},
            {key: 'America/Mexico_City', name: 'America/Mexico_City'},
            {key: 'America/Miquelon', name: 'America/Miquelon'},
            {key: 'America/Moncton', name: 'America/Moncton'},
            {key: 'America/Monterrey', name: 'America/Monterrey'},
            {key: 'America/Montevideo', name: 'America/Montevideo'},
            {key: 'America/Montreal', name: 'America/Montreal'},
            {key: 'America/Montserrat', name: 'America/Montserrat'},
            {key: 'America/Nassau', name: 'America/Nassau'},
            {key: 'America/New_York', name: 'America/New_York'},
            {key: 'America/Nipigon', name: 'America/Nipigon'},
            {key: 'America/Nome', name: 'America/Nome'},
            {key: 'America/Noronha', name: 'America/Noronha'},
            {key: 'America/North_Dakota/Beulah', name: 'America/North_Dakota/Beulah'},
            {key: 'America/North_Dakota/Center', name: 'America/North_Dakota/Center'},
            {key: 'America/North_Dakota/New_Salem', name: 'America/North_Dakota/New_Salem'},
            {key: 'America/Ojinaga', name: 'America/Ojinaga'},
            {key: 'America/Panama', name: 'America/Panama'},
            {key: 'America/Pangnirtung', name: 'America/Pangnirtung'},
            {key: 'America/Paramaribo', name: 'America/Paramaribo'},
            {key: 'America/Phoenix', name: 'America/Phoenix'},
            {key: 'America/Port-au-Prince', name: 'America/Port-au-Prince'},
            {key: 'America/Port_of_Spain', name: 'America/Port_of_Spain'},
            {key: 'America/Porto_Acre', name: 'America/Porto_Acre'},
            {key: 'America/Porto_Velho', name: 'America/Porto_Velho'},
            {key: 'America/Puerto_Rico', name: 'America/Puerto_Rico'},
            {key: 'America/Rainy_River', name: 'America/Rainy_River'},
            {key: 'America/Rankin_Inlet', name: 'America/Rankin_Inlet'},
            {key: 'America/Recife', name: 'America/Recife'},
            {key: 'America/Regina', name: 'America/Regina'},
            {key: 'America/Resolute', name: 'America/Resolute'},
            {key: 'America/Rio_Branco', name: 'America/Rio_Branco'},
            {key: 'America/Rosario', name: 'America/Rosario'},
            {key: 'America/Santa_Isabel', name: 'America/Santa_Isabel'},
            {key: 'America/Santarem', name: 'America/Santarem'},
            {key: 'America/Santiago', name: 'America/Santiago'},
            {key: 'America/Santo_Domingo', name: 'America/Santo_Domingo'},
            {key: 'America/Sao_Paulo', name: 'America/Sao_Paulo'},
            {key: 'America/Scoresbysund', name: 'America/Scoresbysund'},
            {key: 'America/Shiprock', name: 'America/Shiprock'},
            {key: 'America/Sitka', name: 'America/Sitka'},
            {key: 'America/St_Barthelemy', name: 'America/St_Barthelemy'},
            {key: 'America/St_Johns', name: 'America/St_Johns'},
            {key: 'America/St_Kitts', name: 'America/St_Kitts'},
            {key: 'America/St_Lucia', name: 'America/St_Lucia'},
            {key: 'America/St_Thomas', name: 'America/St_Thomas'},
            {key: 'America/St_Vincent', name: 'America/St_Vincent'},
            {key: 'America/Swift_Current', name: 'America/Swift_Current'},
            {key: 'America/Tegucigalpa', name: 'America/Tegucigalpa'},
            {key: 'America/Thule', name: 'America/Thule'},
            {key: 'America/Thunder_Bay', name: 'America/Thunder_Bay'},
            {key: 'America/Tijuana', name: 'America/Tijuana'},
            {key: 'America/Toronto', name: 'America/Toronto'},
            {key: 'America/Tortola', name: 'America/Tortola'},
            {key: 'America/Vancouver', name: 'America/Vancouver'},
            {key: 'America/Virgin', name: 'America/Virgin'},
            {key: 'America/Whitehorse', name: 'America/Whitehorse'},
            {key: 'America/Winnipeg', name: 'America/Winnipeg'},
            {key: 'America/Yakutat', name: 'America/Yakutat'},
            {key: 'America/Yellowknife', name: 'America/Yellowknife'},
            {key: 'Antarctica/Casey', name: 'Antarctica/Casey'},
            {key: 'Antarctica/Davis', name: 'Antarctica/Davis'},
            {key: 'Antarctica/DumontDUrville', name: 'Antarctica/DumontDUrville'},
            {key: 'Antarctica/Macquarie', name: 'Antarctica/Macquarie'},
            {key: 'Antarctica/Mawson', name: 'Antarctica/Mawson'},
            {key: 'Antarctica/McMurdo', name: 'Antarctica/McMurdo'},
            {key: 'Antarctica/Palmer', name: 'Antarctica/Palmer'},
            {key: 'Antarctica/Rothera', name: 'Antarctica/Rothera'},
            {key: 'Antarctica/South_Pole', name: 'Antarctica/South_Pole'},
            {key: 'Antarctica/Syowa', name: 'Antarctica/Syowa'},
            {key: 'Antarctica/Troll', name: 'Antarctica/Troll'},
            {key: 'Antarctica/Vostok', name: 'Antarctica/Vostok'},
            {key: 'Arctic/Longyearbyen', name: 'Arctic/Longyearbyen'},
            {key: 'Asia/Aden', name: 'Asia/Aden'},
            {key: 'Asia/Almaty', name: 'Asia/Almaty'},
            {key: 'Asia/Amman', name: 'Asia/Amman'},
            {key: 'Asia/Anadyr', name: 'Asia/Anadyr'},
            {key: 'Asia/Aqtau', name: 'Asia/Aqtau'},
            {key: 'Asia/Aqtobe', name: 'Asia/Aqtobe'},
            {key: 'Asia/Ashgabat', name: 'Asia/Ashgabat'},
            {key: 'Asia/Ashkhabad', name: 'Asia/Ashkhabad'},
            {key: 'Asia/Baghdad', name: 'Asia/Baghdad'},
            {key: 'Asia/Bahrain', name: 'Asia/Bahrain'},
            {key: 'Asia/Baku', name: 'Asia/Baku'},
            {key: 'Asia/Bangkok', name: 'Asia/Bangkok'},
            {key: 'Asia/Beirut', name: 'Asia/Beirut'},
            {key: 'Asia/Bishkek', name: 'Asia/Bishkek'},
            {key: 'Asia/Brunei', name: 'Asia/Brunei'},
            {key: 'Asia/Calcutta', name: 'Asia/Calcutta'},
            {key: 'Asia/Chita', name: 'Asia/Chita'},
            {key: 'Asia/Choibalsan', name: 'Asia/Choibalsan'},
            {key: 'Asia/Chongqing', name: 'Asia/Chongqing'},
            {key: 'Asia/Chungking', name: 'Asia/Chungking'},
            {key: 'Asia/Colombo', name: 'Asia/Colombo'},
            {key: 'Asia/Dacca', name: 'Asia/Dacca'},
            {key: 'Asia/Damascus', name: 'Asia/Damascus'},
            {key: 'Asia/Dhaka', name: 'Asia/Dhaka'},
            {key: 'Asia/Dili', name: 'Asia/Dili'},
            {key: 'Asia/Dubai', name: 'Asia/Dubai'},
            {key: 'Asia/Dushanbe', name: 'Asia/Dushanbe'},
            {key: 'Asia/Gaza', name: 'Asia/Gaza'},
            {key: 'Asia/Harbin', name: 'Asia/Harbin'},
            {key: 'Asia/Hebron', name: 'Asia/Hebron'},
            {key: 'Asia/Ho_Chi_Minh', name: 'Asia/Ho_Chi_Minh'},
            {key: 'Asia/Hong_Kong', name: 'Asia/Hong_Kong'},
            {key: 'Asia/Hovd', name: 'Asia/Hovd'},
            {key: 'Asia/Irkutsk', name: 'Asia/Irkutsk'},
            {key: 'Asia/Istanbul', name: 'Asia/Istanbul'},
            {key: 'Asia/Jakarta', name: 'Asia/Jakarta'},
            {key: 'Asia/Jayapura', name: 'Asia/Jayapura'},
            {key: 'Asia/Jerusalem', name: 'Asia/Jerusalem'},
            {key: 'Asia/Kabul', name: 'Asia/Kabul'},
            {key: 'Asia/Kamchatka', name: 'Asia/Kamchatka'},
            {key: 'Asia/Karachi', name: 'Asia/Karachi'},
            {key: 'Asia/Kashgar', name: 'Asia/Kashgar'},
            {key: 'Asia/Kathmandu', name: 'Asia/Kathmandu'},
            {key: 'Asia/Katmandu', name: 'Asia/Katmandu'},
            {key: 'Asia/Khandyga', name: 'Asia/Khandyga'},
            {key: 'Asia/Kolkata', name: 'Asia/Kolkata'},
            {key: 'Asia/Krasnoyarsk', name: 'Asia/Krasnoyarsk'},
            {key: 'Asia/Kuala_Lumpur', name: 'Asia/Kuala_Lumpur'},
            {key: 'Asia/Kuching', name: 'Asia/Kuching'},
            {key: 'Asia/Kuwait', name: 'Asia/Kuwait'},
            {key: 'Asia/Macao', name: 'Asia/Macao'},
            {key: 'Asia/Macau', name: 'Asia/Macau'},
            {key: 'Asia/Magadan', name: 'Asia/Magadan'},
            {key: 'Asia/Makassar', name: 'Asia/Makassar'},
            {key: 'Asia/Manila', name: 'Asia/Manila'},
            {key: 'Asia/Muscat', name: 'Asia/Muscat'},
            {key: 'Asia/Nicosia', name: 'Asia/Nicosia'},
            {key: 'Asia/Novokuznetsk', name: 'Asia/Novokuznetsk'},
            {key: 'Asia/Novosibirsk', name: 'Asia/Novosibirsk'},
            {key: 'Asia/Omsk', name: 'Asia/Omsk'},
            {key: 'Asia/Oral', name: 'Asia/Oral'},
            {key: 'Asia/Phnom_Penh', name: 'Asia/Phnom_Penh'},
            {key: 'Asia/Pontianak', name: 'Asia/Pontianak'},
            {key: 'Asia/Pyongyang', name: 'Asia/Pyongyang'},
            {key: 'Asia/Qatar', name: 'Asia/Qatar'},
            {key: 'Asia/Qyzylorda', name: 'Asia/Qyzylorda'},
            {key: 'Asia/Rangoon', name: 'Asia/Rangoon'},
            {key: 'Asia/Riyadh', name: 'Asia/Riyadh'},
            {key: 'Asia/Saigon', name: 'Asia/Saigon'},
            {key: 'Asia/Sakhalin', name: 'Asia/Sakhalin'},
            {key: 'Asia/Samarkand', name: 'Asia/Samarkand'},
            {key: 'Asia/Seoul', name: 'Asia/Seoul'},
            {key: 'Asia/Shanghai', name: 'Asia/Shanghai'},
            {key: 'Asia/Singapore', name: 'Asia/Singapore'},
            {key: 'Asia/Srednekolymsk', name: 'Asia/Srednekolymsk'},
            {key: 'Asia/Taipei', name: 'Asia/Taipei'},
            {key: 'Asia/Tashkent', name: 'Asia/Tashkent'},
            {key: 'Asia/Tbilisi', name: 'Asia/Tbilisi'},
            {key: 'Asia/Tehran', name: 'Asia/Tehran'},
            {key: 'Asia/Tel_Aviv', name: 'Asia/Tel_Aviv'},
            {key: 'Asia/Thimbu', name: 'Asia/Thimbu'},
            {key: 'Asia/Thimphu', name: 'Asia/Thimphu'},
            {key: 'Asia/Tokyo', name: 'Asia/Tokyo'},
            {key: 'Asia/Ujung_Pandang', name: 'Asia/Ujung_Pandang'},
            {key: 'Asia/Ulaanbaatar', name: 'Asia/Ulaanbaatar'},
            {key: 'Asia/Ulan_Bator', name: 'Asia/Ulan_Bator'},
            {key: 'Asia/Urumqi', name: 'Asia/Urumqi'},
            {key: 'Asia/Ust-Nera', name: 'Asia/Ust-Nera'},
            {key: 'Asia/Vientiane', name: 'Asia/Vientiane'},
            {key: 'Asia/Vladivostok', name: 'Asia/Vladivostok'},
            {key: 'Asia/Yakutsk', name: 'Asia/Yakutsk'},
            {key: 'Asia/Yekaterinburg', name: 'Asia/Yekaterinburg'},
            {key: 'Asia/Yerevan', name: 'Asia/Yerevan'},
            {key: 'Atlantic/Azores', name: 'Atlantic/Azores'},
            {key: 'Atlantic/Bermuda', name: 'Atlantic/Bermuda'},
            {key: 'Atlantic/Canary', name: 'Atlantic/Canary'},
            {key: 'Atlantic/Cape_Verde', name: 'Atlantic/Cape_Verde'},
            {key: 'Atlantic/Faeroe', name: 'Atlantic/Faeroe'},
            {key: 'Atlantic/Faroe', name: 'Atlantic/Faroe'},
            {key: 'Atlantic/Jan_Mayen', name: 'Atlantic/Jan_Mayen'},
            {key: 'Atlantic/Madeira', name: 'Atlantic/Madeira'},
            {key: 'Atlantic/Reykjavik', name: 'Atlantic/Reykjavik'},
            {key: 'Atlantic/South_Georgia', name: 'Atlantic/South_Georgia'},
            {key: 'Atlantic/St_Helena', name: 'Atlantic/St_Helena'},
            {key: 'Atlantic/Stanley', name: 'Atlantic/Stanley'},
            {key: 'Australia/ACT', name: 'Australia/ACT'},
            {key: 'Australia/Adelaide', name: 'Australia/Adelaide'},
            {key: 'Australia/Brisbane', name: 'Australia/Brisbane'},
            {key: 'Australia/Broken_Hill', name: 'Australia/Broken_Hill'},
            {key: 'Australia/Canberra', name: 'Australia/Canberra'},
            {key: 'Australia/Currie', name: 'Australia/Currie'},
            {key: 'Australia/Darwin', name: 'Australia/Darwin'},
            {key: 'Australia/Eucla', name: 'Australia/Eucla'},
            {key: 'Australia/Hobart', name: 'Australia/Hobart'},
            {key: 'Australia/LHI', name: 'Australia/LHI'},
            {key: 'Australia/Lindeman', name: 'Australia/Lindeman'},
            {key: 'Australia/Lord_Howe', name: 'Australia/Lord_Howe'},
            {key: 'Australia/Melbourne', name: 'Australia/Melbourne'},
            {key: 'Australia/NSW', name: 'Australia/NSW'},
            {key: 'Australia/North', name: 'Australia/North'},
            {key: 'Australia/Perth', name: 'Australia/Perth'},
            {key: 'Australia/Queensland', name: 'Australia/Queensland'},
            {key: 'Australia/South', name: 'Australia/South'},
            {key: 'Australia/Sydney', name: 'Australia/Sydney'},
            {key: 'Australia/Tasmania', name: 'Australia/Tasmania'},
            {key: 'Australia/Victoria', name: 'Australia/Victoria'},
            {key: 'Australia/West', name: 'Australia/West'},
            {key: 'Australia/Yancowinna', name: 'Australia/Yancowinna'},
            {key: 'Brazil/Acre', name: 'Brazil/Acre'},
            {key: 'Brazil/DeNoronha', name: 'Brazil/DeNoronha'},
            {key: 'Brazil/East', name: 'Brazil/East'},
            {key: 'Brazil/West', name: 'Brazil/West'},
            {key: 'CET', name: 'CET'},
            {key: 'CST6CDT', name: 'CST6CDT'},
            {key: 'Canada/Atlantic', name: 'Canada/Atlantic'},
            {key: 'Canada/Central', name: 'Canada/Central'},
            {key: 'Canada/East-Saskatchewan', name: 'Canada/East-Saskatchewan'},
            {key: 'Canada/Eastern', name: 'Canada/Eastern'},
            {key: 'Canada/Mountain', name: 'Canada/Mountain'},
            {key: 'Canada/Newfoundland', name: 'Canada/Newfoundland'},
            {key: 'Canada/Pacific', name: 'Canada/Pacific'},
            {key: 'Canada/Saskatchewan', name: 'Canada/Saskatchewan'},
            {key: 'Canada/Yukon', name: 'Canada/Yukon'},
            {key: 'Chile/Continental', name: 'Chile/Continental'},
            {key: 'Chile/EasterIsland', name: 'Chile/EasterIsland'},
            {key: 'Cuba', name: 'Cuba'},
            {key: 'EET', name: 'EET'},
            {key: 'EST', name: 'EST'},
            {key: 'EST5EDT', name: 'EST5EDT'},
            {key: 'Egypt', name: 'Egypt'},
            {key: 'Eire', name: 'Eire'},
            {key: 'Etc/GMT', name: 'Etc/GMT'},
            {key: 'Etc/GMT+0', name: 'Etc/GMT+0'},
            {key: 'Etc/GMT+1', name: 'Etc/GMT+1'},
            {key: 'Etc/GMT+10', name: 'Etc/GMT+10'},
            {key: 'Etc/GMT+11', name: 'Etc/GMT+11'},
            {key: 'Etc/GMT+12', name: 'Etc/GMT+12'},
            {key: 'Etc/GMT+2', name: 'Etc/GMT+2'},
            {key: 'Etc/GMT+3', name: 'Etc/GMT+3'},
            {key: 'Etc/GMT+4', name: 'Etc/GMT+4'},
            {key: 'Etc/GMT+5', name: 'Etc/GMT+5'},
            {key: 'Etc/GMT+6', name: 'Etc/GMT+6'},
            {key: 'Etc/GMT+7', name: 'Etc/GMT+7'},
            {key: 'Etc/GMT+8', name: 'Etc/GMT+8'},
            {key: 'Etc/GMT+9', name: 'Etc/GMT+9'},
            {key: 'Etc/GMT-0', name: 'Etc/GMT-0'},
            {key: 'Etc/GMT-1', name: 'Etc/GMT-1'},
            {key: 'Etc/GMT-10', name: 'Etc/GMT-10'},
            {key: 'Etc/GMT-11', name: 'Etc/GMT-11'},
            {key: 'Etc/GMT-12', name: 'Etc/GMT-12'},
            {key: 'Etc/GMT-13', name: 'Etc/GMT-13'},
            {key: 'Etc/GMT-14', name: 'Etc/GMT-14'},
            {key: 'Etc/GMT-2', name: 'Etc/GMT-2'},
            {key: 'Etc/GMT-3', name: 'Etc/GMT-3'},
            {key: 'Etc/GMT-4', name: 'Etc/GMT-4'},
            {key: 'Etc/GMT-5', name: 'Etc/GMT-5'},
            {key: 'Etc/GMT-6', name: 'Etc/GMT-6'},
            {key: 'Etc/GMT-7', name: 'Etc/GMT-7'},
            {key: 'Etc/GMT-8', name: 'Etc/GMT-8'},
            {key: 'Etc/GMT-9', name: 'Etc/GMT-9'},
            {key: 'Etc/GMT0', name: 'Etc/GMT0'},
            {key: 'Etc/Greenwich', name: 'Etc/Greenwich'},
            {key: 'Etc/UCT', name: 'Etc/UCT'},
            {key: 'Etc/UTC', name: 'Etc/UTC'},
            {key: 'Etc/Universal', name: 'Etc/Universal'},
            {key: 'Etc/Zulu', name: 'Etc/Zulu'},
            {key: 'Europe/Amsterdam', name: 'Europe/Amsterdam'},
            {key: 'Europe/Andorra', name: 'Europe/Andorra'},
            {key: 'Europe/Athens', name: 'Europe/Athens'},
            {key: 'Europe/Belfast', name: 'Europe/Belfast'},
            {key: 'Europe/Belgrade', name: 'Europe/Belgrade'},
            {key: 'Europe/Berlin', name: 'Europe/Berlin'},
            {key: 'Europe/Bratislava', name: 'Europe/Bratislava'},
            {key: 'Europe/Brussels', name: 'Europe/Brussels'},
            {key: 'Europe/Bucharest', name: 'Europe/Bucharest'},
            {key: 'Europe/Budapest', name: 'Europe/Budapest'},
            {key: 'Europe/Busingen', name: 'Europe/Busingen'},
            {key: 'Europe/Chisinau', name: 'Europe/Chisinau'},
            {key: 'Europe/Copenhagen', name: 'Europe/Copenhagen'},
            {key: 'Europe/Dublin', name: 'Europe/Dublin'},
            {key: 'Europe/Gibraltar', name: 'Europe/Gibraltar'},
            {key: 'Europe/Guernsey', name: 'Europe/Guernsey'},
            {key: 'Europe/Helsinki', name: 'Europe/Helsinki'},
            {key: 'Europe/Isle_of_Man', name: 'Europe/Isle_of_Man'},
            {key: 'Europe/Istanbul', name: 'Europe/Istanbul'},
            {key: 'Europe/Jersey', name: 'Europe/Jersey'},
            {key: 'Europe/Kaliningrad', name: 'Europe/Kaliningrad'},
            {key: 'Europe/Kiev', name: 'Europe/Kiev'},
            {key: 'Europe/Lisbon', name: 'Europe/Lisbon'},
            {key: 'Europe/Ljubljana', name: 'Europe/Ljubljana'},
            {key: 'Europe/London', name: 'Europe/London'},
            {key: 'Europe/Luxembourg', name: 'Europe/Luxembourg'},
            {key: 'Europe/Madrid', name: 'Europe/Madrid'},
            {key: 'Europe/Malta', name: 'Europe/Malta'},
            {key: 'Europe/Mariehamn', name: 'Europe/Mariehamn'},
            {key: 'Europe/Minsk', name: 'Europe/Minsk'},
            {key: 'Europe/Monaco', name: 'Europe/Monaco'},
            {key: 'Europe/Moscow', name: 'Europe/Moscow'},
            {key: 'Europe/Nicosia', name: 'Europe/Nicosia'},
            {key: 'Europe/Oslo', name: 'Europe/Oslo'},
            {key: 'Europe/Paris', name: 'Europe/Paris'},
            {key: 'Europe/Podgorica', name: 'Europe/Podgorica'},
            {key: 'Europe/Prague', name: 'Europe/Prague'},
            {key: 'Europe/Riga', name: 'Europe/Riga'},
            {key: 'Europe/Rome', name: 'Europe/Rome'},
            {key: 'Europe/Samara', name: 'Europe/Samara'},
            {key: 'Europe/San_Marino', name: 'Europe/San_Marino'},
            {key: 'Europe/Sarajevo', name: 'Europe/Sarajevo'},
            {key: 'Europe/Simferopol', name: 'Europe/Simferopol'},
            {key: 'Europe/Skopje', name: 'Europe/Skopje'},
            {key: 'Europe/Sofia', name: 'Europe/Sofia'},
            {key: 'Europe/Stockholm', name: 'Europe/Stockholm'},
            {key: 'Europe/Tallinn', name: 'Europe/Tallinn'},
            {key: 'Europe/Tirane', name: 'Europe/Tirane'},
            {key: 'Europe/Tiraspol', name: 'Europe/Tiraspol'},
            {key: 'Europe/Uzhgorod', name: 'Europe/Uzhgorod'},
            {key: 'Europe/Vaduz', name: 'Europe/Vaduz'},
            {key: 'Europe/Vatican', name: 'Europe/Vatican'},
            {key: 'Europe/Vienna', name: 'Europe/Vienna'},
            {key: 'Europe/Vilnius', name: 'Europe/Vilnius'},
            {key: 'Europe/Volgograd', name: 'Europe/Volgograd'},
            {key: 'Europe/Warsaw', name: 'Europe/Warsaw'},
            {key: 'Europe/Zagreb', name: 'Europe/Zagreb'},
            {key: 'Europe/Zaporozhye', name: 'Europe/Zaporozhye'},
            {key: 'Europe/Zurich', name: 'Europe/Zurich'},
            {key: 'GB', name: 'GB'},
            {key: 'GB-Eire', name: 'GB-Eire'},
            {key: 'GMT', name: 'GMT'},
            {key: 'GMT+0', name: 'GMT+0'},
            {key: 'GMT-0', name: 'GMT-0'},
            {key: 'GMT0', name: 'GMT0'},
            {key: 'Greenwich', name: 'Greenwich'},
            {key: 'HST', name: 'HST'},
            {key: 'Hongkong', name: 'Hongkong'},
            {key: 'Iceland', name: 'Iceland'},
            {key: 'Indian/Antananarivo', name: 'Indian/Antananarivo'},
            {key: 'Indian/Chagos', name: 'Indian/Chagos'},
            {key: 'Indian/Christmas', name: 'Indian/Christmas'},
            {key: 'Indian/Cocos', name: 'Indian/Cocos'},
            {key: 'Indian/Comoro', name: 'Indian/Comoro'},
            {key: 'Indian/Kerguelen', name: 'Indian/Kerguelen'},
            {key: 'Indian/Mahe', name: 'Indian/Mahe'},
            {key: 'Indian/Maldives', name: 'Indian/Maldives'},
            {key: 'Indian/Mauritius', name: 'Indian/Mauritius'},
            {key: 'Indian/Mayotte', name: 'Indian/Mayotte'},
            {key: 'Indian/Reunion', name: 'Indian/Reunion'},
            {key: 'Iran', name: 'Iran'},
            {key: 'Israel', name: 'Israel'},
            {key: 'Jamaica', name: 'Jamaica'},
            {key: 'Japan', name: 'Japan'},
            {key: 'Kwajalein', name: 'Kwajalein'},
            {key: 'Libya', name: 'Libya'},
            {key: 'MET', name: 'MET'},
            {key: 'MST', name: 'MST'},
            {key: 'MST7MDT', name: 'MST7MDT'},
            {key: 'Mexico/BajaNorte', name: 'Mexico/BajaNorte'},
            {key: 'Mexico/BajaSur', name: 'Mexico/BajaSur'},
            {key: 'Mexico/General', name: 'Mexico/General'},
            {key: 'NZ', name: 'NZ'},
            {key: 'NZ-CHAT', name: 'NZ-CHAT'},
            {key: 'Navajo', name: 'Navajo'},
            {key: 'PRC', name: 'PRC'},
            {key: 'PST8PDT', name: 'PST8PDT'},
            {key: 'Pacific/Apia', name: 'Pacific/Apia'},
            {key: 'Pacific/Auckland', name: 'Pacific/Auckland'},
            {key: 'Pacific/Bougainville', name: 'Pacific/Bougainville'},
            {key: 'Pacific/Chatham', name: 'Pacific/Chatham'},
            {key: 'Pacific/Chuuk', name: 'Pacific/Chuuk'},
            {key: 'Pacific/Easter', name: 'Pacific/Easter'},
            {key: 'Pacific/Efate', name: 'Pacific/Efate'},
            {key: 'Pacific/Enderbury', name: 'Pacific/Enderbury'},
            {key: 'Pacific/Fakaofo', name: 'Pacific/Fakaofo'},
            {key: 'Pacific/Fiji', name: 'Pacific/Fiji'},
            {key: 'Pacific/Funafuti', name: 'Pacific/Funafuti'},
            {key: 'Pacific/Galapagos', name: 'Pacific/Galapagos'},
            {key: 'Pacific/Gambier', name: 'Pacific/Gambier'},
            {key: 'Pacific/Guadalcanal', name: 'Pacific/Guadalcanal'},
            {key: 'Pacific/Guam', name: 'Pacific/Guam'},
            {key: 'Pacific/Honolulu', name: 'Pacific/Honolulu'},
            {key: 'Pacific/Johnston', name: 'Pacific/Johnston'},
            {key: 'Pacific/Kiritimati', name: 'Pacific/Kiritimati'},
            {key: 'Pacific/Kosrae', name: 'Pacific/Kosrae'},
            {key: 'Pacific/Kwajalein', name: 'Pacific/Kwajalein'},
            {key: 'Pacific/Majuro', name: 'Pacific/Majuro'},
            {key: 'Pacific/Marquesas', name: 'Pacific/Marquesas'},
            {key: 'Pacific/Midway', name: 'Pacific/Midway'},
            {key: 'Pacific/Nauru', name: 'Pacific/Nauru'},
            {key: 'Pacific/Niue', name: 'Pacific/Niue'},
            {key: 'Pacific/Norfolk', name: 'Pacific/Norfolk'},
            {key: 'Pacific/Noumea', name: 'Pacific/Noumea'},
            {key: 'Pacific/Pago_Pago', name: 'Pacific/Pago_Pago'},
            {key: 'Pacific/Palau', name: 'Pacific/Palau'},
            {key: 'Pacific/Pitcairn', name: 'Pacific/Pitcairn'},
            {key: 'Pacific/Pohnpei', name: 'Pacific/Pohnpei'},
            {key: 'Pacific/Ponape', name: 'Pacific/Ponape'},
            {key: 'Pacific/Port_Moresby', name: 'Pacific/Port_Moresby'},
            {key: 'Pacific/Rarotonga', name: 'Pacific/Rarotonga'},
            {key: 'Pacific/Saipan', name: 'Pacific/Saipan'},
            {key: 'Pacific/Samoa', name: 'Pacific/Samoa'},
            {key: 'Pacific/Tahiti', name: 'Pacific/Tahiti'},
            {key: 'Pacific/Tarawa', name: 'Pacific/Tarawa'},
            {key: 'Pacific/Tongatapu', name: 'Pacific/Tongatapu'},
            {key: 'Pacific/Truk', name: 'Pacific/Truk'},
            {key: 'Pacific/Wake', name: 'Pacific/Wake'},
            {key: 'Pacific/Wallis', name: 'Pacific/Wallis'},
            {key: 'Pacific/Yap', name: 'Pacific/Yap'},
            {key: 'Poland', name: 'Poland'},
            {key: 'Portugal', name: 'Portugal'},
            {key: 'ROC', name: 'ROC'},
            {key: 'ROK', name: 'ROK'},
            {key: 'Singapore', name: 'Singapore'},
            {key: 'Turkey', name: 'Turkey'},
            {key: 'UCT', name: 'UCT'},
            {key: 'US/Alaska', name: 'US/Alaska'},
            {key: 'US/Aleutian', name: 'US/Aleutian'},
            {key: 'US/Arizona', name: 'US/Arizona'},
            {key: 'US/Central', name: 'US/Central'},
            {key: 'US/East-Indiana', name: 'US/East-Indiana'},
            {key: 'US/Eastern', name: 'US/Eastern'},
            {key: 'US/Hawaii', name: 'US/Hawaii'},
            {key: 'US/Indiana-Starke', name: 'US/Indiana-Starke'},
            {key: 'US/Michigan', name: 'US/Michigan'},
            {key: 'US/Mountain', name: 'US/Mountain'},
            {key: 'US/Pacific', name: 'US/Pacific'},
            {key: 'US/Pacific-New', name: 'US/Pacific-New'},
            {key: 'US/Samoa', name: 'US/Samoa'},
            {key: 'UTC', name: 'UTC'},
            {key: 'Universal', name: 'Universal'},
            {key: 'W-SU', name: 'W-SU'},
            {key: 'WET', name: 'WET'},
            {key: 'Zulu', name: 'Zulu'}
        ];

//
        $scope.get = function () {
            if (id) {
                growl.info("LOADING_RESORT_SETTINGS");
                ResortService.fetchSettings(id).then(function (data) {
                        $scope.settings = data;
                        $scope.settings.unit_format = data.unit_format.value;
                        $scope.settings.default_unit_paper = data.default_unit_paper.value;
                        $scope.settings.datetime_format = data.datetime_format.value;

                        $scope.model.filters = _.map($scope.settings.dispatch_field_choice, function (choice) {
                            return {
                                "field": _.find($scope.schema.properties, function(prop){
                                    return prop.fullkey == choice.field_key;
                                })
                            };
                        });
                    },
                    function (error) {
                        growl.error(error.detail);
                    }
                );
            }
        };

        $scope.save = function () {
            if (id) {
                growl.info("SAVE_RESORT_SETTINGS");

                /*
                 dispatch_field_choice
                 {field_key: "name", field_position: 1}
                 {field_key: "phone", field_position: 2}
                 {field_key: "body_part", field_position: 3}
                 {field_key: "field_52d48077a16be", field_position: 4}
                 */

                $scope.settings.dispatch_field_choice = [];

                $scope.settings.dispatch_field_choice = _.map($scope.model.filters, function (filter) {
                    return {
                        "field_key": filter.field.fullkey
                    };
                });

                ResortService.updateSettings(id, $scope.settings).then(function (data) {
//                        $log.log(data);
                        growl.success("resort_updated_successfully");
                    },
                    function (error) {
//                        growl.info(error.detail);

                        //Global errors
                        if (error.hasOwnProperty('detail')) {
                            $scope.error = error.detail;
                            $scope.form.$setPristine();
                        }

                        $scope.errors = [];
                        angular.forEach(error, function (errors, field) {

                            if (field == 'non_field_errors') {
                                // Global errors
                                $scope.error = errors.join(', ');
                                $scope.form.$setPristine();
                            } else {
                                //Field level errors
                                $scope.form[field].$setValidity('backend', false);
                                $scope.form[field].$dirty = true;
                                $scope.errors[field] = errors.join(', ');
                            }
                        });

                    });
            }
        };

        $scope.generate_oauth_key = function () {
            ResortService.generateOAuth(id, {}).then(function (data) {
                    $scope.settings.client_id = data.client_id;
                    $scope.settings.client_secret = data.client_secret;

                    growl.success("resort_updated_successfully");
                },
                function (error) {
//                        growl.info(error.detail);

                    //Global errors
                    if (error.hasOwnProperty('detail')) {
                        $scope.error = error.detail;
                        $scope.form.$setPristine();
                    }

                    $scope.errors = [];
                    angular.forEach(error, function (errors, field) {

                        if (field == 'non_field_errors') {
                            // Global errors
                            $scope.error = errors.join(', ');
                            $scope.form.$setPristine();
                        } else {
                            //Field level errors
                            $scope.form[field].$setValidity('backend', false);
                            $scope.form[field].$dirty = true;
                            $scope.errors[field] = errors.join(', ');
                        }
                    });

                });
        };

        $scope.regenerate_oauth_key = function () {

            var modalInstance = $modal.open({
                animation: true,
                templateUrl: '/app/resorts/templates/confirm_regenerate.html',
                controller: 'ConfirmRegenerateModalCtrl',
                size: 'md'
            });

            modalInstance.result.then(function (is_allowed) {
                ResortService.regenerateOAuth(id, {}).then(function (data) {
                        $scope.settings.client_id = data.client_id;
                        $scope.settings.client_secret = data.client_secret;

                        growl.success("resort_updated_successfully");
                    },
                    function (error) {
//                        growl.info(error.detail);

                        //Global errors
                        if (error.hasOwnProperty('detail')) {
                            $scope.error = error.detail;
                            $scope.form.$setPristine();
                        }

                        $scope.errors = [];
                        angular.forEach(error, function (errors, field) {

                            if (field == 'non_field_errors') {
                                // Global errors
                                $scope.error = errors.join(', ');
                                $scope.form.$setPristine();
                            } else {
                                //Field level errors
                                $scope.form[field].$setValidity('backend', false);
                                $scope.form[field].$dirty = true;
                                $scope.errors[field] = errors.join(', ');
                            }
                        });

                    });
            });
        };

        $scope.download = function (url, filename) {
            var anchor = angular.element('<a/>');
            anchor.attr({
                href: url,
                target: '_blank',
                download: filename
            })[0].click();
        };

        $scope.removeFile = function (value) {
            $scope.settings[value] = '';
        };

        $scope.schema = {
            type: "object",
            properties: []
        };


//        Schema	Form type
//        "type": "string"	text
//        "type": "number"	number
//        "type": "integer"	number
//        "type": "boolean"	checkbox
//        "type": "object"	fieldset
//        "type": "string" and a "enum"	select
//        "type": "array" and a "enum" in array type	checkboxes
//        "type": "array"	array

        var schema_type = {
            'text': 'string',
            'textarea': 'string',
            'number': 'string',
            'range': 'string',
            'arrows': 'string',
            'select': 'string',
            'multi_select': 'string',
            'radio': 'string',
            'gender': 'string',
            'image': 'object',
            'date_picker': 'string',
            'date_time_picker': 'string',
            'google_map': 'object',
            'file': 'string'
        };

//        Form Type	Becomes
//        fieldset	a fieldset with legend
//        section	just a div
//        conditional	a section with a ng-if
//        actions	horizontal button list, can only submit and buttons as items
//        text	input with type text
//        textarea	a textarea
//        number	input type number
//        password	input type password
//        checkbox	a checkbox
//        checkboxes	list of checkboxes
//        select	a select (single value)
//        submit	a submit button
//        button	a button
//        radios	radio buttons
//        radios-inline	radio buttons in one line
//        radiobuttons	radio buttons with bootstrap buttons
//        help	insert arbitrary html
//        tab	tabs with content
//        array	a list you can add, remove and reorder
//        tabarray	a tabbed version of array

        var form_type = {
            'text': 'text',
            'range': 'text',
            'textarea': 'text',
            'number': 'number',
            'arrows': 'select',
            'select': 'select',
            'multi_select': 'select',
            'radio': 'select',
            'gender': 'select',
            'image': 'file_upload',
            'message': 'help',
            'date_picker': 'date_picker',
            'date_time_picker': 'date_time_picker',
            'google_map': 'googlemap',
            'file': 'text'
        };

        var chosenTypes = [
            'text',
            'range',
            'textarea',
            'number',
            'decimal',
            'arrows',
            'select',
            //'multi_select',
            'radio',
            'gender'
            //'date_picker',
            //'date_time_picker'
        ];

        var tabs = questions.DashboardItems;

        var getChoiceMap = function (mapValues) {
            var _choices = [],
                _titlemap = [];

            // Loop and build choices and titlemap
            angular.forEach(mapValues, function (value) {
                for (var key in value) {
                    //console.log(value[key]);
                    if(key.indexOf("controlled") < 0) {
                        _choices.push({"id": key, "name": $translate.instant(value[key])});
                        _titlemap.push({"value": key, "name": $translate.instant(value[key])});
                    }
                }
            });

            return {
                "choices": _choices,
                "titlemap": _titlemap
            }
        };

        $scope.question_items = [];

        $scope.form_items = [];

        for (var key in tabs) {
            if (tabs.hasOwnProperty(key)) {


                for (var question in tabs[key]) {
                    if (tabs[key].hasOwnProperty(question) && (question == 'Questions' || question == 'RepeatingQuestions')) {

                        for (var m in tabs[key][question]) {
                            if (tabs[key][question].hasOwnProperty(m)) {


                                var q = tabs[key][question][m];

                                var choices = [];
                                var titlemap = [];

                                if (q.Type == 'select' || q.Type == 'arrows') {

                                    for (var key1 in q.Values) {

                                        if (q.Values.hasOwnProperty(key1)) {

                                            var choiceMap = getChoiceMap(q.Values);

                                            choices = choiceMap.choices;
                                            titlemap = choiceMap.titlemap;

                                        }

                                    }
                                }

                                if (q.Type == 'gender') {
                                    titlemap.push({
                                        value: "Male",
                                        name: "Male"
                                    });

                                    titlemap.push({
                                        value: "Female",
                                        name: "Female"
                                    });
                                }

                                if (q.Type == 'radio') {
                                    titlemap.push({
                                        value: "Yes",
                                        name: "Yes"
                                    });

                                    titlemap.push({
                                        value: "No",
                                        name: "No"
                                    });
                                }

                                var item = {
                                    'field': m,
                                    'label': $translate.instant(q.Label),
                                    'type': q.Type,
                                    'required': q.Required,
                                    'placeholder': $translate.instant(q.Placeholder),
                                    'choices': choices,
                                    'order': q.Order
                                };

                                if (chosenTypes.indexOf(q.Type) > -1) {
                                    var fullkey = m;

                                    if (question == 'RepeatingQuestions') {
                                        fullkey = key + '____' + m;
                                    }

                                    $scope.schema.properties.push({
                                        'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q.Label),
                                        'type': schema_type[q.Type],
                                        'order': q.Order,
                                        'fullkey': fullkey,
                                        'key': m,
                                        'formtype': form_type[q.Type],
                                        'placeholder': $translate.instant(q.Placeholder),
                                        'titleMap': titlemap
                                    });


                                    $scope.form_items.push({
                                        type: 'fieldset',
                                        htmlClass: 'col-lg-4 col-xs-12',
                                        items: [
                                            {
                                                key: m,
                                                htmlClass: 'pad-left-right',
                                                type: form_type[q.Type],
                                                placeholder: $translate.instant(q.Placeholder),
                                                order: q.Order,
                                                titleMap: titlemap
                                            }
                                        ]
                                    });

                                    $scope.question_items.push(item);
                                } else {

                                    if (q.Type == "repeater" && q.hasOwnProperty('RepeatingQuestions')) {
                                        for (var question1 in tabs[key][question][m]) {
                                            if (tabs[key][question][m].hasOwnProperty(question1) && (question1 == 'Questions' || question1 == 'RepeatingQuestions')) {
                                                for (var n in tabs[key][question][m][question1]) {
                                                    //console.log(n);

                                                    if (tabs[key][question][m][question1].hasOwnProperty(n)) {


                                                        var q1 = tabs[key][question][m][question1][n];

                                                        var choices = [];
                                                        var titlemap = [];

                                                        if (q1.Type == 'select' || q1.Type == 'arrows') {

                                                            for (var key11 in q1.Values) {

                                                                if (q1.Values.hasOwnProperty(key11)) {

                                                                    var choiceMap = getChoiceMap(q1.Values);

                                                                    choices = choiceMap.choices;
                                                                    titlemap = choiceMap.titlemap;

                                                                }
                                                            }
                                                        }

                                                        if (q1.Type == 'gender') {
                                                            titlemap.push({
                                                                value: "Male",
                                                                name: "Male"
                                                            });

                                                            titlemap.push({
                                                                value: "Female",
                                                                name: "Female"
                                                            });
                                                        }

                                                        if (q1.Type == 'radio') {
                                                            titlemap.push({
                                                                value: "Yes",
                                                                name: "Yes"
                                                            });

                                                            titlemap.push({
                                                                value: "No",
                                                                name: "No"
                                                            });
                                                        }

                                                        var item1 = {
                                                            'field': n,
                                                            'label': $translate.instant(q1.Label),
                                                            'type': q1.Type,
                                                            'required': q1.Required,
                                                            'placeholder': $translate.instant(q1.Placeholder),
                                                            'choices': choices,
                                                            'order': q1.Order
                                                        };

                                                        if (chosenTypes.indexOf(q1.Type) > -1) {
                                                            $scope.schema.properties.push({
                                                                'title': $translate.instant(tabs[key].Label) + ' - ' + $translate.instant(q1.Label),
                                                                'type': schema_type[q1.Type],
                                                                'order': q1.Order,
                                                                'fullkey': m + '____' + n,
                                                                'key': n,
                                                                'formtype': form_type[q1.Type],
                                                                'placeholder': $translate.instant(q1.Placeholder),
                                                                'titleMap': titlemap
                                                            });

                                                            $scope.form_items.push({
                                                                type: 'fieldset',
                                                                htmlClass: 'col-lg-4 col-xs-12',
                                                                items: [
                                                                    {
                                                                        key: n,
                                                                        htmlClass: 'pad-left-right',
                                                                        type: form_type[q1.Type],
                                                                        placeholder: $translate.instant(q1.Placeholder),
                                                                        order: q1.Order,
                                                                        titleMap: titlemap
                                                                    }
                                                                ]
                                                            });

                                                            $scope.question_items.push(item1);
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        $scope.form = [
            {
                type: 'section',
                htmlClass: 'col-xs-12',
                items: $scope.form_items
            }
        ];

        $scope.model = {
            filters: [
                {}
            ]
        };

        $scope.addField = function (filters) {
            filters.push({});
        };

        $scope.removeField = function (index) {
            $scope.model.filters.splice(index, 1);
        };

    }]);