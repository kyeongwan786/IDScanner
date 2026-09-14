import re   # 번호 형식을 검사할 정규표현식을 가져온다.

from collections.abc import Sequence  # OCR 결과 목록의 타입을 가져온다.
from datetime import date  # 날짜 유효성과 미래 날짜 여부를 확인한다.

from idscanner.ocr.engine import OcrText    # 원본 OCR 항목을 가져온다.


MIN_NUMBER_SCORE = 0.90 # 자동 입력에 사용할 초기 점수 기준을 정한다.

NUMBER_PATTERN = re.compile(  # 한 OCR 항목에서 허용할 번호 형식을 정의한다.
    r"(?:주민등록번호\s*[:：]?\s*)?([0-9]{6})\s*[-–—]?\s*([0-9]{7})",  # 선택적인 라벨과 6자리·7자리 숫자를 받는다.
)  # 번호 패턴 정의를 마친다.

MIN_DATE_SCORE = 0.90   # 발급일 후보를 자동 입력할 초기 점수 기준

ISSUE_DATE_PATTERN = re.compile(  # 단일 항목의 날짜 형식을 정의한다.
    r"(?:발급일\s*[:：]?\s*)?([0-9]{4})\s*\.\s*([0-9]{1,2})\s*\.\s*([0-9]{1,2})\s*\.?",  # 선택적인 라벨과 연·월·일을 받는다.
)  # 날짜 패턴 정의를 마친다.

def extract_resident_number(lines: Sequence[OcrText]) -> str | None:    # 번호 후보 하나 또는 추출 보류를 반환
    candidates: list[tuple[str, float]] = [] # 번호와 해당 OCR 점수를 함께 보관

    for line in lines: # 인식 항목을 하나씩 확인
        match = NUMBER_PATTERN.fullmatch(line.text.strip()) # 앞뒤 여백을 제외한 항목 전체 검사

        if match is None:   # 번호 외의 문구가 있거나 자릿수가 다르면 제외한다.
            continue    # 다음 인식 항목을 확인

        number = f"{match.group(1)}-{match.group(2)}"  # 표시 형식을 6자리-7자리로 통일한다.

        candidates.append((number, line.score))  # 낮은 점수의 후보도 중복 판단에 포함한다.

    if len(candidates) != 1: # 후보가 없거나 여러 개이면 임의로 선택하지 않는다.

        return None # 자동 입력을 보류

    number, score = candidates[0]    # 유일한 후보의 번호와 점수를 가져온다.

    if not MIN_NUMBER_SCORE <= score <= 1.0:    # 낮은 점수와 NaN 등 유효하지 않은 값을 제외

        return None  # 불확실한 번호는 자동 입력하지 않는다.

    return number  # 사용자가 확인하고 수정할 번호 후보를 반환한다.

def extract_issue_date(lines: Sequence[OcrText]) -> str | None: # 발급일 후보 또는 추출 보류를 반환

    candidates: list[tuple[int, int, int, float]] = []   # 연 월 일과 ocr 점수를 함께 보관

    for line in lines:  # 인식 항목을 하나씩 확인한다.
        match = ISSUE_DATE_PATTERN.fullmatch(line.text.strip()) # 날짜 외의 문구가 섞여있는지 검사

        if match is None:  # 지원하지 않는 형식인지 확인한다.
            continue  # 다음 항목을 확인한다.

        candidates.append(  # 형식에 맞는 후보를 모아 중복 여부를 판단한다.
            (int(match.group(1)), int(match.group(2)), int(match.group(3)), line.score),  # 연·월·일과 점수를 보관한다.
        )  # 후보 추가를 마친다.

    if len(candidates) != 1:  # 후보가 없거나 중복되면 판단을 보류한다.
        return None  # 불확실한 날짜는 자동 입력하지 않는다.

    year, month, day, score = candidates[0]  # 유일한 후보의 날짜와 점수를 가져온다.

    if not MIN_DATE_SCORE <= score <= 1.0:  # 낮은 점수와 유효하지 않은 점수를 제외한다.
        return None  # 불확실한 날짜는 자동 입력하지 않는다.

    try:  # 존재하는 날짜인지 검사한다.
        issued_on = date(year, month, day)  # 윤년과 월별 일수를 검사하며 날짜를 생성한다.

    except ValueError:  # 존재하지 않는 날짜를 처리한다.
        return None  # 불확실한 날짜는 자동 입력하지 않는다.

    if issued_on > date.today():  # PC 날짜보다 미래인 날짜는 제외한다.
        return None  # 불확실한 날짜는 자동 입력하지 않는다.

    return issued_on.isoformat()  # YYYY-MM-DD 형식으로 표시할 후보를 반환한다.
