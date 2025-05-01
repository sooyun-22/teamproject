# 프로젝트 개요

오늘날 많은 현대인들의 일상생활이 바빠짐에 따라 책 한 권을 모두 읽을 시간이 부족한 경우가 많아졌다. 또한 책을 읽기 전에 수많은 도서들 중에서 자신의 취향에 맞는 책을 찾는 것이 어려운 경우가 많아졌다. 물론 온라인 서점이나 도서 플랫폼에서 책 소개가 간단히 제공되지만 독자가 원하는 길이(짧은 요약, 중간 요약, 긴 요약)로 줄거리를 요약해주지는 않는다. 추천 시스템 역시 단순히 인기 순위나 장르 기반에 머무르는 경우가 많아 개인에게 최적화된 추천을 제공하는 시스템은 부족하다. 따라서 이 프로젝트에서는 사용자가 책을 선택하기 전에 책의 핵심 내용을 빠르게 파악해 책 선택을 쉽게 할 수 있도록 도와줄 것이다. 이를 통해 보다 효율적으로 독서 시간을 절약할 수 있도록 지원한다.



# T5모델 참고 링크
github링크: <https://github.com/wisenut-research/KoT5?tab=readme-ov-file#pre-trained-checkpoints>

hugging face링크: <https://huggingface.co/docs/transformers/model_doc/t5>

# naver_books.py 사용법
## 📘 사용 방법 안내 – 네이버 책 정보 저장 코드

이 프로젝트는 네이버 책 검색 API를 이용해 검색어에 해당하는 책 정보를 가져와 **책만들 개별 CSV 파일**로 저장하는 파이썬 스크립트입니다.

### 🔧 1. 사전 준비 사항

#### ✅ 네이버 개발자 센터에서 API 발금
1. [https://developers.naver.com](https://developers.naver.com) 에서 회원가입 및 로그인
2. "애플리케이션 등록" > "검색 > 책 검색" API 사용
3. `Client ID`, `Client Secret` 복사

---

### 📁 2. `config.py` 생성 및 API 키 보관

프로젝트 폴더 내에 `config.py` 파일을 새로 만들고 다음것과 같이 작성하세요:

```python
# config.py
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
```

> 이 파일은 보안상 `.gitignore`에 추가되어 까지 가지는 것이 권장됩니다.

---

### 🐍 3. 필요한 라이브러리 설치

터미널에서 다음 명령으로 필요한 라이브러리를 설치합니다:

```bash
pip install requests
```

---

### ▶️ 4. 코드 실행 방법

`naver_books.py` 파일을 실행하면 됩니다.

```bash
python naver_books.py
```

> 이때 검색어 목록(`queries = ['소설', '과학']`)에 있는 단어에 따라 관련된 책 정보를 자동으로 가져와서 각 책만들 `.csv` 파일로 저장합니다.

---

### 📄 5. 생성되는 결과 파일

예시:
```
소설/
├── 해리포터와_마법사의_돌_0.csv
├── 해리포터와_비림의_방_1.csv
...
```

각 파일에는 다음 정보가 포함됩니다:
- 책 제목 (`Title`)
- 저자 (`Author`)
- 출판사 (`Publisher`)
- 줄거리 (`Description`)

---

### ✅ 6. 참고 사항

- `display` 값을 수정하면 한 검색어당 가져오는 책 수를 늘린 수 있습니다.
- 파일 이름은 책 제목을 기본으로 생성되며, 파일명 충돌 매기를 위해 인덱스 번호가 들어간다.
- `queries` 목록에 원하는 검색어를 자유롭게 추가할 수 있습니다.

