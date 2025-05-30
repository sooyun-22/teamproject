# 🛠️ 개발자 가이드

> 이 문서는 본 프로젝트를 개발·수정하고자 하는 개발자를 위한 가이드입니다. 전체 구조, 모델 학습 방식, 데이터 포맷, 실행 방법 등을 설명합니다.

## 📁 프로젝트 구조

```
teamproject/
├── src/
│   ├── main.py              # 메인 실행 파일 (GUI 포함)
│   ├── summarize.py         # 요약 모델 로딩 및 실행
│   ├── naver_books.py       # 네이버 책 API 연동
│   ├── p.py                 # PyQt 실행 환경 설정
│   ├── finetune_*.py        # 각 요약 길이별 파인튜닝 코드
│   ├── *_preprocess.py      # 각 요약 길이별 전처리 코드
├── requirements.txt         # 패키지 목록
├── README.md
├── user_guide.md
└── developer_guide.md
```

## 🧹 개발 환경

* Python 3.10 또는 3.11 권장 (3.12 이상에서는 일부 패키지 설치 실패 가능)
* 가상환경 사용 권장
* 주요 라이브러리: `PyQt5`, `transformers`, `datasets`, `keybert`, `sentencepiece` 등

## 📦 데이터 수집 및 전처리

### 📥 AIHub 데이터 수집

* AIHub에서 '책 줄거리 요약 데이터셋' 다운로드 (json 형식)
* 다운로드한 파일은 깃허브에 업로드하지 않도록 주의
* **Colab 환경에서 전처리와 파인튜닝을 수행하였으며, 결과 파일만 로컬에 반영**

### 🧼 전처리

```bash
# 중간 요약용 데이터 전처리
python src/preprocess/aihub_mid_preprocess.py

# 키워드 요약용 전처리
python src/preprocess/keyword_preprocess.py

# 긴 요약용 전처리
python src/preprocess/long_preprocess.py
```

* 결과는 `jsonl/` 폴더에 `.jsonl` 형식으로 저장됨
* 학습용/검증용 데이터로 split 된 파일은 `data/` 폴더에 저장됨

## 📊 학습 데이터 형식

```json
{"input": "줄거리 내용", "output": "요약 또는 키워드"}
```

* 줄거리: 한 문단 내외
* 출력: 요약 또는 쉼표로 구분된 키워드 2개

## 🧠 모델 파인튜닝

```bash
# 키워드 요약 모델 학습
python src/training/finetune_keyword.py

# 중간 요약 모델 학습
python src/training/finetune_mid.py

# 긴 요약 모델 학습
python src/training/finetune_long.py
```

> ⚠️ 학습 시 GPU 사용 권장
> ⚠️ `sentencepiece` 오류 발생 시 Python 3.10 사용
> ✅ Colab에서 사전 학습 및 파인튜닝 후 모델 export하여 로컬에서 사용 가능

## 🚀 실행 및 테스트

```bash
# PyQt 기반 프로그램 실행
python src/main.py
```

* 실행 후 프로젝트 목록에서 책을 선택하고 평가 가능
* 요약 및 키워드는 GUI에서 확인 가능
* `naver_books.py`와 연동되면 책 정보 자동 수집 가능

## 🔍 주요 모듈 상세 설명

### `summarize.py` – 요약 모델 처리 핵심 모듈

| 항목            | 설명                                                                                      |   |
| ------------- | --------------------------------------------------------------------------------------- | - |
| **기능**        | Hugging Face Transformers 기반 모델을 불러와 요약 결과 생성                                           |   |
| **입력값**       | `str` 형태의 줄거리 텍스트                                                                       |   |
| **출력값**       | `str` 형태의 요약 결과 (혹은 키워드 2개)                                                             |   |
| **수정 포인트 예시** | 모델 경로 바꾸기, 추론 max\_length 조정, 다중 요약 지원 등                                                |   |
|               |                                                                                         |   |

### `naver_books.py` – 네이버 API 연동 및 도서 검색

| 항목            | 설명                                                                   |
| ------------- | -------------------------------------------------------------------- |
| **기능**        | 네이버 Open API를 사용해 도서명 기반 검색 및 정보 반환                                  |
| **입력값**       | 검색어 `keyword` (str)                                                  |
| **출력값**       | 책 제목, 저자, 출판사, 설명 등의 딕셔너리 리스트                                        |
| **수정 포인트 예시** | 응답 구조 변경 대응, 검색 결과 수 제한 변경, 필터링 조건 추가                                |
| **주의 사항**     | `client_id` 및 `client_secret`은 코드 상단에 직접 작성해야 함 (별도 관리 권장)           |

## 🧰 디버깅 팁

* `sentencepiece` 오류 발생 시: Python 3.10로 다운그레이드 필요 (다운그레이드 하면 대부분 정상 설치됨)
* PyQt GUI 오류 시: `p.py`에서 Qt 플러그인 경로 수정 확인
* 네이버 API 오류 시: `naver_books.py` 상단의 `client_id`와 `secret` 값 확인

## 💡 기타 팁

* 모든 패키지는 `requirements.txt`로 설치 가능:

```bash
pip install -r requirements.txt
```

* 패키지 충돌 방지를 위해 가상환경 사용 권장:

```bash
python -m venv venv
venv\Scripts\activate
```

> 🧷 개발 초기 또는 실행 오류 발생 시, `README.md`와 `user_guide.md`도 함께 참고 바랍니다.
