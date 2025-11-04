from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import pandas as pd

class InvestmentsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("Upload a CSV file with state-level investments:")
        self.button = QPushButton("Import CSV")
        self.button.clicked.connect(self.load_data)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.canvas = None
        self.setLayout(self.layout)

    def load_data(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file:
            df = pd.read_csv(file)
            self.plot_data(df)

    def plot_data(self, df):
        fig, ax = plt.subplots(figsize=(8, 5))
        grouped = df.groupby('State')['Funding'].sum().sort_values()
        grouped.plot(kind='barh', color='teal', ax=ax)
        ax.set_title("Total Funding by State (Millions $)")
        ax.set_xlabel("Funding ($M)")

        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()

        self.canvas = FigureCanvasQTAgg(fig)
        self.layout.addWidget(self.canvas)

