from flask import Flask, request, make_response
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# Establish MongoDB connection
client = MongoClient('mongodb://mongo:27017/')
db = client['test']
access_log = db['access_log']

# Global counter
counter = 0

@app.route('/')
def index():
    global counter
    # Increment the global counter
    counter += 1

    # Save log to MongoDB
    log_entry = {
        'date_time': datetime.datetime.now(),
        'client_ip': request.remote_addr,
        'internal_ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    }
    access_log.insert_one(log_entry)

    # Create a cookie for 5 minutes with the value of the internal IP
    resp = make_response('Internal IP Address: ' + request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    resp.set_cookie('internal_ip', request.environ.get('HTTP_X_REAL_IP', request.remote_addr), max_age=300)
    return resp

@app.route('/showcount')
def show_count():
    global counter
    return 'Global Counter: ' + str(counter)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
