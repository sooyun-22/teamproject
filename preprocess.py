import pandas as pd
import os
import re

# 1. 데이터 경로 설정
data_dir = './data'
all_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.csv')]

# 2. 파일 합치기
df_list = [pd.read_csv(file) for file in all_files]
df = pd.concat(df_list, ignore_index=True)

# 3. 컬럼명이 들어간 행 제거 (중복된 헤더 방지용)
df = df[df['Title'] != 'Title']

# 4. 전처리 함수 정의
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = re.sub(r'<.*?>', '', text)       # HTML 태그 제거
    text = re.sub(r'[^\w\s가-힣\n]', '', text) # 특수문자 제거, 단 \n은 남김
    text = re.sub(r'[ ]{2,}', ' ', text)    # 이중 공백 이상 정리
    return text.strip()



# 5. 전처리 적용
df['preprocessed'] = df['Description'].apply(clean_text)

# 6. 전처리 확인
print(df[['Description', 'preprocessed']].head(1))

# 7. Description 덮어쓰기 및 저장
df['Description'] = df['preprocessed']
df.drop(columns=['preprocessed'], inplace=True)
df.to_csv('preprocessed_books.csv', index=False, encoding='utf-8-sig')
print("✅ 전처리 완료 및 저장됨.")
