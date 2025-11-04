from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QLineEdit, QHBoxLayout, QMessageBox, QFormLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

class InvestmentsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Title
        self.label = QLabel("Upload data or add new investments")
        self.layout.addWidget(self.label)

        # Upload CSV button
        self.upload_btn = QPushButton("Import CSV")
        self.upload_btn.clicked.connect(self.load_data)
        self.layout.addWidget(self.upload_btn)

        # --- New: manual data entry form ---
        form_layout = QFormLayout()
        self.state_input = QLineEdit()
        self.county_input = QLineEdit()
        self.project_input = QLineEdit()
        self.industry_input = QLineEdit()
        self.funding_input = QLineEdit()
        self.jobs_input = QLineEdit()
        self.start_input = QLineEdit()
        self.end_input = QLineEdit()

        form_layout.addRow("State:", self.state_input)
        form_layout.addRow("County:", self.county_input)
        form_layout.addRow("Project Name:", self.project_input)
        form_layout.addRow("Industry:", self.industry_input)
        form_layout.addRow("Funding ($M):", self.funding_input)
        form_layout.addRow("Jobs Created:", self.jobs_input)
        form_layout.addRow("Start Year:", self.start_input)
        form_layout.addRow("End Year:", self.end_input)

        self.layout.addLayout(form_layout)

        self.save_btn = QPushButton("Add to Database")
        self.save_btn.clicked.connect(self.add_to_database)
        self.layout.addWidget(self.save_btn)

        # Chart placeholder
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

    def add_to_database(self):
        try:
            data = (
                self.state_input.text(),
                self.county_input.text(),
                self.project_input.text(),
                self.industry_input.text(),
                float(self.funding_input.text()),
                int(self.jobs_input.text()),
                int(self.start_input.text()),
                int(self.end_input.text())
            )

            conn = sqlite3.connect('data/financeflow.db')
            c = conn.cursor()
            c.execute("""
                INSERT INTO investments (state, county, project_name, industry, funding, jobs_created, start_year, end_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "New investment added successfully!")

            # Clear inputs
            for widget in [self.state_input, self.county_input, self.project_input, self.industry_input,
                           self.funding_input, self.jobs_input, self.start_input, self.end_input]:
                widget.clear()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not add investment: {e}")
