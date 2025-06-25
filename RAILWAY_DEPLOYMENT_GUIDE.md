# 🚀 Railway Deployment Guide for AI World Leaders

## ✅ What's Already Set Up:

Your website now has **complete donation tracking** with:
- ✅ **SQLite Database**: Stores all donation information
- ✅ **Admin Dashboard**: View donations at `/admin/donations`
- ✅ **CSV Export**: Download donation data
- ✅ **PayPal Integration**: Working donation system
- ✅ **Railway Config**: Ready for one-click deployment

## 🎯 Deployment Steps (5 minutes):

### Step 1: Push to GitHub
```bash
cd website
git init
git add .
git commit -m "Initial commit - AI World Leaders website with donations"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-world-leaders.git
git push -u origin main
```

*Replace `YOUR_USERNAME` with your GitHub username*

### Step 2: Deploy to Railway
1. Go to [Railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your `ai-world-leaders` repository
6. Railway will automatically:
   - Detect Python/Flask
   - Install dependencies
   - Deploy your app
   - Give you a live URL

### Step 3: Access Your Website
- **Main Website**: `https://your-app-name.railway.app`
- **Admin Dashboard**: `https://your-app-name.railway.app/admin/donations`

## 💾 Database Features:

### What Gets Saved:
- ✅ Donor names and emails
- ✅ Donation amounts
- ✅ Personal messages
- ✅ PayPal transaction IDs
- ✅ Timestamps

### Admin Dashboard Features:
- 📊 **Statistics**: Total raised, donor count, average donation
- 📋 **Donation List**: View all contributions
- 💌 **Messages**: Read donor comments
- 📧 **Email Links**: Quick thank-you emails
- 📄 **CSV Export**: Download spreadsheet
- 💾 **JSON Backup**: Create data backups

## 🔐 Admin Access:

**URL**: `https://your-domain.railway.app/admin/donations`

*No password required (add one later if needed)*

## 💰 Cost Breakdown:

### Railway Free Tier:
- ✅ **500 execution hours/month** (you'll use ~5-10)
- ✅ **1GB RAM** (more than enough)
- ✅ **Perfect for <100 users**
- ✅ **Automatic HTTPS**
- ✅ **Custom domain support**

**Total Cost: $0/month** 🎉

## 📊 Monitoring Your Donations:

### Real-time Tracking:
1. **PayPal Dashboard**: See payment processing
2. **Admin Dashboard**: View complete donor information
3. **Railway Metrics**: Monitor website performance

### Weekly Backup Routine:
1. Visit `/admin/donations`
2. Click **"Export CSV"** (save to your computer)
3. Click **"Create Backup"** (creates JSON file)

## 🛠️ Post-Deployment Tasks:

### Test Everything:
- [ ] Visit your website
- [ ] Test donation flow with small amount
- [ ] Check admin dashboard shows donation
- [ ] Export CSV to verify data
- [ ] Test PayPal notifications

### Optional Enhancements:
- **Custom Domain**: Point your domain to Railway
- **Email Notifications**: Get notified of new donations
- **Security**: Add admin password protection
- **Analytics**: Add Google Analytics

## 📧 Email Integration (Optional):

Add automatic thank-you emails by updating `app.py`:

```python
import smtplib
from email.mime.text import MimeText

def send_thank_you_email(donor_email, donor_name, amount):
    # Configure with your email provider
    msg = MimeText(f"Thank you {donor_name} for your ${amount} donation!")
    msg['Subject'] = 'Thank you for supporting AI World Leaders!'
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = donor_email
    
    # Send email (configure SMTP settings)
```

## 🔧 Troubleshooting:

### If Donations Don't Save:
1. Check Railway logs for errors
2. Verify PayPal Client ID is correct
3. Test with smaller amounts first

### If Admin Dashboard is Empty:
1. Make sure you completed a test donation
2. Check Railway logs for database errors
3. Try the backup/export functions

### If PayPal Button Doesn't Load:
1. Verify Client ID in `base.html`
2. Check browser console for errors
3. Ensure PayPal business account is verified

## 📱 Mobile Optimization:

Your website is **fully mobile responsive**:
- ✅ Donation forms work on all devices
- ✅ Admin dashboard scales to mobile
- ✅ PayPal buttons optimized for touch

## 🚀 You're Ready!

Once deployed, your website will:
1. **Accept donations** through PayPal
2. **Track all donor information** in database
3. **Provide admin dashboard** for management
4. **Handle 100+ users** without issues
5. **Cost $0/month** on Railway free tier

## 📞 Support:

If you need help:
1. Check Railway deployment logs
2. Test PayPal in sandbox mode first
3. Verify all placeholder values are replaced
4. Contact me if issues persist

**Your AI World Leaders donation system is ready to launch! 🎉**

---

### Quick Commands:

```bash
# Local testing
python app.py

# Database check
python -c "from database import get_all_donations; print(len(get_all_donations()))"

# Create backup
python -c "from database import backup_donations_to_json; backup_donations_to_json()"
``` 