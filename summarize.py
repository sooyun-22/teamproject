from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "wisenut-nlp-team/KoT5",
    revision="summarization",
    token="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"
)
model = AutoModelForSeq2SeqLM.from_pretrained(
    "wisenut-nlp-team/KoT5",
    revision="summarization",
    token="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"
)

def generate_summary(text, length='medium'):
    length_map = {
        'short': 30,
        'medium': 80,
        'long': 150
    }
    max_len = length_map.get(length, 80)

    input_ids = tokenizer.encode(text, return_tensors='pt', truncation=True, max_length=512)
    summary_ids = model.generate(input_ids, max_length=max_len, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def prioritize_summary(summary, limit=3):
    sentences = summary.split('. ')
    prioritized = sorted(sentences, key=len, reverse=True)[:limit]
    return '. '.join(prioritized)

def summarize_text(text, length='medium'):
    raw_summary = generate_summary(text, length)
    return prioritize_summary(raw_summary)
