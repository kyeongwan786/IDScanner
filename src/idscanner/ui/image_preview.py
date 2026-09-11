from PySide6.QtCore import Qt  # 정렬과 이미지 크기 조절 옵션을 가져온다.
from PySide6.QtGui import (  # 이미지 표시와 크기 변경 타입을 가져온다.
    QPixmap,  # 화면에 표시할 이미지
    QResizeEvent,  # 위젯 크기 변경 이벤트
)  # 이미지 관련 import를 마친다.
from PySide6.QtWidgets import (  # 미리보기 구성 요소를 가져온다.
    QLabel,  # 이미지와 안내 문구 표시
    QSizePolicy,  # 레이아웃 안에서의 크기 정책
    QWidget,  # 부모 위젯 타입
)  # 위젯 관련 import를 마친다.


class ImagePreview(QLabel):  # 이미지 비율을 유지하는 미리보기 위젯을 정의한다.
    def __init__(self, parent: QWidget | None = None) -> None:  # 초기 상태를 설정한다.
        super().__init__(parent)  # 부모 위젯을 전달해 라벨을 초기화한다.
        self._source_pixmap = QPixmap()  # 크기 조절의 기준이 되는 원본을 보관한다.
        self.setObjectName("preview")  # 공통 미리보기 스타일을 적용한다.
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 이미지를 중앙에 표시한다.
        self.setWordWrap(True)  # 긴 안내 문구를 줄바꿈한다.
        self.setMinimumSize(240, 200)  # 미리보기의 최소 크기를 지정한다.
        self.setSizePolicy(  # 원본 크기가 화면 배치를 밀어내지 않도록 설정한다.
            QSizePolicy.Policy.Ignored,  # 가로 크기는 레이아웃에 맡긴다.
            QSizePolicy.Policy.Ignored,  # 세로 크기는 레이아웃에 맡긴다.
        )  # 크기 정책 설정을 마친다.
        self.setText("파일 불러오기를 눌러 이미지를 선택하세요.")  # 초기 안내를 표시한다.

    def set_image(self, pixmap: QPixmap) -> None:  # 새 이미지를 전달받는다.
        self._source_pixmap = pixmap  # 이후 크기 변경에도 사용할 원본을 보관한다.
        self._update_preview()  # 현재 영역 크기에 맞춰 표시한다.

    def resizeEvent(self, event: QResizeEvent) -> None:  # Qt의 크기 변경 이벤트를 처리한다.
        super().resizeEvent(event)  # 라벨의 기본 크기 변경 처리를 실행한다.
        self._update_preview()  # 변경된 영역 크기에 맞춰 다시 표시한다.

    def _update_preview(self) -> None:  # 원본에서 표시용 이미지를 생성한다.
        if self._source_pixmap.isNull():  # 아직 이미지가 없는지 확인한다.
            return  # 초기 안내 문구를 유지한다.

        target_size = self.contentsRect().size()  # 표시 영역의 크기를 가져온다.
        if target_size.isEmpty():  # 표시할 공간이 없는지 확인한다.
            return  # 유효한 크기를 받을 때까지 표시를 미룬다.

        scaled_pixmap = self._source_pixmap.scaled(  # 원본을 표시 영역에 맞춰 조절한다.
            target_size,  # 표시할 영역 크기를 전달한다.
            Qt.AspectRatioMode.KeepAspectRatio,  # 원본의 가로세로 비율을 유지한다.
            Qt.TransformationMode.SmoothTransformation,  # 부드럽게 크기를 조절한다.
        )  # 표시용 이미지 생성을 마친다.
        self.setPixmap(scaled_pixmap)  # 안내 문구 대신 이미지를 표시한다.
