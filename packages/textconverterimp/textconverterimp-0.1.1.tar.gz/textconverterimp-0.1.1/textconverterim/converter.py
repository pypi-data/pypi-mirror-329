def to_sentence_case(text):
    """Преобразует текст в формат 'Текст из слов'."""
    return text.capitalize()

def to_title_case(text):
    """Преобразует текст в формат 'Текст Из Слов'."""
    return text.title()

def to_kebab_case(text):
    """Преобразует текст в формат 'текст-из-слов'."""
    return text.lower().replace(" ", "-")