import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QHBoxLayout, QLineEdit, QScrollArea, QMessageBox, QStackedWidget, QTextEdit, QFrame
)
from PyQt5.QtCore import Qt
from naver_books import recommend_books
from summarize import summarize_text

class PlainTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())

class MainMenu(QWidget):
    def __init__(self, switch_screen_func):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #FDF9F3;
            }
            QLabel#TitleLabel {
                font-size: 56px;
                font-weight: bold;
                color: #333;
            }
            QLabel#SubLabel {
                font-size: 26px;
                color: #777;
                margin-bottom: 50px;
            }
            QPushButton#CardButton {
                background-color: #FCDDA1;
                border: none;
                border-radius: 30px;
                padding: 40px;
                font-size: 28px;
                font-weight: bold;
                min-width: 280px;
                min-height: 160px;
            }
            QPushButton#CardButton2 {
                background-color: #F7B6AC;
                border: none;
                border-radius: 30px;
                padding: 40px;
                font-size: 28px;
                font-weight: bold;
                min-width: 280px;
                min-height: 160px;
            }
            QLabel#CardDescription {
                font-size: 20px;
                color: #444;
                margin-top: 10px;
            }
            QPushButton#ExitButton {
                background: none;
                border: none;
                color: #555;
                font-size: 20px;
                margin-top: 60px;
            }
            QPushButton#ExitButton:hover {
                color: #000;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        title = QLabel("책 줄거리 요약")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("무엇을 도와드릴까요?")
        subtitle.setObjectName("SubLabel")
        subtitle.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        card_layout = QHBoxLayout()
        card_layout.setSpacing(60)
        card_layout.setContentsMargins(100, 40, 100, 40)

        # 책 추천 카드
        book_card = QVBoxLayout()
        book_btn = QPushButton("📚 책 추천")
        book_btn.setObjectName("CardButton")
        book_btn.clicked.connect(lambda: switch_screen_func("book"))
        desc1 = QLabel("추천할 만한 책을 찾아드립니다.")
        desc1.setObjectName("CardDescription")
        desc1.setWordWrap(True)
        desc1.setAlignment(Qt.AlignCenter)
        book_card.addWidget(book_btn, alignment=Qt.AlignCenter)
        book_card.addWidget(desc1)

        # 텍스트 요약 카드
        summary_card = QVBoxLayout()
        summary_btn = QPushButton("📝 텍스트 요약")
        summary_btn.setObjectName("CardButton2")
        summary_btn.clicked.connect(lambda: switch_screen_func("summary"))
        desc2 = QLabel("입력된 텍스트를 요약합니다.")
        desc2.setObjectName("CardDescription")
        desc2.setWordWrap(True)
        desc2.setAlignment(Qt.AlignCenter)
        summary_card.addWidget(summary_btn, alignment=Qt.AlignCenter)
        summary_card.addWidget(desc2)

        card_layout.addLayout(book_card)
        card_layout.addLayout(summary_card)
        layout.addLayout(card_layout)

        # 종료 버튼
        exit_btn = QPushButton("종료")
        exit_btn.setObjectName("ExitButton")
        exit_btn.clicked.connect(self.confirm_exit)
        layout.addWidget(exit_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def confirm_exit(self):
        reply = QMessageBox.question(self, "종료 확인", "프로그램을 종료하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()




class BookRecommendScreen(QWidget):
     def __init__(self, back_func):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #F9F7F2;
            }
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #CCC;
                border-radius: 10px;
                padding: 15px;
                font-size: 18px;
            }
            QPushButton {
                font-size: 18px;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton#RecommendBtn {
                background-color: #FCDDA1;
                font-weight: bold;
            }
            QPushButton#BackBtn {
                background-color: #CCCCCC;
            }
            QLabel#BookLabel {
                background-color: #FFFFFF;
                border: 1px solid #DDD;
                border-radius: 10px;
                padding: 15px;
                font-size: 18px;
                color: #333;
            }
        """)

        self.image_refs = []

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("키워드를 입력하세요")
        self.input_field.setFixedHeight(50)

        recommend_btn = QPushButton("추천")
        recommend_btn.setObjectName("RecommendBtn")
        recommend_btn.clicked.connect(self.on_recommend)
        recommend_btn.setFixedHeight(50)

        back_btn = QPushButton("🔙 처음으로")
        back_btn.setObjectName("BackBtn")
        back_btn.clicked.connect(back_func)
        back_btn.setFixedHeight(50)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(recommend_btn)
        input_layout.addWidget(back_btn)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(15)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.scroll_content)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(80, 40, 80, 40)
        main_layout.setSpacing(20)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

     def on_recommend(self):
        keyword = self.input_field.text().strip()
        if not keyword:
            QMessageBox.warning(self, "입력 오류", "키워드를 입력해주세요.")
            return

        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        recommend_books(keyword, self.scroll_layout, self.image_refs)

class SummarizeScreen(QWidget):
    def __init__(self, back_func):
        super().__init__()

        self.setStyleSheet("""
    QWidget {
        background-color: #F9F7F2;
    }
    QTextEdit {
        background-color: #F5F5EB;;
        border: 1px solid #CCC;
        border-radius: 10px;
        padding: 20px;
        font-size: 20px;
    }
    QPushButton {
        font-size: 20px;
        padding: 12px 24px;
        border-radius: 10px;
    }
    QPushButton#KeywordBtn {
        background-color: #EFE7DA;
    }
    QPushButton#MediumBtn {
        background-color: #EFE7DA;
    }
    QPushButton#LongBtn {
        background-color: #EFE7DA;
    }
    QPushButton#SummarizeBtn {
        background-color: #C1B6A3;
        font-weight: bold;
    }
    QPushButton#BackBtn {
        background-color: #C1B6A3;
    }
    QLabel#ResultLabel {
        background-color: #F5F5EB;
        border: 1px solid #DDD;
        border-radius: 10px;
        padding: 16px;
        font-size: 18px;
        color: #333;
    }
