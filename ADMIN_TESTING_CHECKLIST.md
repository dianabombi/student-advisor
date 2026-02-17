# Admin Panel Testing Checklist

This document provides a comprehensive manual testing checklist for the Student Platform Admin Panel.

## Prerequisites

Before starting testing:
- ✅ Backend server is running (`docker-compose up` or `uvicorn main:app`)
- ✅ Frontend server is running (`npm run dev`)
- ✅ Admin user created (run `python backend/scripts/create_admin.py`)
- ✅ Database has some test data (users, universities)

**Admin Credentials:**
- Email: `admin@student.com`
- Password: `Admin123!`

---

## 1. Authentication & Access Control

### ☐ Login as Admin
**Steps:**
1. Navigate to `http://localhost:3000/auth/login`
2. Enter email: `admin@student.com`
3. Enter password: `Admin123!`
4. Click "Login"

**Expected:**
- ✅ Successful login
- ✅ Redirect to `/admin/dashboard`
- ✅ JWT token stored in localStorage
- ✅ No errors in console

**Failure Cases to Test:**
- ❌ Wrong password → Error message displayed
- ❌ Non-admin user → Redirect to home page
- ❌ No token → Redirect to login

---

## 2. Dashboard Page

### ☐ Dashboard Metrics Display
**Steps:**
1. After login, verify you're on `/admin/dashboard`
2. Check all 4 StatCards are visible

**Expected:**
- ✅ **Total Users** card shows correct count
- ✅ **Universities** card shows correct count
- ✅ **Consultations** card shows correct count
- ✅ **Documents** card shows correct count
- ✅ Icons display correctly (Users, GraduationCap, MessageSquare, FileText)
- ✅ Numbers are not "0" if data exists

### ☐ User Growth Chart
**Steps:**
1. Scroll to "User Growth" section
2. Click each period button: "30 Days", "3 Months", "1 Year", "All Time"
3. Verify chart updates

**Expected:**
- ✅ Chart displays with blue line
- ✅ X-axis shows dates
- ✅ Y-axis shows user counts
- ✅ Clicking period buttons updates chart data
- ✅ Loading spinner shows while fetching
- ✅ Hover over chart shows tooltip with exact values

**Edge Cases:**
- ⚠️ No data → "No growth data available" message
- ⚠️ API error → Error state displayed

### ☐ Recent Activity Feed
**Steps:**
1. Scroll to "Recent Activity" section
2. Verify activities are listed
3. Wait 30 seconds (auto-refresh)

**Expected:**
- ✅ Last 10 activities displayed
- ✅ Each activity shows:
  - Icon (based on type)
  - Description
  - User email
  - Time ago (e.g., "5 min ago")
- ✅ Auto-refreshes every 30 seconds
- ✅ Different activity types have different icons/colors

**Edge Cases:**
- ⚠️ No activities → "No recent activity" empty state

---

## 3. Users Management

### ☐ Users Table with Pagination
**Steps:**
1. Click "Users" in sidebar
2. Navigate to `/admin/users`
3. Verify table displays

**Expected:**
- ✅ Table shows users with columns:
  - Name
  - Email
  - Role
  - Status (Active/Inactive badge)
  - Actions (View, Block/Unblock)
- ✅ Pagination controls at bottom
- ✅ "Previous" and "Next" buttons work
- ✅ Page numbers displayed (e.g., "Page 1 of 5")

### ☐ User Search
**Steps:**
1. On Users page, use search input
2. Type user email or name
3. Press Enter or click search

**Expected:**
- ✅ Table filters to matching users
- ✅ Search is case-insensitive
- ✅ Clear search shows all users again

### ☐ View User Details
**Steps:**
1. Click "View" button on any user
2. Modal opens with user details

**Expected:**
- ✅ Modal displays:
  - User name
  - Email
  - Role
  - Registration date
  - Statistics (consultations, documents)
- ✅ "Close" button works
- ✅ Click outside modal closes it

### ☐ Block/Unblock User
**Steps:**
1. Find an active user
2. Click "Block" button
3. Verify user status changes
4. Click "Unblock" to restore

