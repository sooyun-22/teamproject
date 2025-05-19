# 1. 필요한 패키지 설치
!pip install transformers sentencepiece torch --quiet

# 2. 파일 업로드
from google.colab import files
uploaded = files.upload()  # 👉 여기서 파일 선택하세요

input_file = list(uploaded.keys())[0]  # 업로드된 파일 이름
output_file = "long_summary_output.jsonl"

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

# 5. 파일 분할 & 처리
import json

def process_jsonl_file(input_path, output_path, chunk_size=100):
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for i in range(0, len(lines), chunk_size):
            chunk = lines[i:i+chunk_size]
            for line in chunk:
                try:
                    obj = json.loads(line)
                    original_text = obj.get("text") or obj.get("input")
                    if not original_text:
                        continue
                    summary_long = generate_long_summary_kobart(original_text)
                    obj["summary_long"] = summary_long
                    outfile.write(json.dumps(obj, ensure_ascii=False) + "\n")
                except Exception as e:
                    print(f"❌ 오류 발생 (건너뜀): {e}")
                    continue

# 6. 실행
process_jsonl_file(input_file, output_file)
print("✅ 긴 요약 생성 완료!")

# 7. 다운로드 링크 제공
files.download(output_file)
