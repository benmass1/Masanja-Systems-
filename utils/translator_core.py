from googletrans import Translator

def translate_content(text_list, target_lang='sw'):
    """
    Inatafsiri orodha ya maandishi kwenda lugha husika
    """
    translator = Translator()
    translated_pages = []
    
    for text in text_list:
        try:
            # Tunatafsiri kila ukurasa
            translation = translator.translate(text, dest=target_lang)
            translated_pages.append(translation.text)
        except Exception as e:
            translated_pages.append(f"[Hitilafu ya Tafsiri]: {e}")
            
    return translated_pages
￼Enter