**Expected:**
- ✅ Toast notification: "User blocked successfully"
- ✅ Status badge changes to "Inactive" (red)
- ✅ Button changes to "Unblock"
- ✅ Unblock shows toast: "User unblocked successfully"
- ✅ Status badge changes to "Active" (green)

**Verify:**
- ✅ Blocked user cannot login
- ✅ Unblocked user can login again

---

## 4. Universities Management

### ☐ Universities Table
**Steps:**
1. Click "Universities" in sidebar
2. Navigate to `/admin/universities`
3. Verify table displays

**Expected:**
- ✅ Table shows universities with columns:
  - Name
  - Country
  - Type (University, Language School, etc.)
  - Website
  - Actions (View, Edit)
- ✅ Pagination works
- ✅ Stats cards show:
  - Total universities
  - Count by country
  - Count by type

### ☐ University Search & Filter
**Steps:**
1. Use search input to find university by name
2. Use country dropdown to filter
3. Combine search + filter

**Expected:**
- ✅ Search filters by name
- ✅ Country filter works
- ✅ Combined filters work together
- ✅ Clear filters shows all universities

---

## 5. Settings Page

### ☐ Settings Display & Edit
**Steps:**
1. Click "Settings" in sidebar
2. Navigate to `/admin/settings`
3. Verify form displays current settings

**Expected:**
- ✅ Form shows:
  - Platform Name (pre-filled)
  - Support Email (pre-filled)
  - Maintenance Mode toggle
  - OpenAI API Key (masked)
- ✅ All fields are editable

### ☐ Save Settings
**Steps:**
1. Change "Platform Name" to "Test Platform"
2. Change "Support Email" to "test@example.com"
3. Click "Save Settings"

**Expected:**
- ✅ Toast notification: "Settings saved successfully!" (green)
- ✅ Button shows "Saving..." during request
- ✅ Settings persist after page reload

### ☐ Maintenance Mode Toggle
**Steps:**
1. Click Maintenance Mode toggle to ON
2. Verify warning appears
3. Save settings
4. Toggle back to OFF

**Expected:**
- ✅ Toggle switches smoothly
- ✅ Warning message: "⚠️ Platform is currently in maintenance mode"
- ✅ Toast confirms save
- ✅ (Optional) Verify users cannot access platform when ON

### ☐ API Key Visibility
**Steps:**
1. Verify API key is masked (shows `sk-••••••••1234`)
2. Click eye icon to show
3. Click eye-off icon to hide

**Expected:**
- ✅ Key is masked by default
- ✅ Eye icon toggles visibility
- ✅ Full key visible when shown
- ✅ Key hidden when toggled off

---

## 6. Responsive Design

### ☐ Mobile View (< 640px)
**Steps:**
1. Open Chrome DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select "iPhone 12 Pro" or similar
4. Navigate through admin panel

**Expected:**
- ✅ **Sidebar:**
  - Hidden by default
  - Hamburger menu (☰) visible in header
  - Clicking hamburger opens sidebar from left
  - Dark overlay appears
  - Clicking overlay or X closes sidebar
- ✅ **StatCards:** 1 column (stacked vertically)
- ✅ **Tables:** Horizontal scroll if needed
- ✅ **Charts:** Responsive width
- ✅ **Padding:** Reduced (p-4)

### ☐ Tablet View (640px - 1024px)
**Steps:**
1. Select "iPad" or set width to 768px
2. Navigate through admin panel

**Expected:**
- ✅ **Sidebar:** Still collapsible with hamburger
- ✅ **StatCards:** 2 columns
- ✅ **Tables:** Better fit, less scrolling
- ✅ **Padding:** Medium (p-6)

### ☐ Desktop View (> 1024px)
**Steps:**
1. Set width to 1920px or use full screen
2. Navigate through admin panel

**Expected:**
- ✅ **Sidebar:** Always visible, no hamburger
- ✅ **StatCards:** 4 columns
- ✅ **Tables:** Full width, no scroll
- ✅ **Padding:** Large (p-8)

---

## 7. Error Handling

### ☐ Loading States
**Steps:**
1. Open Network tab in DevTools
2. Throttle to "Slow 3G"
3. Navigate to Dashboard, Users, Universities
4. Observe loading states

