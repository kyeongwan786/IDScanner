# IDScanner

여러 종류의 신분증에서 필요한 정보를 추출하고,
사용자가 인식 결과를 확인·수정할 수 있는 데스크톱 프로그램.

## 목표

- 신분증 종류 자동 판별
- 종류별 필요한 항목 추출
- 불필요한 배경 문구와 도장 문구를 최종 결과에서 제외
- 누락되거나 불확실한 항목의 확인 안내
- 인식 결과 직접 수정
- 사용자 확인 후 결과 확정

주민등록증부터 구현한 뒤 운전면허증, 복지카드,
국가유공자카드 등으로 지원 범위를 확장한다.
지원하는 종류와 서식은 별도로 관리한다.

## 개발 환경

- 개발 OS: macOS
- 최종 실행 OS: Windows
- Python: 3.12
- GUI: PySide6
- OCR 엔진: 샘플 평가 후 선정

## 프로젝트 구조

```text
src/
└── idscanner/
    ├── __init__.py
    ├── __main__.py
    └── ui/
        ├── __init__.py
        ├── image_preview.py
        ├── main_window.py
        └── theme.py
```

- `__main__.py`: 애플리케이션 실행
- `ui/image_preview.py`: 이미지 표시와 크기 조절
- `ui/main_window.py`: 메인 화면 구성
- `ui/theme.py`: 공통 스타일

OCR, 신분증 분류·추출, 검증 모듈은 구현 단계에서 추가한다.

## 개발 환경 구성

### macOS

```bash
# Python 3.12로 가상환경을 생성한다.
python3.12 -m venv .venv

# 가상환경을 활성화한다.
source .venv/bin/activate

# 프로젝트와 의존성을 개발 모드로 설치한다.
python -m pip install -e .
```

### Windows PowerShell

Python 3.12 설치 후 실행한다.

```powershell
# Python 3.12로 가상환경을 생성한다.
py -3.12 -m venv .venv

# 가상환경의 Python으로 프로젝트를 설치한다.
.\.venv\Scripts\python.exe -m pip install -e .
```

## 실행

### macOS

```bash
# 가상환경을 활성화한다.
source .venv/bin/activate

# 애플리케이션을 실행한다.
python -m idscanner
```

### Windows PowerShell

```powershell
# 가상환경의 Python으로 애플리케이션을 실행한다.
.\.venv\Scripts\python.exe -m idscanner
```

## 현재 구현 범위

- 기본 화면과 공통 스타일
- PNG·JPG 이미지 불러오기와 비율 유지 미리보기
- 창 크기 변경에 따른 이미지 크기 조절
- 파일 선택 취소와 읽기 실패 시 기존 작업 유지
- 편집 가능한 결과 입력창
- 새 이미지 로딩 성공 시 이전 입력값 초기화

자동 분류, OCR, 검증, 결과 저장은 아직 구현하지 않았다.
Windows 실행은 별도 검증이 필요하다.

## 개발 원칙

- 화면, OCR, 신분증 분류·추출, 검증의 책임을 분리한다.
- OCR 원본 결과와 사용자 수정 결과를 구분한다.
- 판별하거나 읽지 못한 결과를 임의로 확정하지 않는다.
- 실제 신분증 이미지와 개인정보가 포함된 결과는 커밋하지 않는다.
- 로컬 개인정보 자료는 Git에서 제외된 `data/local/`에 보관한다.
- 테스트에는 가상의 개인정보를 사용한다.

## Git 작업 방식

1. 이슈에 작업 목표와 완료 조건을 작성한다.
2. main에서 작업 브랜치를 생성한다.
3. 작업 내용을 구현하고 실행을 확인한다.
4. 변경 사항을 커밋하고 푸시한다.
5. PR에 변경 내용과 확인 결과를 작성한다.
6. 검토 후 main에 병합한다.
