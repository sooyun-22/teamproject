import sys
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QHBoxLayout, QLineEdit, QScrollArea, QMessageBox, QStackedWidget, QTextEdit
)
from PyQt5.QtCore import Qt
from naver_books import recommend_books
from summarize import summarize_text

class PlainTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def insertFromMimeData(self, source):
        # 복사된 데이터 중 텍스트만 가져와서 plain text로 삽입
        self.insertPlainText(source.text())

class MainMenu(QWidget):
    def __init__(self, switch_screen_func):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(QLabel("<h1>📘 기능을 선택하세요</h1>"))

        book_btn = QPushButton("📚 도서 추천")
        book_btn.setFixedHeight(50)
        book_btn.clicked.connect(lambda: switch_screen_func("book"))

        summary_btn = QPushButton("📝 텍스트 요약")
        summary_btn.setFixedHeight(50)
        summary_btn.clicked.connect(lambda: switch_screen_func("summary"))

        exit_btn = QPushButton("❌ 종료")
        exit_btn.setFixedHeight(50)
        exit_btn.setStyleSheet("color: red;")
        exit_btn.clicked.connect(self.confirm_exit)

        layout.addWidget(book_btn)
        layout.addWidget(summary_btn)
        layout.addWidget(exit_btn)
        self.setLayout(layout)

    def confirm_exit(self):
        reply = QMessageBox.question(self, "종료 확인", "프로그램을 종료하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()


class BookRecommendScreen(QWidget):
    def __init__(self, back_func):
        super().__init__()
        self.image_refs = []

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("키워드를 입력하세요. 책을 검색할 경우 \"책 제목\"으로 입력하세요")
        self.input_field.setFixedHeight(60)  # ← 추가: 입력 칸 높이 증가

        recommend_btn = QPushButton("추천")
        recommend_btn.clicked.connect(self.on_recommend)
        recommend_btn.setFixedHeight(60)

        back_btn = QPushButton("🔙 처음으로")
        back_btn.clicked.connect(back_func)
        back_btn.setFixedHeight(60)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(recommend_btn)
        input_layout.addWidget(back_btn)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.scroll_content)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def on_recommend(self):
        keyword = self.input_field.text().strip()
        if not keyword:
            QMessageBox.warning(self, "입력 오류", "키워드를 입력해주세요.")
            return

        # 기존 출력 삭제
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        recommend_books(keyword, self.scroll_layout, self.image_refs)

class SummarizeScreen(QWidget):
    def __init__(self, back_func):
        super().__init__()

        self.input_field = PlainTextEdit()  # 수정된 텍스트 에디트 사용
        self.input_field.setPlaceholderText("요약할 텍스트를 입력하세요")
        self.input_field.setFixedHeight(300)

        # 요약 버튼
        summarize_btn = QPushButton("📝 요약")
        summarize_btn.clicked.connect(self.on_summarize)
        summarize_btn.setFixedHeight(60)

        # 뒤로 버튼
        back_btn = QPushButton("🔙 처음으로")
        back_btn.clicked.connect(back_func)
        back_btn.setFixedHeight(60)

        # 버튼 배치
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(summarize_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()

        # 출력 영역
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.scroll_content)

        # 전체 배치
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_field)       # 상단: 입력창
        main_layout.addLayout(button_layout)          # 중간: 버튼
        main_layout.addWidget(scroll_area)            # 하단: 출력창

        self.setLayout(main_layout)

    def on_summarize(self):
        text = self.input_field.toPlainText().strip()  # ✅ QTextEdit에서는 toPlainText()
        if not text:
            QMessageBox.warning(self, "입력 오류", "텍스트를 입력해주세요.")
            return

        # 기존 출력 제거
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        summary = summarize_text(text, length='medium')
        summary_label = QLabel(summary)
        summary_label.setWordWrap(True)
        self.scroll_layout.addWidget(summary_label)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📚 도서 추천 및 텍스트 요약 프로그램")
        self.showFullScreen()

        self.stack = QStackedWidget()

        # 화면 구성
        self.menu_screen = MainMenu(self.switch_screen)
        self.book_screen = BookRecommendScreen(lambda: self.switch_screen("menu"))
        self.summary_screen = SummarizeScreen(lambda: self.switch_screen("menu"))

        # 스택에 추가
        self.stack.addWidget(self.menu_screen)     # index 0
        self.stack.addWidget(self.book_screen)     # index 1
        self.stack.addWidget(self.summary_screen)  # index 2

        self.setCentralWidget(self.stack)
        self.stack.setCurrentWidget(self.menu_screen)

    def clear_book_screen(self):
        # 입력 필드 초기화
        self.book_screen.input_field.clear()
        # 출력 초기화
        for i in reversed(range(self.book_screen.scroll_layout.count())):
            widget = self.book_screen.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.book_screen.image_refs.clear()

    def clear_summary_screen(self):
        # 입력 필드 초기화
        self.summary_screen.input_field.clear()
        # 출력 초기화
        for i in reversed(range(self.summary_screen.scroll_layout.count())):
            widget = self.summary_screen.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    def switch_screen(self, screen_name):
        if screen_name == "menu":
            # 처음으로 돌아갈 때 모든 화면 초기화
            self.clear_book_screen()
            self.clear_summary_screen()
            self.stack.setCurrentWidget(self.menu_screen)
        elif screen_name == "book":
            self.stack.setCurrentWidget(self.book_screen)
        elif screen_name == "summary":
            self.stack.setCurrentWidget(self.summary_screen)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 18))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
