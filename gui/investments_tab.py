from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QFormLayout, QMessageBox, QCompleter
)
from PyQt5.QtCore import Qt
import geopandas as gpd
import pandas as pd
import sqlite3
import os
from us import states

def load_county_data():
    """Load and cache US counties locally to avoid freezing."""
    cache_path = "data/us_counties.geojson"

    # If cached file exists, use it
    if os.path.exists(cache_path):
        return gpd.read_file(cache_path)

    # Otherwise download once and save
    print("Downloading county shapefile... (first run only)")
    url = "https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip"
    df = gpd.read_file(url)
    df.to_file(cache_path, driver="GeoJSON")
    print("Saved cached county file to:", cache_path)
    return df

class InvestmentsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

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

        # --- State completer ---
        all_states = [s.name for s in states.STATES]
        self.state_completer = QCompleter(all_states)
        self.state_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.state_input.setCompleter(self.state_completer)

        # --- Empty county completer initially ---
        self.county_completer = QCompleter([])
        self.county_completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.county_input.setCompleter(self.county_completer)

        # --- When state changes, load counties dynamically ---
        self.state_input.textChanged.connect(self.update_county_completer)

        # --- Save button ---
        self.save_btn = QPushButton("Save Record")
        self.save_btn.clicked.connect(self.add_to_database)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def update_county_completer(self):
        """Load official county names dynamically for the selected state."""
        state_name = self.state_input.text().strip()
        st = states.lookup(state_name)
        if not st:
            self.county_completer = QCompleter([])
            self.county_input.setCompleter(self.county_completer)
            return

        try:
            # Download or read the US counties shapefile (Census TIGER)
            url = "https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip"
            df = gpd.read_file(url)

            # Filter by selected state FIPS
            state_counties = df[df["STATEFP"] == st.fips]["NAME"].tolist()
            state_counties.sort()

            # Update county completer dynamically
            self.county_completer = QCompleter(state_counties)
            self.county_completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.county_input.setCompleter(self.county_completer)

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load counties: {e}")

    def add_to_database(self):
        """Save new investment entry."""
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
