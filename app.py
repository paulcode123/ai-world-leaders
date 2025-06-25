from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, make_response
import csv
import io
import os
from dotenv import load_dotenv
from database import init_database, save_donation, get_all_donations, get_donation_stats, backup_donations_to_json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Use environment variables for security
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'ai-world-leaders-fallback-key')

# Get PayPal Client ID from environment
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID', '')

# Initialize database on startup
init_database()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/donate')
def donate():
    return render_template('donate.html', paypal_client_id=PAYPAL_CLIENT_ID)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Here you would typically save to database or send email
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/donation-success', methods=['POST'])
def donation_success():
    try:
        data = request.get_json()
        paypal_details = data.get('paypal_details', {})
        donor_info = data.get('donor_info', {})
        
        # Prepare donation data for database
        donation_data = {
            'first_name': donor_info.get('firstName', ''),
            'last_name': donor_info.get('lastName', ''),
            'email': donor_info.get('email', ''),
            'message': donor_info.get('message', ''),
            'amount': float(data.get('amount', 0)),
            'transaction_id': paypal_details.get('id', ''),
            'payer_email': paypal_details.get('payer', {}).get('email_address', ''),
            'donation_type': 'oneTime'  # Can be extended for recurring
        }
        
        # Save to database
        donation_id = save_donation(donation_data)
        
        if donation_id:
            print(f"Donation saved: ${donation_data['amount']} from {donation_data['first_name']} {donation_data['last_name']}")
            return jsonify({'status': 'success', 'message': 'Donation recorded successfully', 'donation_id': donation_id})
        else:
            return jsonify({'status': 'warning', 'message': 'Donation processed but may be duplicate'})
            
    except Exception as e:
        print(f"Error processing donation: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Failed to record donation'}), 500

@app.route('/admin/donations')
def admin_donations():
    """Admin page to view all donations"""
    donations = get_all_donations()
    stats = get_donation_stats()
    return render_template('admin_donations.html', donations=donations, stats=stats)

@app.route('/admin/donations/export')
def export_donations():
    """Export donations to CSV"""
    donations = get_all_donations()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Amount', 'Message', 'PayPal Transaction ID', 'PayPal Email', 'Date'])
    
    # Write data
    for donation in donations:
        writer.writerow([
            donation['id'],
            donation['first_name'],
            donation['last_name'],
            donation['email'],
            f"${donation['amount']:.2f}",
            donation['message'],
            donation['paypal_transaction_id'],
            donation['paypal_payer_email'],
            donation['created_at']
        ])
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=donations_export.csv'
    
    return response

@app.route('/admin/donations/backup')
def backup_donations():
    """Create JSON backup of donations"""
    filename = backup_donations_to_json()
    if filename:
        flash(f'Backup created successfully: {filename}', 'success')
    else:
        flash('Failed to create backup', 'error')
    return redirect(url_for('admin_donations'))

if __name__ == '__main__':
    app.run(debug=True) 