import sqlite3
import json
from datetime import datetime
import os

DATABASE_PATH = 'donations.db'

def init_database():
    """Initialize the donations database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            message TEXT,
            amount REAL NOT NULL,
            paypal_transaction_id TEXT UNIQUE,
            paypal_payer_email TEXT,
            donation_type TEXT DEFAULT 'oneTime',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def save_donation(donation_data):
    """Save a donation to the database"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO donations 
            (first_name, last_name, email, message, amount, paypal_transaction_id, paypal_payer_email, donation_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            donation_data.get('first_name', ''),
            donation_data.get('last_name', ''),
            donation_data.get('email', ''),
            donation_data.get('message', ''),
            float(donation_data.get('amount', 0)),
            donation_data.get('transaction_id', ''),
            donation_data.get('payer_email', ''),
            donation_data.get('donation_type', 'oneTime')
        ))
        
        conn.commit()
        donation_id = cursor.lastrowid
        conn.close()
        
        print(f"Donation saved successfully with ID: {donation_id}")
        return donation_id
        
    except sqlite3.IntegrityError:
        print(f"Donation with transaction ID {donation_data.get('transaction_id')} already exists")
        return None
    except Exception as e:
        print(f"Error saving donation: {str(e)}")
        return None

def get_all_donations():
    """Get all donations from the database"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, first_name, last_name, email, message, amount, 
                   paypal_transaction_id, paypal_payer_email, donation_type, created_at
            FROM donations 
            ORDER BY created_at DESC
        ''')
        
        donations = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        donation_list = []
        for donation in donations:
            donation_list.append({
                'id': donation[0],
                'first_name': donation[1],
                'last_name': donation[2],
                'email': donation[3],
                'message': donation[4],
                'amount': donation[5],
                'paypal_transaction_id': donation[6],
                'paypal_payer_email': donation[7],
                'donation_type': donation[8],
                'created_at': donation[9]
            })
        
        return donation_list
        
    except Exception as e:
        print(f"Error retrieving donations: {str(e)}")
        return []

def get_donation_stats():
    """Get basic donation statistics"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Total donations and amount
        cursor.execute('SELECT COUNT(*), SUM(amount) FROM donations')
        count, total = cursor.fetchone()
        
        # Average donation
        cursor.execute('SELECT AVG(amount) FROM donations')
        average = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_donations': count or 0,
            'total_amount': total or 0,
            'average_donation': round(average or 0, 2)
        }
        
    except Exception as e:
        print(f"Error getting donation stats: {str(e)}")
        return {'total_donations': 0, 'total_amount': 0, 'average_donation': 0}

def backup_donations_to_json():
    """Create a JSON backup of all donations"""
    try:
        donations = get_all_donations()
        stats = get_donation_stats()
        
        backup_data = {
            'backup_date': datetime.now().isoformat(),
            'stats': stats,
            'donations': donations
        }
        
        backup_filename = f'donations_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(backup_filename, 'w') as f:
            json.dump(backup_data, f, indent=2, default=str)
        
        print(f"Backup created: {backup_filename}")
        return backup_filename
        
    except Exception as e:
        print(f"Error creating backup: {str(e)}")
        return None

# Initialize database when module is imported
if __name__ == "__main__":
    init_database() 