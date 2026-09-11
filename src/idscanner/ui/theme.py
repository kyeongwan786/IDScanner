# 앱 전체에 적용할 Qt 스타일시트를 문자열로 정의한다.
APP_STYLE = """
QWidget {
    color: #172B4D;
    font-size: 14px;
}

QMainWindow {
    background-color: #F3F5F9;
}

QLabel {
    background: transparent;
}

QLabel#appTitle {
    font-size: 26px;
    font-weight: 700;
}

QLabel#sectionTitle {
    font-size: 18px;
    font-weight: 600;
}

QLabel#subtitle,
QLabel#hint {
    color: #607089;
}

QLabel#statusBadge {
    background-color: #E8EEF9;
    color: #315A9C;
    border-radius: 12px;
    padding: 8px 14px;
}

QFrame#panel {
    background-color: #FFFFFF;
    border: 1px solid #E1E7F0;
    border-radius: 16px;
}

QLabel#preview {
    background-color: #F8FAFD;
    color: #718096;
    border: 2px dashed #CFD8E6;
    border-radius: 12px;
    padding: 20px;
}

QLineEdit {
    background-color: #FFFFFF;
    border: 1px solid #CCD5E2;
    border-radius: 8px;
    padding: 10px 12px;
    selection-background-color: #DCE8FF;
    selection-color: #172B4D;
}

QLineEdit:focus {
    border: 1px solid #356AE6;
}

QPushButton {
    background-color: #FFFFFF;
    border: 1px solid #CCD5E2;
    border-radius: 8px;
    padding: 11px 18px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #F0F4FA;
}

QPushButton:focus {
    border: 1px solid #356AE6;
}

QPushButton#primaryButton {
    background-color: #356AE6;
    color: #FFFFFF;
    border: 1px solid #356AE6;
}

QPushButton#primaryButton:hover {
    background-color: #2856C5;
}

QPushButton:disabled,
QPushButton#primaryButton:disabled {
    background-color: #EDF1F6;
    color: #8A97AB;
    border: 1px solid #E1E7F0;
}
"""
