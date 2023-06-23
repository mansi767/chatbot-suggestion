from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

# Sample authorized users
authorized_users = {
    'admin': 'password123',
    'user1': 'pass456',
    'user2': 'secret789'
}

suggestions = []

def authenticate(username, password):
    return username in authorized_users and authorized_users[username] == password

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not authenticate(auth.username, auth.password):
            return jsonify({'message': 'Authentication required!'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/suggest', methods=['POST'])
@requires_auth
def suggest():
    data = request.json
    
    name = data.get('name')
    department = data.get('department')
    suggestion = data.get('suggestion')
    
    if name and department and suggestion:
        suggestions.append({
            'name': name,
            'department': department,
            'suggestion': suggestion
        })
    
        return jsonify({'message': 'Suggestion submitted successfully!'})
    else:
        return jsonify({'message': 'Invalid input data!'}), 400

@app.route('/suggestions', methods=['GET'])
@requires_auth
def get_suggestions():
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)
