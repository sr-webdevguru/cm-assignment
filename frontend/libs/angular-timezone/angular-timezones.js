(function (root) {

  var angular = root.angular
    , timezoneJS = root.timezoneJS
    , jstz = root.jstz

  var toExtendedNative = function (wrapped) {
    /* Tricks the isDate method in Angular into treating these objects like it
     * would any other Date. May be horribly slow. */
    var native = new Date()
    for (key in wrapped) {
      native[key] = wrapped[key]
    }
    return native
  }

  var module = angular.module('Timezones', [])

  module.config(function () {
    timezoneJS.fromLocalString = function (str, tz) {
      // https://github.com/csnover/js-iso8601/blob/master/iso8601.js – MIT license

      var minutesOffset = 0
      var struct = /^(\d{4}|[+\-]\d{6})(?:-(\d{2})(?:-(\d{2}))?)?(?:T(\d{1,2}):(\d{1,2})(?::(\d{1,2})(?:\.(\d{3}))?)?(?:(Z)|([+\-])(\d{2})(?::(\d{2}))?)?)?$/.exec(str)
      var numericKeys = [ 1, 4, 5, 6, 7, 10, 11 ]
      // avoid NaN timestamps caused by “undefined” values being passed to Date.UTC
      for (var i = 0, k; (k = numericKeys[i]); ++i) {
        struct[k] = +struct[k] || 0
      }

      // allow undefined days and months
      struct[2] = (+struct[2] || 1) - 1
      struct[3] = +struct[3] || 1

      return toExtendedNative(new timezoneJS.Date(struct[1], struct[2], struct[3], struct[4], struct[5], struct[6], struct[7], tz))
    }
  })

  module.constant('$timezones.definitions.location', '/tz/data')

  module.run(['$timezones.definitions.location', '$log', function (location, $log) {
    timezoneJS.timezone.zoneFileBasePath = location
    timezoneJS.timezone.init({ async : false })
  }])

  module.factory('$timezones', function () {
    var resolve = function (timezone, reference) {
      if ('number' === typeof(reference)) {
        reference = new Date(reference)
      }

      /*
       * TODO: Support resolution without reference dates.
       *
       * For now, we must use reference dates. There's just not enough time
       * to write and test code that would resolve all possible definitions
       * for any given timezone. Hopefully the TimezoneJS folks will support
       * that some day.
       */

      if (!angular.isDate(reference)) {
        throw {
          name : 'DateObjectExpected',
          message : 'Expected a Date object; got "' + date + '".'
        }
      }

      /* This is not terribly efficient, but necessary because some timezone
       * specifics (like the abbreviation and offset) are temporal. */
      reference = new timezoneJS.Date(reference, timezone)

      var name = reference.getTimezone()

      var result = {
        name : name,
        abbreviation : reference.getTimezoneAbbreviation(),
        offset : reference.getTimezoneOffset(),
        region : name.split('/')[0],
        locality : name.split('/')[1].replace('_', ' ')
      }

      return result
    }

    return {

      /**
       * Aligns the provided Date object to the specified timezone.
       *
       * @param date
       * Reference date.
       *
       * @param timezone
       * An Olson name (e.g., America/New_York), or a timezone object
       * (produced by the resolve function).
       *
       * @returns {*} A Date "aligned" to the desired timezone.
       */
      align : function (date, timezone, silent) {
        if (!angular.isDate(date)) {
          throw {
            name : 'DateObjectExpected',
            message : 'Expected a Date object; got "' + date + '".'
          }
        }

        if (angular.isObject(timezone) && timezone.name) {
          return toExtendedNative(new timezoneJS.Date(date, timezone.name))
        }

        if (angular.isString(timezone)) {
          return toExtendedNative(new timezoneJS.Date(date, timezone))
        }

        if (true === silent) {
          return date
        }

        throw new Error('The timezone argument must either be an Olson name (e.g., America/New_York), or a timezone object (produced by the resolve function) bearing an Olson name on the name property.')
      },

      /**
       * Generate an object that defines the timezone.
       *
       * @param timezone
       * An Olson name (e.g., America/New_York) to resolve.
       *
       * @param reference
       * A reference date used to determine values for temporal timezone
       * properties like the offset and abbreviation (which vary between
       * standard and daylight times).
       *
       * @returns {{name: string, abbreviation: string, offset: number, region: string, locality: string}}
       */
      resolve : resolve,

      /**
       * If the jsTimezoneDetect library is available, use it to make an
       * approximate guess at the current timezone Olson name. From there,
       * perform resolution as usual (which implicitly gets the authoritative
       * definitions from the IANA database).
       */
      getLocal : function () {
        if ('undefined' === typeof(jstz) || 'function' !== typeof(jstz.determine)) {
          throw {
            name : 'JSTZLibraryMissing',
            message : 'The jsTimezoneDetect library, available at https://bitbucket.org/pellepim/jstimezonedetect, is required to detect the local timezone.'
          }
        }

        var name = jstz.determine().name()
          , now = new Date()

        return resolve(name, now)
      }

    }
  })

  module.filter('tzAlign', function ($timezones) {
    return function (date, timezone) {
      if (!(angular.isDate(date) || angular.isNumber(date) || angular.isString(date)) || !(angular.isString(timezone) || angular.isObject(timezone))) {
        return date
      }

      var verifiedDate = date

      if (angular.isNumber(date)) {
        verifiedDate = new Date(date)
      } else if (angular.isString(date)) {
        var milliseconds = parseInt(date)

        if (!angular.isNumber(milliseconds)) {
          milliseconds = Date.parse(date)
        }

        verifiedDate = new Date(milliseconds)
      }

      if (!angular.isDate(verifiedDate) || isNaN(verifiedDate.getTime())) {
        return date
      }

      var alignedDate = $timezones.align(verifiedDate, timezone, true)

      if (isNaN(alignedDate.getTime())) {
        return date
      }

      return alignedDate
    }
  })

})(this)