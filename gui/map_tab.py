from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium, io

class MapTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        view = QWebEngineView()

        # Create U.S. base map
        m = folium.Map(location=[37.8, -96], zoom_start=4)
        folium.Marker([32.3, -86.9], popup="Montgomery, AL").add_to(m)
        folium.Marker([34.0, -118.2], popup="Los Angeles, CA").add_to(m)
        folium.Marker([40.7, -74.0], popup="New York, NY").add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)
        view.setHtml(data.getvalue().decode())

        layout.addWidget(view)

