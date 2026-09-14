from PySide6.QtCore import (
    Qt, # 화면 정렬 옵션
    Slot,   # 화면에서 실행할 시그널 수신 메서드 지정
) # 화면 정렬 옵션을 가져온다.
from PySide6.QtGui import (  # 이미지 읽기와 표시 기능을 가져온다.
    QCloseEvent,    # 창 종료 요청을 처리한다.
    QImage,         # 현재 선택한 이미지를 보관
    QImageReader,  # 파일에서 이미지를 읽는다.
    QPixmap,  # 읽은 이미지를 화면 표시용으로 변환한다.
)  # 이미지 관련 import를 마친다.
from PySide6.QtWidgets import (  # 화면 구성 요소를 가져온다.
    QFileDialog,  # 파일 선택 창
    QFrame,  # 패널 컨테이너
    QHBoxLayout,  # 가로 배치
    QLabel,  # 텍스트 표시
    QLineEdit,  # 결과 입력창
    QMainWindow,  # 메인 창
    QMessageBox,  # 안내 창
    QPlainTextEdit,  # 여러 줄의 인식 결과 표시
    QPushButton,  # 버튼
    QVBoxLayout,  # 세로 배치
    QWidget,  # 기본 위젯
)  # QtWidgets import를 마친다.

from idscanner.documents.classifier import (  # 신분증 종류 판별 기능을 가져온다.
    DocumentType,  # 종류 후보의 자료형을 가져온다.
    classify_document,  # OCR 제목 판별 함수를 가져온다.
)  # 판별 기능 import를 마친다.
from idscanner.documents.resident_card import extract_resident_number  # 주민등록증 번호 추출 함수를 가져온다.
from idscanner.ocr.engine import OcrText  # 원본 OCR 자료형을 가져온다.
from idscanner.ocr.worker import OcrWorker  # 백그라운드 인식 작업을 가져온다.
from idscanner.ui.image_preview import ImagePreview  # 이미지 미리보기 위젯을 가져온다.



