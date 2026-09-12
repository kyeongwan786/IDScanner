from pathlib import Path  # 임시 이미지의 경로를 처리한다.
from tempfile import TemporaryDirectory  # 작업 종료 후 자동 정리되는 임시 폴더를 사용한다.

from PySide6.QtCore import (  # 백그라운드 실행과 알림 도구를 가져온다.
    QObject,  # 부모 객체 타입
    QThread,  # 별도 실행 스레드
    Signal,  # 화면에 전달할 알림
)  # QtCore import를 마친다.
from PySide6.QtGui import QImage  # 화면에서 선택한 이미지를 전달받는다.

from idscanner.ocr.engine import OcrEngine  # 기존 OCR 엔진을 가져온다.


class OcrWorker(QThread):  # 이미지 한 장의 OCR을 백그라운드에서 실행한다.
    progress = Signal(str)  # 현재 처리 상태를 화면에 전달한다.
    result_ready = Signal(object)  # OcrText 목록을 화면에 전달한다.
    failed = Signal(str)  # 실패 안내를 화면에 전달한다.

    def __init__(  # 작업 생성에 필요한 입력을 정의한다.
        self,  # 현재 작업 객체
        image: QImage,  # 화면에 불러온 이미지
        parent: QObject | None = None,  # 작업 객체를 소유할 부모
    ) -> None:  # 실행 준비만 수행한다.
        super().__init__(parent)  # Qt 스레드 객체를 초기화한다.
        self._image = image.copy()  # 원본과 독립된 이미지 복사본을 보관한다.

    def run(self) -> None:  # start 호출 시 별도 스레드에서 실행된다.
        try:  # 작업 중 발생한 오류를 화면에 전달하도록 처리한다.
            if self._image.isNull():  # 전달받은 이미지가 비어 있는지 확인한다.
                self.failed.emit("인식할 이미지가 없습니다.")  # 입력 오류를 알린다.
                return  # 모델을 준비하지 않고 작업을 종료한다.

            with TemporaryDirectory(prefix="idscanner-ocr-") as directory:  # 작업 전용 임시 폴더를 만든다.
                image_path = Path(directory) / "input.png"  # 엔진에 전달할 이미지 경로를 만든다.
                if not self._image.save(str(image_path), "PNG"):  # 화면과 동일한 이미지를 PNG로 저장한다.
                    self.failed.emit("인식용 이미지를 준비하지 못했습니다.")  # 이미지 준비 실패를 알린다.
                    return  # 임시 폴더를 정리하고 종료한다.

                self.progress.emit("인식 준비 중")  # 모델 준비 상태를 알린다.
                engine = OcrEngine()  # 무거운 모델 준비를 백그라운드에서 수행한다.
                self.progress.emit("글자 인식 중")  # 실제 인식 시작을 알린다.
                lines = engine.read(image_path)  # 기존 엔진으로 글자·점수·좌표를 읽는다.

            self.result_ready.emit(lines)  # 임시 파일 정리 후 결과를 전달한다.
        except Exception:  # 작업 경계에서 오류를 받아 실패 상태로 전달한다.
            self.failed.emit(  # 화면에서 표시할 실패 안내를 보낸다.
                "글자 인식에 실패했습니다. 이미지와 모델 다운로드 연결을 확인해 주세요.",  # 안내 내용
            )  # 실패 알림을 마친다.
