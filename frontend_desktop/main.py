import sys, requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Desktop Pro")
        layout = QVBoxLayout()

        self.label = QLabel("Upload a CSV to see stats")
        layout.addWidget(self.label)

        btn = QPushButton("Upload CSV")
        btn.clicked.connect(self.upload)
        layout.addWidget(btn)

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def upload(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open CSV")
        if path:
            files = {'file': open(path, 'rb')}
            r = requests.post("http://127.0.0.1:8000/api/upload/", files=files)
            data = r.json()
            self.label.setText(f"Avg Pressure: {data['avg_pressure']}")
            self.plot(data['type_distribution'])

    def plot(self, counts):
        ax = self.canvas.figure.gca()
        ax.clear()
        ax.bar(counts.keys(), counts.values())
        self.canvas.draw()

app = QApplication(sys.argv)
win = App()
win.show()
sys.exit(app.exec_())