class MainWindow(QMainWindow):  # 신분증 이미지와 결과를 보여 줄 메인 창 정의:

    def __init__(self) -> None: # 창 생성 시 필요한 상태와 화면을 초기화:

        super().__init__()  # 부모 클래스의 창 초기화를 실행

        self._image = QImage()  # 화면에 불러온 이미지를 보관

        self._worker: OcrWorker | None = None # 진행 중인 작업을 보관한다.

        self._ocr_results: list[OcrText] = []   # 글자 점수 좌표가 포함된 원본 결과를 보관

        self._recognize_button = QPushButton("인식 시작")   # 인식 실행 버튼을 만든다.

        self._ocr_output = QPlainTextEdit()     # 인식된 글자를 표시할 영역을 만든다.

        self._fields: dict[str, QLineEdit] = {} # 항목 이름별 입력창을 보관

        self._status_label = QLabel("준비") # 현재 처리 상태 표시

        self._preview_label = ImagePreview()  # 이미지 또는 이미지 안내 문구 표시

        self._document_type_label = QLabel("신분증 종류: 인식 대기")    # 판별 상태 표시

        self._open_button = QPushButton("파일 불러오기")    # 이미지 선택 버튼 생성

        self._confirm_button = QPushButton("확인 완료")     # 결과 확정 버튼 생성

        self.setWindowTitle("IDScanner")    # 운영체제 창 제목 설정

        self.resize(1120, 760)  # 초기 창 크기 설정

        self.setMinimumSize(960, 720)   # 화면 구성 유지 최소 창 크기

        self._build_ui()    # 화면에 위젯 배치

    def _build_ui(self) -> None:    # 메인 창의 전체 배치 구성

        central_widget = QWidget()  # 창의 본문을 담을 위젯 구성

        self.setCentralWidget(central_widget)   # 메인 창의 중앙 위젯으로 등록

        root_layout = QVBoxLayout(central_widget)   # 본문 세로 배치

        root_layout.setContentsMargins(32, 28, 32, 28)  #본문 바깥 여백 설정

        root_layout.setSpacing(24)  # 본문의 영역 간 간격을 설정

        root_layout.addLayout(self._build_header())     # 제목과 상태 표시를 추가한다.

        content_layout = QHBoxLayout()  # 두 패널을 가로로 배치

        content_layout.setSpacing(24)   # 패널 사이의 간격 설정

        content_layout.addWidget(self._build_preview_panel(), 3)    # 이미지 패널 추가

        content_layout.addWidget(self._build_result_panel(), 2) # 결과 패널 추가

        root_layout.addLayout(content_layout, 1)    # 남는 세로 공간을 패널 영역에 배정

        footer_label = QLabel("입력한 내용은 현재 저장되지 않습니다.")  # 저장 상태를 안내

        footer_label.setObjectName("hint")  # 보조 문구 스타일 지정

        root_layout.addWidget(footer_label) # 안내를 화면 하단에 추가.


    def _build_header(self) -> QHBoxLayout: # 제목과 상태 표시 영역 구성

        header_layout = QHBoxLayout()   # 헤더를 가로로 배치

        title_layout = QVBoxLayout()    # 제목과 설명을 세로로 배치

        title_layout.setSpacing(6)      # 제목과 설명 사이의 간격을 설정

        title_label = QLabel("ID Scanner")  # 앱 제목 생성

        title_label.setObjectName("appTitle")   # 앱 제목 스타일 지정

        subtitle_label = QLabel("신분증 정보를 인식하고 확인하세요.")

        subtitle_label.setObjectName("subtitle")

        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)  # 제목 아래에 설명을 표시한다.

        header_layout.addLayout(title_layout)

        header_layout.addStretch()  # 상태 표시를 오른쪽 끝으로 밀어냄

        self._status_label.setObjectName("statusBadge") # 처리 상태 스타일

        header_layout.addWidget(
            self._status_label, # 상태 표시 위젯 전달
            alignment=Qt.AlignmentFlag.AlignVCenter # 헤더와 세로로 중앙에 맞춤

        )

        return header_layout

    def _create_panel(self, title: str) -> QFrame:  # 공통 외형의 패널 생성

        panel = QFrame()    # 패널 컨테이너 생성
        panel.setObjectName("panel")

        layout = QVBoxLayout(panel)

        layout.setContentsMargins(24, 24, 24, 24)

        layout.setSpacing(12)

        title_label = QLabel(title)

        title_label.setObjectName("sectionTitle")

        layout.addWidget(title_label)

        return panel

    def _build_preview_panel(self) -> QFrame:   # 이미지와 인식 실행 영역 구성

        panel = self._create_panel("신분증 이미지") # 공통 패널을 생성

        layout = panel.layout() # 패널의 레이아웃을 가져온다.

        layout.addWidget(self._preview_label, 1)    # 남는 세로 공간에 이미지를 배치한다.

        buttons = QHBoxLayout() # 두 버튼 가로 배치

        self._open_button.setEnabled(True)  # 파일 선택을 허용

        self._open_button.setToolTip("PNG 또는 JPG 이미지를 선택하세요.")   # 지원 형식을 안내한다.

        self._open_button.clicked.connect(self._open_image) # 파일 선택 동작 연결

        buttons.addWidget(self._open_button)    # 파일 선택 버튼 추가

        self._recognize_button.setObjectName("primaryButton")

        self._recognize_button.setEnabled(False)

        self._recognize_button.clicked.connect(self._start_ocr)

        buttons.addWidget(self._recognize_button)  # 인식 버튼을 화면에 배치한다.

        layout.addLayout(buttons)

        layout.addWidget(QLabel("인식된 글자")) # 글자 영역의 제목을 추가

        self._ocr_output.setPlaceholderText("인식 시작을 누르면 글자가 표시됩니다.")  # 초기 안내를 표시한다.

        self._ocr_output.setReadOnly(True)  # 원본 결과는 읽기 전용

        self._ocr_output.setFixedHeight(140) # 긴 결과는 영역안에서 스크롤

        layout.addWidget(self._ocr_output)  # 결과 표시 영역 추가

        return panel    # 완성한 패널을 반환



    def _build_result_panel(self) -> QFrame:    # 인식 결과를 편집할 패널을 구성
        panel = self._create_panel("인식 결과")

        layout = panel.layout()

        self._document_type_label.setObjectName("hint")

        layout.addWidget(self._document_type_label)

        field_specs = (
            ("name", "이름"),
            ("resident_number", "주민등록번호"),
            ("address", "주소"),
            ("issue_date", "발급일"),
        )

        for key, label in field_specs:  # 정의한 순서대로 입력 항목들을 구성

            self._add_result_field(layout, key, label)    # 라벨과 입력창 추가

        hint_label = QLabel(  # 자동 입력 범위와 수정 방법을 안내한다.
            "주민등록증 후보의 번호를 자동 입력합니다.\n"  # 이번 단계에서 지원하는 항목을 설명한다.
            "원본과 비교해 수정하세요. 재인식하면 번호가 초기화됩니다.",  # 수정과 초기화 동작을 안내한다.
        )  # 안내 문구 생성을 마친다.

        hint_label.setObjectName("hint")

        hint_label.setWordWrap(True)
        layout.addWidget(hint_label)  # 안내 문구를 입력창 아래에 표시한다.

        layout.addStretch()

        self._confirm_button.setObjectName("primaryButton")

        self._confirm_button.setEnabled(False)

        layout.addWidget(self._confirm_button)

        return panel

    def _add_result_field(  # 라벨과 입력창을 한 쌍으로 추가하는 메서드 정의
            self,   # 현재 창 인스턴스 받는다.
            layout: QVBoxLayout,    # 항목 추가 레이아웃
            key: str,   # 입력창을 찾을 때 사용할 내부 이름
            label: str, # 화면에 표시할 항목 이름
    ) -> None:
        field_label = QLabel(label) # 항목 이름을 표시할 라벨을 생성

        editor = QLineEdit()

        editor.setPlaceholderText(f"{label} 인식 결과")

        editor.setAccessibleName(label) # 접근성 도구가 읽을 항목 이름 설정

        editor.setClearButtonEnabled(True)  # 입력 내용을 지우는 버튼 제공

        field_label.setBuddy(editor)

        self._fields[key] = editor  # 이후 결과 표시와 수정값 조회에 사용할 입력창 보관

        layout.addWidget(field_label)

        layout.addWidget(editor)

    def _open_image(self) -> None:  # 파일을 선택하고 성공한 이미지만 화면에 반영한다.

        if self._worker is not None:    # 진행 중이거나 종료 처리 중인 작업을 확인한다.

            return  # 인식 중에는 이미지를 바꾸지 않는다.

        file_path, _ = QFileDialog.getOpenFileName(
            self,   # 파일 선택창의 부모를 지정
            "신분증 이미지 선택",   # 파일 선택 창 제목을 지정
            "",     # 기본 시작 폴더를 사용
            "이미지 파일 (*.png *.jpg *.jpeg)",
        )

        if not file_path:   # 사용자가 선택을 취소했는지 확인
            return          # 기존 이미지와 결과를 유지

        reader = QImageReader(file_path)    # 이미지 리더를 생성.
        reader.setAutoTransform(True)   # 이미지에 기록된 방향 정보를 적용

        image = reader.read()   # 파일에서 이미지를 읽는다

        if image.isNull():  # 이미지 읽기에 실패했는지 확인한다.
            QMessageBox.warning(
                self,   # 안내 창의 부모를 지정
                "이미지 불러오기 실패", # 안내 제목을 지정한다.
                "이미지를 읽을 수 없습니다. 다른 이미지 파일을 선택하세요."
            )

            return

        self._preview_label.set_image(QPixmap.fromImage(image)) # 성공한 이미지를 표시

        self._image = image.copy()  # 화면과 같은 이미지를 인식용으로 보관

        self._ocr_results.clear()   # 이전 이미지의 원본 결과를 비운다.

        self._ocr_output.clear()    # 이전 이미지의 결과 표시를 비운다.

        for editor in self._fields.values():    # 기존 결과 입력창을 순회

            editor.clear()  # 이전 이미지의 입력값을 비운다.

        self._document_type_label.setText("신분증 종류: 인식 대기")

        self._status_label.setText("이미지 준비")

        self._recognize_button.setEnabled(True)

        self._confirm_button.setEnabled(False)

    @Slot() # 버튼 클릭을 화면 스레드에서 처리한다.
    def _start_ocr(self) -> None:   # 현재 이미지의 인식을 시작한다.

        if self._image.isNull() or self._worker is not None: # 이미지 없음과 중복 실행 확인
            return

        self._open_button.setEnabled(False) # 인식 중 이미지 변경을 막는다.

        self._recognize_button.setEnabled(False)    # 중복 인식을 막는다.

        self._confirm_button.setEnabled(False)  # 확정 기능은 아직 활성화 안한다.

        self._ocr_results.clear()   # 이전 원본 결과를 비운다.

        self._ocr_output.clear()    # 이전 결과 표시를 비운다.

        self._fields["resident_number"].clear() # 재인식 전에 번호와 수정값을 비운다.

        self._document_type_label.setText("신분증 종류: 인식 대기")  # 재인식 전에 이전 종류 표시를 초기화한다.

        self._status_label.setText("인식 준비 중")

        self._worker = OcrWorker(self._image, self) # 현재 이미지로 작업을 생성한다.

        self._worker.progress.connect(self._status_label.setText)   # 준비 인식 상태를 표시

        self._worker.result_ready.connect(self._on_ocr_result)  # 인식 결과를 화면으로 전달한다.

        self._worker.failed.connect(self._on_ocr_error) # 실패 안내를 받는다.

        self._worker.finished.connect(self._on_ocr_finished)    # 공통 종료 처리를 연결

        self._worker.start()

    @Slot(object)   # OCR 결과를 화면 스레드에서 처리
    def _on_ocr_result(self, lines: list[OcrText]) -> None: # 종류 후보와 추출한 번호를 표시
        self._ocr_results = list(lines) # 원본 OCR 결과를 수정값과 별도로 보관

        self._fields["resident_number"].clear() # 이번 결과에 이전 번호가 섞이지 않도록 비운다.

        self._document_type_label.setText("신분증 종류: 확인 필요") # 판별 전에는 종류를 확정하지 않는다.

        self._status_label.setText("확인 필요") # 자동 입력 여부와 관계없이 사용자 확인 요구

        if not lines:  # 인식된 글자가 없는지 확인한다.
            self._ocr_output.setPlainText("글자를 찾지 못했습니다. 다른 이미지로 다시 시도해주세요.")  # 빈 결과의 재시도를 안내한다.
            return  # 이번 결과 처리를 종료한다.

        self._ocr_output.setPlainText(  # 원본 글자를 화면에 표시한다.
            "\n".join(line.text for line in lines),  # 항목을 줄바꿈으로 구분한다.
        )  # 원본 표시를 마친다.

        document_type = classify_document(lines)    # 제목으로 신분증 종류 후보 판별

        if document_type != DocumentType.RESIDENT_CARD: # 주민등록증 후보가 아니면 전용 규칙을 적용하지않는다.
            return  # 이번 결과 처리를 종료한다.

        self._document_type_label.setText("신분증 종류: 주민등록증 후보")  # 종류 후보를 표시한다.

        number = extract_resident_number(lines) # 번호 형식과 점수 조건을 확인

        if number is None:  # 번호 후보를 하나로 선택할 수 없는지 확인한다.
            self._status_label.setText("번호 확인 필요")  # 자동 입력하지 못한 번호의 확인을 요청한다.
            return  # 이번 결과 처리를 종료한다.

        self._fields["resident_number"].setText(number)  # 번호 후보를 편집 가능한 입력창에 넣는다.

        self._status_label.setText("추출값 확인 필요")  # 자동 입력한 값도 원본과 대조하도록 안내한다.

    # 백그라운드 실패 알림을 화면 스레드에서 받는다.
    @Slot(str)

    # 인식 실패를 표시한다.
    def _on_ocr_error(self, message: str) -> None:

        self._status_label.setText("인식 실패") # 실패 상태로 변경

        self._ocr_output.setPlainText(message)  # 결과 영역에 실패 안내를 표시

    # 스레드가 종료된 뒤 화면 스레드에서 정리
    @Slot()
    def _on_ocr_finished(self) -> None: # 작업 객체와 버튼 상태를 정리

        if self._worker is not None:    # 정리할 작업 객체가 있는지 확인

            self._worker.deleteLater()  # Qt 이벤트 처리 과정에서 객체를 제거한다.

            self._worker = None # 다음 작업을 받을 수 있도록 참조를 비운다.

        self._open_button.setEnabled(True)

        self._recognize_button.setEnabled(not self._image.isNull())

    def closeEvent(self, event: QCloseEvent) -> None:   # 창 종료 요청을 처리

        if self._worker is not None:    # 진행중이거나 종료 처리 중인 작업을 확인

            event.ignore()  # 실행중인 스레드가 파괴되지 않도록 종료를 미룬다.

            QMessageBox.information(
                self,
                "인식 진행 중",
                "인식이 끝난 뒤 창을 닫아주세요",
            )
            return
        super().closeEvent(event)
