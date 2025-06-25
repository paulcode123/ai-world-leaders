#!/usr/bin/env python3
"""
Test script to verify AI World Leaders website setup
Run this before deploying to Railway
"""

import sys
import os
import sqlite3
from database import init_database, save_donation, get_all_donations, get_donation_stats

def test_database():
    """Test database functionality"""
    print("🧪 Testing database...")
    
    try:
        # Initialize database
        init_database()
        print("✅ Database initialized")
        
        # Test saving a donation
        test_donation = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'message': 'This is a test donation',
            'amount': 25.00,
            'transaction_id': 'TEST123456',
            'payer_email': 'testpayer@example.com',
            'donation_type': 'oneTime'
        }
        
        donation_id = save_donation(test_donation)
        if donation_id:
            print("✅ Test donation saved successfully")
        else:
            print("❌ Failed to save test donation")
            return False
        
        # Test retrieving donations
        donations = get_all_donations()
        if donations and len(donations) > 0:
            print(f"✅ Retrieved {len(donations)} donation(s)")
        else:
            print("❌ No donations found")
            return False
        
        # Test stats
        stats = get_donation_stats()
        print(f"✅ Stats: {stats['total_donations']} donations, ${stats['total_amount']:.2f} total")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

def test_flask_app():
    """Test Flask app imports and routes"""
    print("\n🧪 Testing Flask app...")
    
    try:
        # Test imports
        from app import app
        print("✅ Flask app imports successfully")
        
        # Test app context
        with app.app_context():
            from flask import url_for
            
            # Test route generation
            routes = [
                ('home', '/'),
                ('about', '/about'),
                ('donate', '/donate'),
                ('contact', '/contact'),
                ('admin_donations', '/admin/donations'),
                ('export_donations', '/admin/donations/export'),
                ('backup_donations', '/admin/donations/backup'),
                ('donation_success', '/donation-success')
            ]
            
            for route_name, expected_path in routes:
                try:
                    path = url_for(route_name)
                    print(f"✅ Route '{route_name}': {path}")
                except Exception as e:
                    print(f"❌ Route '{route_name}' failed: {str(e)}")
                    return False
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {str(e)}")
        return False

def test_files():
    """Test required files exist"""
    print("\n🧪 Testing required files...")
    
    required_files = [
        'app.py',
        'database.py',
        'requirements.txt',
        'Procfile',
        'railway.json',
        'templates/base.html',
        'templates/donate.html',
        'templates/admin_donations.html',
        'static/js/script.js',
        'static/css/style.css'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_paypal_config():
    """Test PayPal configuration"""
    print("\n🧪 Testing PayPal configuration...")
    
    try:
        # Check base.html for PayPal SDK
        with open('templates/base.html', 'r') as f:
            base_content = f.read()
        
        if 'paypal.com/sdk/js' in base_content:
            print("✅ PayPal SDK found in base.html")
        else:
            print("❌ PayPal SDK not found in base.html")
            return False
        
        if 'YOUR_PAYPAL_CLIENT_ID' in base_content:
            print("⚠️  Warning: PayPal Client ID placeholder not replaced")
        else:
            print("✅ PayPal Client ID appears to be configured")
        
        # Check donate.html for PayPal email
        with open('templates/donate.html', 'r') as f:
            donate_content = f.read()
        
        if 'YOUR_PAYPAL_EMAIL_HERE' in donate_content:
            print("❌ PayPal email placeholder not replaced")
            return False
        else:
            print("✅ PayPal email appears to be configured")
        
        return True
        
    except Exception as e:
        print(f"❌ PayPal config test failed: {str(e)}")
        return False

def cleanup_test_data():
    """Clean up test data"""
    try:
        # Remove test donation
        conn = sqlite3.connect('donations.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM donations WHERE paypal_transaction_id = 'TEST123456'")
        conn.commit()
        conn.close()
        print("✅ Test data cleaned up")
    except Exception as e:
        print(f"⚠️  Could not clean up test data: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 AI World Leaders Website Setup Test")
    print("=" * 50)
    
    tests = [
        ("Files", test_files),
        ("Database", test_database),
        ("Flask App", test_flask_app),
        ("PayPal Config", test_paypal_config)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All tests passed! Ready for Railway deployment 🚀")
        cleanup_test_data()
        return 0
    else:
        print("❌ Some tests failed. Please fix issues before deploying.")
        cleanup_test_data()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 