import psycopg2
import psycopg2.extras
import json
from datetime import datetime
import os

def get_db_connection():
    """Get database connection using Railway environment variables"""
    # Railway provides these automatically when you add PostgreSQL
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Use DATABASE_URL if available (Railway format)
        return psycopg2.connect(database_url, sslmode='require')
    else:
        # Fallback to individual environment variables
        return psycopg2.connect(
            host=os.getenv('PGHOST', 'localhost'),
            port=os.getenv('PGPORT', 5432),
            database=os.getenv('PGDATABASE', 'donations'),
            user=os.getenv('PGUSER', 'postgres'),
            password=os.getenv('PGPASSWORD', ''),
            sslmode='require'
        )

def init_database():
    """Initialize the donations database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS donations (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                email VARCHAR(255),
                message TEXT,
                amount DECIMAL(10,2) NOT NULL,
                paypal_transaction_id VARCHAR(255) UNIQUE,
                paypal_payer_email VARCHAR(255),
                donation_type VARCHAR(50) DEFAULT 'oneTime',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for better performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_donations_created_at 
            ON donations(created_at DESC)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_donations_transaction_id 
            ON donations(paypal_transaction_id)
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("PostgreSQL database initialized successfully")
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

def save_donation(donation_data):
    """Save a donation to the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO donations 
            (first_name, last_name, email, message, amount, paypal_transaction_id, paypal_payer_email, donation_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
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
        
        donation_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Donation saved successfully with ID: {donation_id}")
        return donation_id
        
    except psycopg2.IntegrityError:
        print(f"Donation with transaction ID {donation_data.get('transaction_id')} already exists")
        if conn:
            conn.rollback()
            cursor.close()
            conn.close()
        return None
    except Exception as e:
        print(f"Error saving donation: {str(e)}")
        if conn:
            conn.rollback()
            cursor.close()
            conn.close()
        return None

def get_all_donations():
    """Get all donations from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute('''
            SELECT id, first_name, last_name, email, message, amount, 
                   paypal_transaction_id, paypal_payer_email, donation_type, created_at
            FROM donations 
            ORDER BY created_at DESC
        ''')
        
        donations = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convert to list of dictionaries for compatibility
        donation_list = []
        for donation in donations:
            donation_dict = dict(donation)
            # Convert datetime to string for JSON serialization
            if donation_dict['created_at']:
                donation_dict['created_at'] = donation_dict['created_at'].isoformat()
            donation_list.append(donation_dict)
        
        return donation_list
        
    except Exception as e:
        print(f"Error retrieving donations: {str(e)}")
        return []

def get_donation_stats():
    """Get basic donation statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total donations and amount
        cursor.execute('SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM donations')
        count, total = cursor.fetchone()
        
        # Average donation
        cursor.execute('SELECT COALESCE(AVG(amount), 0) FROM donations WHERE amount > 0')
        average = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return {
            'total_donations': count or 0,
            'total_amount': float(total or 0),
            'average_donation': round(float(average or 0), 2)
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

def test_database_connection():
    """Test database connection and return status"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return True, "Database connection successful"
    except Exception as e:
        return False, f"Database connection failed: {str(e)}"

# Only initialize database when explicitly called
if __name__ == "__main__":
    init_database() 