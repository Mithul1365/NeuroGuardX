from settings import load_language

MESSAGES = {

    "en": {

        "welcome": "Welcome to NeuroGuard X.",

        "sleep": "Driver fatigue detected.",

        "focus": "Please focus on the road.",

        "yawn": "Yawning detected.",

        "driver_not_visible": "Driver not visible.",

        "microsleep": "Emergency! Microsleep detected.",

        "safe": "Driver is safe.",

        "blink": "Blink detected."

    },

    "hi": {

        "welcome": "न्यूरोगार्ड एक्स में आपका स्वागत है।",

        "sleep": "चेतावनी! चालक को नींद आ रही है।",

        "focus": "कृपया सड़क पर ध्यान दें।",

        "yawn": "जंभाई का पता चला।",

        "driver_not_visible": "ड्राइवर दिखाई नहीं दे रहा है।",

        "microsleep": "आपातकाल! माइक्रोस्लीप का पता चला।",

        "safe": "ड्राइवर सुरक्षित है।",

        "blink": "पलक झपकना पाया गया।"

    }

}


def get_message(key):

    language = load_language()

    if language not in MESSAGES:
        language = "en"

    return MESSAGES[language].get(key, key)