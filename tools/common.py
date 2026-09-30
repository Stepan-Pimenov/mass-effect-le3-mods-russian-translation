import re

# Строки, которые переводить не нужно и не следует.
_PLACEHOLDER = re.compile(r'^\s*\[[^\]]*\]\s*$')          # [VOLUS DIPLOMAT GAW 1 NAME]
_TOKENS = re.compile(r'^\s*[\d\W_]*$', re.UNICODE)         # только цифры/символы
_DOLLAR = re.compile(r'^\s*\$\d+\s*$')                     # $724686
_CODE = re.compile(r'^\s*<CUSTOM\d>.*$')
_SERVICE = {'Male', 'Female', 'en-us', 'ru-ru'}


def skip(text: str) -> bool:
    t = text.strip()
    if not t or t in _SERVICE:
        return True
    if t.startswith('DLC_MOD') or t.startswith('DLC_Shared'):
        return True
    if _PLACEHOLDER.match(t) or _DOLLAR.match(t) or _TOKENS.match(t):
        return True
    # строки вида "+<CUSTOM0>%", "X: -<CUSTOM0>"
    stripped = re.sub(r'<CUSTOM\d>|[%+\-XYZ:\s\d]', '', t)
    if not stripped:
        return True
    # очень короткие латинские коды без гласных-слов: H1N7, AEND, Kor
    if len(t) <= 4 and re.fullmatch(r'[A-Za-z0-9]+', t):
        return True
    # каталожные обозначения: DH1993, AB-431a, 42-518P-III, 5276-NX-V, LV-426
    if len(t) <= 14 and ' ' not in t and re.search(r'\d', t) and re.fullmatch(r'[A-Za-z0-9\-/]+', t):
        return True
    return False
