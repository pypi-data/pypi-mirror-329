# utils.py
# ------------------------------------------------------------
# 한글 유니코드 및 구성 요소 관련 상수, 리스트, 매핑 정보를 정의합니다.
# ------------------------------------------------------------

# [1] 한글 유니코드 범위 설정
HANGUL_BEGIN_UNICODE = 0xAC00  # '가'
HANGUL_END_UNICODE = 0xD7A3    # '힣'

# [2] 한글 자모 리스트 및 계산 상수

# 초성 리스트 (총 19자)
CHOSUNG_LIST = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 
    'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]
CHOSUNG_BASE = 588  # 21 * 28

# 중성 리스트 (총 21자)
JUNGSUNG_LIST = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 
    'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 
    'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
]
JUNGSUNG_BASE = 28

# 종성 리스트 (총 28자; 첫 번째는 받침 없음)
JONGSUNG_LIST = [
    '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 
    'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 
    'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]
JONGSUNG_COUNT = 28

# [3] 복합 자모 분해 및 결합 정보

# 복합 중성 분해 정보
JUNGSUNG_DECOMPOSE = {
    'ㅘ': ('ㅗ', 'ㅏ'),
    'ㅙ': ('ㅗ', 'ㅐ'),
    'ㅚ': ('ㅗ', 'ㅣ'),
    'ㅝ': ('ㅜ', 'ㅓ'),
    'ㅞ': ('ㅜ', 'ㅔ'),
    'ㅟ': ('ㅜ', 'ㅣ'),
    'ㅢ': ('ㅡ', 'ㅣ')
}

# 복합 종성 분해 정보
JONGSUNG_DECOMPOSE = {
    'ㄳ': ('ㄱ', 'ㅅ'),
    'ㄵ': ('ㄴ', 'ㅈ'),
    'ㄶ': ('ㄴ', 'ㅎ'),
    'ㄺ': ('ㄹ', 'ㄱ'),
    'ㄻ': ('ㄹ', 'ㅁ'),
    'ㄼ': ('ㄹ', 'ㅂ'),
    'ㄽ': ('ㄹ', 'ㅅ'),
    'ㄾ': ('ㄹ', 'ㅌ'),
    'ㄿ': ('ㄹ', 'ㅍ'),
    'ㅀ': ('ㄹ', 'ㅎ'),
    'ㅄ': ('ㅂ', 'ㅅ')
}

# 초성 쌍자음 매핑 (allowDoubleConsonant 옵션 적용)
DOUBLE_INITIAL_MAP = {
    ('ㄱ', 'ㄱ'): 'ㄲ',
    ('ㄷ', 'ㄷ'): 'ㄸ',
    ('ㅂ', 'ㅂ'): 'ㅃ',
    ('ㅅ', 'ㅅ'): 'ㅆ',
    ('ㅈ', 'ㅈ'): 'ㅉ'
}

# 겹받침(종성) 결합 매핑
COMPOUND_FINAL_MAP = {
    ('ㄱ', 'ㅅ'): 'ㄳ',
    ('ㄴ', 'ㅈ'): 'ㄵ',
    ('ㄴ', 'ㅎ'): 'ㄶ',
    ('ㄹ', 'ㄱ'): 'ㄺ',
    ('ㄹ', 'ㅁ'): 'ㄻ',
    ('ㄹ', 'ㅂ'): 'ㄼ',
    ('ㄹ', 'ㅅ'): 'ㄽ',
    ('ㄹ', 'ㅌ'): 'ㄾ',
    ('ㄹ', 'ㅍ'): 'ㄿ',
    ('ㄹ', 'ㅎ'): 'ㅀ',
    ('ㅂ', 'ㅅ'): 'ㅄ'
}

# 겹받침 분해 매핑
COMPOUND_FINAL_DECOMP = {
    'ㄳ': ['ㄱ', 'ㅅ'],
    'ㄵ': ['ㄴ', 'ㅈ'],
    'ㄶ': ['ㄴ', 'ㅍ'],
    'ㄺ': ['ㄹ', 'ㄱ'],
    'ㄻ': ['ㄹ', 'ㅁ'],
    'ㄼ': ['ㄹ', 'ㅂ'],
    'ㄽ': ['ㄹ', 'ㅅ'],
    'ㄾ': ['ㄹ', 'ㅌ'],
    'ㄿ': ['ㄹ', 'ㅍ'],
    'ㅀ': ['ㄹ', 'ㅎ'],
    'ㅄ': ['ㅂ', 'ㅅ']
}

# 모음 결합 정보
VOWEL_COMBO = {
    ('ㅗ', 'ㅏ'): 'ㅘ',
    ('ㅗ', 'ㅐ'): 'ㅙ',
    ('ㅗ', 'ㅣ'): 'ㅚ',
    ('ㅜ', 'ㅓ'): 'ㅝ',
    ('ㅜ', 'ㅔ'): 'ㅞ',
    ('ㅜ', 'ㅣ'): 'ㅟ',
    ('ㅡ', 'ㅣ'): 'ㅢ'
}

# [4] 숫자 읽기 관련 상수
UNITS = [
    "", "십", "백", "천", "만", "십만", "백만", "천만", "억", "십억", "백억", "천억",
    "조", "십조", "백조", "천조", "경", "십경", "백경", "천경", "해", "십해", "백해", "천해",
    "자", "십자", "백자", "천자", "양", "십양", "백양", "천양", "구", "십구", "백구", "천구",
    "간", "십간", "백간", "천간", "정", "십정", "백정", "천정", "재", "십재", "백재", "천재",
    "극", "십극", "백극", "천극", "항하사", "십항하사", "백항하사", "천항하사", "아승기", "십아승기", "백아승기", "천아승기",
    "나유타", "십나유타", "백나유타", "천나유타", "불가사의", "십불가사의", "백불가사의", "천불가사의", "무량대수", "십무량대수", "백무량대수", "천무량대수",
    "겁", "십겁", "백겁", "천겁", "훈공", "십훈공", "백훈공", "천훈공"
]

NUMBERS = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]

