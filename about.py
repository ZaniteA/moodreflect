from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

import configs
from components import AboutPageText



class AboutPage(QWidget):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(self.parent)
        self.init_ui()


    def init_ui(self):
        self.setStyleSheet('background-color: none;')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addStretch()

        # Logo
        self.logo = QLabel()
        self.logo_pixmap = QPixmap('assets/logo/moodreflect_320px.png')
        self.logo.setPixmap(self.logo_pixmap)
        self.logo.setFixedSize(self.logo_pixmap.width(), self.logo_pixmap.height())
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addSpacing(32)

        # App name
        self.app_name = AboutPageText(f'<b>{configs.APP_NAME}</b>')
        self.app_name.setFont(self.parent.heading_font(configs.H1_FONT_SIZE))
        self.layout.addWidget(self.app_name)

        # App version
        self.app_version = AboutPageText(configs.APP_VERSION)
        self.app_version.setFont(self.parent.body_font(configs.H3_FONT_SIZE))
        self.layout.addWidget(self.app_version)

        # App details
        self.app_details = AboutPageText(configs.APP_DETAILS)
        self.app_details.setFont(self.parent.body_font(configs.BODY_FONT_SIZE))
        self.layout.addWidget(self.app_details)

        self.layout.addSpacing(32)

        # App author organization
        self.app_author_org = AboutPageText(f'<b>{configs.APP_AUTHOR_ORG}</b>')
        self.app_author_org.setFont(self.parent.body_font(configs.H3_FONT_SIZE))
        self.layout.addWidget(self.app_author_org)

        self.app_authors = []
        for line in configs.APP_AUTHORS:
            self.app_authors.append(AboutPageText(line))
            self.app_authors[-1].setFont(self.parent.body_font(configs.BODY_FONT_SIZE))
            self.layout.addWidget(self.app_authors[-1])

        self.layout.addStretch()
