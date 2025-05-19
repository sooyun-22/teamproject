# 1. 필요한 패키지 설치
!pip install transformers sentencepiece torch --quiet

# 2. 파일 업로드
from google.colab import files
uploaded = files.upload()  # 👉 여기서 파일 선택하세요

input_file = list(uploaded.keys())[0]  # 업로드된 파일 이름

# 3. 모델 로딩 (KoBART - 긴 요약용)
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = "digit82/kobart-summarization"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

# 4. 요약 함수 정의
def generate_long_summary_kobart(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True).to(device)
    output = model.generate(
        inputs["input_ids"],
        max_length=90,
        min_length=70,
        num_beams=4,
        repetition_penalty=2.0,
        no_repeat_ngram_size=3,
        early_stopping=True
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)

# 5. 파일 분할 & 처리 함수
import json
import os

def process_jsonl_file(input_path, start_index=0, end_index=None):
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    if end_index is None:
        end_index = len(lines)

    lines_to_process = lines[start_index:end_index]

    # 출력 파일명 자동 생성
    output_file = f"long_summary_{start_index}_{end_index or 'end'}.jsonl"
    
    # 파일 모드 설정: 처음이면 'w', 있으면 'a'
    file_mode = 'a' if os.path.exists(output_file) else 'w'

    with open(output_file, file_mode, encoding='utf-8') as outfile:
        for idx, line in enumerate(lines_to_process, start=start_index):
            try:
                obj = json.loads(line)
                original_text = obj.get("text") or obj.get("input")
                if not original_text:
                    continue
                summary_long = generate_long_summary_kobart(original_text)
                obj["summary_long"] = summary_long
                outfile.write(json.dumps(obj, ensure_ascii=False) + "\n")
            except Exception as e:
                print(f"❌ {idx}번째 줄 처리 중 오류 발생: {e}")
                continue

    print(f"✅ {output_file} 저장 완료!")
    return output_file

# 6. 실행 예시 (원하는 구간만 수정하면 됨)
output_file = process_jsonl_file(input_file, start_index=0, end_index=100)

# 7. 다운로드
files.download(output_file)
