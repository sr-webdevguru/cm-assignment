# Authentication API documentation

This module details the Authentication API used in Medic52.
    
## Discover

This API can be used to get the domain name associated with user (or) resort.

#### API URL
```
/api/v3/auth/discover/
```

#### API Method
```
POST
```

#### Prerequisite
```
access_token - set header "Authorization: Bearer sald97asdasuhsd7dwq0ddisakdjsakd8u"
```

#### API Parameters

* JSON Data
    * `email` is mandatory for user.
    * `resort_token` (or) `resort_name` is required for resort  
    * `email`
        * email of the user
        * **Default** - `None`
    * `resort_token`
        * resort token
        * **Default** - `None`
    * `resort_name`
        * name of the resort 
        * **Default** - `None`
    
#### Response Type
* `200 (OK)`

        {"location":"us.dev.api.medic52.com "}
    
#### Example Request
```
curl -X POST -H "Authorization: Bearer U8achiIvMdIw867QLNEeIoNkYU41EI" -d '{"email": "duncan@medic52.com"}' http://api.dev.medic52.com/api/v3/auth/discover/
```


## Login

This API can be used to get user logged in to the system.

* Web - Sets session in cookie for web which expires at 2 hour
* Mobile - Returns access token which never expires

#### API URL
```
/api/v3/auth/login/
```

#### API Method
```
POST
```

#### Prerequisite
```
access_token - set header "Authorization: Bearer sald97asdasuhsd7dwq0ddisakdjsakd8u"
```

#### API Parameters

* JSON Data
    * `email` (**required**)
        * email of the user
        * **Default** - `None`
    * `password` (**required**)
        * password of user account
        * **Default** - `None`
    
#### Response Type
* `200 (OK)`

        {
          "user": {
            "user_id": "4969b3b1-4faf-43b6-945e-4dff2fc92f08",
            "name": "David Holt",
            "email": "dispatcher@summit.com",
            "role_id": 1,
            "token": "DSUFYRH-D6SJGO5-SJSVISS7-SDJSDBSFJ6",
            "resort_count": "2",
            "resorts": [
              {
                "resort_name": "Summit",
                "resort_id": "33d0a784-3111-4624-a4f1-92857a9b7bb2",
                "kml_file": "http://nz.media.medic52.com/resorts/summit.kml",
                "map_type": "google-map",
                "lat": "33.0000000",
                "long": "-26.0000000",
                "report_form": "http://nz.media.medic52.com/resorts/summit.html",
                "default_unit_temp": "c",
                "default_unit_length": "m",
                "default_distance_distance": "km",
                "timezone": "America/Los Angeles"
              },
              {
                "resort_name": "Peak",
                "resort_id": "1f3efe2c-4500-4eeb-a09b-2c1320957813",
                "kml_file": "http://nz.media.medic52.com/resorts/peak.kml",
                "map_type": "google-earth",
                "lat": "34.0000000",
                "long": "-25.0000000",
                "report_form": "http://nz.media.medic52.com/resorts/peak.html",
                "default_unit_temp": "c",
                "default_unit_length": "m",
                "default_distance_distance": "km",
                "timezone": "America/Los Angeles"
              }
            ]
          }
        }
        
* `401 (UNAUTHORIZED)` - If email and/or password does not matches any user in the system

        {"detail":"Invalid email/password. Please try with correct email/password"}
        
* `401 (UNAUTHORIZED)` - If invalid credential provided

        {"detail":"Invalid credential provided"}

    
#### Example Request
```
curl -X POST -H "Authorization: Bearer 8CXRT4QpQmb9js8xEdajGqdWO3fEBl" -H "Content-Type: application/json" -d '{"email": "duncan@medic52.com","password": "realpassword"}' http://api.dev.medic52.com/api/v3/auth/login/
```

## Logout

This API can be used to logout user.

* Web - Invalidates session for the user

#### API URL
```
/api/v3/auth/logout/<user_id>
```

#### API Method
```
POST
```

#### Prerequisite
```
access_token - set header "Authorization: Bearer sald97asdasuhsd7dwq0ddisakdjsakd8u"
```

#### API Parameters

* None
    
#### Response Type
* `200 (OK)`

        {"detail":"User is logged out"}

    
#### Example Request
```
curl -X POST -H "Authorization: Bearer 8CXRT4QpQmb9js8xEdajGqdWO3fEBl" http://localhost:8090/api/v3/auth/logout/9704b80d-cd29-43ea-95be-eb4809803b4b
```

## Register

This API can be used to register new user in the system

#### API URL
```
/api/v3/auth/register/
```

#### API Method
```
POST
```

#### Prerequisite
```
access_token - set header "Authorization: Bearer sald97asdasuhsd7dwq0ddisakdjsakd8u"
```

#### API Parameters

* JSON Data
    * `name` (**required**)
        * Name of user
    * `email_address` (**required**)
        * Email of user
    * `resort_name` (**required**)
        * Name of resort
    * `resort_network_key`
        * If user needs to be connected to existing resort through network key
    * `device_push_token` (**required**)
        * Push token of device to be registered
    * `device_os` (**required**)
        * OS of device to be registered
    * `device_type` (**required**)
        * Device type of the device to be registered
    * `country` (**required**)
        * country where user resides
    * `timezone` (**required**)
        * Timezone information
    * `password` (**required**)
        * Password for user account
    
#### Response Type
* `200 (OK)`

        {
            "resort_id": "f820e113-8c70-4bd3-8c7f-72cffed2c4cd",
            "token": "4cb4cdd47c3415ab7a5ac879d3a39ef50c997001",
            "user_id": "775934b9-973d-4514-98ac-654b6d292cca",
            "device_id": "5b9df746-e43d-408f-b53b-1b0e3b8d8334"
        }
        
* `400 (Bad Request)` - If resort name and resort network key not passed

        {"detail":"resort name and/or resort network key not provided"}
        
* `400 (Bad Request)` - If provided network key does not matches with any resort

        {"detail": "Resort with network key does not exist"}
        
        
#### Example Request
```
curl -X POST -H "Authorization: Bearer EU7EerAa61565wxn7H1EaPFAG9PqkN" -d '{
    "name":"Mr Roberts",
    "email":"manager@summit.com",
    "resort_name": "Perisher",
    "device_push_token":"3a0c0ac71ee49eac8b0444a85f1c16692106c3d",
    "device_os":"iOS 7.0.2",
    "device_type":"iPhone 6",
    "country":"Australia",
    "timezone":"Australia/Sydney",
    "password":"PLAINTEXTPASSWORD"
}' http://api.dev.medic52.com/api/v3/auth/register/
```