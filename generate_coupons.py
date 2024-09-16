import random
import string
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def generate_coupon_code(length=8):
    """Generate a random coupon code consisting of uppercase letters and digits."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

def store_coupons(num_coupons):
    """Store generated coupons in Firestore."""
    for i in range(num_coupons):
        coupon_code = generate_coupon_code()
        # Store each coupon in Firestore
        coupon_data = {
            'code': coupon_code,
            'expiry_date': '2024-12-31',  # Set expiry date for the coupon
            'is_verified': False,  # Initially not verified
            'used_on': None,  # No date when used yet
        }
        db.collection('coupons').add(coupon_data)
        print(f"Coupon {i+1}: {coupon_code} added to Firestore")

if __name__ == "__main__":
    store_coupons(155)  # Generate and store 155 coupons
