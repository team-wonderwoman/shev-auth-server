const_value = {
    'TTL' : 2592000,
    'HEADER_DOES_NOT_EXIST' : 'NO_token_in_header',
    'SESSION_EXIST' : 'Session_exist',
    'SESSION_CREATED' : 'Session_created',
    'TOKEN_DOES_NOT_EXIST' : 'Token does not exist'
}

status_code = {
    'SUCCESS' :{
            "code" : 0,
            "msg": "Request Succes",
            "option": ""
    },
    'SIGNUP_SUCCESS' : {
        "code": 1200,
        "msg": "SignUp Success",
        "option": ""
    },

    'SIGNUP_WRONG_PARAMETER': {
        "code": 1401,
        "msg": "SignUp Wrong Parameter",
        "option": ""
    },

    'SIGNUP_INVALID_EMAIL' : {
        "code": 1402,
        "msg": "SignUp Invalid Email",
        "option": ""
    },

    'LOGIN_SUCCESS' : {
        "code" : 2200,
        "msg" : "Login success",
        "option" : ""
    },
    'LOGIN_WRONG_PARAMETER' : {
        "code" : 2401,
        "msg" : "Login Wrong Parameter",
        "option" : ""
    },
    'LOGIN_INVALID_EMAIL' : {
        "code" : 2402,
        "msg" : "Login Invalid Email",
        "option" : ""
    },
    'LOGIN_INVALID_PASSWORD': {
        "code": 2403,
        "msg": "Login Invalid Password",
        "option": ""
    },
    'LOGIN_SESSION_EXISTS' : {
        "code" : 2304,
        "msg" : "Session Exists",
        "option" : ""
    },

    'LOGOUT_SUCCESS' : {
        "code" : 3200,
        "msg" : "Logout Success",
        "option" : ""
    },
    'LOGOUT_FAILURE' : {
        "code" : 3401,
        "msg" : "Logout Failure",
        "option" : ""
    },

    'USER_INFO_GET_SUCCESS' : {
        "code" : 4200,
        "msg" : "User information Retrieve",
        "option" : ""
    },
    'USER_INFO_GET_FAILURE' : {
        "code" : 4401,
        "msg" : "User information retrieve fail",
        "option" : ""
    },
    'USER_INFO_MODIFY_SUCCESS' : {
        "code" : 4202,
        "msg" : "User information modified",
        "option" : ""
    },
    'USER_INFO_MODIFY_FAILURE' : {
        "code" : 4403,
        "msg" : "User information modification failure",
        "option" : ""
    },
}