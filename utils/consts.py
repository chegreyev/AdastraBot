
# Teacher grades
GRADES = ['1-5', '6-9', '10+', 'confirm', 'change']

CALLBACK_GRADES = {
    '1-5': {
        'data': 'configure_next_grades__primary',
        'text': '1-5',
    },
    '6-9': {
        'data': 'configure_next_grades__middle',
        'text': '6-9',
    },
    '10+': {
        'data': 'configure_next_grades__high',
        'text': '10+',
    },
    'confirm': {
        'data': 'confirm_grades',
        'text': 'Я все выбрал!',
    },
    'change': {
        'data': 'change_grades',
        'text': 'Я ошибся...',
    }
}

# Teacher languages
LANGUAGES = ['казахский', 'русский', 'английский', 'confirm', 'change']

CALLBACK_LANGUAGES = {
    'казахский':{
        'data': 'configure_next_language__kazakh',
        'text': 'казахский',
    },
    'русский':{
        'data': 'configure_next_language__russian',
        'text': 'русский',
    },
    'английский':{
        'data': 'configure_next_language__english',
        'text': 'английский',
    },
    'confirm':{
        'data': ['confirm_languages__fizmat', 'confirm_languages__english'],
        'text': 'Я все выбрал!',
    },
    'change':{
        'data': 'change_languages',
        'text': 'Я ошибся...',
    }
}

# Teacher levels (subject == english )
LEVELS = [
    'beginner', 'elementary', 'pre-intermediate',
    'intermediate', 'upper-intermediate',
    'confirm', 'change',
]

CALLBACK_LEVELS = {
    'beginner': {
        'data': 'configure_next_level__beginner',
        'text': 'beginner',
    },
    'elementary': {
        'data': 'configure_next_level__elementary',
        'text': 'elementary',
    },
    'pre-intermediate': {
        'data': 'configure_next_level__pre_intermediate',
        'text': 'pre-intermediate',
    },
    'intermediate': {
        'data': 'configure_next_level__intermediate',
        'text': 'intermediate',
    },
    'upper-intermediate': {
        'data': 'configure_next_level__upper_intermediate',
        'text': 'upper-intermediate',
    },
    'confirm':{
        'data': 'confirm_levels',
        'text': 'Я все выбрал!',
    },
    'change':{
        'data': 'change_levels',
        'text': 'Я ошибся...',
    }
}