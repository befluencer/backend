"""


Use:
    Configurations can be added in a form of dictionary
    Added configurations must be inserted appended as part of the
    CONFIG variable
"""

CONFIG = {
    "cors": {
        # in array values, use * to mean everything is allowed
        "allowedOrigins": [
            "http://localhost:3000",
            "https://dev.mydreemuni.com",
            "https://admin.mydreemuni.com",
            "https://www.mydreemuni.com",
            "https://dev.dreemuni.com",
            "https://admin.dreemuni.com",
            "https://www.dreemuni.com",
            "http://172.20.16.1",
            "http://172.20.10.2",
            'http://172.20.16.1:81',
            'http://172.20.16.1:4173',

        ],
        'allowedMethods': ['GET','POST','PUT','DELETE'],
        'notAllowedHeaders': [],
        'allowCredentials': True
    },
    
    "redisKeys":{
        'SCHOOLS': 'schools',
        'USERS': 'users',
        'APPINFO': 'appInfo',
        'FLAGS': 'flags',
        'SUBJECTS': 'subjects',
        'GRADES': 'grades',
        'RESULTS': 'results',
        'STUDENTS': 'students',
        'ADMINS': 'admins',
        "UNIS": 'universities',
        "NOTFSUBS": 'notfsubscriptions',
        'MEDIUMS': 'notfmediums',
        'NOTFPLAN': 'notificationplans',
        'NOTFINS': 'notificationinstitutions',
        'MESSAGES': 'messages',
        'CMESSAGES': 'cmessages',
        'PAYMENTS': 'payments',
        'SCHTYPES': 'scholarshiptypes',
        'SCHCHECKS': 'scholarshipchecks',
        'SCHLABELS': 'scholarshipLabels',
        'SCHSAVED': 'savedScholarships',
        'DISCOUNTS': 'discounts',
        'CHECKERS': 'checkers',
        'CHECKSALES': 'checkerorders',
        'FORMS': 'forms',
        'FORMSALES': 'formorders',
        "CREDITUSAGE": "creditUsage"

        
    },
    "files": {
        "maxUploadSize": 1_048_576,
        "allowedFiles": ["*"],
    },
}
