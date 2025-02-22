import sys
import os
import webbrowser
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
                            QTableWidgetItem, QProgressBar, QLabel, QFileDialog,
                            QHeaderView, QStyle, QStyleFactory, QComboBox, QTextEdit, QDialog, QPlainTextEdit, QCheckBox, QButtonGroup)
from PySide6.QtCore import Qt, Signal, QObject, QThread
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap
import requests
from io import BytesIO
from PIL import Image
from datetime import datetime
import json
from pathlib import Path
from packaging import version
import subprocess
import re
import yt_dlp

from .ytsage_downloader import DownloadThread, SignalManager  # Changed to relative import
from .ytsage_utils import check_ffmpeg, get_yt_dlp_path, load_saved_path, save_path  # Changed to relative import


class LogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('yt-dlp Log')
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout(self)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: Consolas, monospace;
                font-size: 12px;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
            }
        """)

        layout.addWidget(self.log_text)

    def append_log(self, message):
        self.log_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

class CustomCommandDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle('Custom yt-dlp Command')
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout(self)

        # Help text
        help_text = QLabel(
            "Enter custom yt-dlp commands below. The URL will be automatically appended.\n"
            "Example: --extract-audio --audio-format mp3 --audio-quality 0\n"
            "Note: Download path and output template will be preserved."
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: #999999; padding: 10px;")
        layout.addWidget(help_text)

        # Command input
        self.command_input = QPlainTextEdit()
        self.command_input.setPlaceholderText("Enter yt-dlp arguments...")
        self.command_input.setStyleSheet("""
            QPlainTextEdit {
                background-color: #363636;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px;
                font-family: Consolas, monospace;
            }
        """)
        layout.addWidget(self.command_input)

        # Add SponsorBlock checkbox
        self.sponsorblock_checkbox = QCheckBox("Remove Sponsor Segments")
        self.sponsorblock_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 20px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;  /* Make indicator round */
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #2b2b2b;
                border-radius: 9px;  /* Make indicator round */
            }
            QCheckBox::indicator:checked {
                border: 2px solid #ff0000;
                background: #ff0000;
                border-radius: 9px;  /* Make indicator round */
            }
        """)
        layout.insertWidget(layout.indexOf(self.command_input), self.sponsorblock_checkbox)

        # Buttons
        button_layout = QHBoxLayout()

        self.run_btn = QPushButton("Run Command")
        self.run_btn.clicked.connect(self.run_custom_command)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)

        button_layout.addWidget(self.run_btn)
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 8px;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.log_output)

        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)

    def run_custom_command(self):
        url = self.parent.url_input.text().strip()
        if not url:
            self.log_output.append("Error: No URL provided")
            return

        command = self.command_input.toPlainText().strip()
        path = self.parent.path_input.text().strip()

        self.log_output.clear()
        self.log_output.append(f"Running command with URL: {url}")
        self.run_btn.setEnabled(False)

        # Start command in thread
        import threading
        threading.Thread(target=self._run_command_thread,
                        args=(command, url, path),
                        daemon=True).start()

    def _run_command_thread(self, command, url, path):
        try:
            class CommandLogger:
                def debug(self, msg):
                    self.dialog.log_output.append(msg)
                def warning(self, msg):
                    self.dialog.log_output.append(f"Warning: {msg}")
                def error(self, msg):
                    self.dialog.log_output.append(f"Error: {msg}")
                def __init__(self, dialog):
                    self.dialog = dialog

            # Split command into arguments
            args = command.split()

            # Base options
            ydl_opts = {
                'logger': CommandLogger(self),
                'paths': {'home': path},
                'debug_printout': True,
                'postprocessors': []
            }

            # Add SponsorBlock options if enabled
            if self.sponsorblock_checkbox.isChecked():
                ydl_opts['postprocessors'].extend([{
                    'key': 'SponsorBlock',
                    'categories': ['sponsor', 'selfpromo', 'interaction'],
                    'api': 'https://sponsor.ajay.app'
                }, {
                    'key': 'ModifyChapters',
                    'remove_sponsor_segments': ['sponsor', 'selfpromo', 'interaction'],
                    'sponsorblock_chapter_title': '[SponsorBlock]: %(category_names)l',
                    'force_keyframes': True
                }])

            # Add custom arguments
            for i in range(0, len(args), 2):
                if i + 1 < len(args):
                    key = args[i].lstrip('-').replace('-', '_')
                    value = args[i + 1]
                    try:
                        # Try to convert to appropriate type
                        if value.lower() in ('true', 'false'):
                            value = value.lower() == 'true'
                        elif value.isdigit():
                            value = int(value)
                        ydl_opts[key] = value
                    except:
                        ydl_opts[key] = value

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.log_output.append("Command completed successfully")

        except Exception as e:
            self.log_output.append(f"Error: {str(e)}")
        finally:
            self.run_btn.setEnabled(True)

class FFmpegCheckDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('FFmpeg Required')
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # Message
        message_label = QLabel(
            "FFmpeg is not installed. Please install it.\n"
            "To install FFmpeg, click the button below."
        )
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        # Install button
        install_btn = QPushButton("Install FFmpeg")
        install_btn.clicked.connect(lambda: webbrowser.open('https://github.com/oop7/ffmpeg-install-guide'))
        layout.addWidget(install_btn)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        # Style the dialog
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
                padding: 10px;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)


class YTDLPUpdateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Update yt-dlp')
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # Version info and message
        self.version_label = QLabel()
        self.version_label.setWordWrap(True)
        layout.addWidget(self.version_label)

        self.message_label = QLabel(
            "Would you like to update yt-dlp to the latest version?\n"
            "This will download and install the latest yt-dlp executable."
        )
        self.message_label.setWordWrap(True)
        layout.addWidget(self.message_label)

        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        # Buttons
        button_layout = QHBoxLayout()

        self.update_btn = QPushButton("Update yt-dlp")
        self.update_btn.clicked.connect(self.start_update)
        self.update_btn.setEnabled(False)  # Disabled until version check

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)

        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.close_btn)
        layout.addLayout(button_layout)

        # Style the dialog
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
                padding: 10px;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
            QPushButton:disabled {
                background-color: #666666;
            }
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #ff0000;
            }
        """)

        # Check versions when dialog opens
        self.check_versions()

    def check_versions(self):
        import threading
        threading.Thread(target=self._check_versions_thread, daemon=True).start()

    def _check_versions_thread(self):
        try:
            # Get current version with proper path
            yt_dlp_path = get_yt_dlp_path()
            if os.path.exists(yt_dlp_path):
                try:
                    # Use the full path to yt-dlp executable
                    result = subprocess.run([yt_dlp_path, '--version'],
                                         capture_output=True,
                                         text=True,
                                         timeout=5,
                                         creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
                    if result.returncode == 0:
                        current_version = result.stdout.strip()
                    else:
                        # Try using pip to get version as fallback
                        try:
                            current_version = yt_dlp.version.__version__
                        except:
                            current_version = "Not installed"
                except (subprocess.SubprocessError, subprocess.TimeoutExpired):
                    # Try using pip to get version as fallback
                    try:
                        current_version = yt_dlp.version.__version__
                    except:
                        current_version = "Not installed"
            else:
                # Try using pip to get version as fallback
                try:
                    current_version = yt_dlp.version.__version__
                except:
                    current_version = "Not installed"

            # Get latest version from GitHub API with timeout
            try:
                response = requests.get(
                    "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest",
                    timeout=10
                )
                response.raise_for_status()
                latest_version = response.json()["tag_name"]
            except Exception as e:
                raise Exception(f"Could not fetch latest version: {str(e)}")

            self.version_label.setText(
                f"Current version: {current_version}\n"
                f"Latest version: {latest_version}"
            )

            if current_version == "Not installed" or current_version != latest_version:
                self.update_btn.setEnabled(True)
                self.message_label.setText("An update is available!")
            else:
                self.message_label.setText("You have the latest version installed.")
                self.update_btn.setEnabled(False)

        except Exception as e:
            self.version_label.setText("Could not check versions")
            self.message_label.setText(f"Error: {str(e)}")
            self.update_btn.setEnabled(True)


    def start_update(self):
        self.update_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Starting update...")

        # Start update in a separate thread
        import threading
        threading.Thread(target=self._update_thread, daemon=True).start()

    def _update_thread(self):
        temp_path = None
        try:
            # Create necessary directories
            target_path = get_yt_dlp_path()
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            # Determine platform and get URLs
            if sys.platform == 'win32':
                url = 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe'
            else:
                url = 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp'

            temp_path = target_path + '.download'

            # Download with proper error handling
            try:
                response = requests.get(url, stream=True, timeout=30)
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                block_size = 8192  # Increased for better performance

                with open(temp_path, 'wb') as f:
                    for data in response.iter_content(block_size):
                        if data:  # Filter out keep-alive chunks
                            f.write(data)
                            progress = int((f.tell() * 100) / total_size) if total_size > 0 else 0
                            self.progress_bar.setValue(progress)
                            self.status_label.setText(f"Downloading: {progress}%")
            except requests.exceptions.RequestException as e:
                raise Exception(f"Download failed: {str(e)}")

            # Set proper permissions
            if sys.platform != 'win32':
                try:
                    os.chmod(temp_path, 0o755)
                except Exception as e:
                    print(f"Warning: Could not set executable permissions: {e}")

            # Handle file replacement
            try:
                if os.path.exists(target_path):
                    if sys.platform == 'win32':
                        # Windows-specific file replacement
                        import ctypes
                        if not ctypes.windll.kernel32.MoveFileExW(target_path, None, 4):  # MOVEFILE_DELAY_UNTIL_REBOOT
                            os.remove(target_path)
                    else:
                        os.remove(target_path)
            except PermissionError:
                raise Exception("Cannot update while yt-dlp is in use. Please close any active downloads and try again.")
            except Exception as e:
                raise Exception(f"Error removing existing file: {str(e)}")

            # Move temporary file to final location
            try:
                os.rename(temp_path, target_path)
            except Exception as e:
                raise Exception(f"Error moving new file into place: {str(e)}")

            self.status_label.setText("yt-dlp updated successfully!")
            self.close_btn.setText("Done")

            # Refresh version info
            self.check_versions()

        except Exception as e:
            self.status_label.setText(f"Error updating yt-dlp: {str(e)}")
        finally:
            # Clean up temp file if it exists
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            self.update_btn.setEnabled(True)

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('About YTSage')
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)

        # App title and version
        title_label = QLabel("YTSage")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #ff0000;
            padding: 10px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        version_label = QLabel(f"Version {parent.version}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        # Description
        description = QLabel(
            "A modern YouTube downloader with a clean interface.\n"
            "Download videos in any quality, extract audio, fetch subtitles,\n"
            "and view video metadata. Built with yt-dlp for reliable performance."
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)

        # Features list
        features_label = QLabel(
            "Key Features:\n"
            "• Smart video quality selection\n"
            "• Audio extraction\n"
            "• Subtitle support\n"
            "• Playlist downloads\n"
            "• Real-time progress tracking\n"
            "• Custom command support\n"
            "• SponsorBlock Integration\n"
            "• SponsorBlock Integration\n"
            "• One-click updates"
        )
        features_label.setStyleSheet("padding: 10px;")
        layout.addWidget(features_label)

        # Credits
        credits_label = QLabel(
            "Powered by:\n"
            "• yt-dlp\n"
            "• PySide6\n"
            "• FFmpeg"
        )
        credits_label.setStyleSheet("padding: 10px;")
        layout.addWidget(credits_label)

        # GitHub link
        github_btn = QPushButton("Visit GitHub Repository")
        github_btn.clicked.connect(lambda: webbrowser.open('https://github.com/oop7/YTSage'))
        layout.addWidget(github_btn)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        # Style the dialog
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)


class YTSageApp(QMainWindow): # Renamed class to YTSageApp to avoid name conflict with original file name
    def __init__(self):
        super().__init__()
        # Check for FFmpeg before proceeding
        if not check_ffmpeg():
            self.show_ffmpeg_dialog()

        self.version = "4.0.0"
        self.check_for_updates()
        self.config_file = Path.home() / '.ytsage_config.json'
        load_saved_path(self)
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown))
        self.signals = SignalManager()
        self.download_paused = False
        self.current_download = None
        self.download_cancelled = False
        self.save_thumbnail = False  # Initialize thumbnail state
        self.thumbnail_url = None    # Add this to store thumbnail URL
        self.init_ui()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                background-color: #363636;
                color: #ffffff;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;  /* YouTube red */
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;  /* Darker red on hover */
            }
            QPushButton:pressed {
                background-color: #990000;  /* Even darker red when pressed */
            }
            QTableWidget {
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                background-color: #363636;
                gridline-color: #3d3d3d;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                padding: 5px;
                border: 1px solid #3d3d3d;
                color: #ffffff;
            }
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #ff0000;  /* YouTube red */
                border-radius: 2px;
            }
            QLabel {
                color: #ffffff;
            }
            /* Style for filter buttons */
            QPushButton.filter-btn {
                background-color: #363636;
                padding: 5px 10px;
                margin: 0 5px;
            }
            QPushButton.filter-btn:checked {
                background-color: #ff0000;
            }
            QPushButton.filter-btn:hover {
                background-color: #444444;
            }
            QPushButton.filter-btn:checked:hover {
                background-color: #cc0000;
            }
            /* Modern Scrollbar Styling */
            QScrollBar:vertical {
                border: none;
                background: #2b2b2b;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: #404040;
                min-height: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background: #505050;
            }
            QScrollBar::sub-line:vertical {
                border: none;
                background: #2b2b2b;
                height: 15px;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:vertical {
                border: none;
                background: #2b2b2b;
                height: 15px;
                border-bottom-left-radius: 7px;
                border-bottom-right-radius: 7px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical:hover,
            QScrollBar::add-line:vertical:hover {
                background: #404040;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
                width: 0;
                height: 0;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            /* Horizontal Scrollbar */
            QScrollBar:horizontal {
                border: none;
                background: #2b2b2b;
                height: 14px;
                margin: 0 15px 0 15px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal {
                background: #404040;
                min-width: 30px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #505050;
            }
            QScrollBar::sub-line:horizontal {
                border: none;
                background: #2b2b2b;
                width: 15px;
                border-top-left-radius: 7px;
                border-bottom-left-radius: 7px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:horizontal {
                border: none;
                background: #2b2b2b;
                width: 15px;
                border-top-right-radius: 7px;
                border-bottom-right-radius: 7px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:horizontal:hover,
            QScrollBar::add-line:horizontal:hover {
                background: #404040;
            }
            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
                background: none;
                width: 0;
                height: 0;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)
        self.signals.update_progress.connect(self.update_progress_bar)

    def load_saved_path(self): # Using function from ytsage_utils now - no longer needed in class
        pass # Handled in class init now via ytsage_utils.load_saved_path(self)

    def save_path(self, path): # Using function from ytsage_utils now - no longer needed in class
        save_path(self, path) # Call the utility function

    def init_ui(self):
        self.setWindowTitle('YTSage  v4.0.0')
        self.setMinimumSize(900, 600)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # URL input section
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('Enter YouTube URL...')

        # Add Paste URL button
        self.paste_btn = QPushButton('Paste URL')
        self.paste_btn.clicked.connect(self.paste_url)

        self.analyze_btn = QPushButton('Analyze')
        self.analyze_btn.clicked.connect(self.analyze_url)

        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.paste_btn)
        url_layout.addWidget(self.analyze_btn)
        layout.addLayout(url_layout)

        # Create a horizontal layout for thumbnail and video info
        media_info_layout = QHBoxLayout()

        # Thumbnail on the left
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(320, 180)
        self.thumbnail_label.setStyleSheet("border: 2px solid #3d3d3d; border-radius: 4px;")
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        media_info_layout.addWidget(self.thumbnail_label)

        # Video information on the right
        video_info_layout = QVBoxLayout()
        self.title_label = QLabel()
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.channel_label = QLabel()
        self.views_label = QLabel()
        self.date_label = QLabel()
        self.duration_label = QLabel()

        # Style the info labels
        for label in [self.channel_label, self.views_label, self.date_label, self.duration_label]:
            label.setStyleSheet("""
                QLabel {
                    color: #cccccc;
                    font-size: 12px;
                    padding: 2px 0;
                }
            """)

        # Subtitle section with improved styling
        subtitle_layout = QHBoxLayout()
        self.subtitle_check = QPushButton("Download Subtitles")
        self.subtitle_check.setCheckable(True)
        self.subtitle_check.clicked.connect(self.toggle_subtitle_controls)
        self.subtitle_check.setStyleSheet("""
            QPushButton {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:checked {
                background-color: #ff0000;
                border-color: #cc0000;
            }
        """)
        subtitle_layout.addWidget(self.subtitle_check)

        # Create subtitle combo box
        self.subtitle_combo = QComboBox()
        self.subtitle_combo.setVisible(False)
        self.subtitle_combo.setStyleSheet("""
            QComboBox {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
                min-width: 200px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #363636;
                selection-background-color: #ff0000;
                selection-color: white;
            }
        """)

        # Create subtitle filter input
        self.subtitle_filter_input = QLineEdit()
        self.subtitle_filter_input.setPlaceholderText("Filter languages (e.g., en, es)")
        self.subtitle_filter_input.setMaximumWidth(200)
        self.subtitle_filter_input.textChanged.connect(self.filter_subtitles)
        self.subtitle_filter_input.setVisible(False)
        self.subtitle_filter_input.setStyleSheet("""
            QLineEdit {
                background-color: #363636;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }
            QLineEdit:focus {
                border-color: #ff0000;
            }
        """)

        # Add filter label and components to layout
        self.subtitle_filter_label = QLabel("Filter:")
        self.subtitle_filter_label.setVisible(False)
        subtitle_layout.addWidget(self.subtitle_filter_label)
        subtitle_layout.addWidget(self.subtitle_filter_input)
        subtitle_layout.addWidget(self.subtitle_combo)

        # Add merge subtitle toggle button
        self.merge_subs_btn = QPushButton('Merge Subtitles')
        self.merge_subs_btn.setCheckable(True)
        self.merge_subs_btn.setVisible(False)
        self.merge_subs_btn.setStyleSheet("""
            QPushButton {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:checked {
                background-color: #ff0000;
                border-color: #cc0000;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:checked:hover {
                background-color: #cc0000;
            }
        """)
        subtitle_layout.addWidget(self.merge_subs_btn)

        subtitle_layout.addStretch()

        # Add all info widgets to the video info layout
        video_info_layout.addWidget(self.title_label)
        video_info_layout.addWidget(self.channel_label)
        video_info_layout.addWidget(self.views_label)
        video_info_layout.addWidget(self.date_label)
        video_info_layout.addWidget(self.duration_label)
        video_info_layout.addLayout(subtitle_layout)
        video_info_layout.addStretch()

        media_info_layout.addLayout(video_info_layout)
        layout.addLayout(media_info_layout)

        # Add playlist information section with improved styling
        self.playlist_info_label = QLabel()
        self.playlist_info_label.setVisible(False)
        self.playlist_info_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #ff9900;
                padding: 5px;
                background-color: #363636;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.playlist_info_label)

        # Create format selection layout (horizontal)
        self.format_layout = QHBoxLayout()

        # Show formats label
        self.show_formats_label = QLabel("Show formats:")
        self.show_formats_label.setStyleSheet("color: white;")
        self.format_layout.addWidget(self.show_formats_label)

        # Format buttons group
        self.format_buttons = QButtonGroup(self)
        self.format_buttons.setExclusive(True)

        # Video button
        self.video_button = QPushButton("Video")
        self.video_button.setCheckable(True)
        self.video_button.setChecked(True)  # Set video as default
        self.video_button.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #363636;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #ff0000;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:checked:hover {
                background-color: #cc0000;
            }
        """)
        self.format_buttons.addButton(self.video_button)
        self.format_layout.addWidget(self.video_button)

        # Audio button
        self.audio_button = QPushButton("Audio Only")
        self.audio_button.setCheckable(True)
        self.audio_button.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #363636;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #ff0000;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QPushButton:checked:hover {
                background-color: #cc0000;
            }
        """)
        self.format_buttons.addButton(self.audio_button)
        self.format_layout.addWidget(self.audio_button)

        # Connect format buttons
        self.format_buttons.buttonClicked.connect(self.handle_format_selection)

        # Add SponsorBlock checkbox
        self.sponsorblock_checkbox = QCheckBox("Remove Sponsor Segments")
        self.sponsorblock_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 20px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #2b2b2b;
                border-radius: 9px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #ff0000;
                background: #ff0000;
                border-radius: 9px;
            }
        """)
        self.format_layout.addWidget(self.sponsorblock_checkbox)

        # Add Save Thumbnail checkbox with same style as SponsorBlock
        self.save_thumbnail_checkbox = QCheckBox("Save Thumbnail")
        self.save_thumbnail_checkbox.setStyleSheet("""
            QCheckBox {
                color: #ffffff;
                padding: 5px;
                margin-left: 20px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #666666;
                background: #2b2b2b;
                border-radius: 9px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #ff0000;
                background: #ff0000;
                border-radius: 9px;
            }
        """)
        self.save_thumbnail_checkbox.clicked.connect(self.toggle_save_thumbnail)
        self.format_layout.addWidget(self.save_thumbnail_checkbox)
        
        self.format_layout.addStretch()

        # Add format layout to main layout
        layout.addLayout(self.format_layout)

        # Format table with improved styling
        self.format_table = QTableWidget()
        self.format_table.setColumnCount(6)
        self.format_table.setHorizontalHeaderLabels(['Format ID', 'Extension', 'Resolution', 'File Size', 'Codec', 'Audio'])
        self.format_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.format_table.setStyleSheet("""
            QTableWidget {
                background-color: #363636;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                gridline-color: #3d3d3d;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #ff0000;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                padding: 5px;
                border: 1px solid #3d3d3d;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.format_table)

        # Download section
        download_layout = QHBoxLayout()

        # Add existing buttons
        self.custom_cmd_btn = QPushButton('Custom Command')
        self.custom_cmd_btn.clicked.connect(self.show_custom_command)

        self.update_ytdlp_btn = QPushButton('Update yt-dlp')
        self.update_ytdlp_btn.clicked.connect(self.update_ytdlp)

        self.about_btn = QPushButton('About')
        self.about_btn.clicked.connect(self.show_about_dialog)

        self.path_input = QLineEdit(self.last_path)
        self.path_input.setPlaceholderText('Download path...')

        self.browse_btn = QPushButton('Browse')
        self.browse_btn.clicked.connect(self.browse_path)

        self.download_btn = QPushButton('Download')
        self.download_btn.clicked.connect(self.start_download)

        # Add pause and cancel buttons
        self.pause_btn = QPushButton('Pause')
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setVisible(False)  # Hidden initially

        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setVisible(False)  # Hidden initially

        # Add all buttons to layout in the correct order
        download_layout.addWidget(self.custom_cmd_btn)
        download_layout.addWidget(self.update_ytdlp_btn)
        download_layout.addWidget(self.about_btn)
        download_layout.addWidget(self.path_input)
        download_layout.addWidget(self.browse_btn)
        download_layout.addWidget(self.download_btn)
        download_layout.addWidget(self.pause_btn)
        download_layout.addWidget(self.cancel_btn)

        layout.addLayout(download_layout)

        # Progress section with improved styling
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                color: white;
                background-color: #363636;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #ff0000;
                border-radius: 2px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)

        # Add download details label with improved styling
        self.download_details_label = QLabel()
        self.download_details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.download_details_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 12px;
                padding: 5px;
            }
        """)
        progress_layout.addWidget(self.download_details_label)

        self.status_label = QLabel('Ready')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 12px;
                padding: 5px;
            }
        """)
        progress_layout.addWidget(self.status_label)

        layout.addLayout(progress_layout)

        # Connect signals
        self.signals.update_formats.connect(self.update_format_table)
        self.signals.update_status.connect(self.status_label.setText)
        self.signals.update_progress.connect(self.update_progress_bar)

    def analyze_url(self):
        url = self.url_input.text().strip()
        if not url:
            self.signals.update_status.emit("Invalid URL or please enter a URL.")
            return

        self.signals.update_status.emit("Analyzing (0%)... Preparing request")
        import threading # Import threading here as it is only used in GUI and downloader
        threading.Thread(target=self._analyze_url_thread, args=(url,), daemon=True).start()

    def _analyze_url_thread(self, url):
        try:
            self.signals.update_status.emit("Analyzing (20%)... Extracting basic info")

            # Clean up the URL to handle both playlist and video URLs
            if 'list=' in url and 'watch?v=' in url:
                playlist_id = url.split('list=')[1].split('&')[0]
                url = f'https://www.youtube.com/playlist?list={playlist_id}'

            # Initial extraction with basic options
            ydl_opts = {
                'quiet': False,
                'no_warnings': False,
                'extract_flat': True,
                'force_generic_extractor': False,
                'ignoreerrors': True,
                'no_color': True,
                'verbose': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    basic_info = ydl.extract_info(url, download=False)
                    if not basic_info:
                        raise Exception("Could not extract basic video information")
                except Exception as e:
                    print(f"First extraction failed: {str(e)}")
                    raise Exception("Could not extract video information, please check your link")

            self.signals.update_status.emit("Analyzing (40%)... Extracting detailed info")
            # Configure options for detailed extraction
            ydl_opts.update({
                'extract_flat': False,
                'format': None,
                'writesubtitles': True,
                'allsubtitles': True,
                'writeautomaticsub': True,
                'playliststart': 1,
                'playlistend': 1,
                'youtube_include_dash_manifest': True,
                'youtube_include_hls_manifest': True
            })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    self.signals.update_status.emit("Analyzing (60%)... Processing video data")
                    if basic_info.get('_type') == 'playlist':
                        self.is_playlist = True
                        self.playlist_info = basic_info

                        # Get the first video URL from the playlist
                        first_video = None
                        for entry in basic_info['entries']:
                            if entry:
                                first_video = entry
                                break

                        if not first_video:
                            raise Exception("No valid videos found in playlist")

                        # Get the video URL
                        video_url = first_video.get('url') or first_video.get('webpage_url')
                        if not video_url:
                            raise Exception("Could not extract video URL from playlist")

                        # Extract detailed information for the first video
                        self.video_info = ydl.extract_info(video_url, download=False)

                        # Update playlist info
                        playlist_text = f"Playlist: {basic_info.get('title', 'Unknown')} | {len(basic_info['entries'])} videos"
                        self.playlist_info_label.setText(playlist_text)
                        self.playlist_info_label.setVisible(True)
                    else:
                        self.is_playlist = False
                        self.video_info = ydl.extract_info(url, download=False)
                        self.playlist_info_label.setVisible(False)

                    # Verify we have format information
                    if not self.video_info or 'formats' not in self.video_info:
                        print(f"Debug - video_info keys: {self.video_info.keys() if self.video_info else 'None'}")
                        raise Exception("No format information available")

                    self.signals.update_status.emit("Analyzing (80%)... Processing formats")
                    self.all_formats = self.video_info['formats']

                    # Update UI
                    self.update_video_info(self.video_info)

                    # Update thumbnail
                    self.signals.update_status.emit("Analyzing (90%)... Loading thumbnail")
                    self.download_thumbnail(self.video_info.get('thumbnail'))
                    
                    # Save thumbnail if enabled - use the stored VIDEO URL
                    if self.save_thumbnail:
                        self.download_thumbnail_file(self.video_url, self.path_input.text())

                    # Update subtitles
                    self.signals.update_status.emit("Analyzing (95%)... Processing subtitles")
                    self.available_subtitles = self.video_info.get('subtitles', {})
                    self.available_automatic_subtitles = self.video_info.get('automatic_captions', {})
                    self.update_subtitle_list()

                    # Update format table
                    self.signals.update_status.emit("Analyzing (98%)... Updating format table")
                    self.video_button.setChecked(True)
                    self.audio_button.setChecked(False)
                    self.filter_formats()

                    self.signals.update_status.emit("Analysis complete!")

                except Exception as e:
                    print(f"Detailed extraction failed: {str(e)}")
                    raise Exception(f"Failed to extract video details: {str(e)}")

        except Exception as e:
            error_message = str(e)
            print(f"Error in analysis: {error_message}")
            self.signals.update_status.emit(f"Error: {error_message}")

    def update_video_info(self, info):
        # Format view count with commas
        views = int(info.get('view_count', 0))
        formatted_views = f"{views:,}"

        # Format upload date
        upload_date = info.get('upload_date', '')
        if upload_date:
            date_obj = datetime.strptime(upload_date, '%Y%m%d')
            formatted_date = date_obj.strftime('%B %d, %Y')
        else:
            formatted_date = 'Unknown date'

        # Format duration
        duration = info.get('duration', 0)
        minutes = duration // 60
        seconds = duration % 60
        duration_str = f"{minutes}:{seconds:02d}"

        # Update labels
        self.title_label.setText(info.get('title', 'Unknown title'))
        self.channel_label.setText(f"Channel: {info.get('uploader', 'Unknown channel')}")
        self.views_label.setText(f"Views: {formatted_views}")
        self.date_label.setText(f"Upload date: {formatted_date}")
        self.duration_label.setText(f"Duration: {duration_str}")

    def toggle_subtitle_controls(self):
        is_checked = self.subtitle_check.isChecked()
        self.merge_subs_btn.setVisible(is_checked)
        self.subtitle_combo.setVisible(is_checked)
        self.subtitle_filter_input.setVisible(is_checked)
        self.subtitle_filter_label.setVisible(is_checked)

    def update_subtitle_list(self):
        self.subtitle_combo.clear()

        if not (self.available_subtitles or self.available_automatic_subtitles):
            self.subtitle_combo.addItem("No subtitles available")
            return

        # Add subtitle options
        self.subtitle_combo.addItem("Select subtitle language")

        # Filter and add subtitles
        filter_text = self.subtitle_filter_input.text().lower()

        # Add manual subtitles
        for lang_code, subtitle_info in self.available_subtitles.items():
            if not filter_text or filter_text in lang_code.lower():
                self.subtitle_combo.addItem(f"{lang_code} - Manual")

        # Add auto-generated subtitles
        for lang_code, subtitle_info in self.available_automatic_subtitles.items():
            if not filter_text or filter_text in lang_code.lower():
                self.subtitle_combo.addItem(f"{lang_code} - Auto-generated")

    def filter_subtitles(self):
        self.subtitle_filter = self.subtitle_filter_input.text()
        self.update_subtitle_list()

    def download_thumbnail(self, url):
        try:
            # Store both thumbnail URL and video URL
            self.thumbnail_url = url
            self.video_url = self.url_input.text()  # Get actual video URL
            
            # Download thumbnail but don't save yet
            response = requests.get(url)
            self.thumbnail_image = Image.open(BytesIO(response.content))
            
            # Display thumbnail
            image = self.thumbnail_image.resize((320, 180), Image.Resampling.LANCZOS)
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='PNG')
            pixmap = QPixmap()
            pixmap.loadFromData(img_byte_arr.getvalue())
            self.thumbnail_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Error loading thumbnail: {str(e)}")

    def filter_formats(self):
        # Clear current table
        self.format_table.setRowCount(0)

        # Determine which formats to show
        filtered_formats = []

        if self.video_button.isChecked():
            # Include all video formats (both with and without audio)
            filtered_formats.extend([f for f in self.all_formats
                                  if f.get('vcodec') != 'none'
                                  and f.get('filesize') is not None])

        if self.audio_button.isChecked():
            # Add audio-only formats
            filtered_formats.extend([f for f in self.all_formats
                                  if (f.get('vcodec') == 'none'
                                      or 'audio only' in f.get('format_note', '').lower())
                                  and f.get('acodec') != 'none'
                                  and f.get('filesize') is not None])

        # Sort formats by quality
        def get_quality(f):
            if f.get('vcodec') != 'none':
                # Extract height from resolution (e.g., "1920x1080" -> 1080)
                res = f.get('resolution', '0x0').split('x')[-1]
                try:
                    return int(res)
                except ValueError:
                    return 0
            else:
                return f.get('abr', 0)

        filtered_formats.sort(key=get_quality, reverse=True)

        # Update table with filtered formats
        self.update_format_table(filtered_formats)

    def update_format_table(self, formats):
        self.format_table.setRowCount(0)
        for f in formats:
            row = self.format_table.rowCount()
            self.format_table.insertRow(row)

            # Format ID
            self.format_table.setItem(row, 0, QTableWidgetItem(str(f.get('format_id', ''))))

            # Extension
            self.format_table.setItem(row, 1, QTableWidgetItem(f.get('ext', '')))

            # Resolution
            resolution = f.get('resolution', 'N/A')
            if f.get('vcodec') == 'none':
                resolution = 'Audio only'
            self.format_table.setItem(row, 2, QTableWidgetItem(resolution))

            # File Size
            filesize = f"{f.get('filesize', 0) / 1024 / 1024:.2f} MB"
            self.format_table.setItem(row, 3, QTableWidgetItem(filesize))

            # Codec
            if f.get('vcodec') == 'none':
                codec = f.get('acodec', 'N/A')
            else:
                codec = f"{f.get('vcodec', 'N/A')}"
                if f.get('acodec') != 'none':
                    codec += f" / {f.get('acodec', 'N/A')}"
            self.format_table.setItem(row, 4, QTableWidgetItem(codec))

            # Audio Status
            needs_audio = f.get('acodec') == 'none'
            audio_status = "Will merge audio" if needs_audio else "✓ Has Audio"
            audio_item = QTableWidgetItem(audio_status)
            if needs_audio:
                audio_item.setForeground(QColor('#ffa500'))  # Orange for merge indication
            self.format_table.setItem(row, 5, audio_item)

    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Download Directory", self.last_path)
        if path:
            self.path_input.setText(path)
            self.save_path(path) # Use save_path utility function
            self.last_path = path

    def start_download(self):
        url = self.url_input.text().strip()
        path = self.path_input.text().strip()

        if not url or not path:
            self.status_label.setText("Please enter URL and download path")
            return

        # Get selected format
        selected_items = self.format_table.selectedItems()
        if not selected_items:
            self.status_label.setText("Please select a format")
            return

        format_id = self.format_table.item(selected_items[0].row(), 0).text()

        # Get resolution for filename
        resolution = self.format_table.item(selected_items[0].row(), 2).text()
        resolution = resolution.replace(' ', '').lower()  # Clean up resolution string

        # Get subtitle selection if available
        subtitle_lang = None
        if hasattr(self, 'subtitle_combo') and self.subtitle_combo.currentIndex() > 0:
            subtitle_lang = self.subtitle_combo.currentText()

        # Check if it's a playlist
        is_playlist = 'playlist' in url.lower() and '/watch?' not in url

        # Save thumbnail if enabled
        if self.save_thumbnail:
            self.download_thumbnail_file(url, path)

        # Create download thread with resolution in output template
        self.download_thread = DownloadThread(
            url=url,
            path=path,
            format_id=format_id,
            subtitle_lang=subtitle_lang,
            is_playlist=is_playlist,
            merge_subs=bool(subtitle_lang),
            enable_sponsorblock=self.sponsorblock_checkbox.isChecked(),
            resolution=resolution
        )

        # Connect signals
        self.download_thread.progress_signal.connect(self.update_progress_bar)
        self.download_thread.status_signal.connect(self.signals.update_status.emit)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.error_signal.connect(self.download_error)

        # Reset download state
        self.download_paused = False
        self.download_cancelled = False

        # Show pause/cancel buttons
        self.pause_btn.setText('Pause')
        self.pause_btn.setVisible(True)
        self.cancel_btn.setVisible(True)

        # Start download thread
        self.current_download = self.download_thread
        self.download_thread.start()
        self.toggle_download_controls(False)

    def download_finished(self):
        self.toggle_download_controls(True)
        self.pause_btn.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.progress_bar.setValue(100)
        self.status_label.setText("Download completed!")

    def download_error(self, error_message):
        self.toggle_download_controls(True)
        self.pause_btn.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.status_label.setText(f"Error: {error_message}")

    def update_progress_bar(self, value):
        try:
            # Ensure the value is an integer
            int_value = int(value)
            self.progress_bar.setValue(int_value)
        except Exception as e:
            print(f"Progress bar update error: {str(e)}")

    def toggle_pause(self):
        if self.current_download:
            self.current_download.paused = not self.current_download.paused
            if self.current_download.paused:
                self.pause_btn.setText('Resume')
                self.signals.update_status.emit("Download paused")
            else:
                self.pause_btn.setText('Pause')
                self.signals.update_status.emit("Download resumed")

    def check_for_updates(self):
        try:
            # Get the latest release info from GitHub
            response = requests.get(
                "https://api.github.com/repos/oop7/YTSage/releases/latest",
                headers={"Accept": "application/vnd.github.v3+json"}
            )
            response.raise_for_status()

            latest_release = response.json()
            latest_version = latest_release["tag_name"].lstrip('v')

            # Compare versions
            if version.parse(latest_version) > version.parse(self.version):
                self.show_update_dialog(latest_version, latest_release["html_url"])
        except Exception as e:
            print(f"Failed to check for updates: {str(e)}")

    def show_update_dialog(self, latest_version, release_url):
        msg = QDialog(self)
        msg.setWindowTitle("Update Available")
        msg.setMinimumWidth(400)

        layout = QVBoxLayout(msg)

        # Update message
        message_label = QLabel(
            f"A new version of YTSage is available!\n\n"
            f"Current version: {self.version}\n"
            f"Latest version: {latest_version}"
        )
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        # Buttons
        button_layout = QHBoxLayout()

        download_btn = QPushButton("Download Update")
        download_btn.clicked.connect(lambda: self.open_release_page(release_url))

        remind_btn = QPushButton("Remind Me Later")
        remind_btn.clicked.connect(msg.close)

        button_layout.addWidget(download_btn)
        button_layout.addWidget(remind_btn)
        layout.addLayout(button_layout)

        # Style the dialog
        msg.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
                padding: 10px;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #ff0000;
                border: none;
                border-radius: 4px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)

        msg.show()

    def open_release_page(self, url):
        webbrowser.open(url)

    def show_custom_command(self):
        dialog = CustomCommandDialog(self)
        dialog.exec()

    def cancel_download(self):
        if self.current_download:
            self.current_download.cancelled = True
            self.signals.update_status.emit("Cancelling download...")


    def show_ffmpeg_dialog(self):
        dialog = FFmpegCheckDialog(self)
        dialog.exec()

    def paste_url(self):
        clipboard = QApplication.clipboard()
        self.url_input.setText(clipboard.text())

    def update_ytdlp(self):
        dialog = YTDLPUpdateDialog(self)
        dialog.exec()

    def toggle_save_thumbnail(self):
        self.save_thumbnail = self.save_thumbnail_checkbox.isChecked()
        print(f"Save thumbnail toggled: {self.save_thumbnail}")  # Debug print

    def download_thumbnail_file(self, video_url, path):
        if not self.save_thumbnail:
            return False
        
        try:
            from yt_dlp import YoutubeDL
            import requests  # Use requests instead of urlopen

            print(f"Attempting to save thumbnail for URL: {video_url}")

            ydl_opts = {
                'quiet': True,
                'skip_download': True,
                'force_generic_extractor': False,
                'no_warnings': True,
                'extract_flat': False
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                thumbnails = info.get('thumbnails', [])
                
                if not thumbnails:
                    raise ValueError("No thumbnails available")
                    
                thumbnail_url = max(
                    thumbnails,
                    key=lambda t: (t.get('height', 0) or 0) * (t.get('width', 0) or 0)
                ).get('url')

                if not thumbnail_url:
                    raise ValueError("Failed to extract thumbnail URL")

                # Download using requests
                response = requests.get(thumbnail_url)
                response.raise_for_status()

                # Save the thumbnail
                thumb_dir = os.path.join(path, 'Thumbnails')
                os.makedirs(thumb_dir, exist_ok=True)
                
                filename = f"{self.sanitize_filename(info['title'])}.jpg"
                thumbnail_path = os.path.join(thumb_dir, filename)
                
                with open(thumbnail_path, 'wb') as f:
                    f.write(response.content)

                print(f"Thumbnail saved to: {thumbnail_path}")
                self.signals.update_status.emit(f"✅ Thumbnail saved: {filename}")
                return True

        except Exception as e:
            error_msg = f"❌ Thumbnail error: {str(e)}"
            print(f"Thumbnail Save Error: {str(e)}")
            self.signals.update_status.emit(error_msg)
            return False

    def sanitize_filename(self, name):
        """Clean filename for filesystem safety"""
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()[:75]

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def toggle_download_controls(self, enabled=True):
        """Enable or disable download-related controls"""
        self.url_input.setEnabled(enabled)
        self.analyze_btn.setEnabled(enabled)
        self.format_table.setEnabled(enabled)
        self.path_input.setEnabled(enabled)
        self.browse_btn.setEnabled(enabled)
        self.download_btn.setEnabled(enabled)
        if hasattr(self, 'subtitle_combo'):
            self.subtitle_combo.setEnabled(enabled)
        self.video_button.setEnabled(enabled)
        self.audio_button.setEnabled(enabled)
        self.sponsorblock_checkbox.setEnabled(enabled)

    def handle_format_selection(self, button):
        # Update formats
        self.filter_formats()