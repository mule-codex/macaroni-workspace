import os
import sys
import json
import time
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QSplitter,
    QStatusBar,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QLabel,
    QFrame,
    QSizePolicy,
)

from PyQt6.QtGui import (
    QAction,
    QFont,
)

from PyQt6.QtCore import (
    Qt,
    QUrl,
    QSize,
    QTimer,
)

from PyQt6.QtWebEngineWidgets import (
    QWebEngineView
)

from PyQt6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEnginePage,
    QWebEngineSettings,
)


class MacaroniIDE(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Macaroni Workspace"
        )

        self.current_file = None

        self.session_file = "sessions.json"

        self.health_file = "health.json"

        self.dark_mode = True

        self.file_history = []

        self.app_start_time = time.time()

        self.health_data = {
            "app_launches": 0,
            "browser_url": "",
            "editor_characters": 0,
            "files_opened": 0,
            "files_saved": 0,
            "theme": "dark",
            "uptime_seconds": 0,
            "last_updated": "",
        }

        self.setWindowState(
            Qt.WindowState.WindowFullScreen
        )

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        self.sidebar_search = QLineEdit()

        self.sidebar_search.setPlaceholderText(
            "Search workspace files"
        )

        self.sidebar_search.textChanged.connect(
            self.filter_history_live
        )

        self.history_list = QListWidget()

        self.history_list.itemClicked.connect(
            self.open_history_item
        )

        sidebar_title = QLabel(
            "Workspace"
        )

        sidebar_title.setObjectName(
            "SidebarTitle"
        )

        sidebar_subtitle = QLabel(
            "Recent documents"
        )

        sidebar_subtitle.setObjectName(
            "SidebarSub"
        )

        sidebar_layout = QVBoxLayout()

        sidebar_layout.setContentsMargins(
            24,
            24,
            24,
            24
        )

        sidebar_layout.setSpacing(
            16
        )

        sidebar_layout.addWidget(
            sidebar_title
        )

        sidebar_layout.addWidget(
            sidebar_subtitle
        )

        sidebar_layout.addWidget(
            self.sidebar_search
        )

        sidebar_layout.addWidget(
            self.history_list
        )

        sidebar_widget = QFrame()

        sidebar_widget.setObjectName(
            "SidebarPanel"
        )

        sidebar_widget.setLayout(
            sidebar_layout
        )

        sidebar_widget.setMinimumWidth(
            300
        )

        sidebar_widget.setMaximumWidth(
            360
        )

        self.editor = QTextEdit()

        self.editor.setFont(
            QFont(
                "Segoe UI",
                13
            )
        )

        self.editor.setPlaceholderText(
            "Write notes, plans, prompts, or code..."
        )

        self.editor.textChanged.connect(
            self.auto_save_session
        )

        editor_container = QFrame()

        editor_container.setObjectName(
            "MainPanel"
        )

        editor_layout = QVBoxLayout()

        editor_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        editor_layout.setSpacing(
            12
        )

        editor_label = QLabel(
            "Editor"
        )

        editor_label.setObjectName(
            "SectionLabel"
        )

        editor_layout.addWidget(
            editor_label
        )

        editor_layout.addWidget(
            self.editor
        )

        editor_container.setLayout(
            editor_layout
        )

        profile_path = os.path.join(
            os.getcwd(),
            "browser_profile"
        )

        os.makedirs(
            profile_path,
            exist_ok=True
        )

        self.web_profile = QWebEngineProfile(
            "MacaroniProfile",
            self
        )

        self.web_profile.setPersistentStoragePath(
            profile_path
        )

        self.web_profile.setCachePath(
            os.path.join(
                profile_path,
                "cache"
            )
        )

        self.web_profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
        )

        self.web_profile.settings().setAttribute(
            QWebEngineSettings.WebAttribute.LocalStorageEnabled,
            True
        )

        self.web_profile.settings().setAttribute(
            QWebEngineSettings.WebAttribute.JavascriptEnabled,
            True
        )

        self.web_profile.settings().setAttribute(
            QWebEngineSettings.WebAttribute.PluginsEnabled,
            True
        )

        self.web_profile.settings().setAttribute(
            QWebEngineSettings.WebAttribute.FullScreenSupportEnabled,
            True
        )

        self.web_profile.settings().setAttribute(
            QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled,
            True
        )

        self.web_page = QWebEnginePage(
            self.web_profile,
            self
        )

        self.browser = QWebEngineView()

        self.browser.setPage(
            self.web_page
        )

        self.browser.setUrl(
            QUrl(
                "https://chat.com"
            )
        )

        self.browser.urlChanged.connect(
            self.auto_save_session
        )

        self.browser.loadStarted.connect(
            self.browser_load_started
        )

        self.browser.loadProgress.connect(
            self.browser_load_progress
        )

        self.browser.loadFinished.connect(
            self.browser_load_finished
        )

        browser_container = QFrame()

        browser_container.setObjectName(
            "MainPanel"
        )

        browser_layout = QVBoxLayout()

        browser_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        browser_layout.setSpacing(
            12
        )

        browser_label = QLabel(
            "Chat"
        )

        browser_label.setObjectName(
            "SectionLabel"
        )

        self.loading_container = QWidget()

        self.loading_container.setFixedHeight(
            36
        )

        loading_layout = QVBoxLayout()

        loading_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        loading_layout.setSpacing(
            4
        )

        self.loading_label = QLabel(
            "Ready"
        )

        self.progress_bar = QProgressBar()

        self.progress_bar.setFixedHeight(
            4
        )

        self.progress_bar.setTextVisible(
            False
        )

        self.progress_bar.setValue(
            0
        )

        loading_layout.addWidget(
            self.loading_label
        )

        loading_layout.addWidget(
            self.progress_bar
        )

        self.loading_container.setLayout(
            loading_layout
        )

        browser_layout.addWidget(
            browser_label
        )

        browser_layout.addWidget(
            self.loading_container
        )

        browser_layout.addWidget(
            self.browser
        )

        browser_container.setLayout(
            browser_layout
        )

        self.main_splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        self.main_splitter.setHandleWidth(
            1
        )

        self.main_splitter.addWidget(
            sidebar_widget
        )

        self.main_splitter.addWidget(
            editor_container
        )

        self.main_splitter.addWidget(
            browser_container
        )

        self.main_splitter.setSizes([
            300,
            760,
            920
        ])

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            12,
            12,
            12,
            12
        )

        main_layout.setSpacing(
            12
        )

        main_layout.addWidget(
            self.main_splitter
        )

        central_widget.setLayout(
            main_layout
        )

        self.create_toolbar()

        self.create_statusbar()

        self.restore_session()

        self.apply_theme()

        self.initialize_health()

        self.health_timer = QTimer()

        self.health_timer.timeout.connect(
            self.export_health_metrics
        )

        self.health_timer.start(
            5000
        )

    def create_toolbar(self):

        navbar = QToolBar()

        navbar.setMovable(False)

        navbar.setIconSize(
            QSize(18, 18)
        )

        self.addToolBar(
            navbar
        )

        actions = [

            ("New File", self.new_file),

            ("Open File", self.open_file_dialog),

            ("Save File", self.save_file),
        ]

        for text, callback in actions:

            action = QAction(
                text,
                self
            )

            action.triggered.connect(
                callback
            )

            navbar.addAction(
                action
            )

        spacer = QWidget()

        spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        navbar.addWidget(
            spacer
        )

        self.workspace_label = QLabel(
            "Macaroni Workspace"
        )

        self.workspace_label.setObjectName(
            "TopbarTitle"
        )

        navbar.addWidget(
            self.workspace_label
        )

    def create_statusbar(self):

        self.status = QStatusBar()

        self.setStatusBar(
            self.status
        )

    def add_to_history(self, path):

        if not path:
            return

        if path in self.file_history:

            self.file_history.remove(
                path
            )

        self.file_history.insert(
            0,
            path
        )

        self.refresh_history()

        self.auto_save_session()

    def refresh_history(self):

        self.history_list.clear()

        for path in self.file_history:

            item = QListWidgetItem(
                os.path.basename(path)
            )

            item.setToolTip(
                path
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                path
            )

            self.history_list.addItem(
                item
            )

    def filter_history_live(self):

        query = self.sidebar_search.text().strip().lower()

        self.history_list.clear()

        if not query:

            self.refresh_history()

            return

        for path in self.file_history:

            filename = os.path.basename(
                path
            ).lower()

            full_path = path.lower()

            if (
                query in filename
                or query in full_path
            ):

                item = QListWidgetItem(
                    os.path.basename(path)
                )

                item.setToolTip(
                    path
                )

                item.setData(
                    Qt.ItemDataRole.UserRole,
                    path
                )

                self.history_list.addItem(
                    item
                )

    def open_history_item(self, item):

        path = item.data(
            Qt.ItemDataRole.UserRole
        )

        if os.path.exists(path):

            self.load_file(
                path
            )

    def browser_load_started(self):

        self.loading_label.setText(
            "Connecting to chat..."
        )

        self.progress_bar.setValue(
            0
        )

    def browser_load_progress(self, progress):

        self.progress_bar.setValue(
            progress
        )

        self.loading_label.setText(
            f"Loading chat... {progress}%"
        )

    def browser_load_finished(self):

        self.loading_label.setText(
            "Connected"
        )

        self.progress_bar.setValue(
            100
        )

    def apply_theme(self):

        self.setStyleSheet("""

            QMainWindow {

                background: #0b0b0c;
            }

            QWidget {

                background: transparent;
                color: #f5f5f5;
                font-family: "Segoe UI";
                font-size: 13px;
            }

            QToolBar {

                background: #161616;

                border: 1px solid #2f2f2f;

                spacing: 10px;

                padding: 14px;

                margin: 0px 0px 10px 0px;

                min-height: 54px;
            }

            QToolButton {

                background: #242424;

                border: 1px solid #3a3a3a;

                border-radius: 6px;

                padding: 10px 18px;

                color: #ffffff;

                font-weight: 600;

                min-width: 110px;
            }

            QToolButton:hover {

                background: #323232;
            }

            QFrame#SidebarPanel {

                background: #161616;

                border: 1px solid #2d2d2d;

                border-radius: 10px;
            }

            QFrame#MainPanel {

                background: #161616;

                border: 1px solid #2d2d2d;

                border-radius: 10px;
            }

            QTextEdit {

                background: #101010;

                border: 1px solid #2d2d2d;

                border-radius: 8px;

                padding: 22px;

                color: #ffffff;

                selection-background-color: #6b7280;
            }

            QListWidget {

                background: transparent;

                border: none;

                padding: 4px;
            }

            QListWidget::item {

                background: transparent;

                margin-top: 4px;

                margin-bottom: 4px;

                padding: 14px;

                border-radius: 6px;
            }

            QListWidget::item:hover {

                background: #242424;
            }

            QListWidget::item:selected {

                background: #303030;
            }

            QLineEdit {

                background: #101010;

                border: 1px solid #303030;

                border-radius: 8px;

                padding: 12px 14px;

                color: white;

                min-height: 20px;
            }

            QLineEdit:focus {

                border: 1px solid #bdbdbd;
            }

            QLabel#SidebarTitle {

                font-size: 22px;

                font-weight: 700;

                color: #ffffff;
            }

            QLabel#SidebarSub {

                color: #a1a1aa;

                margin-bottom: 6px;
            }

            QLabel#SectionLabel {

                font-size: 15px;

                font-weight: 700;

                color: #f3f4f6;

                padding-bottom: 2px;
            }

            QLabel#TopbarTitle {

                color: #d4d4d4;

                font-size: 13px;

                font-weight: 700;

                padding-right: 10px;
            }

            QProgressBar {

                background: #262626;

                border-radius: 2px;
            }

            QProgressBar::chunk {

                background: #d1d5db;

                border-radius: 2px;
            }

            QWebEngineView {

                background: #0f0f10;

                border: 1px solid #2d2d2d;

                border-radius: 8px;
            }

            QSplitter::handle {

                background: #202020;

                width: 1px;
            }

            QStatusBar {

                background: #141414;

                border-top: 1px solid #2a2a2a;

                color: #cfcfcf;

                padding-left: 10px;
            }

        """)

    def auto_save_session(self):

        session_data = {

            "editor_content":
                self.editor.toPlainText(),

            "current_file":
                self.current_file,

            "browser_url":
                self.browser.url().toString(),

            "main_splitter_sizes":
                self.main_splitter.sizes(),

            "file_history":
                self.file_history,
        }

        try:

            with open(
                self.session_file,
                "w",
                encoding="utf-8"
            ) as session:

                json.dump(
                    session_data,
                    session,
                    indent=4
                )

        except Exception as e:

            print(
                "Session save error:",
                e
            )

    def restore_session(self):

        if not os.path.exists(
            self.session_file
        ):
            return

        try:

            with open(
                self.session_file,
                "r",
                encoding="utf-8"
            ) as session:

                data = json.load(
                    session
                )

            self.editor.setPlainText(
                data.get(
                    "editor_content",
                    ""
                )
            )

            self.current_file = data.get(
                "current_file"
            )

            self.browser.setUrl(
                QUrl(
                    "https://chat.com"
                )
            )

            self.file_history = data.get(
                "file_history",
                []
            )

            self.refresh_history()

        except Exception as e:

            print(
                "Session restore error:",
                e
            )

    def new_file(self):

        self.editor.clear()

        self.current_file = None

    def open_file_dialog(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "All Files (*)"
        )

        if path:

            self.load_file(
                path
            )

    def load_file(self, path):

        try:

            with open(
                path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                content = file.read()

            self.editor.setPlainText(
                content
            )

            self.current_file = path

            self.add_to_history(
                path
            )

            filename = os.path.basename(
                path
            )

            self.setWindowTitle(
                f"{filename} - Macaroni Workspace"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

    def save_file(self):

        if self.current_file:

            try:

                with open(
                    self.current_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        self.editor.toPlainText()
                    )

                self.status.showMessage(
                    "File saved successfully",
                    3000
                )

            except Exception as e:

                QMessageBox.critical(
                    self,
                    "Error",
                    str(e)
                )

        else:

            self.save_file_as()

    def save_file_as(self):

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File As",
            "",
            "Text Files (*.txt);;Markdown (*.md);;All Files (*)"
        )

        if path:

            try:

                with open(
                    path,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        self.editor.toPlainText()
                    )

                self.current_file = path

                self.add_to_history(
                    path
                )

                self.status.showMessage(
                    "File saved successfully",
                    3000
                )

            except Exception as e:

                QMessageBox.critical(
                    self,
                    "Error",
                    str(e)
                )

    def initialize_health(self):

        self.health_data["app_launches"] += 1

        self.export_health_metrics()

    def export_health_metrics(self):

        self.health_data["browser_url"] = (
            self.browser.url().toString()
        )

        self.health_data["editor_characters"] = (
            len(
                self.editor.toPlainText()
            )
        )

        self.health_data["uptime_seconds"] = int(
            time.time() - self.app_start_time
        )

        self.health_data["last_updated"] = (
            datetime.now().isoformat()
        )

        try:

            with open(
                self.health_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.health_data,
                    file,
                    indent=4
                )

        except Exception as e:

            print(
                "Health export error:",
                e
            )

    def closeEvent(self, event):

        self.auto_save_session()

        self.export_health_metrics()

        event.accept()


if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    app.setStyle(
        "Fusion"
    )

    window = MacaroniIDE()

    window.showFullScreen()

    sys.exit(
        app.exec()
    )