# [5] 영문 키보드와 한글 자모 간 매핑 정보

# 영문 자판 → 한글 초성 매핑 (대소문자 모두 처리)
CONSONANT_MAP = {
    'r': 'ㄱ',
    'R': 'ㄲ',
    's': 'ㄴ',
    'e': 'ㄷ',
    'E': 'ㄸ',
    'f': 'ㄹ',
    'a': 'ㅁ',
    'q': 'ㅂ',
    'Q': 'ㅃ',
    't': 'ㅅ',
    'T': 'ㅆ',
    'd': 'ㅇ',
    'w': 'ㅈ',
    'W': 'ㅉ',
    'c': 'ㅊ',
    'z': 'ㅋ',
    'x': 'ㅌ',
    'v': 'ㅍ',
    'g': 'ㅎ'
}

# 영문 자판 → 한글 모음 매핑
VOWEL_MAP = {
    'k': 'ㅏ',
    'o': 'ㅐ',
    'i': 'ㅑ',
    'O': 'ㅒ',
    'j': 'ㅓ',
    'p': 'ㅔ',
    'u': 'ㅕ',
    'P': 'ㅖ',
    'h': 'ㅗ',
    'hk': 'ㅘ',
    'ho': 'ㅙ',
    'hl': 'ㅚ',
    'y': 'ㅛ',
    'n': 'ㅜ',
    'nj': 'ㅝ',
    'np': 'ㅞ',
    'nl': 'ㅟ',
    'b': 'ㅠ',
    'm': 'ㅡ',
    'ml': 'ㅢ',
    'l': 'ㅣ'
}

# 한글 자모 → 영문 자판 매핑 (koen용)
CONSONANT_RMAP = {
    'ㄱ': 'r',
    'ㄲ': 'R',
    'ㄴ': 's',
    'ㄷ': 'e',
    'ㄸ': 'E',
    'ㄹ': 'f',
    'ㅁ': 'a',
    'ㅂ': 'q',
    'ㅃ': 'Q',
    'ㅅ': 't',
    'ㅆ': 'T',
    'ㅇ': 'd',
    'ㅈ': 'w',
    'ㅉ': 'W',
    'ㅊ': 'c',
    'ㅋ': 'z',
    'ㅌ': 'x',
    'ㅍ': 'v',
    'ㅎ': 'g'
}

VOWEL_RMAP = {
    'ㅏ': 'k',
    'ㅐ': 'o',
    'ㅑ': 'i',
    'ㅒ': 'O',
    'ㅓ': 'j',
    'ㅔ': 'p',
    'ㅕ': 'u',
    'ㅖ': 'P',
    'ㅗ': 'h',
    'ㅘ': 'hk',
    'ㅙ': 'ho',
    'ㅚ': 'hl',
    'ㅛ': 'y',
    'ㅜ': 'n',
    'ㅝ': 'nj',
    'ㅞ': 'np',
    'ㅟ': 'nl',
    'ㅠ': 'b',
    'ㅡ': 'm',
    'ㅢ': 'ml',
    'ㅣ': 'l'
}

# [6] 한글 관련 함수들

def is_hangul(text, spaces=False):
    """
    입력된 문자열의 모든 문자가 한글 완성형(또는 띄어쓰기)인지 확인합니다.
    
    :param text: 검사할 문자열 또는 문자
    :param spaces: True인 경우 띄어쓰기도 한글로 허용합니다.
    :return: 모든 문자가 한글(또는 spaces True 시 띄어쓰기 포함)이면 True, 그렇지 않으면 False.
    """
    if not isinstance(text, str):
        return False
    for char in text:
        if char == ' ' and spaces:
            continue
        code = ord(char)
        if not (HANGUL_BEGIN_UNICODE <= code <= HANGUL_END_UNICODE):
            return False
    return True

def compose_syllable(cho, jung, jong):
    """
    초성, 중성, (선택적) 종성을 결합하여 완성형 한글 음절을 생성합니다.
    
    :param cho: 초성 (예: 'ㄱ')
    :param jung: 중성 (예: 'ㅏ')
    :param jong: 종성 (예: 'ㄴ'); 받침이 없으면 빈 문자열('')
    :return: 완성형 한글 음절 (예: '간')
    :raises Exception: 유효하지 않은 자모 입력 시 예외 발생
    """
    if cho not in CHOSUNG_LIST:
        raise Exception(f"Error: '{cho}' is not a valid initial consonant.")
    if jung not in JUNGSUNG_LIST:
        raise Exception(f"Error: '{jung}' is not a valid medial vowel.")
    if jong and jong not in JONGSUNG_LIST:
        raise Exception(f"Error: '{jong}' is not a valid final consonant.")
    
    cho_index = CHOSUNG_LIST.index(cho)
    jung_index = JUNGSUNG_LIST.index(jung)
    jong_index = JONGSUNG_LIST.index(jong) if jong else 0
    
    code = HANGUL_BEGIN_UNICODE + (cho_index * 21 + jung_index) * 28 + jong_index
    return chr(code)
