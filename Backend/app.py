from flask import Flask, request, jsonify
import os
import redis
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Redis configuration from environment variables
redis_hash = {
    "url": os.getenv("UPSTASH_REDIS_REST_URL"),
    "token": os.getenv("UPSTASH_REDIS_REST_TOKEN"),
    "PORT": int(os.getenv("PORT"))
}

# Create connectivity to the Redis server
def redis_connect():
    try:
        client = redis.Redis(
            host=redis_hash["url"],
            port=redis_hash["PORT"],
            password=redis_hash["token"],
            db=0,
            socket_timeout=5,
            ssl=True  # Use SSL for secure connection
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)

# Create client
redis_client = redis_connect()

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username or password is missing'}), 400
    
    username = data['username']
    password = data['password']
    try:
        stored_password = redis_client.get(username)
        if stored_password and stored_password.decode('utf-8') == password:
            return jsonify({'message': 'Authentication successful'}) # Add redirection later
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except redis.RedisError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'error': 'Email is missing'}), 400

    email = data['email']
    waitlist_file = 'waitlist.json'

    if os.path.exists(waitlist_file):
        with open(waitlist_file, 'r+') as file:
            try:
                waitlist = json.load(file)
            except json.JSONDecodeError:
                waitlist = []
    else:
        waitlist = []

    # Append the new email to the waitlist
    waitlist.append(email)

    # Write the updated waitlist back to the file
    with open(waitlist_file, 'w') as file:
        json.dump(waitlist, file, indent=4)

    return jsonify({'message': 'Email registered successfully'})

# Main driver function
if __name__ == '__main__':
    app.run()
