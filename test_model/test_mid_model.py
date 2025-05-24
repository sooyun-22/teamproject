from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# 디바이스 설정
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 중간 요약 모델 경로
model_path = "./kot5-mid-summary-v1" 

# 모델과 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, local_files_only=True).to(device)

# 요약 함수
def generate_mid_summary(text):
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
        max_length=92,  # 중간 요약 길이
        num_beams=4,
        early_stopping=True,
        decoder_start_token_id=model.config.decoder_start_token_id 
    )

    decoded = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    cleaned = decoded.replace("<unk>", "").replace("</s>", "").strip()
    return cleaned


# 테스트 예시
test_input = (
    "한편 스마트 기기의 확산과 각종 콘텐츠의 양이 범람함에 따라 이용자들에게 꼭 필요한 콘텐츠를 선별적으로 제공하는 서비스들이 등장하고 있다. 음악시장, 동영상시장, 검색시장에서 빅데이터와 결합된 맞춤형 추천형 콘텐츠가 인기를 끌고 있다. 네이버는 9월 1일부터 새롭게 PC 통합검색 서비스를 개시하여 그동안 단순한 검색결과를 나열식으로 보여주는 것에서 벗어나 이용자가 원하는 맞춤형 결과를 제공하는 방향으로 검색 알고리즘을 바꾸었다. 이용자가 검색어를 입력할 때 원하는 정보가 무엇인지를 유추하여 이에 맞는 검색결과를 제공하기 위한 변화라고 할 수 있다."
)

print(" 원문:\n", test_input)
print(" 중간 요약:\n", generate_mid_summary(test_input))
