# 🧑‍💻 사용자 가이드

## ✅ 설치 방법 (VS Code 기준, Windows 사용자용)

### 1. 프로젝트 다운로드 및 폴더 열기

```bash
git clone https://github.com/sooyun-22/teamproject.git
cd teamproject
```

* VS Code를 열고 위에서 다운로드한 `teamproject` 폴더를 열어주세요.
* 메뉴 경로: `파일 > 폴더 열기`

---

### 2. VS Code에서 터미널 열기 및 가상환경 설정 (선택)

> ❗ PowerShell에서 `activate` 명령이 차단될 경우:
> 관리자 권한 PowerShell을 열고 아래 명령어를 입력하세요:
>
> ```powershell
> Set-ExecutionPolicy RemoteSigned
> ```
>
> 이후 `Y`를 눌러 설정을 허용한 뒤 다시 시도하세요.

```bash
python -m venv venv
venv\Scripts\activate
```

> ❗ 가상환경은 설치된 패키지가 시스템 전체에 영향을 주지 않도록 도와줍니다.

---

### 3. 패키지 설치

> ❗ pip 업그레이드 중 아래와 같은 메시지가 뜰 경우:
>
> ```
> ERROR: To modify pip, please run the following command:
> C:\...python.exe -m pip install --upgrade pip
> ```
>
> 아래 명령어를 대신 사용하세요:
>
> ```bash
> python -m pip install --upgrade pip
> ```

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> ❗ `sentencepiece` 관련 오류 발생 시 아래 명령으로 해결할 수 있습니다:

```bash
pip uninstall sentencepiece
pip install sentencepiece
```

---

### 4. 네이버 API 키 입력

* `src/naver_books.py` 파일 상단에 본인의 [네이버 개발자 센터](https://developers.naver.com/main/)에서 발급받은 `Client ID`와 `Client Secret`을 직접 입력하세요.

---

## ▶ 실행 방법

```bash
python src/main.py
```

* 실행하면 GUI 창이 뜨고, 검색 키워드를 입력하면 책 정보를 확인할 수 있습니다.
* 줄거리를 입력하면 요약 결과도 바로 확인됩니다.

---

## 📌 실행에 필요한 주요 파일 구성

* `summarize.py`: Hugging Face 모델 로딩 및 요약 생성
* `naver_books.py`: 네이버 API를 통한 책 정보 수집
* `p.py`: PyQt 환경 설정
* `requirements.txt`: 전체 환경 구축에 필요한 패키지 목록

---

## 📁 폴더 열기 경로 예시

```text
C:\Users\사용자이름\teamproject
```

또는 GitHub에서 `.zip`으로 다운로드했다면, 압축을 푼 후 생성된 `teamproject-main` 폴더를 열어주세요.
