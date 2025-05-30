from konlpy.tag import Okt
from sentence_transformers import SentenceTransformer, util
import numpy as np
import json
from tqdm import tqdm
from google.colab import files

okt = Okt() # 형태소 분석기
model = SentenceTransformer('jhgan/ko-sbert-nli') # 한국어 임베딩 모델

# 불용어 - 필요없는 단어 제거 (추가할 거 있으면 더 추가 가능)
stopwords = {"근거", "방법", "조사", "단계", "수준", "내용", "이유", "형태", "제시", "현황", "한계", "보급", "효과", "연구"}

# 명사 중 후보 키워드 추출
def get_noun_candidates(text):
    words = okt.pos(text, norm=True, stem=True)
    candidates = []
    buffer = []
    for word, tag in words:
        if tag == "Noun" and word not in stopwords:
            buffer.append(word)
        else:
            if buffer:
                combined = ''.join(buffer)
                if len(combined) > 1:
                    candidates.append(combined)
                buffer = []
    if buffer:
        combined = ''.join(buffer)
        if len(combined) > 1:
            candidates.append(combined)
    return list(set(candidates))

# mmr 알고리즘 - 겹치지 않는 가장 중요한 키워드 2개 추출
def mmr(doc_embedding, candidate_embeddings, words, top_n, diversity):
    word_doc_sim = util.cos_sim(candidate_embeddings, doc_embedding)
    word_sim = util.cos_sim(candidate_embeddings, candidate_embeddings)

    keywords_idx = [np.argmax(word_doc_sim)]
    candidates_idx = [i for i in range(len(words)) if i != keywords_idx[0]]

    for _ in range(top_n - 1):
        mmr_dist = []
        for idx in candidates_idx:
            sim_to_doc = word_doc_sim[idx]
            sim_to_selected = max([word_sim[idx][kw_idx] for kw_idx in keywords_idx])
            score = diversity * sim_to_doc - (1 - diversity) * sim_to_selected
            mmr_dist.append((idx, score))
        mmr_dist.sort(key=lambda x: x[1], reverse=True)
        next_idx = mmr_dist[0][0]
        keywords_idx.append(next_idx)
        candidates_idx.remove(next_idx)

    return [words[i] for i in keywords_idx]

# 업로드
uploaded = files.upload()
filename = next(iter(uploaded))

# jsonl 파일에서의 input과 output 합치기
docs = []
originals = []

with open(filename, 'r', encoding='utf-8') as f:
    for line in tqdm(f):
        try:
            data = json.loads(line)
            input_text = data.get("input", "")
            output_text = data.get("output", "")
            full_text = input_text + " " + output_text
            originals.append(full_text)
            docs.append(full_text)
        except:
            continue

# 키워드 추출
results = []
for doc, original in zip(docs, originals):
    candidates = get_noun_candidates(doc)
    if not candidates:
        results.append({"text": original, "keywords": []})
        continue

    doc_embedding = model.encode(doc, convert_to_tensor=True)
    candidate_embeddings = model.encode(candidates, convert_to_tensor=True)

    keywords = mmr(doc_embedding, candidate_embeddings, candidates, top_n=2, diversity=0.7)

    results.append({
        "text": original,
        "keywords": keywords
    })

# 결과 다운로
output_filename = "custom_mmr_keywords.jsonl"
with open(output_filename, 'w', encoding='utf-8') as f_out:
    for item in results:
        f_out.write(json.dumps(item, ensure_ascii=False) + '\n')

files.download(output_filename)
