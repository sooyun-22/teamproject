# 1. 파일 업로드
from google.colab import files
uploaded = files.upload()  # 👉 여기서 로컬에서 .jsonl 파일 선택

# 2. 업로드된 파일 이름 가져오기
input_path = list(uploaded.keys())[0]  # 업로드한 파일명 자동 추출
output_path = input_path.replace(".jsonl", "_refined.jsonl")  # 저장할 파일명

# 3. 정제 함수 정의
import json
import re

def refine_summary_enhanced(text):
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r'국민의 생명과 재산을 보호하는 것이.*?의무이기 때문이다\.', '국민의 생명과 재산 보호는 국가의 기본적인 의무이다.', text)
    text = re.sub(r'(가장 기본적인 의무이기 때문에|가장 기본적인 의무이기 때문이다)', '기본적인 의무이다', text)
    text = re.sub(r'(이는 )?([^\.\n]+)\. \2\.', r'\2.', text)
    text = re.sub(r'\.\s*\.', '.', text)
    text = text.replace('수급조절을 지연시킨다든지', '수급조절을 의도적으로 지연시키거나')
    text = text.replace('가격을 높게 책정하여', '가격을 인위적으로 높게 책정하여')
    text = re.sub(r' +', ' ', text)
    if not text.endswith('.'):
        text += '.'
    return text

# 4. 파일 읽고 정제하여 저장
with open(input_path, 'r', encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        data = json.loads(line)
        summary = data.get("summary_long", "")
        refined = refine_summary_enhanced(summary)
        data["summary_long_refined"] = refined
        f_out.write(json.dumps(data, ensure_ascii=False) + "\n")

print("✅ 정제 완료! →", output_path)

# 5. 정제된 파일 다운로드
files.download(output_path)