""")


        self.selected_length = None

        self.input_field = PlainTextEdit()
        self.input_field.setPlaceholderText("요약할 텍스트를 입력하세요")
        self.input_field.setFixedHeight(300)

        self.keyword_btn = QPushButton("키워드 요약")
        self.medium_btn = QPushButton("중간 요약")
        self.long_btn = QPushButton("긴 요약")

        self.keyword_btn.setObjectName("KeywordBtn")
        self.medium_btn.setObjectName("MediumBtn")
        self.long_btn.setObjectName("LongBtn")

        for btn in [self.keyword_btn, self.medium_btn, self.long_btn]:
            btn.setCheckable(True)
            btn.setFixedHeight(50)

        self.keyword_btn.clicked.connect(lambda: self.set_length("keyword"))
        self.medium_btn.clicked.connect(lambda: self.set_length("medium"))
        self.long_btn.clicked.connect(lambda: self.set_length("long"))

        length_button_layout = QHBoxLayout()
        length_button_layout.setSpacing(30)
        length_button_layout.addStretch()
        length_button_layout.addWidget(self.keyword_btn)
        length_button_layout.addWidget(self.medium_btn)
        length_button_layout.addWidget(self.long_btn)
        length_button_layout.addStretch()

        self.summarize_btn = QPushButton("요약 실행")
        self.summarize_btn.setObjectName("SummarizeBtn")
        self.summarize_btn.clicked.connect(self.on_summarize)

        self.back_btn = QPushButton("🔙 처음으로")
        self.back_btn.setObjectName("BackBtn")
        self.back_btn.clicked.connect(back_func)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()
        button_layout.addWidget(self.summarize_btn)
        button_layout.addWidget(self.back_btn)
        button_layout.addStretch()

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(20)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.scroll_content)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(80, 40, 80, 40)
        main_layout.setSpacing(30)
        main_layout.addWidget(self.input_field)
        main_layout.addLayout(length_button_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def set_length(self, length):
        self.selected_length = length
        self.keyword_btn.setChecked(length == "keyword")
        self.medium_btn.setChecked(length == "medium")
        self.long_btn.setChecked(length == "long")
        self.update_button_styles()

    def update_button_styles(self):
        for btn, key in zip(
            [self.keyword_btn, self.medium_btn, self.long_btn],
            ["keyword", "medium", "long"]
        ):
            if self.selected_length == key:
                btn.setStyleSheet(btn.styleSheet() + "border: 3px solid #555;")
            else:
                btn.setStyleSheet(btn.styleSheet() + "border: none;")

    def on_summarize(self):
        text = self.input_field.toPlainText().strip()
        if self.selected_length is None:
            QMessageBox.warning(self, "선택 오류", "요약 길이를 선택해주세요.")
            return

        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        summary = summarize_text(text, length=self.selected_length)
        summary_label = QLabel(summary)
        summary_label.setObjectName("ResultLabel")
        summary_label.setWordWrap(True)
        self.scroll_layout.addWidget(summary_label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📚 도서 추천 및 텍스트 요약 프로그램")
        self.setGeometry(100, 100, 1600, 1000)

        self.stack = QStackedWidget()

        self.menu_screen = MainMenu(self.switch_screen)
        self.book_screen = BookRecommendScreen(lambda: self.switch_screen("menu"))
        self.summary_screen = SummarizeScreen(lambda: self.switch_screen("menu"))

        self.stack.addWidget(self.menu_screen)
        self.stack.addWidget(self.book_screen)
        self.stack.addWidget(self.summary_screen)

        self.setCentralWidget(self.stack)
        self.stack.setCurrentWidget(self.menu_screen)

    def clear_book_screen(self):
        self.book_screen.input_field.clear()
        for i in reversed(range(self.book_screen.scroll_layout.count())):
            widget = self.book_screen.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.book_screen.image_refs.clear()

    def clear_summary_screen(self):
        self.summary_screen.input_field.clear()
        for i in reversed(range(self.summary_screen.scroll_layout.count())):
            widget = self.summary_screen.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    def switch_screen(self, screen_name):
        if screen_name == "menu":
            self.clear_book_screen()
            self.clear_summary_screen()
            self.stack.setCurrentWidget(self.menu_screen)
        elif screen_name == "book":
            self.stack.setCurrentWidget(self.book_screen)
        elif screen_name == "summary":
            self.stack.setCurrentWidget(self.summary_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 22))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
