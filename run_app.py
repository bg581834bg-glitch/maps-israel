import webview
import threading
from pathlib import Path
import http.server
import socketserver
import subprocess

osrm_process = None      # משתנה גלובלי לשרת OSRM
tile_server = None       # משתנה גלובלי לשרת האריחים

def run_tile_server():
    global tile_server
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    tile_server = socketserver.TCPServer(("", PORT), Handler)
    print(f"שרת האריחים פועל על פורט {PORT}")
    try:
        tile_server.serve_forever()
    except Exception as e:
        print(f"שגיאה בשרת האריחים: {e}")

def run_osrm_server():
    global osrm_process
    try:
        osrm_path = Path("osrm")
        data_file = "israel-and-palestine-latest.osrm"
        if not (osrm_path / data_file).exists():
            print("שגיאה: קובץ הנתונים לא נמצא")
            return None
        cmd = f"osrm-routed {data_file}"
        osrm_process = subprocess.Popen(cmd, shell=True, cwd=osrm_path)
        print("שרת OSRM הופעל")
        return osrm_process
    except Exception as e:
        print(f"שגיאה בהפעלת שרת OSRM: {e}")
        return None

def on_closed():
    global osrm_process, tile_server
    # סגור את שרת OSRM
    if osrm_process:
        try:
            osrm_process.terminate()
            osrm_process.wait(timeout=5)
            print("שרת OSRM כובה.")
        except Exception:
            osrm_process.kill()
            print("שרת OSRM נהרג בכוח.")
    # סגור את שרת האריחים
    if tile_server:
        try:
            tile_server.shutdown()
            print("שרת האריחים כובה.")
        except Exception as e:
            print(f"שגיאה בכיבוי שרת האריחים: {e}")

def main():
    splash_path = f'file://{Path("splash.html").absolute()}'
    window = webview.create_window(
        'go\'maps',
        splash_path,
        width=1200,
        height=900,
        min_size=(800, 600),
        resizable=True
    )

    # הפעל שרת האריחים כ-thread (לא דמוני!)
    tile_server_thread = threading.Thread(target=run_tile_server)
    tile_server_thread.start()
    run_osrm_server()

    # חבר את האירוע של סגירת החלון
    window.events.closed += on_closed

    # טען את הדף הראשי
    html_path = f'file://{Path("index.html").absolute()}'
    def load_main(window):
        window.load_url(html_path)
    webview.start(load_main, window)

if __name__ == "__main__":
    main()
