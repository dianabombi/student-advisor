# Admin Panel User Guide

**Student Platform - Administrator Documentation**

Version 1.0 | Last Updated: February 2026

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Dashboard Overview](#2-dashboard-overview)
3. [User Management](#3-user-management)
4. [Universities Management](#4-universities-management)
5. [Analytics & Reports](#5-analytics--reports)
6. [System Settings](#6-system-settings)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Getting Started

### 1.1 Accessing the Admin Panel

**URL:** `http://localhost:3000/auth/login` (or your production domain)

**Default Admin Credentials:**
- **Email:** `admin@student.com`
- **Password:** `Admin123!`

> ⚠️ **Security Note:** Change the default password immediately after first login!

### 1.2 Login Process

1. Navigate to the login page
2. Enter your admin email address
3. Enter your password
4. Click **"Login"** button
5. You will be redirected to the Admin Dashboard

```
┌─────────────────────────────────┐
│   Student Platform Login        │
├─────────────────────────────────┤
│ Email:    [admin@student.com  ] │
│ Password: [••••••••••••••••••] │
│                                 │
│         [  Login  ]             │
└─────────────────────────────────┘
```

### 1.3 First Time Setup

After logging in for the first time:

1. ✅ Verify dashboard loads correctly
2. ✅ Check that statistics are displaying
3. ✅ Navigate to **Settings** and configure:
   - Platform name
   - Support email
   - OpenAI API key (if using AI features)
4. ✅ Review existing users and universities

---

## 2. Dashboard Overview

The Dashboard is your central hub for monitoring platform activity.

### 2.1 Statistics Cards

At the top of the dashboard, you'll see 4 key metrics:

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Total Users  │ Universities │Consultations │  Documents   │
│    1,234     │     156      │    3,456     │    2,890     │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

**What each metric means:**
- **Total Users:** Number of registered users on the platform
- **Universities:** Total universities in the database
- **Consultations:** Total AI consultations performed
- **Documents:** Total documents uploaded by users

### 2.2 User Growth Chart

**Purpose:** Visualize user registration trends over time

**Features:**
- **Period Selection:** Choose from:
  - 30 Days (last month)
  - 3 Months (quarterly view)
  - 1 Year (annual view)
  - All Time (complete history)
- **Interactive:** Hover over data points to see exact numbers
- **Auto-refresh:** Updates when you change the period

```
User Growth Chart
┌─────────────────────────────────────────┐
│ [30 Days] [3 Months] [1 Year] [All Time]│
├─────────────────────────────────────────┤
│                                    ╱    │
│                               ╱╲  ╱     │
│                          ╱╲  ╱  ╲╱      │
│                     ╱╲  ╱  ╲╱           │
│ ────────────────╱──╲╱─────────────────  │
│ Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  │
└─────────────────────────────────────────┘
```

**Use Cases:**
- Monitor user acquisition trends
- Identify growth spikes or drops
- Plan marketing campaigns based on patterns

### 2.3 Recent Activity Feed

**Purpose:** Real-time view of user actions on the platform

**Displays:**
- Last 10 user activities
- Activity type (registration, consultation, document upload, etc.)
- User email
- Timestamp (e.g., "5 min ago")

```
Recent Activity
┌─────────────────────────────────────────┐
│ 👤 New user registered                  │
│    user@example.com • 2 min ago         │
├─────────────────────────────────────────┤
│ 💬 Consultation started                 │
│    student@uni.com • 15 min ago         │
├─────────────────────────────────────────┤
│ 📄 Document uploaded                    │
│    john@email.com • 1 hour ago          │
└─────────────────────────────────────────┘
```

**Features:**
- **Auto-refresh:** Updates every 30 seconds
- **Color-coded icons:** Different colors for different activity types
- **Quick overview:** See what users are doing in real-time

---

## 3. User Management

Navigate to **Users** in the sidebar to manage platform users.

### 3.1 Users Table

**Columns:**
- **Name:** User's full name
- **Email:** User's email address
- **Role:** User role (client, lawyer, admin, partner_lawyer)
- **Status:** Active (green) or Inactive (red)
- **Actions:** View details, Block/Unblock

```
Users
┌────────────┬──────────────────┬────────┬────────┬─────────┐
│ Name       │ Email            │ Role   │ Status │ Actions │
├────────────┼──────────────────┼────────┼────────┼─────────┤
│ John Doe   │ john@email.com   │ client │ Active │ View Block│
│ Jane Smith │ jane@email.com   │ client │ Active │ View Block│
│ Bob Admin  │ bob@admin.com    │ admin  │ Active │ View Block│
└────────────┴──────────────────┴────────┴────────┴─────────┘
```

### 3.2 Search & Filter Users

**Search Bar:**
- Type user name or email
- Results filter in real-time
- Case-insensitive search

**Example:**
```
Search: [john@email.com]  [Search]
```

### 3.3 View User Details

**Steps:**
1. Click **"View"** button next to any user
2. Modal window opens with detailed information

**Information Displayed:**
- Full name
- Email address
- User role
- Registration date
- Account status
- **Statistics:**
  - Number of consultations
  - Number of documents uploaded
  - Last activity date

```
┌─────────────────────────────────────┐
│  User Details                    [X]│
├─────────────────────────────────────┤
│ Name:     John Doe                  │
│ Email:    john@email.com            │
│ Role:     Client                    │
│ Joined:   Jan 15, 2026              │
│ Status:   Active                    │
│                                     │
│ Statistics:                         │
│ • Consultations: 23                 │
│ • Documents: 12                     │
│ • Last Active: 2 hours ago          │
│                                     │
│         [Close]                     │
└─────────────────────────────────────┘
```

### 3.4 Block/Unblock Users

**When to Block a User:**
- Violation of terms of service
- Suspicious activity
- User request
- Account security concerns

**How to Block:**
1. Find the user in the table
2. Click **"Block"** button
3. Confirm action (if prompted)
4. Success toast notification appears
5. Status changes to "Inactive" (red badge)

**Effect of Blocking:**
- ❌ User cannot login
- ❌ User cannot access platform features
- ❌ Active sessions are terminated

**How to Unblock:**
1. Find the blocked user (red "Inactive" badge)
2. Click **"Unblock"** button
3. Success toast notification appears
4. Status changes to "Active" (green badge)

> 💡 **Tip:** Use the search function to quickly find specific users before blocking/unblocking.

### 3.5 Pagination

**Navigation:**
- **Previous:** Go to previous page
- **Next:** Go to next page
- **Page indicator:** Shows current page (e.g., "Page 2 of 10")

```
[← Previous]  Page 2 of 10  [Next →]
```

**Items per page:** 20 users (default)

---

## 4. Universities Management

Navigate to **Universities** in the sidebar to manage educational institutions.

### 4.1 Universities Overview

**Statistics Cards:**
- **Total Universities:** Overall count
- **By Country:** Breakdown by country
- **By Type:** Breakdown by institution type

```
┌──────────────┬──────────────┬──────────────┐
│    Total     │  By Country  │   By Type    │
│     156      │  SK: 45      │  Uni: 89     │
│              │  CZ: 38      │  Lang: 34    │
│              │  PL: 73      │  Voc: 33     │
└──────────────┴──────────────┴──────────────┘
```

### 4.2 Universities Table

**Columns:**
- **Name:** University name
- **Country:** Country code (SK, CZ, PL, etc.)
- **Type:** University, Language School, Vocational School, etc.
- **Website:** Official website URL
- **Actions:** View, Edit

```
Universities
┌─────────────────────┬─────────┬──────────┬──────────────┬─────────┐
│ Name                │ Country │ Type     │ Website      │ Actions │
├─────────────────────┼─────────┼──────────┼──────────────┼─────────┤
│ Comenius University │ SK      │ Univ     │ uniba.sk     │ View Edit│
│ Charles University  │ CZ      │ Univ     │ cuni.cz      │ View Edit│
│ Jagiellonian Univ   │ PL      │ Univ     │ uj.edu.pl    │ View Edit│
└─────────────────────┴─────────┴──────────┴──────────────┴─────────┘
```

### 4.3 Search & Filter

**Search by Name:**
```
Search: [Comenius]  [Search]
```

**Filter by Country:**
```
Country: [All Countries ▼]
         - All Countries
         - Slovakia (SK)
         - Czech Republic (CZ)
         - Poland (PL)
         - ...
```

**Combined Filters:**
- Use search + country filter together
- Results update in real-time

### 4.4 View University Details

**Steps:**
1. Click **"View"** button
2. Modal opens with full details

**Information:**
- University name
- Country and city
- Type of institution
- Official website
- Contact information (if available)
- Number of students using platform

---

## 5. Analytics & Reports

Navigate to **Analytics** in the sidebar for detailed insights.

### 5.1 Available Analytics

**Current Features:**
- User growth trends (on Dashboard)
- Recent activity feed (on Dashboard)
- University statistics (on Universities page)

**Coming Soon:**
- Consultation analytics
- Document upload trends
- User engagement metrics
- Geographic distribution
- Peak usage times

### 5.2 Interpreting Data

**User Growth Chart:**
- **Upward trend:** Good! User acquisition is growing
- **Flat line:** Stable user base, consider marketing
- **Downward trend:** Investigate issues (bugs, competition, etc.)

**Activity Feed:**
- **High activity:** Platform is being actively used
- **Low activity:** May indicate technical issues or low engagement
- **Unusual patterns:** Could indicate bot activity or abuse

---

## 6. System Settings

Navigate to **Settings** in the sidebar to configure the platform.

### 6.1 Platform Configuration

```
Settings
┌─────────────────────────────────────────┐
│ Platform Name                           │
│ [Student Platform                     ] │
│                                         │
│ Support Email                           │
│ [support@student.com                  ] │
│                                         │
│ Maintenance Mode          [OFF] [ON]    │
│                                         │
│ OpenAI API Key                          │
│ [sk-••••••••••••••••••••••1234] [👁]   │
│                                         │
│         [Save Settings]                 │
└─────────────────────────────────────────┘
```

### 6.2 Settings Explained

#### Platform Name
**Purpose:** Display name shown to users throughout the platform

**Example:** "Student Platform", "EduConnect", "University Hub"

**Where it appears:**
- Website header
- Email notifications
- Login page

#### Support Email
**Purpose:** Contact email for user support inquiries

**Best Practice:**
- Use a monitored email address
- Set up auto-responders
- Ensure team has access

#### Maintenance Mode
**Purpose:** Temporarily disable platform access for maintenance

**When to use:**
- Database migrations
- Major updates
- Emergency fixes
- Scheduled maintenance

**Effect when ON:**
- ⚠️ Users cannot access the platform
- ⚠️ Login page shows maintenance message
- ✅ Admin panel remains accessible

**Steps to enable:**
1. Toggle switch to **ON**
2. Warning message appears
3. Click **"Save Settings"**
4. Verify users see maintenance page

**Steps to disable:**
1. Toggle switch to **OFF**
2. Click **"Save Settings"**
3. Platform is accessible again

> ⚠️ **Warning:** Always notify users before enabling maintenance mode!

#### OpenAI API Key
**Purpose:** Enable AI-powered features (consultations, document analysis)

**How to obtain:**
1. Create account at https://platform.openai.com
2. Navigate to API Keys section
3. Generate new secret key
4. Copy and paste here

**Security:**
- Key is masked by default (shows `sk-••••1234`)
- Click eye icon (👁) to reveal/hide
- Never share your API key
- Rotate keys regularly

**Features enabled:**
- AI legal consultations
- Document analysis
- University chat assistants

### 6.3 Saving Settings

**Steps:**
1. Make your changes
2. Click **"Save Settings"** button
3. Wait for confirmation toast
4. Settings are applied immediately

**Success:**
```
✅ Settings saved successfully!
```

**Error:**
```
❌ Failed to save settings. Please try again.
```

---

## 7. Troubleshooting

### 7.1 Common Issues

#### Cannot Login
**Symptoms:** Login fails with error message

**Solutions:**
1. ✅ Verify email and password are correct
2. ✅ Check if account is active (not blocked)
3. ✅ Clear browser cache and cookies
4. ✅ Try different browser
5. ✅ Contact system administrator

#### Dashboard Not Loading
**Symptoms:** Blank page or loading spinner

**Solutions:**
1. ✅ Check internet connection
2. ✅ Verify backend server is running
3. ✅ Check browser console for errors (F12)
4. ✅ Refresh the page (Ctrl+R)
5. ✅ Clear browser cache

#### Statistics Show Zero
**Symptoms:** All metrics show "0"

**Possible Causes:**
- Database is empty (new installation)
- Backend API not responding
- Database connection issue

**Solutions:**
1. ✅ Verify backend is running
2. ✅ Check database connection
3. ✅ Review backend logs for errors

#### Toast Notifications Not Appearing
**Symptoms:** No success/error messages

**Solutions:**
1. ✅ Check if browser blocks notifications
2. ✅ Disable ad blockers
3. ✅ Check browser console for errors

### 7.2 Error Messages

#### "Unauthorized" or "403 Forbidden"
**Meaning:** You don't have admin permissions

**Solution:**
- Verify your account has `role: admin`
- Contact system administrator to update role

#### "Network Error"
**Meaning:** Cannot connect to backend server

**Solution:**
- Check if backend is running
- Verify API URL is correct
- Check firewall settings

#### "Session Expired"
**Meaning:** Your login session has timed out

**Solution:**
- Login again
- Session lasts 30 minutes by default

### 7.3 Browser Compatibility

**Recommended Browsers:**
- ✅ Google Chrome (latest)
- ✅ Mozilla Firefox (latest)
- ✅ Microsoft Edge (latest)
- ✅ Safari (latest)

**Not Supported:**
- ❌ Internet Explorer

### 7.4 Mobile Access

**Responsive Design:**
- ✅ Works on smartphones (iOS, Android)
- ✅ Works on tablets (iPad, Android tablets)
- ✅ Optimized for touch interactions

**Mobile Features:**
- Hamburger menu for navigation
- Touch-friendly buttons
- Responsive tables with horizontal scroll

### 7.5 Getting Help

**Resources:**
1. **This Guide:** Comprehensive admin documentation
2. **Testing Checklist:** `ADMIN_TESTING_CHECKLIST.md`
3. **Technical Support:** Contact your system administrator
4. **Bug Reports:** Use the bug reporting template in testing checklist

**Contact Information:**
- **Support Email:** support@student.com (or your configured email)
- **Technical Issues:** Contact development team

---

## Appendix

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+K` | Focus search bar |
| `Esc` | Close modal/overlay |
| `Tab` | Navigate between fields |
| `Enter` | Submit form |

### User Roles

| Role | Permissions |
|------|-------------|
| **admin** | Full access to admin panel |
| **client** | Regular user access |
| **lawyer** | Lawyer-specific features |
| **partner_lawyer** | Partner lawyer features |

### Activity Types

| Type | Icon | Description |
|------|------|-------------|
| Registration | 👤 | New user signed up |
| Consultation | 💬 | AI consultation started |
| Document Upload | 📄 | User uploaded document |
| University Chat | 🎓 | University chat initiated |
| Subscription | 💳 | Subscription purchased |

---

## Changelog

**Version 1.0** (February 2026)
- Initial release
- Dashboard with statistics
- User management
- Universities management
- Settings configuration
- Responsive design
- Error handling

---

**End of Admin Panel User Guide**

For technical documentation, see developer documentation.
For testing procedures, see `ADMIN_TESTING_CHECKLIST.md`.

*Last updated: February 11, 2026*
