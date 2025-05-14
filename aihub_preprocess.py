#pandas는 미리 설치해 놓아야 하고 코랩 기반으로 만들어진 코드라 
#vscode에서는 수정해야 합니다.

import pandas as pd 
import json
import re
import os
from google.colab import files

# 파일 업로드
uploaded = files.upload()  # 드래그하거나 여러 개 업로드 가능

# 전처리 함수
def preprocess_passage(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = re.sub(r'<.*?>', '', text)               # HTML 태그 제거
    text = re.sub(r'\([^)]*\)', '', text)           # 괄호 안 내용 제거
    text = re.sub(r'[^\w\s가-힣.,!?]', '', text)     # 특수문자 제거
    text = re.sub(r'\s+', ' ', text).strip()        # 공백 정리
    return text

# 전처리 수행
output = []

for filename in uploaded.keys():  # 업로드한 파일 목록 순회
    if filename.endswith(".json"):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            passage = preprocess_passage(data.get("passage", ""))
            summary = preprocess_passage(data.get("summary", ""))
            if passage and summary:
                output.append({"input": passage, "output": summary})

# JSONL 저장
jsonl_filename = "preprocessed_data.jsonl"
with open(jsonl_filename, "w", encoding="utf-8") as f:
    for item in output:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

# 다운로드
files.download(jsonl_filename)
