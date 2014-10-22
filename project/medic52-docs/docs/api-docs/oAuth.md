# oAuth API documentation

This module details the oAuth2 API used in Medic52.

## Register a new client

To create new **oAuth2 client application** follow the process below

1. Go to the URL `http://api.dev.medic52.com/oauth/applications/register/`
2. If not logged in this will prompt you for the login information. Provide admin login information.
3. On Register new application provide the following information
    * `Name` (required) - Provide the name for application
    * `Client type` (required) - Select `confidential` as the option from dropdown
    * `Authorization grant type` (required) - select `Client credentials` from dropdown
    * `Redirect uris` - Leave it as empty
    * `Client id` and `Client secret` - Note down this value as it will be required for generating access token
    
## Get access token

This API can be used to get access token with validity of 30 mins in exchange for the client id and client secret of 
the application

#### API URL
```
/auth/access_token/
```

#### API Method
```
POST
```

#### API Parameters
* `grant_type` (**required**)
    * This parameter defines the grant requirement for the application
    * **Default** - `None`
    * **Required Value** - `client_credentials`
* `client_id` (**required**)
    * This provides client id for the targeted application 
    * **Default** - `None`
* `client_secret` (**required**)
    * This provides client secret for the targeted application 
    * **Default** - `None`
    
#### Response Type
* `200 (OK)`

        {
         "access_token": "i7lMTGchdNhHkeznnfjMY3qYgpSelq",
         "token_type": "Bearer",
         "expires_in": 1800,
         "scope": "read write"
        }
        
* `400 (BAD REQUEST)` : If no valid `grant_type` is sent

        {
         "error": "unsupported_grant_type"
        }
        
* `401 (UNAUTHORIZED)` : If provided `client_id` (or) `client_secret` is not valid

        {
         "error": "invalid_client"
        }
    
#### Example Request
```
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d 'grant_type=client_credential&client_id=lRvn55x9bsnpL0Al2qHzJ3q8Aay1B5j8qqGWtpvi&client_secret=qppsn8taUnDqwHMPNqBC8hMWSwhVd5S5QIJrp5xaJc2cqGVncD7Y9rRq0Wk0CZr2ckwDXJQLBepP82k08Iq031eNf7e8F6QLiKvLIBlutS5eJw6Muuxn4pcQAy1pImoE' http://api.dev.medic52.com/oauth/token/
```