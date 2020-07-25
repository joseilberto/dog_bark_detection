buttons_dict = {
    "n_files": 
        {
            "label": "Number of files to be recorded (n_files)",
            "default": "5",
        },
    "length": 
        {
            "label": "Duration of an audio file (in seconds)",
            "default": "30",
        },
    "attempts": 
        {
            "label": "Attempts of creating n_files",
            "default": "20",
        },
    "sender":
        {
            "label": "Email of sender",
            "default": "jojo.barks.messenger@gmail.com",            
        },
    "sender_password":
        {
            "label": "Password of sender",
            "default": "****",
        },
    "receiver":
        {
            "label": "Email of receiver",
            "default": "ilbertofjunior@gmail.com"
        },
}

message = {
    "subject": "Sending you proofs of my barking/howling",
    "body_start": "Hi, mom \nHere are some proofs of my barks and howls, don't show the neighbors, please. \n",
    "body_end": "\nWith love and shame, \n\t\t\t",
    "signature": "Jojo",
    "pattern": "I {}ed at {}:{}:{} on the {} \n".format,
}