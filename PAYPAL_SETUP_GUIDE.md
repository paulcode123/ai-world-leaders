# PayPal Donation Setup Guide

## Prerequisites
- PayPal Business Account (✅ You already have this!)
- Access to PayPal Developer Dashboard

## Step 1: Get Your PayPal API Credentials

1. Go to [PayPal Developer](https://developer.paypal.com/)
2. Log in with your PayPal business account
3. Click "Create App" in the Dashboard
4. Choose:
   - **App Name**: AI World Leaders Donations
   - **Merchant**: Your business account email
   - **Platform**: Web
   - **Product**: Checkout
5. Copy your **Client ID** (you'll need this)

## Step 2: Update Your Website Configuration

### Replace Placeholder Values

You need to update these files with your actual PayPal information:

#### 1. Update base.html
Find this line in `templates/base.html`:
```html
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_PAYPAL_CLIENT_ID&currency=USD&intent=capture"></script>
```

Replace `YOUR_PAYPAL_CLIENT_ID` with your actual Client ID from Step 1.

#### 2. Update donate.html
Find this line in `templates/donate.html`:
```html
<input type="hidden" name="business" value="YOUR_PAYPAL_EMAIL_HERE" />
```

Replace `YOUR_PAYPAL_EMAIL_HERE` with your PayPal business account email.

## Step 3: Test Your Integration

### Sandbox Testing (Recommended First)
1. Use PayPal's sandbox environment for testing
2. Replace the SDK URL with:
   ```html
   <script src="https://www.paypal.com/sdk/js?client-id=YOUR_SANDBOX_CLIENT_ID&currency=USD&intent=capture"></script>
   ```
3. Create sandbox accounts for testing donations

### Live Testing
1. Use your live Client ID
2. Test with small amounts first
3. Verify donations appear in your PayPal dashboard

## Step 4: Configure Webhooks (Optional but Recommended)

1. In PayPal Developer Dashboard, go to your app
2. Add webhook URL: `https://yourdomain.com/paypal-webhook`
3. Select events: `PAYMENT.CAPTURE.COMPLETED`
4. This will notify your server when donations are completed

## Step 5: Security Considerations

### Environment Variables (Recommended)
Instead of hardcoding your Client ID, use environment variables:

1. Create a `.env` file:
   ```
   PAYPAL_CLIENT_ID=your_actual_client_id_here
   PAYPAL_CLIENT_SECRET=your_client_secret_here
   ```

2. Update your Flask app to use environment variables:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
   ```

3. Pass it to your template:
   ```python
   @app.route('/donate')
   def donate():
       return render_template('donate.html', paypal_client_id=PAYPAL_CLIENT_ID)
   ```

4. Update base.html to use the variable:
   ```html
   <script src="https://www.paypal.com/sdk/js?client-id={{ paypal_client_id }}&currency=USD&intent=capture"></script>
   ```

## Step 6: Additional Features You Can Add

### Database Tracking
- Create a donations table to track all contributions
- Store donor information, amounts, and PayPal transaction IDs

### Email Notifications
- Send thank you emails to donors
- Notify yourself when donations are received

### Analytics
- Track donation patterns
- Generate reports for your records

## Current Features

Your donation system now includes:

✅ **Multiple Payment Options**: Advanced PayPal button + traditional donate button
✅ **Smart Amount Selection**: Click preset amounts or enter custom amounts
✅ **Donor Information Collection**: Names, email, and optional messages
✅ **Real-time Feedback**: Success/error messages after donation attempts
✅ **Mobile Responsive**: Works on all devices
✅ **Professional UI**: Matches your website's design

## Testing Checklist

Before going live, test:

- [ ] PayPal button loads correctly
- [ ] Amount selection works (preset and custom)
- [ ] Donation flow completes successfully
- [ ] Success messages appear
- [ ] Error handling works
- [ ] Traditional donate button works as fallback
- [ ] Mobile responsiveness
- [ ] Email notifications (if implemented)

## Support

If you encounter issues:
1. Check PayPal Developer Dashboard for error logs
2. Check browser console for JavaScript errors
3. Verify your Client ID is correct
4. Ensure your PayPal business account is verified

## Next Steps

1. Replace the placeholder values with your actual PayPal credentials
2. Test the donation flow
3. Go live and start accepting donations!

Your AI World Leaders mission can now receive secure donations through PayPal! 🎉 