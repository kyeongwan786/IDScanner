import argparse # 터미널에서 전달한 이미지 경로 처리

from pathlib import Path    # 운영체제에 맞게 파일 경로 처리

def main() -> int:  # 이미지 한 장의 OCR 결과를 확인하는 진입점을 정의
    parser = argparse.ArgumentParser(   # 명령줄 사용법과 인자를 설정

        description="가상 정보 이미지의 한국어 OCR 결과를 확인합니다."  # 명령의 용도를 설명한다.
    )  # 함수 호출을 마친다.

    parser.add_argument("image", type=Path, help="인식할 PNG 또는 JPG 경로")  # 이미지 경로 인자를 등록한다.

    args = parser.parse_args()  # 전달된 명령줄 인자를 해석

    image_path = args.image.expanduser().resolve() # 이미지 경로를 절대 경로로 정의

    if not image_path.is_file():    # 실제 파일이 존재하는지 확인
        parser.error("이미지 파일이 없습니다. 입력한 경로를 확인하세요.")  # 잘못된 경로를 안내하고 종료한다.

    if image_path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:  # 지원 확장자인지 확인한다.
        parser.error("PNG 또는 JPG 이미지를 지정하세요.")  # 지원 형식을 안내하고 종료한다.

    from paddleocr import PaddleOCR # 경로 확인 후 무거운 OCR 라이브러리를 불러온다.
    print("OCR 모델을 준비합니다. 첫 실행에서는 모델을 다운로드합니다.", flush=True)  # 모델 준비 상태를 즉시 표시한다.

    engine = PaddleOCR(  # OCR 엔진을 초기화한다.
        text_detection_model_name="PP-OCRv5_mobile_det",  # 가벼운 글자 영역 검출 모델을 지정한다.
        text_recognition_model_name="korean_PP-OCRv5_mobile_rec",  # 한국어 인식 모델을 정확한 이름으로 지정한다.
        device="cpu",  # CPU에서 모델을 실행한다.
        enable_mkldnn=False,    # 우선 하드웨어별 최적화 없이 기본동작을 확인한다.
        use_doc_orientation_classify=False, # 문서 전체 방향 분류는 이번 단계에서 사용하지 않는다.
        use_doc_unwarping=False,    # 문서 굴곡 보정은 이번 단계에서 사용하지않는다.
        use_textline_orientation=False, # 글줄 방향 분류는 이번 단계에서 사용하지 않는다.
    )  # 함수 호출을 마친다.
    print("이미지에서 글자를 읽고 있습니다", flush=True)  # 인식 시작을 알린다.

    count = 0   # 전체 인식

    for result in engine.predict(str(image_path)):  # 이미지의 OCR 결과를 순서대로 처리한다.

        records = zip(  # 같은 항목의 글자 점수 좌표를 묶는다.
            result["rec_texts"],    # 인식한 문자열 목록
            result["rec_scores"],   # 각 문자열의 인식 점수 목록
            result["rec_polys"],    # 각 문자열 영역의 꼭짓점 좌표 목록
            strict=True,    # 목록 길이가 다르면 오류로 알려준다
        )  # 함수 호출을 마친다.

        # 인식 항목을 하나씩 출력한다.
        for text, score, polygon in records:  # 항목별 글자와 점수 및 좌표를 처리한다.
            count += 1  # 인식 항목 수를 증가시킨다.
            print(f"[{count}] 글자: {text}")  # 인식 문자열을 출력한다.

            print(f"    인식 점수: {float(score):.3f}")  # 인식 점수를 출력한다.

            print(f"    좌표: {polygon.tolist()}")  # 좌표 배열을 목록으로 출력한다.

    print(f"완료: {count}개 항목을 읽었습니다.")  # 전체 결과 처리가 끝난 뒤 요약한다.

    return 0  # 정상 종료 코드를 반환한다.

if __name__ == "__main__":  # 이 패키지를 명령줄에서 실행했는지 확인한다.
    raise SystemExit(main())    # 실행 결과를 프로세스 종료 코드로 전달한다.
