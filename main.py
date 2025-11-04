from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from gui.investments_tab import InvestmentsTab
from gui.analytics_tab import AnalyticsTab
from gui.map_tab import MapTab
from gui.investments_tab import InvestmentsTab
self.tabs.addTab(InvestmentsTab(), "Investments")
import sys

class FinanceFlowMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FinanceFlow USA - Economic Analytics Dashboard")
        self.setMinimumSize(1200, 700)
        self.initUI()

    def initUI(self):
        tabs = QTabWidget()
        tabs.addTab(InvestmentsTab(), "Investments")
        tabs.addTab(AnalyticsTab(), "Analytics")
        tabs.addTab(MapTab(), "Map")
        self.setCentralWidget(tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # optional: load stylesheet
    try:
        with open("assets/styles.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass

    window = FinanceFlowMain()
    window.show()
    sys.exit(app.exec_())

