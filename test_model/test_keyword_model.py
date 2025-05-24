from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_path = "./kot5-keyword-summary-v5" 
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, local_files_only=True).to(device)

def generate_keyword_summary(text):
    inputs = tokenizer(
        text,
        max_length=512,
        truncation=True,
        padding="max_length",
        return_tensors="pt"
    ).to(device)

    output_ids = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=35,
        num_beams=4,
        early_stopping=True,
        decoder_start_token_id=tokenizer.pad_token_id 
    )

    decoded = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    cleaned = decoded.replace(" ", "").replace("<unk>", "").replace("</s>", "").strip() 
    return cleaned

# 테스트 예시
test_input = (
    "인공지능은 인간의 사고를 모방하여 문제를 해결하거나 학습하는 기술이다. 최근에는 기계학습, 특히 딥러닝의 발전으로 인해 영상 인식, 음성 인식, 자연어 처리 등 다양한 분야에서 활용되고 있다. 자율주행차, 의료 진단, 추천 시스템 등 실제 산업 분야에서도 인공지능이 빠르게 적용되고 있으며, 이로 인해 윤리적 문제나 일자리 대체 등의 논의도 활발하다.")

print("원문:\n", test_input)
print("키워드 요약:\n", generate_keyword_summary(test_input))
