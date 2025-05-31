from flask import Flask, request, jsonify
import requests
from datetime import datetime
import sys  # import sys to flush stdout

app = Flask(__name__)

def get_client_ip():
    # Try common headers for real client IP behind proxies
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()
    return ip

@app.route('/')
def index():
    return '''
        <h2>Consent to Logging Visitor Info</h2>
        <p>By clicking "Log Me," you consent to share your visitor info for testing.</p>
        <form action="/log" method="post">
            <button type="submit">Log Me</button>
        </form>
    '''

@app.route('/log', methods=['POST'])
def log_visitor():
    print(">>> /log route triggered <<<")
    sys.stdout.flush()

    visitor_ip = get_client_ip()
    user_agent = request.headers.get('User-Agent')
    referrer = request.referrer
    headers = dict(request.headers)
    query_params = request.args.to_dict()
    timestamp = datetime.utcnow().isoformat() + 'Z'

    # Optional: Get geolocation from free API
    geo_info = {}
    try:
        resp = requests.get(f'https://ipinfo.io/{visitor_ip}/json')
        if resp.status_code == 200:
            geo_info = resp.json()
    except Exception as e:
        geo_info = {"error": str(e)}

    # Log all info to console (Render logs)
    print(f"--- Visitor Logged at {timestamp} ---")
    print(f"IP: {visitor_ip}")
    print(f"User-Agent: {user_agent}")
    print(f"Referrer: {referrer}")
    print(f"Headers: {headers}")
    print(f"Query Params: {query_params}")
    print(f"GeoIP Info: {geo_info}")
    print("------------------------------")
    sys.stdout.flush()

    return jsonify({
        "message": "Visitor info logged with consent.",
        "ip": visitor_ip,
        "user_agent": user_agent,
        "referrer": referrer,
        "query_params": query_params,
        "geo_info": geo_info,
        "timestamp": timestamp
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

