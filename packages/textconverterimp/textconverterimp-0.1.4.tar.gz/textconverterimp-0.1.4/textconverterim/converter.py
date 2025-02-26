def to_sentence_case(text):
    """Преобразует текст в формат 'Текст из слов'."""
    if not text:
        return text
    result = []
    for i, char in enumerate(text):
        if i == 0:
            # Первый символ делаем заглавным
            if ord(char) >= 0x430 and ord(char) <= 0x44F:
                result.append(chr(ord(char) - 32))
            else:
                result.append(char)
        else:
            # Остальные символы делаем строчными
            if ord(char) >= 0x410 and ord(char) <= 0x42F:
                result.append(chr(ord(char) + 32))
            else:
                result.append(char)
    return ''.join(result)

def to_title_case(text):
    """Преобразует текст в формат 'Текст Из Слов'."""
    if not text:
        return text
    result = []
    capitalize_next = True  # Флаг, указывающий, что следующий символ нужно сделать заглавным
    for char in text:
        if char == ' ':
            capitalize_next = True
            result.append(char)
        elif capitalize_next:
            if ord(char) >= 0x430 and ord(char) <= 0x44F:
                result.append(chr(ord(char) - 32))
            else:
                result.append(char)
            capitalize_next = False
        else:
            if ord(char) >= 0x410 and ord(char) <= 0x42F:
                result.append(chr(ord(char) + 32))
            else:
                result.append(char)
    return ''.join(result)

def to_kebab_case(text):
    """Преобразует текст в формат 'текст-из-слов'."""
    if not text:
        return text
    result = []
    for char in text:
        if char == ' ':
            result.append('-')
        else:
            if ord(char) >= 0x410 and ord(char) <= 0x42F:
                result.append(chr(ord(char) + 32))
            else:
                result.append(char)
    return ''.join(result)