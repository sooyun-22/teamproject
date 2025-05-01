import os
import requests
import csv
import re

# 네이버 API 클라이언트 ID와 클라이언트 시크릿 입력
client_id = os.getenv('NAVER_CLIENT_ID')  # 환경변수에서 클라이언트 ID를 가져옵니다.
client_secret = os.getenv('NAVER_CLIENT_SECRET')  # 환경변수에서 클라이언트 시크릿을 가져옵니다.

# 책 정보를 가져오는 함수
def fetch_books(query):
    url = "https://openapi.naver.com/v1/search/book.json"
    params = {'query': query, 'display': 10}  # 쿼리와 결과 개수 지정 (여기선 10개)
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# 책 데이터를 CSV로 저장하는 함수
def save_book_to_csv(book, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Author', 'Publisher', 'Description'])  # 헤더 작성
        title = book['title']
        author = book['author']
        publisher = book['publisher']
        description = book['description']
        writer.writerow([title, author, publisher, description])

# 책 제목에 대해 검색하여 저장하는 함수
def search_and_save_books(query):
    books_data = fetch_books(query)
    for i, item in enumerate(books_data['items']):
        title = item['title']
        # 제목을 파일 이름에 사용할 수 있도록 적절히 변환
        filename = f"{re.sub('[^0-9a-zA-Z가-힣]', '_', title)}_{i}.csv"  # 책마다 파일을 구별하기 위해 인덱스 추가
        save_book_to_csv(item, filename)

# 여러 검색어로 책 정보 저장하기
queries = ['소설']  # 여러 검색어 추가
for query in queries:
    search_and_save_books(query)
