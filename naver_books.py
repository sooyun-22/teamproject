import random
import requests
from urllib.parse import quote
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt  
from io import BytesIO
from PIL import Image

# 네이버 API 키
client_id = 'crmFhpIDo84nKGVPAFnp'
client_secret = 'IbfZJb0j1v'

def preprocess_query(raw_keyword):
    # 사용자가 "과학 + 영화" 형태로 입력한 경우
    if '+' in raw_keyword:
        keywords = raw_keyword.split('+')
        # strip()을 써서 공백 제거 후 띄어쓰기로 연결
        return ' '.join(k.strip() for k in keywords)
    return raw_keyword

def fetch_books(query, display=3):
    # 정확한 제목 검색 여부
    exact_match = query.startswith('"') and query.endswith('"')
    
    # 검색 쿼리 인코딩
    query = quote(query)

    # 최대 50개까지 가져와서 무작위 추출할 준비
    total_fetch = 50 if not exact_match else display
    start = 1  # 정확 검색이면 start는 항상 1
    url = f"https://openapi.naver.com/v1/search/book.json?query={query}&display={total_fetch}&start={start}&sort=date"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    all_books = response.json().get("items", [])

    # 중복 제거 (책 제목 기준)
    unique_books = []
    seen_titles = set()
    for book in all_books:
        title = book.get("title", "").strip()
        if title not in seen_titles:
            seen_titles.add(title)
            unique_books.append(book)

    # 무작위로 display 개수만 추출
    random.shuffle(unique_books)
    return unique_books[:display]


def recommend_books(keyword, parent_layout, image_refs):
    """
    keyword : 검색어 문자열
    parent_layout : QWidget의 레이아웃 (QVBoxLayout) - 책 정보를 표시할 영역
    image_refs : QPixmap 참조 리스트 (이미지 소멸 방지용)
    """

    keyword = preprocess_query(keyword)  # ← 전처리
    # 정확한 제목 검색 여부 판단
    exact_match = keyword.startswith('"') and keyword.endswith('"')
    display = 1 if exact_match else 3

    books = fetch_books(keyword, display=display)
    
    # 기존 내용 초기화
    for i in reversed(range(parent_layout.count())):
        item = parent_layout.itemAt(i).widget()
        if item:
            item.setParent(None)
    image_refs.clear()

    if books:
        for i, book in enumerate(books):
            book_widget = QWidget()
            layout = QHBoxLayout()
            book_widget.setLayout(layout)

            # 이미지 처리
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

            # 텍스트 정보 출력
            text = (
                f"{i+1}. 제목: {book['title']}\n"
                f"   저자: {book['author']}\n"
                f"   출판사: {book['publisher']}\n"
                f"   설명: {book['description'][:200]}..."
            )
            text_label = QLabel(text)
            text_label.setWordWrap(True)
            text_label.setFixedHeight(280)  # ← 이미지 높이와 맞춤
            text_label.setStyleSheet("font-size: 18px;")
            text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 수평 왼쪽 + 수직 중앙
            text_label.setTextInteractionFlags(Qt.TextSelectableByMouse) # 텍스트 선택 및 복사 가능하게 설정
            layout.addWidget(text_label)
            layout.setAlignment(text_label, Qt.AlignVCenter)

            parent_layout.addWidget(book_widget)
    else:
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(None, "검색 결과 없음", "⚠️ 검색 결과가 없습니다.")
