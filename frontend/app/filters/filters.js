'use strict';

angular.module('app')
    .filter('startFrom', function () {
        return function (input, start) {
            if (input) {
                start = 0 + start; //parse to int
                return input.slice(start);
            }
            return [];
        }
    })
    .filter('range', function () {
        return function (input, total) {
            total = parseInt(total);
            for (var i = 1; i <= total; i++)
                input.push(i);
            return input;
        };
    })
    .filter('toLocal', function ($filter) {
        return function (input) {
            if (input && input.indexOf('T')>0) {
                return moment.utc(input).local().format("hh:mm A");
            } else {
                return input;
            }
        };
    })
    .filter('toLocalDateTime', function ($filter,UserService) {
        return function (input) {
            var tz = jstz.determine();

            if (input) {
                return moment.utc(input).tz(tz.name()).format(UserService.currentUser().resorts[0].datetime_format.key);
            } else {
                return input;
            }
        };
    })
    .filter('toElapsedTime', function ($filter) {
        return function (input, format) {
            if (input) {
                var from = moment.utc(input);
                var now = moment();
                return  moment.duration(now.diff(from, "seconds"), "seconds").format(format) ;
            } else {
                return input;
            }
        };
    })
    .filter('toTitlecase', function ($filter) {

        String.prototype.toTitleCase = function () {
            return this.replace(/\w\S*/g, function(txt){
                return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
            });
        };

        return function (input) {
            if (input && (typeof input == 'string' || input instanceof String)) {
                return (""+input).toTitleCase();
            } else {
                return input;
            }
        };
    })
    .filter('keysOnly', function ($filter) {
        return function (input) {
            if (input) {
                //var data =  $.grep(input, function(v) {
                //    return v.selected === true;
                //});

                var keys = _.pluck(input, "key");
                return keys.join(", ");

            } else {
                return input;
            }
        };
    })
    .filter('transformInjury', function ($filter, $translate) {
        return function (input) {
            if (input) {
                var data = $.map( input, function( val, i ) {
                    return $translate.instant(val.injury_location) + " " + $translate.instant(val.body_part) + " " + $translate.instant(val.injury_type);
                });

                return data.join (", ");

            } else {
                return input;
            }
        };
    })
    .filter('transformInjuryFirst', function ($filter, $translate) {
        return function (input) {
            if (input) {
                var data = $.map( input, function( val, i ) {
                    return $translate.instant(val.injury_location) + " " + $translate.instant(val.body_part) + " " + $translate.instant(val.injury_type);
                });

                return data[0];

            } else {
                return input;
            }
        };
    })
    .filter('transformInjuryLocationPart', function ($filter, $translate) {
        return function (input) {
            if (input) {
                var data = $.map( input, function( val, i ) {
                    return $translate.instant(val.injury_location) + " " + $translate.instant(val.body_part);
                });

                return data.join (", ");

            } else {
                return input;
            }
        };
    })
    .filter('transformInjuryType', function ($filter, $translate) {
        return function (input) {
            if (input) {
                var data = $.map( input, function( val, i ) {
                    return $translate.instant(val.injury_type);
                });

                return data.join (", ");

            } else {
                return input;
            }
        };
    })
    .filter('transformTreatment', function ($filter, $translate) {
        return function (input) {
            if (input) {
                var data = $.map( input, function( val, i ) {
                    return $translate.instant(_.values(val)[0]);
                });

                return data.join (", ");

            } else {
                return input;
            }
        };
    })
    .filter('transformPatient', function ($filter) {
        return function (input) {
            if (input) {
                return input.name;

            } else {
                return input;
            }
        };
    })
;
