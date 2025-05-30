from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 모델 경로 정의 (공개된 Hugging Face ID 사용)
model_paths = {
    "keyword": "JiinLee/kot5-keyword-summary",
    "medium": "JiinLee/kot5-mid-summary",
    "long": "JiinLee/kot5-long-summary"
}

# 모델과 토크나이저 불러오기 (토큰 없이)
models = {}
tokenizers = {}

for key, path in model_paths.items():
    tokenizers[key] = AutoTokenizer.from_pretrained(path)
    models[key] = AutoModelForSeq2SeqLM.from_pretrained(path).to(device)

# 길이 선택에 따라 요약 실행
def generate_summary(text, length="medium"):
    length_map = {
        "keyword": 32,
        "medium": 96,
        "long": 256
    }
    key = length if length in models else "medium"
    model = models[key]
    tokenizer = tokenizers[key]
    max_len = length_map[key]

    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=384
    ).to(device)

    model.eval()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=max_len,
            num_beams=4,
            early_stopping=True
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# UI에서 호출용
def summarize_text(text, length="medium"):
    return generate_summary(text, length)
