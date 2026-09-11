import sys  # 실행 인자와 프로세스 종료 코드를 처리한다.

from PySide6.QtWidgets import QApplication  # Qt 애플리케이션 실행 관리

from idscanner.ui.main_window import MainWindow # 앱의 메인 화면을 가져온다.

from idscanner.ui.theme import APP_STYLE    # 앱 전체에 적용할 스타일을 가져온다.

def main() -> int:  # 애플리케이션을 실행하고 종료 코드를 반환
    app = QApplication(sys.argv)    # 명령줄 인자를 전달해 Qt 앱을  생성
    app.setApplicationName("IDScanner") # 이름 등록
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLE)

    window = MainWindow()   # 메인 창 생성
    window.show()   # 생성한 창을 화면에 표시

    return app.exec()   # 창이 닫힐 때까지 이벤트를 처리하고 종료 코드를 반환

if __name__ == "__main__":  # 이 모듈이 실행 진입점으로 호출됐는지 확인
    raise SystemExit(main())    # 앱 실행 결과를 프로세스 종료 코드로 전달.
