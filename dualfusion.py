from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QLabel, QRadioButton, QGroupBox, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt
from theme import apply_nordic_theme
from ui import DragDropList, ProcessThread

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DualFusion")
        self.resize(540, 500)
        self.thread = None

        self.tabs = QTabWidget()
        self.series_tab = DragDropList()
        self.info_tab = QLabel(self.get_info_text())
        self.info_tab.setAlignment(Qt.AlignTop)
        self.info_tab.setWordWrap(True)
        self.tabs.addTab(self.series_tab, "Dizi")
        self.tabs.addTab(self.info_tab, "Nedir?")

        self.dual_radio = QRadioButton("Dual (Orijinal + Türkçe)")
        self.only_tr_radio = QRadioButton("Sadece Türkçe Dublaj")
        self.only_tr_radio.setChecked(True)
        self.mode_group = QGroupBox("Ses Modu Seçimi")
        mode_layout = QVBoxLayout()
        mode_layout.addWidget(self.dual_radio)
        mode_layout.addWidget(self.only_tr_radio)
        self.mode_group.setLayout(mode_layout)

        self.delay_input = QLineEdit("0")
        self.delay_input.setPlaceholderText("Delay (ms)")

        self.action_button = QPushButton("Dizileri İşle")
        self.stop_button = QPushButton("Durdur")
        self.clear_button = QPushButton("Temizle")
        self.action_button.clicked.connect(self.process_files)
        self.stop_button.clicked.connect(self.stop_processing)
        self.clear_button.clicked.connect(self.clear_lists)
        self.tabs.currentChanged.connect(self.update_button_label)

        self.progress_bar = QProgressBar()
        self.footer = QLabel("xmtaha tarafından sevgi ile kodlanmıştır ❤️  |  GitHub: https://github.com/xmtaha")
        self.footer.setAlignment(Qt.AlignCenter)

        self.layout_ui()
        self.update_button_label()

    def layout_ui(self):
        layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.action_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.clear_button)

        layout.addWidget(self.tabs)
        layout.addWidget(self.mode_group)
        layout.addWidget(QLabel("Ses Gecikmesi (ms):"))
        layout.addWidget(self.delay_input)
        layout.addLayout(button_layout)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.footer)
        self.setLayout(layout)

    def update_button_label(self):
        self.action_button.setText(
            "Dizileri İşle" if self.tabs.currentIndex() == 0 else ""
        )

    def get_mode(self):
        return "dual" if self.dual_radio.isChecked() else "turkish-only"

    def get_delay(self):
        try:
            return int(self.delay_input.text())
        except ValueError:
            return 0

    def process_files(self):
        files = [self.series_tab.item(i).text() for i in range(self.series_tab.count())]
        if not files:
            QMessageBox.warning(self, "Uyarı", "Lütfen dosyaları sürükleyin.")
            return
        self.run_processing(files)

    def run_processing(self, files):
        self.thread = ProcessThread(files, self.get_mode(), self.get_delay(), True)
        self.thread.progress_signal.connect(self.progress_bar.setValue)
        self.thread.finished_signal.connect(lambda: QMessageBox.information(self, "İşlem Tamamlandı", "İşlem başarıyla tamamlandı!"))
        self.thread.finished_signal.connect(self.thread.deleteLater)
        self.thread.start()

    def stop_processing(self):
        if self.thread and self.thread.isRunning():
            self.thread.terminate()
            self.thread.wait()
            self.progress_bar.setValue(0)
            QMessageBox.information(self, "Durduruldu", "İşlem kullanıcı tarafından durduruldu.")

    def clear_lists(self):
        self.series_tab.clear()
        self.progress_bar.setValue(0)
        QMessageBox.information(self, "Temizlendi", "Dosya listesi sıfırlandı.")

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        event.accept()

    def get_info_text(self):
        return (
            "Dual ses: Dizi bölümünde hem orijinal hem Türkçe dublaj ses bulunur.\n"
            "Türkçe Dublaj: Yalnızca Türkçe ses içerir.\n\n"
            "Not: Tüm altyazılar kaldırılır. Elle eklenirse mux yapılır.\n\n"
            "xmtaha tarafından sevgi ile kodlanmıştır ❤️"
        )

if __name__ == "__main__":
    app = QApplication([])
    apply_nordic_theme(app)
    window = MainApp()
    window.show()
    app.exec_()
