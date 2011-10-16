angular.module('app.services')
    .service('DateRangeService', ['$http', '$q', 'UserService', function ($http, $q, UserService) {
        var current = new Date();
        var tz = jstz.determine();

        var datetime_format = UserService.currentUser().resorts[0].datetime_format.key;

        function toUTC(value) {
            return moment.tz(value, datetime_format, tz.name()).utc().format('YYYY-MM-DD HH:mm:ss');
        }

        function toLocalTime(value) {
            return moment.utc(value).tz(tz.name()).format(datetime_format);
        }

        var diff = new Date(current.getTime() - (7 * 24 * 60 * 60 * 1000));

        var start = moment(diff); // + 'T00:00:00.000Z';
        var end = moment(current);//.tz(tz.name()).format('YYYY-MM-DD')+ 'T23:59:59.999Z';

        var range = {
            dateFrom: start,
            dateTo: end
        };

        var service = {

            setStart: function (date) {
                range.dateFrom = date;
            },

            setEnd: function (date) {
                range.dateTo = date;
            },

            getStart: function (date) {
                return range.dateFrom;
            },

            getEnd: function (date) {
                return range.dateTo;
            },

            range: range
        };

        return service;
    }]);

