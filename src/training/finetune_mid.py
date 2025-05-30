# 중간 요약 모델 학습 코드 (Colab용)

import json
from google.colab import files
uploaded = files.upload()  # summary_mid_train.jsonl, summary_mid_val.jsonl 업로드

# Hugging Face 로그인
from huggingface_hub import login
login()

# 라이브러리 설치
!pip install transformers sentencepiece --quiet

# 기본 구성
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm

# 모델과 토크나이저 로드
model_name = "wisenut-nlp-team/KoT5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda" if torch.cuda.is_available() else "cpu")

# 키워드 요약용 데이터셋 클래스 정의
class MidSummaryDataset(Dataset):
    def __init__(self, filepath, tokenizer, max_input_len=384, max_output_len=96):
        self.samples = []
        self.tokenizer = tokenizer
        self.max_input_len = max_input_len
        self.max_output_len = max_output_len

        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                self.samples.append(item)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]
        inputs = self.tokenizer(sample["input"], padding="max_length", truncation=True, max_length=self.max_input_len, return_tensors="pt")
        targets = self.tokenizer(sample["output"], padding="max_length", truncation=True, max_length=self.max_output_len, return_tensors="pt")

        labels = targets["input_ids"].squeeze()
        labels[labels == tokenizer.pad_token_id] = -100

        return {
            "input_ids": inputs["input_ids"].squeeze(),
            "attention_mask": inputs["attention_mask"].squeeze(),
            "labels": labels
        }

# 데이터 로딩
train_dataset = MidSummaryDataset("summary_mid_train.jsonl", tokenizer)
val_dataset = MidSummaryDataset("summary_mid_val.jsonl", tokenizer)
train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=4)

# 옵티마이저 설정
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

# 학습 루프
epochs = 3
save_path = "kot5-mid-summary-v1"
best_val_loss = float('inf')
device = model.device

for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}"):
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        total_loss += loss.item()
    avg_train_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch+1} Train Loss: {avg_train_loss:.4f}")

    # 검증
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for batch in val_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            val_loss += outputs.loss.item()
    avg_val_loss = val_loss / len(val_loader)
    print(f"Epoch {epoch+1} Val Loss: {avg_val_loss:.4f}")

    # 최적 모델 저장
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        print(f"✅ Best model updated at epoch {epoch+1} (val_loss={best_val_loss:.4f})")
        model.save_pretrained(save_path)
        tokenizer.save_pretrained(save_path)
