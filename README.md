# 📚 책 줄거리 요약 프로젝트

바쁜 일상 속에서 독서 시간을 충분히 확보하기 어려운 현대인을 위해,  
이 프로젝트는 책을 읽기 전 줄거리의 핵심 내용을 다양한 길이로 요약해주는 기능을 제공합니다.  
그 뿐 아니라, 사용자는 키워드를 입력해 관련 책을 추천 받을 수 있습니다.

요약은 Hugging Face의 KoT5 기반 모델을 파인튜닝하여 생성되며,  
PyQt5 기반의 직관적인 인터페이스를 통해 책 정보와 요약 결과를 쉽게 확인할 수 있습니다.

---

## ✅ 프로젝트 개요

- 💡 **목적**: 책 줄거리의 핵심 내용을 다양한 길이로 자동 요약, 사용자에게 맞는 책 추천
- 🧠 **사용 모델**: Hugging Face KoT5 파인튜닝 모델 3종 (keyword / mid / long)
- 🖥️ **UI 구성**: PyQt5로 간단한 데스크탑 인터페이스 구현
- 🔍 **책 정보**: 네이버 책 검색 API 활용

---

## 🔧 사용 기술 스택

| 분야       | 기술 |
|------------|------|
| 프로그래밍 | Python 3.9+ |
| 프론트엔드 | PyQt5 |
| NLP 모델   | Hugging Face Transformers, KoT5 |
| 기타       | PIL, requests, jsonl 포맷 | 

---



## 🤖 사용 모델 (Hugging Face) 
JiinLee/kot5-keyword-summary

JiinLee/kot5-mid-summary

JiinLee/kot5-long-summary

모델은 모두 공개(Public) 상태이며, transformers 라이브러리에서 토큰 없이 직접 불러올 수 있습니다.
자세한 정보는 huggingface_links.md 참조.

---

## 📁 디렉토리 구조
```plaintext 
teamproject/
│
├── README.md                  # 전체 개요 및 실행 안내
├── requirements.txt           # 필요한 패키지
├── .gitignore                 # 캐시, 민감 정보 제외  
├── huggingface_links.md     # 모델 링크 정리
│
├── src/                       # 소스 코드
│   ├── main.py                # 실행 (GUI 포함)
│   ├── summarize.py           # 모델 요약 실행
│   ├── naver_books.py         # 책 정보 수집
│   ├── p.py                   # PyQt 환경 설정
│   ├── preprocess/
│   	  │── aihub_mid_preprocess.py # 중간 요약 전처리 코드
│   	  │── keyword_preprocess.py # 키워드 요약 전처리 코드
│   	  │── long_preprocess.py # 긴 요약 전처리 코드
│   └── training/              # 모델 학습 코드
│       ├── finetune_keyword.py
│       ├── finetune_mid.py
│       └── finetune_long.py
│
├── data/                      # 데이터셋 (jsonl 포맷)
│   ├── preprocessed_data.jsonl
│   ├── summary_keyword_train.jsonl
│   ├── summary_keyword_val.jsonl
│   └── ... 생략
│
└── docs/                      # 문서 폴더
    ├── user_guide.md          # 사용자 가이드
    └── developer_guide.md     # 개발자 가이드
```
---

## 📄 문서 바로 가기
📘 사용자 가이드
🛠️ 개발자 가이드

