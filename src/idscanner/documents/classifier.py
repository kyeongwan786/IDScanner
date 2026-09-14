from collections.abc import Sequence  # OCR 결과 목록의 타입을 가져온다.
from enum import StrEnum  # 문자열 값을 갖는 열거형을 가져온다.

from idscanner.ocr.engine import OcrText  # 원본 OCR 항목의 자료형을 가져온다.


MIN_TITLE_SCORE = 0.90  # 초기 제목 점수 기준이며 정답 확률을 뜻하지 않는다.


class DocumentType(StrEnum):  # 현재 구분하는 종류를 정의한다.
    RESIDENT_CARD = "resident_card"  # 주민등록증 후보를 나타낸다.
    UNKNOWN = "unknown"  # 판단을 보류한 상태를 나타낸다.


def classify_document(lines: Sequence[OcrText]) -> DocumentType:  # 제목에서 종류 후보를 판별한다.
    titles = [  # 공백을 제외한 제목이 완전히 일치하는 항목을 모은다.
        line  # 점수 확인을 위해 원본 항목을 유지한다.
        for line in lines  # 모든 인식 항목을 확인한다.
        if "".join(line.text.split()) == "주민등록증"  # 다른 문구가 섞인 항목은 제외한다.
    ]  # 제목 후보 수집을 마친다.
    if len(titles) != 1:  # 제목이 없거나 중복되면 판단을 보류한다.
        return DocumentType.UNKNOWN  # 확인이 필요한 상태를 반환한다.
    if not MIN_TITLE_SCORE <= titles[0].score <= 1.0:  # 낮은 점수와 NaN 등 범위 밖 값을 제외한다.
        return DocumentType.UNKNOWN  # 불확실한 제목으로 종류를 확정하지 않는다.
    return DocumentType.RESIDENT_CARD  # 제목 조건을 만족한 후보를 반환한다.
