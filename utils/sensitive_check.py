def has_sensitive_words(text, keywords=None):
    if keywords is None:
        keywords = ["禁止词1", "敏感词2"]
    return [kw for kw in keywords if kw in text]
