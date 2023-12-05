from flask import Flask, render_template, send_file, request
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from sys import argv
from PIL import Image, ImageDraw
import io
import math

app = Flask(__name__)

GOLDEN_RATIO = (1 + 5**0.5) / 2
R1 = r = (1 / GOLDEN_RATIO)**(1 / GOLDEN_RATIO)
R2 = R1**2
ANGLE1 = math.acos((1 + r**2 - r**4) / (2 * r))
ANGLE2 = math.acos((1 + r**4 - r**2) / (2 * r**2))

def frac(x1, y1, x2, y2, turn, n):
    def gf(draw, x1, y1, x2, y2, turn, n):
        if n == 1:
            draw.line([x1, y1, x2, y2], fill='white')
        else:
            dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
            
            if dist < 1:
                draw.line([x1, y1, x2, y2], fill='white')
            else:
                angle = math.atan2(y2 - y1, x2 - x1)
                
                if turn:
                    px = x1 + dist * R1 * math.cos(angle + ANGLE1)
                    py = y1 + dist * R1 * math.sin(angle + ANGLE1)
                else:
                    px = x1 + dist * R2 * math.cos(angle - ANGLE2)
                    py = y1 + dist * R2 * math.sin(angle - ANGLE2)
                    
                gf(draw, x1, y1, px, py, True, n - 1)
                gf(draw, px, py, x2, y2, False, n - 1)
            
    img = Image.new('RGB', (750, 750), color='black')
    draw = ImageDraw.Draw(img)
    gf(draw, x1, y1, x2, y2, turn, n)

    return img

@app.route('/fractal')
def draw_fractal():
    n = request.args.get('n', type=int, default=14)
    img = frac(50, 350, 650, 350, True, n if n > 1 else 1)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

@app.route('/')
def index():
    return render_template('index.html')

class WebViewApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('DRAGGGGGOON')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        self.webview = QWebEngineView(self)
        layout.addWidget(self.webview)

if __name__ == '__main__':
    from threading import Thread
    Thread(target=app.run, kwargs={'host': '0.0.0.0'}).start()

    qt_app = QApplication(argv)
    main_window = WebViewApp()
    main_window.webview.setUrl(QUrl('http://127.0.0.1:5000'))
    main_window.show()
    qt_app.exec_()
