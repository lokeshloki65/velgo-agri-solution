from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import os
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, auth, firestore
 
app = Flask(__name__) 
CORS(app)
app.secret_key = 'velgo_admin_secret_key_12345'

app.permanent_session_lifetime = timedelta(days=30)

try: 
    cred = credentials.Certificate('firebase-admin-sdk.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase Admin SDK Initialized Successfully.")
except ValueError:
    print("Firebase Admin SDK already initialized.")
    db = firestore.client()
except FileNotFoundError:
    print("CRITICAL ERROR: 'firebase-admin-sdk.json' not found.")
    db = None
except Exception as e:
    print(f"An error occurred during Firebase Admin initialization: {e}")
    db = None

# --- API Routes (Receiving data from frontend) ---
@app.route('/api/book', methods=['POST'])
def handle_booking():
    if not db: return jsonify({'status': 'error', 'message': 'Backend Firebase connection error.'}), 500
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer ' not in auth_header: return jsonify({'status': 'error', 'message': 'Authorization token required.'}), 401
        
        id_token = auth_header.split('Bearer ')[1]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        user_email = decoded_token.get('email', 'N/A')
        data = request.json
        
        # Add server-side data
        data.update({
            'timestamp': datetime.now(),
            'user_uid': uid,
            'user_email': user_email,
            'status': 'pending',
            'rejection_reason': None
        })
        db.collection('bookings').add(data)
        return jsonify({'status': 'success', 'message': 'Booking received!'})
    except auth.InvalidIdTokenError: return jsonify({'status': 'error', 'message': 'Invalid authentication token.'}), 403
    except Exception as e: print(f"Error in handle_booking: {e}"); return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/consult', methods=['POST'])
def handle_consultation():
    if not db: return jsonify({'status': 'error', 'message': 'Backend Firebase connection error.'}), 500
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or 'Bearer ' not in auth_header: return jsonify({'status': 'error', 'message': 'Authorization token required.'}), 401
        
        id_token = auth_header.split('Bearer ')[1]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        user_email = decoded_token.get('email', 'N/A')
        data = request.json
        
        # Add server-side data
        data.update({
            'timestamp': datetime.now(),
            'user_uid': uid,
            'user_email': user_email,
            'status': 'pending',
            'rejection_reason': None
        })
        db.collection('consultations').add(data)
        return jsonify({'status': 'success', 'message': 'Consultation request received!'})
    except auth.InvalidIdTokenError: return jsonify({'status': 'error', 'message': 'Invalid authentication token.'}), 403
    except Exception as e: print(f"Error in handle_consultation: {e}"); return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/update_status', methods=['POST'])
def update_status():
    if 'admin_logged_in' not in session: return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    if not db: return jsonify({'status': 'error', 'message': 'Backend Firebase connection error.'}), 500
    
    try:
        data = request.json
        doc_id = data.get('doc_id')
        collection_name = data.get('collection')
        new_status = data.get('new_status')
        reason = data.get('reason', None)

        if not doc_id or not collection_name or not new_status:
            return jsonify({'status': 'error', 'message': 'Missing doc_id, collection, or new_status'}), 400
            
        if new_status not in ['accepted', 'rejected', 'completed']:
             return jsonify({'status': 'error', 'message': 'Invalid status provided.'}), 400

        update_data = {
            'status': new_status,
            'status_updated_at': datetime.now()
        }
        
        if new_status == 'rejected':
            update_data['rejection_reason'] = reason if reason else "No reason provided."
        else:
            update_data['rejection_reason'] = None

        doc_ref = db.collection(collection_name).document(doc_id)
        doc_ref.update(update_data)
        
        return jsonify({'status': 'success', 'message': f'Status updated to {new_status}'})
        
    except Exception as e:
        print(f"Error in update_status: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin-auth', methods=['POST'])
def admin_auth():
    if not db: return jsonify({'status': 'error', 'message': 'Backend Firebase connection error.'}), 500
    try:
        data = request.json
        id_token = data.get('token')
        if not id_token: return jsonify({'status': 'error', 'message': 'No token provided.'}), 400
        
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        
        user_doc_ref = db.collection('users').document(uid)
        user_doc = user_doc_ref.get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()
            if user_data.get('role') == 'admin':
                session['admin_logged_in'] = True
                session['admin_email'] = user_data.get('email', decoded_token.get('email', 'Admin'))
                
                # --- (படி 1): Logout செய்ய வசதியாக, admin_uid-ஐயும் session-ல் சேமிக்கவும் ---
                session['admin_uid'] = uid 
                
                session.permanent = True
                
                print(f"Admin session created for: {session['admin_email']} (UID: {uid})")
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'error', 'message': 'Not an admin user.'}), 403
        else:
            return jsonify({'status': 'error', 'message': 'User record not found in Firestore.'}), 404
    except auth.InvalidIdTokenError: return jsonify({'status': 'error', 'message': 'Invalid token.'}), 403
    except Exception as e: print(f"Error in admin_auth: {e}"); return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/admin')
def admin():
    if 'admin_logged_in' not in session:
        print("Admin access denied. Not logged in. Redirecting to home.")
        return redirect(url_for('index'))
        
    if not db: return "Error: Cannot connect to Firestore. Check backend logs.", 500
    
    view = request.args.get('view', 'dashboard')
    services_list = ["Agri Consulting", "Soil Testing", "Crop Planning", "Livestock Integration", "AI & IoT Farming", "Farm Management"]
    data = []
    
    try:
        collection_name = ''
        query = None
        
        if view == 'consultations':
            collection_name = 'consultations'
            query = db.collection(collection_name).order_by('timestamp', direction=firestore.Query.DESCENDING)
        elif view in services_list:
            collection_name = 'bookings'
            query = db.collection(collection_name).where('service', '==', view).order_by('timestamp', direction=firestore.Query.DESCENDING)
            
        if query:
            docs = query.stream()
            for doc in docs:
                doc_data = doc.to_dict()
                doc_data['doc_id'] = doc.id
                data.append(doc_data)
                
    except Exception as e: print(f"Error fetching data for admin panel: {e}")
    
    return render_template('admin.html', current_view=view, data=data, services_list=services_list, admin_email=session.get('admin_email', 'Admin'))

# --- (படி 2): Logout செயல்பாட்டை முழுமையாகப் புதுப்பிக்கவும் ---
@app.route('/logout')
def logout():
    try:
        # Session-லிருந்து admin UID-ஐ எடுக்கவும் (session-ஐ அழிக்கும் முன்)
        admin_uid = session.get('admin_uid')
        if admin_uid:
            # இது Firebase Client-Side (index.html) login-ஐயும் அழித்துவிடும்
            auth.revoke_refresh_tokens(admin_uid)
            print(f"Successfully revoked Firebase tokens for UID: {admin_uid}")
        else:
            print("Could not find admin_uid in session to revoke tokens.")
    except Exception as e:
        # இந்த படி தோல்வியடைந்தாலும், Flask session-ஐ அழித்துவிட வேண்டும்
        print(f"WARNING: Could not revoke Firebase tokens. Error: {e}")
    
    # --- இப்போது Flask Server Session-ஐ அழிக்கவும் ---
    session.pop('admin_logged_in', None)
    session.pop('admin_email', None)
    session.pop('admin_uid', None) # admin_uid-ஐயும் session-லிருந்து நீக்கவும்
    session.permanent = False
    
    print("Admin Flask session cleared. Redirecting to home.")
    # முகப்புப் பக்கத்திற்குத் திருப்பி அனுப்புகிறது
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':

    app.run(debug=True)




