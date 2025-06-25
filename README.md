# AI World Leaders Website

A modern, responsive website for AI World Leaders - a non-profit organization founded by Paul Nieuwerburgh and Rylin Reitz to democratize AI education in developing countries.

## 🚀 Features

- **Modern Design**: Beautiful, responsive design with animations and smooth transitions
- **Multiple Pages**: Home, About Us, Donate, and Contact pages
- **Interactive Elements**: Animated counters, smooth scrolling, and hover effects
- **Donation System**: Ready for PayPal integration (currently shows placeholder)
- **Contact Form**: Functional contact form with form validation
- **Mobile Responsive**: Optimized for all device sizes
- **Performance Optimized**: Fast loading with modern web technologies

## 🛠 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Framework**: Bootstrap 5.3
- **Icons**: Font Awesome 6.4
- **Fonts**: Google Fonts (Inter & Space Grotesk)
- **Animations**: CSS animations and JavaScript interactions

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🔧 Installation & Setup

1. **Clone or navigate to the project directory**:
   ```bash
   cd AIWL
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Website

1. **Start the Flask development server**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. **The website should now be running locally!**

## 📁 Project Structure

```
AIWL/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── info.md               # Organization information
├── website.md            # Website specifications
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Home page
│   ├── about.html        # About Us page
│   ├── donate.html       # Donation page
│   └── contact.html      # Contact page
└── static/               # Static files
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── script.js     # Custom JavaScript
```

## 🎨 Key Features

### Home Page
- Hero section with animated background
- Mission statement and vision
- Cameroon project overview
- Call-to-action sections

### About Us Page
- Founder profiles (Paul & Rylin)
- Story timeline
- Vision and goals
- Achievement statistics

### Donate Page
- Interactive donation amount selection
- Donor information form
- PayPal integration placeholder
- Impact explanation
- FAQ section

### Contact Page
- Contact form with validation
- Contact information
- Social media links
- FAQ section

## 🎭 Interactive Features

- **Smooth Scrolling**: Navigation links smoothly scroll to sections
- **Animated Counters**: Numbers animate when scrolled into view
- **Hover Effects**: Cards lift and transform on hover
- **Responsive Navigation**: Mobile-friendly collapsible menu
- **Form Interactions**: Interactive donation amount selection
- **Loading States**: Buttons show loading states during form submission

## 🎨 Design Elements

- **Gradient Backgrounds**: Beautiful gradient overlays
- **Modern Cards**: Clean card designs with shadows and borders
- **Typography**: Modern font combinations (Inter + Space Grotesk)
- **Color Scheme**: Professional blue and purple gradient theme
- **Animations**: Subtle animations throughout the site
- **Icons**: Font Awesome icons for visual appeal

## 🔧 Customization

### Colors
Edit the CSS custom properties in `static/css/style.css`:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    --accent-color: #06b6d4;
    /* ... other colors */
}
```

### Content
- Edit content in the HTML templates in the `templates/` folder
- Update organization information in `info.md`
- Modify the Flask routes in `app.py` as needed

### Styling
- Add custom styles to `static/css/style.css`
- Modify JavaScript interactions in `static/js/script.js`

## 🚀 Deployment

For production deployment, consider:

1. **Set a secure secret key** in `app.py`
2. **Use a production WSGI server** like Gunicorn
3. **Set up SSL certificates** for HTTPS
4. **Configure environment variables** for sensitive data
5. **Set up PayPal integration** when non-profit status is approved

## 📧 Contact Information

- **Organization**: AI World Leaders
- **Founders**: Paul Nieuwerburgh & Rylin Reitz
- **Location**: Bronx, New York
- **Mission**: Democratizing AI education in developing countries

## 🎯 Mission Statement

At AI World Leaders, we believe that artificial intelligence has the power to revolutionize education and innovation across the globe. Our mission is to break down barriers and provide students in developing countries with the tools, knowledge, and inspiration they need to become leaders in the AI revolution.

## 🌍 Cameroon Project

Our inaugural project involves a 5-day AI workshop in Cameroon for 100 students, where we'll provide:
- Comprehensive AI education
- Hands-on learning experiences
- 15 AI-capable laptops for students to keep
- Ongoing support and resources

---

**Built with ❤️ for democratizing AI education worldwide** 