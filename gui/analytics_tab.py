from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

class AnalyticsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.btn = QPushButton("Generate ROI Chart from Database")
        self.btn.clicked.connect(self.generate_chart)
        layout.addWidget(self.btn)
        self.canvas = None
        self.setLayout(layout)
        self.layout = layout

    def generate_chart(self):
        conn = sqlite3.connect('data/financeflow.db')
        df = pd.read_sql_query(
            "SELECT state, SUM(funding) AS funding, SUM(jobs_created) AS jobs "
            "FROM investments GROUP BY state", conn
        )
        conn.close()

        df['ROI'] = df['funding'] / (df['jobs'] + 1)
        fig, ax = plt.subplots()
        ax.bar(df['state'], df['ROI'], color='darkcyan')
        ax.set_title("Funding Efficiency (ROI $ per Job)")
        ax.set_ylabel("Funding per job ($)")
        ax.set_xlabel("State")

        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()

        self.canvas = FigureCanvasQTAgg(fig)
        self.layout.addWidget(self.canvas)

