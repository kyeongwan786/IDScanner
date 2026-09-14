import re   # 번호 형식을 검사할 정규표현식을 가져온다.

from collections.abc import Sequence    # OCR 결과 목록의 타입을 가져온다.

from idscanner.ocr.engine import OcrText    # 원본 OCR 항목을 가져온다.

MIN_NUMBER_SCORE = 0.90 # 자동 입력에 사용할 초기 점수 기준을 정한다.

NUMBER_PATTERN = re.compile(  # 한 OCR 항목에서 허용할 번호 형식을 정의한다.
    r"(?:주민등록번호\s*[:：]?\s*)?([0-9]{6})\s*[-–—]?\s*([0-9]{7})",  # 선택적인 라벨과 6자리·7자리 숫자를 받는다.
)  # 번호 패턴 정의를 마친다.

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
