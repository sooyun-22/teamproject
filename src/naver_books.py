import random
import requests
from urllib.parse import quote
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt  
from io import BytesIO
from PIL import Image

# 네이버 API 키
client_id = 'your_client_id_here'
client_secret = 'your_client_secret_here'

def preprocess_query(raw_keyword):
    # 사용자가 "과학 + 영화" 형태로 입력한 경우
    if '+' in raw_keyword:
        keywords = raw_keyword.split('+')
        # strip()을 써서 공백 제거 후 띄어쓰기로 연결
        return ' '.join(k.strip() for k in keywords)
    return raw_keyword

# 전역 상태 저장: 키워드별로 이미 출력한 책 제목 기억
shown_titles_by_keyword = {}

def fetch_books(query, display=3, shown_titles=None):
    # 정확한 제목 검색 여부
    exact_match = query.startswith('"') and query.endswith('"')
    
    # 검색 쿼리 인코딩
    encoded_query = quote(query)
    total_fetch = 50 if not exact_match else display
    url = f"https://openapi.naver.com/v1/search/book.json?query={encoded_query}&display={total_fetch}&start=1"

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    all_books = response.json().get("items", [])

    # 중복 제거 및 이미 본 책 제외
    unique_books = []
    seen = set() if shown_titles is None else set(shown_titles)
    for book in all_books:
        title = book.get("title", "").strip()
        if title not in seen:
            seen.add(title)
            unique_books.append(book)

    # 무작위로 display개 추출
    random.shuffle(unique_books)
    return unique_books[:display]

def simple_summary(desc, max_len=300):
    import html
    clean = html.unescape(desc).replace('\n', ' ').replace('\t', ' ').strip()
    clean = ' '.join(clean.split())
    return clean[:max_len] + '...' if len(clean) > max_len else clean

def recommend_books(keyword, parent_layout, image_refs):
    global shown_titles_by_keyword

    keyword = preprocess_query(keyword)
    exact_match = keyword.startswith('"') and keyword.endswith('"')
    display = 1 if exact_match else 3

    # 이전에 보여준 제목 리스트 가져오기
    shown_titles = shown_titles_by_keyword.get(keyword, set())

    books = fetch_books(keyword, display=display, shown_titles=shown_titles)

    # 만약 새로운 결과가 없다면 캐시 초기화 후 다시 시도
    if not books and shown_titles:
        shown_titles_by_keyword[keyword] = set()
        books = fetch_books(keyword, display=display, shown_titles=set())

    # 레이아웃 초기화
    for i in reversed(range(parent_layout.count())):
        item = parent_layout.itemAt(i).widget()
        if item:
            item.setParent(None)
    image_refs.clear()

    if books:
        for i, book in enumerate(books):
            shown_titles_by_keyword.setdefault(keyword, set()).add(book['title'])

            book_widget = QWidget()
            layout = QHBoxLayout()
            book_widget.setLayout(layout)

            # 이미지
            img_url = book.get('image')
            if img_url:
                try:
                    img_data = requests.get(img_url).content
                    img = Image.open(BytesIO(img_data)).resize((200, 280))
                    img_bytes = BytesIO()
                    img.save(img_bytes, format='PNG')
                    pixmap = QPixmap()
                    pixmap.loadFromData(img_bytes.getvalue())
                    img_label = QLabel()
                    img_label.setPixmap(pixmap)
                    img_label.setFixedSize(200, 280)
                    layout.addWidget(img_label)
                    image_refs.append(pixmap)
                except Exception as e:
                    print(f"이미지 로드 실패: {e}")

            # 텍스트
            text = (
                f"{i+1}. 제목: {book['title']}\n"
                f"   저자: {book['author']}\n"
                f"   출판사: {book['publisher']}\n"
                f"   설명: {simple_summary(book['description'])}"
            )
            text_label = QLabel(text)
            text_label.setWordWrap(True)
            text_label.setFixedHeight(280)
            text_label.setStyleSheet("font-family: 'Arial'; font-size: 24px;")
            text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            text_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            layout.addWidget(text_label)
            layout.setAlignment(text_label, Qt.AlignVCenter)

            parent_layout.addWidget(book_widget)
    else:
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(None, "검색 결과 없음", "⚠️ 더 이상 새로운 결과가 없습니다.")
