from google.colab import files
uploaded = files.upload()
from huggingface_hub import login
login()  # 여기에 토큰을 입력하라고 나옵니다
# ✅ KoT5 중간 요약 파인튜닝 (Hugging Face Trainer 없이 PyTorch 직접 학습)

!pip install transformers sentencepiece --quiet

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from torch.utils.data import Dataset, DataLoader
import json
from tqdm import tqdm

# 1. 모델 및 토크나이저 로딩
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "wisenut-nlp-team/KoT5"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


# 2. 커스텀 데이터셋
class SummaryDataset(Dataset):
    def __init__(self, path, tokenizer, max_input_len=512, max_target_len=128):
        self.data = []
        self.tokenizer = tokenizer
        self.max_input_len = max_input_len
        self.max_target_len = max_target_len
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                self.data.append(item)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        inputs = self.tokenizer(
            item["input"], max_length=self.max_input_len, truncation=True, padding="max_length", return_tensors="pt"
        )
        targets = self.tokenizer(
            item["output"], max_length=self.max_target_len, truncation=True, padding="max_length", return_tensors="pt"
        )
        return {
            "input_ids": inputs["input_ids"].squeeze(),
            "attention_mask": inputs["attention_mask"].squeeze(),
            "labels": targets["input_ids"].squeeze()
        }

# 3. 데이터 로딩
train_dataset = SummaryDataset("summary_mid_train_final.jsonl", tokenizer, max_input_len=384, max_target_len=96)
val_dataset = SummaryDataset("summary_mid_val_final.jsonl", tokenizer)
train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=4)

# 4. 옵티마이저 설정
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

# 5. 학습 루프
num_epochs = 5
for epoch in range(num_epochs):
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
    print(f"Epoch {epoch+1} Train Loss: {total_loss / len(train_loader):.4f}")

    # 검증
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for batch in val_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            val_loss += outputs.loss.item()
    print(f"Epoch {epoch+1} Val Loss: {val_loss / len(val_loader):.4f}")

# 6. 모델 저장
model.save_pretrained("kot5-mid-summary-manual")
tokenizer.save_pretrained("kot5-mid-summary-manual")
