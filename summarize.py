# 1. 필요한 라이브러리 설치
!pip install transformers sentencepiece

# 2. 라이브러리 임포트
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
import pandas as pd
from tqdm import tqdm

# 3. Kobart 모델 불러오기 (한국어 요약 특화)
tokenizer = PreTrainedTokenizerFast.from_pretrained("digit82/kobart-summarization")
model = BartForConditionalGeneration.from_pretrained("digit82/kobart-summarization")

# 4. 텍스트 전처리 함수
def clean_text(text):
    return str(text).replace('\n', ' ').replace('\r', '').strip()

# 5. 프롬프트 생성 (문장 수 명시)
def make_prompt(text, style):
    if style == "short":
        return f"다음 글을 1~2문장으로 요약해줘: {text}"
    elif style == "medium":
        return f"다음 글을 3~4문장으로 요약해줘: {text}"
    elif style == "long":
        return f"다음 글을 5문장 이상으로 요약해줘: {text}"

# 6. 문장 수 조절 함수
def trim_to_sentence_count(text, target_range):
    sentences = text.strip().replace("..", ".").split('. ')
    sentences = [s.strip() for s in sentences if s]
    min_s, max_s = target_range
    if len(sentences) < min_s:
        return '. '.join(sentences).strip() + '.'
    elif len(sentences) > max_s:
        return '. '.join(sentences[:max_s]).strip() + '.'
    else:
        return '. '.join(sentences).strip() + '.'

# 7. 요약 함수
def generate_summary(text, style):
    prompt = make_prompt(text, style)
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    output = model.generate(inputs["input_ids"], max_length=256, num_beams=4, early_stopping=True)
    result = tokenizer.decode(output[0], skip_special_tokens=True)

    sentence_ranges = {
        "short": (1, 2),
        "medium": (3, 4),
        "long": (5, 100)
    }
    return trim_to_sentence_count(result, sentence_ranges[style])

# 8. CSV 불러오기 (파일명을 업로드한 파일명으로 맞추세요)
df = pd.read_csv("books.csv")  # 업로드 후 실행

# 9. 요약 실행 및 저장
short_summaries = []
medium_summaries = []
long_summaries = []

print("⏳ 요약 생성 중...")

for desc in tqdm(df["Description"]):
    short_summaries.append(generate_summary(desc, "short"))
    medium_summaries.append(generate_summary(desc, "medium"))
    long_summaries.append(generate_summary(desc, "long"))

df["summary_short"] = short_summaries
df["summary_medium"] = medium_summaries
df["summary_long"] = long_summaries

# 10. 결과 저장
df.to_csv("books_with_multi_summary.csv", index=False)
print("✅ 요약 완료! 'books_with_multi_summary.csv'로 저장되었습니다.")
