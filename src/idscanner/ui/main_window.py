from PySide6.QtCore import Qt   # 정렬 방향 등 Qt의 공통 설정값을 가져옴.

from PySide6.QtWidgets import ( # 화면 구성에 사용할 위젯과 레이아웃
    QFrame, # 패널 컨테이너
    QHBoxLayout,    # 가로 배치
    QLabel, # 텍스트 이미지 표시
    QLineEdit,  # 한 줄 입력
    QMainWindow,    # 메인창
    QPushButton,    # 버튼
    QVBoxLayout,    # 세로배치
    QWidget,    # 기본 위젯
)

class MainWinodw(QMainWindow):  # 신분증 이미지와 결과를 보여 줄 메인 창 정의:

    def __init__(self) -> None: # 창 생성 시 피룡한 상태와 화면을 초기화:

        super().__init__()  # 부모 클래스의 창 최고화를실행

        self._fields: dict[str, QLineEdit] = {} # 항목 이름별 입력창을 보관

        self._status_label = QLabel("준비") # 현재 처리 상태 표시

        self._preview_label = QLabel()  # 이미지 또는 이미지 안내 문구 표시

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

    def _build_preview_panel(self) -> QFrame:   # 이미지 미리보기 패널

        panel = self._create_panel("신분증 이미지")

        layout = panel.layout() # 공통 생성 과정에서 등록한 레이아웃 가져옴

        self._preview_label.setText(
            "신분증 이미지 미리보기\n\n이미지를 불러오면 이곳에 표시됩ㄴ디ㅏ."
        )

        self._preview_label.setObjectName("preview")

        self._preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._preview_label.setWordWrap(True)

        self._preview_label.setMinimumHeight(280)

        layout.addWidget(self._preview_label, 1)

        self._open_button.setEnabled(False) # 이미지 기능을 연결할때까지 비활성화

        self._open_button.setToolTip("이미지 불러오기는 다음 단계에서 연결")

        layout.addWidget(self._open_button) # 이미지 선택 버튼을 패널 하단에 추가한다.

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

            self._add_result(layout, key, label)    # 라벨과 입력창 추가

            hint_label = QLabel(
                "인식된 내용은 직접 수정할 수 있습니다.\n"
                "현재는 입력창의 편집 동작만 확인할 수 있습니다."
            )

            hint_label.setObjectName("hint")

            hint_label.setWordWrap(True)

            layout.addStretch()

            self._confirm_button.setObjectName("primaryButton")

            self._confirm_button.setEnabled(False)

            layout.addWidget(self._confirm_button)

            return panel
    def _add_result_field(  # 라벨과 입력창을 한 쌍으로 추가하는 메서드 정의
            self,   # 현재 창 인스터스 받는다.
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






