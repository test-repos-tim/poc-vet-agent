#!/usr/bin/env python3
"""
bridge/http_server.py — Zero-dependency HTTP server for vet agent.
Runs on localhost:5000. Uses only stdlib (http.server, json, sqlite3).
Handles both GET and POST for /chat endpoint.
"""
import json
import sqlite3
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

KB_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'vet_knowledge_base.json')
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'vet_agent.db')

with open(KB_PATH) as f:
    KB = json.load(f)

def reply(msg):
    m = msg.lower()
    for faq in KB['faqs']:
        if any(word in m for word in faq['question'].lower().split()):
            return faq['answer']
    if any(w in m for w in ['hello','hi','hey']): return 'Hello! How can I help with your pet?'
    if 'appoint' in m or 'book' in m or 'schedule' in m: return 'Please provide pet name, species, preferred date/time, and reason.'
    if 'emergency' in m or 'urgent' in m: return 'Call (555) 123-4567 immediately for emergencies.'
    if 'prescription' in m or 'refill' in m: return 'Provide pet name, medication, dosage, pharmacy contact.'
    if 'hour' in m or 'open' in m or 'time' in m: return 'Mon-Fri 8am-8pm, Sat 9am-5pm, Sun Closed.'
    return 'I can help with appointments, hours, prescriptions. Call (555) 123-4567 for urgent needs.'

class Handler(BaseHTTPRequestHandler):
    def _handle_chat(self):
        """Shared handler for GET and POST — extracts message from either method."""
        msg = ''
        if self.command == 'POST':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            try:
                data = json.loads(body)
                msg = data.get('message', '')
            except:
                msg = body
        else:  # GET
            parsed = urlparse(self.path)
            qs = parse_qs(parsed.query)
            msg = qs.get('message', [''])[0]
            if not msg:
                # Fallback: try query string as plain text
                msg = parsed.query

        if not msg:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'No message provided'}).encode())
            return

        bot = reply(msg)
        # Log to SQLite
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO conversations (session_id, user_message, bot_response, timestamp) VALUES (?, ?, ?, ?)",
                         ("default", msg, bot, datetime.now().isoformat()))
            conn.commit(); conn.close()
        except Exception:
            pass

        resp = json.dumps({"reply": bot}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(resp)

    def do_POST(self):
        path = urlparse(self.path).path
        if path == '/chat':
            self._handle_chat()
        else:
            self.send_response(404); self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/chat':
            self._handle_chat()
        else:
            self.send_response(404); self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, fmt, *args):
        pass  # Suppress default logging

if __name__ == '__main__':
    srv = HTTPServer(('0.0.0.0', 5000), Handler)
    print('Vet Agent Bridge running on http://localhost:5000/chat (GET + POST)')
    srv.serve_forever()