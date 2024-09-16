from flask import Flask, jsonify, render_template, request
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Flask app
app = Flask(__name__)

# Firebase setup
cred = credentials.Certificate('firebase-adminsdk.json')  # The Firebase Admin SDK JSON file
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/coupon/<coupon_id>', methods=['GET', 'POST'])
def handle_coupon(coupon_id):
    doc_ref = db.collection('coupons').document(coupon_id)
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({"message": "Invalid coupon"}), 404

    coupon = doc.to_dict()

    # Check if coupon is already verified (used)
    if coupon['is_verified']:
        return jsonify({
            "message": "Coupon already used",
            "coupon_code": coupon['code'],
            "used_on": coupon['used_on']
        })

    if request.method == 'GET':
        # First scan (display coupon details)
        return jsonify({
            "message": "Valid coupon",
            "coupon_code": coupon['code'],
            "expiry_date": coupon['expiry_date'],
            "is_verified": coupon['is_verified']
        })

    if request.method == 'POST':
        data = request.get_json()

        # Step 1: Verify the coupon (verify flag is sent in POST)
        if 'verify' in data and data['verify'] == True:
            doc_ref.update({
                'is_verified': True,
                'used_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return jsonify({"message": "Coupon verified", "coupon_code": coupon['code']})

        # Step 2: Accept and store user details
        else:
            name = data.get('name')
            gender = data.get('gender')
            phone = data.get('phone')

            # Save user details in Firestore
            doc_ref.update({
                'user_name': name,
                'user_gender': gender,
                'user_phone': phone
            })

            return jsonify({"message": "User details saved", "coupon_code": coupon['code']})

if __name__ == '__main__':
    app.run(debug=True)
