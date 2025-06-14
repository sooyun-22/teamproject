# 키워드 요약 모델 학습 코드 (Colab용)

# 파일 업로드
from google.colab import files
uploaded = files.upload()  # summary_keyword_train.jsonl, summary_keyword_val.jsonl

# 전처리: 띄어쓰기 없이 output 유지
import json

with open("summary_keyword_train.jsonl", "r", encoding="utf-8") as fin, \
     open("summary_keyword_train_clean.jsonl", "w", encoding="utf-8") as fout:
    for line in fin:
        item = json.loads(line)
        # 띄어쓰기 없이 그대로
        fout.write(json.dumps(item, ensure_ascii=False) + "\n")

with open("summary_keyword_val.jsonl", "r", encoding="utf-8") as fin, \
     open("summary_keyword_val_clean.jsonl", "w", encoding="utf-8") as fout:
    for line in fin:
        item = json.loads(line)
        fout.write(json.dumps(item, ensure_ascii=False) + "\n")

# huggingface 로그인
from huggingface_hub import login
login()

# 라이브러리 설치
!pip install transformers sentencepiece --quiet

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm

# 모델과 토크나이저 로드
model_name = "wisenut-nlp-team/KoT5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda" if torch.cuda.is_available() else "cpu")
device = model.device

# 키워드 요약용 데이터셋 클래스 정의
class KeywordSummaryDataset(Dataset):
    def __init__(self, path, tokenizer, max_input_len=384, max_output_len=32):
        self.samples = []
        self.tokenizer = tokenizer
        self.max_input_len = max_input_len
        self.max_output_len = max_output_len

        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                self.samples.append(json.loads(line))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item = self.samples[idx]
        inputs = self.tokenizer(
            item["input"], padding="max_length", truncation=True, max_length=self.max_input_len, return_tensors="pt")
        targets = self.tokenizer(
            item["output"], padding="max_length", truncation=True, max_length=self.max_output_len, return_tensors="pt")

        labels = targets["input_ids"].squeeze()
        labels[labels == tokenizer.pad_token_id] = -100

        return {
            "input_ids": inputs["input_ids"].squeeze(),
            "attention_mask": inputs["attention_mask"].squeeze(),
            "labels": labels
        }

# 데이터 로딩
train_dataset = KeywordSummaryDataset("summary_keyword_train_clean.jsonl", tokenizer)
val_dataset = KeywordSummaryDataset("summary_keyword_val_clean.jsonl", tokenizer)
train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=4)

# 옵티마이저 설정
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

# 학습 루프
epochs = 3
best_val_loss = float('inf')
save_path = "kot5-keyword-summary-v5"

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
