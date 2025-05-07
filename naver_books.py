import os
import requests
import csv
import re
from config import client_id, client_secret


# 저장 폴더 경로
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)  # 폴더 없으면 생성

# 최대 저장할 파일 수 설정
MAX_FILES = 100

# 책 정보를 가져오는 함수
def fetch_books(query):
    url = "https://openapi.naver.com/v1/search/book.json"
    params = {'query': query, 'display': 20}
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# 책 데이터를 CSV로 저장하는 함수
def save_book_to_csv(book, filepath):
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Author', 'Publisher', 'Description'])
        writer.writerow([book['title'], book['author'], book['publisher'], book['description']])

# 책 검색 후 저장하는 함수
def search_and_save_books(query):
    print(f"\n검색어: {query}")
    books_data = fetch_books(query)
    saved_files = 0  # 저장된 파일 수 카운트

    for i, item in enumerate(books_data['items']):
        # 파일 이름 생성
        base_name = f"{re.sub('[^0-9a-zA-Z가-힣]', '_', item['title'])}_{i}.csv"
        filepath = os.path.join(DATA_DIR, base_name)

        # 중복 체크 및 저장된 파일 수 확인
        if os.path.exists(filepath):
            print(f"이미 존재함: {filepath} → 저장 생략")
            continue

        if saved_files >= MAX_FILES:
            print(f"최대 저장 개수({MAX_FILES})에 도달했습니다. 저장을 중지합니다.")
            break

        # 파일 저장
        save_book_to_csv(item, filepath)
        saved_files += 1
        print(f"저장됨: {filepath}")

# 여러 검색어 리스트
queries = ['소설', '과학', '경제', '에세이', '역사']

for query in queries:
    search_and_save_books(query)

