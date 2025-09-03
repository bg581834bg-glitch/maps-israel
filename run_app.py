import webview
import threading
import http.server
import socketserver
import os
from pathlib import Path
import subprocess

def run_tile_server():
    """הפעלת שרת סטטי לאריחי המפה"""
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"שרת האריחים פועל על פורט {PORT}")
        httpd.serve_forever()

def run_osrm_server():
    """OSRM הפעלת שרת"""
    try:
        osrm_path = Path("osrm")
        data_file = "israel-and-palestine-latest.osrm"
        
        if not (osrm_path / data_file).exists():
            print("שגיאה: קובץ הנתונים לא נמצא")
            return
            
        cmd = f"osrm-routed {data_file}"
        process = subprocess.Popen(cmd, shell=True, cwd=osrm_path)
        print("שרת OSRM הופעל")
        return process
    except Exception as e:
        print(f"שגיאה בהפעלת שרת OSRM: {e}")
        return None

def main():
    # הפעלת שרת האריחים ברקע
    tile_server_thread = threading.Thread(target=run_tile_server, daemon=True)
    tile_server_thread.start()
    
    # OSRM הפעלת שרת
    osrm_process = run_osrm_server()
    
    if osrm_process:
        try:
            # קביעת גודל החלון
            screen_width = webview.screens[0].width
            screen_height = webview.screens[0].height
            
            # חישוב גודל החלון (80% מגודל המסך)
            window_width = int(screen_width * 1.0)
            window_height = int(screen_height * 1.0)
            
            # חישוב מיקום החלון (ממורכז)
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            # יצירת חלון אפליקציה
            html_path = f'file://{Path("INDEX.html").absolute()}'
            window = webview.create_window(
                'go\'maps - ניווט ומפות ישראל',
                html_path,
                width=window_width,
                height=window_height,
                x=x,
                y=y,
                min_size=(800, 600),
                resizable=True
            )
            
            # הגדרות נוספות לחלון
            webview.start(debug=False)
            
        finally:
            print("\nסוגר את האפליקציה...")
            osrm_process.terminate()
            osrm_process.wait()
            print("האפליקציה נסגרה בהצלחה.")

if __name__ == "__main__":
    main()