**Expected:**
- ✅ **Dashboard:** Skeleton loaders for StatCards, Chart, Activity
- ✅ **Settings:** Form skeleton while loading
- ✅ **Tables:** Loading spinner or skeleton rows
- ✅ No "undefined" or broken UI during load

### ☐ Error States
**Steps:**
1. Stop backend server
2. Try to load Dashboard
3. Try to save Settings
4. Observe error handling

**Expected:**
- ✅ **API Failure:** Error state component with "Try Again" button
- ✅ **Settings Save Fail:** Toast notification (red) with error message
- ✅ **Network Error:** Graceful error message, not crash
- ✅ **Retry Button:** Clicking retry re-fetches data

### ☐ Empty States
**Steps:**
1. Create fresh database with no data
2. Navigate to Dashboard, Users, Universities

**Expected:**
- ✅ **No Users:** "No users found" empty state
- ✅ **No Universities:** "No universities found" empty state
- ✅ **No Activity:** "No recent activity" empty state with icon
- ✅ Empty states have helpful icons and descriptions

### ☐ Error Boundary
**Steps:**
1. (Advanced) Intentionally cause a React error in admin panel
2. Verify Error Boundary catches it

**Expected:**
- ✅ Error Boundary page displays
- ✅ Shows error icon and message
- ✅ "Reload Admin Panel" button works
- ✅ "Go to Main Platform" button redirects to home
- ✅ Main platform still works (not affected)

---

## 8. Toast Notifications

### ☐ Success Toasts
**Test in:**
- Settings save
- User block/unblock

**Expected:**
- ✅ Green toast with checkmark icon
- ✅ Appears top-right
- ✅ Auto-dismisses after 3 seconds
- ✅ Dark theme styling

### ☐ Error Toasts
**Test in:**
- Failed settings save (stop backend)
- Failed user action

**Expected:**
- ✅ Red toast with X icon
- ✅ Appears top-right
- ✅ Auto-dismisses after 4 seconds
- ✅ Clear error message

---

## 9. Navigation & UX

### ☐ Sidebar Navigation
**Steps:**
1. Click each menu item: Dashboard, Users, Universities, Analytics, Settings
2. Verify active state

**Expected:**
- ✅ Active page highlighted (blue background)
- ✅ URL changes correctly
- ✅ Page content loads
- ✅ Smooth transitions

### ☐ Logout
**Steps:**
1. Click "Logout" in sidebar
2. Verify redirect

**Expected:**
- ✅ Redirects to `/auth/login`
- ✅ Token removed from localStorage
- ✅ Cannot access admin pages without re-login

---

## 10. Performance

### ☐ Page Load Times
**Expected:**
- ✅ Dashboard loads < 2 seconds
- ✅ Tables load < 1 second
- ✅ Settings load < 1 second
- ✅ No layout shift during load

### ☐ Smooth Interactions
**Expected:**
- ✅ Sidebar slide animation smooth (300ms)
- ✅ Modal open/close smooth
- ✅ Toast animations smooth
- ✅ No lag when typing in search/inputs

---

## Testing Summary

After completing all tests, verify:

- [ ] All core features work
- [ ] Responsive on all screen sizes
- [ ] Error handling is graceful
- [ ] Loading states display correctly
- [ ] Toast notifications work
- [ ] No console errors
- [ ] Performance is acceptable

---

## Bug Reporting Template

If you find a bug, report it with:

```
**Bug:** [Short description]
**Steps to Reproduce:**
1. 
2. 
3. 

**Expected:** [What should happen]
**Actual:** [What actually happened]
**Screenshot:** [If applicable]
**Browser:** [Chrome/Firefox/Safari]
**Screen Size:** [Desktop/Tablet/Mobile]
```

---

## Notes

- Test with **real data** when possible (not just empty states)
- Test **edge cases** (very long names, special characters, etc.)
- Test **concurrent actions** (multiple tabs, rapid clicks)
- Test **different browsers** (Chrome, Firefox, Safari)
- Test **keyboard navigation** (Tab, Enter, Esc)

**Happy Testing! 🚀**
