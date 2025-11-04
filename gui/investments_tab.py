from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QFormLayout, QMessageBox, QCompleter
)
from PyQt5.QtCore import Qt
import geopandas as gpd
import pandas as pd
import sqlite3
from us import states

class InvestmentsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # --- Title ---
        self.layout.addWidget(QLabel("Add New Investment Record"))

        # --- Form fields ---
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

        # --- Autocomplete datasets ---
        states = [
            "Alabama","Alaska","Arizona","Arkansas","California","Colorado",
            "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
            "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
            "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
            "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
            "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
            "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
            "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"
        ]
        industries = [
            "Agriculture","Construction","Education","Energy","Finance","Healthcare",
            "Infrastructure","Manufacturing","Research","Retail","Technology","Tourism",
            "Transportation","Renewable Energy"
        ]
        counties = [
            "Jefferson","Mobile","Madison","Montgomery","Los Angeles","Orange",
            "Travis","Kings","Cook","Harris"
        ]

        state_completer = QCompleter(states)
        industry_completer = QCompleter(industries)
        county_completer = QCompleter(counties)

        self.state_input.setCompleter(state_completer)
        self.industry_input.setCompleter(industry_completer)
        self.county_input.setCompleter(county_completer)

        # --- Submit button ---
        self.save_btn = QPushButton("Save Record")
        self.save_btn.clicked.connect(self.add_to_database)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

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

            conn = sqlite3.connect("data/financeflow.db")
            c = conn.cursor()
            c.execute("""
                INSERT INTO investments (state, county, project_name, industry, funding, jobs_created, start_year, end_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Investment added successfully!")
            for field in [self.state_input, self.county_input, self.project_input,
                          self.industry_input, self.funding_input, self.jobs_input,
                          self.start_input, self.end_input]:
                field.clear()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not add investment: {e}")
