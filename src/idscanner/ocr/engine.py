from dataclasses import dataclass  # OCR 결과를 담을 자료형을 정의한다.
from pathlib import Path  # 이미지 파일 경로를 처리한다.


@dataclass(frozen=True)  # 원본 인식 결과를 변경 불가능한 객체로 만든다.
class OcrText:  # 인식 항목 하나의 구조를 정의한다.
    text: str  # 인식한 문자열
    score: float  # 엔진이 반환한 인식 점수
    polygon: tuple[tuple[float, float], ...]  # 글자 영역의 꼭짓점 좌표


class OcrEngine:  # 화면과 출력 방식에 독립적인 OCR 기능을 정의한다.
    def __init__(self) -> None:  # 엔진 생성 시 모델을 준비한다.
        from paddleocr import PaddleOCR  # 실제 엔진 생성 시 라이브러리를 불러온다.

        self._reader = PaddleOCR(  # 사용할 모델과 실행 옵션을 설정한다.
            text_detection_model_name="PP-OCRv5_mobile_det",  # 글자 영역 검출 모델
            text_recognition_model_name="korean_PP-OCRv5_mobile_rec",  # 한국어 인식 모델
            device="cpu",  # CPU에서 실행한다.
            enable_mkldnn=False,  # 하드웨어별 최적화를 비활성화한다.
            use_doc_orientation_classify=False,  # 문서 방향 분류를 비활성화한다.
            use_doc_unwarping=False,  # 문서 굴곡 보정을 비활성화한다.
            use_textline_orientation=False,  # 글줄 방향 분류를 비활성화한다.
        )  # 모델 설정을 마친다.

    def read(self, image_path: Path) -> list[OcrText]:  # 이미지의 인식 결과를 반환한다.
        lines: list[OcrText] = []  # 전체 인식 항목을 모을 목록을 만든다.
        for result in self._reader.predict(str(image_path)):  # 이미지의 결과를 순회한다.
            records = zip(  # 같은 항목의 문자열·점수·좌표를 묶는다.
                result["rec_texts"],  # 인식 문자열 목록
                result["rec_scores"],  # 인식 점수 목록
                result["rec_polys"],  # 글자 영역 좌표 목록
                strict=True,  # 목록 길이가 다르면 오류로 처리한다.
            )  # 결과 묶음을 구성한다.
            for text, score, polygon in records:  # 각 항목을 프로젝트 자료형으로 변환한다.
                points = tuple(  # 좌표를 변경 불가능한 Python 자료형으로 변환한다.
                    (float(x), float(y)) for x, y in polygon  # 꼭짓점별 좌표를 변환한다.
                )  # 좌표 변환을 마친다.
                lines.append(  # 변환한 항목을 결과 목록에 추가한다.
                    OcrText(text=str(text), score=float(score), polygon=points),  # 항목을 생성한다.
                )  # 결과 추가를 마친다.
        return lines  # 모든 항목을 반환하며 결과가 없으면 빈 목록을 반환한다.
