from PySide6.QtCore import Qt  # 화면 정렬 옵션을 가져온다.
from PySide6.QtGui import (  # 이미지 읽기와 표시 기능을 가져온다.
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
    QMessageBox,  # 오류 안내 창
    QPushButton,  # 버튼
    QVBoxLayout,  # 세로 배치
    QWidget,  # 기본 위젯
)  # 위젯 관련 import를 마친다.

from idscanner.ui.image_preview import ImagePreview  # 이미지 미리보기 위젯을 가져온다.

class MainWindow(QMainWindow):  # 신분증 이미지와 결과를 보여 줄 메인 창 정의:

    def __init__(self) -> None: # 창 생성 시 필요한 상태와 화면을 초기화:

        super().__init__()  # 부모 클래스의 창 초기화를 실행

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

    def _build_preview_panel(self) -> QFrame:   # 미리보기와 파일 선택 버튼 배치

        panel = self._create_panel("신분증 이미지")

        layout = panel.layout() # 패널에 등록된 레이아웃을 가져온다.

        layout.addWidget(self._preview_label, 1)    # 남는 공간에 미리 보기 배치

        self._open_button.setEnabled(True)

        self._open_button.setToolTip("PNG 또는 JPG 이미지를 선택하세요.")

        self._open_button.clicked.connect(self._open_image)

        layout.addWidget(self._open_button)

        return panel


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

        hint_label = QLabel(
            "인식된 내용은 직접 수정할 수 있습니다.\n"
            "현재는 입력창의 편집 동작만 확인할 수 있습니다."
        )

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

    def _open_image(self) -> None:  # 파일을 선택하고 읽기에 성공한 이미지만 반영한다.
        file_path, _ = QFileDialog.getOpenFileName(  # 파일 경로와 선택한 필터를 받는다.
            self,  # 파일 선택 창의 부모를 지정한다.
            "신분증 이미지 선택",  # 파일 선택 창 제목을 지정한다.
            "",  # 기본 시작 폴더를 사용한다.
            "이미지 파일 (*.png *.jpg *.jpeg)",  # 선택할 이미지 형식을 지정한다.
        )  # 파일 선택을 마친다.
        if not file_path:  # 사용자가 선택을 취소했는지 확인한다.
            return  # 기존 이미지와 입력값을 유지한다.

        reader = QImageReader(file_path)  # 선택한 파일의 이미지 리더를 생성한다.
        reader.setAutoTransform(True)  # 이미지에 기록된 방향 정보를 적용한다.
        image = reader.read()  # 파일에서 이미지를 읽는다.
        if image.isNull():  # 손상된 파일 등으로 읽기에 실패했는지 확인한다.
            QMessageBox.warning(  # 실패 안내 창을 표시한다.
                self,  # 안내 창의 부모를 지정한다.
                "이미지 불러오기 실패",  # 안내 창 제목을 지정한다.
                "이미지를 읽을 수 없습니다. 다른 PNG 또는 JPG 파일을 선택하세요.",  # 해결 방법을 안내한다.
            )  # 오류 안내를 마친다.
            return  # 기존 이미지와 입력값을 유지한다.

        self._preview_label.set_image(QPixmap.fromImage(image))  # 성공한 이미지를 표시한다.
        for editor in self._fields.values():  # 이전 결과 입력창을 순회한다.
            editor.clear()  # 새 이미지에 이전 입력값이 남지 않도록 비운다.
        self._document_type_label.setText("신분증 종류 · 인식 대기")  # 판별 상태를 초기화한다.
        self._status_label.setText("이미지 준비")  # 이미지 로딩 완료를 표시한다.
        self._confirm_button.setEnabled(False)  # 인식과 검증 전에는 확정을 막는다.
