from flask import Flask, request, jsonify, render_template
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant


app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/token')
def generate_token():
    #add your twilio credentials 
    TWILIO_ACCOUNT_SID = 'AC80414424bd5f2bbcc46060d74f787d49'
    TWILIO_SYNC_SERVICE_SID = 'IS40888ed63285b482648ee237c5b8aac1'
    TWILIO_API_KEY = 'SKa07cf6cc3c644e4db24a13630434312c'
    TWILIO_API_SECRET = 'A7tdiQxtlHNM4sCerR7KqE6zuLv0SWx5'

    username = request.args.get('username', fake.user_name())
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

@app.route('/', methods=["POST"])
def download_text():
    text_from_notepad = request.form['text']
    with open('workfile.txt', 'w') as f:
        f.write(text_from_notepad)

    path_to_store_txt = "workfile.txt"
    
    return send_file(path_to_store_txt, as_attachment=True)    

if __name__ == "__main__":
    app.run(port=5001)

