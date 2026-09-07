import http.server
import socketserver
import subprocess
import json
import os
import sys
import threading
from datetime import datetime

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE = sys.executable

is_scraping = False
scrape_lock = threading.Lock()

class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_POST(self):
        global is_scraping
        if self.path == '/api/scrape':
            with scrape_lock:
                if is_scraping:
                    self.send_response(429)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "busy", "message": "Un scraping est déjà en cours..."}, ensure_ascii=False).encode('utf-8'))
                    return
                is_scraping = True

            try:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Web scraping button triggered via /api/scrape...", flush=True)
                
                # 1. Run build_verified_database.py
                p1 = subprocess.run([PYTHON_EXE, os.path.join(BASE_DIR, "scraper", "build_verified_database.py")], capture_output=True, text=True, cwd=BASE_DIR)
                
                # 2. Run verify_all_links.py
                p2 = subprocess.run([PYTHON_EXE, os.path.join(BASE_DIR, "scraper", "verify_all_links.py")], capture_output=True, text=True, cwd=BASE_DIR)
                
                # Count current jobs
                jobs_path = os.path.join(BASE_DIR, "data", "jobs.json")
                count = 0
                if os.path.exists(jobs_path):
                    with open(jobs_path, "r", encoding="utf-8") as f:
                        count = len(json.load(f))

                from datetime import timezone
                now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                meta_path = os.path.join(BASE_DIR, "data", "meta.json")
                meta = {}
                if os.path.exists(meta_path):
                    try:
                        with open(meta_path, "r", encoding="utf-8") as f:
                            meta = json.load(f)
                    except Exception:
                        pass
                meta["total"] = count
                meta["last_scraped_at"] = now_iso
                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(meta, f, ensure_ascii=False, indent=2)

                print(f"[{datetime.now().strftime('%H:%M:%S')}] Scraping completed successfully! {count} jobs active.", flush=True)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "jobs_count": count,
                    "last_scraped_at": now_iso,
                    "timestamp": now_iso,
                    "message": f"Scraping terminé avec succès ! {count} stages M2 vérifiés et à jour."
                }, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                print(f"[ERROR] Scraping error: {e}", flush=True)
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False).encode('utf-8'))
            finally:
                with scrape_lock:
                    is_scraping = False
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHTTPHandler) as httpd:
        print(f"Server started at http://localhost:{PORT} with /api/scrape support", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.", flush=True)
