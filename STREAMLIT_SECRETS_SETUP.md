# Quick Setup Guide: Add Database to Streamlit Cloud

## Your Supabase Connection String

Use this connection string (already formatted for Streamlit):

```
postgresql+psycopg2://postgres:Qx7hpacuJyMjcnm8@db.ypzycptidfpqxikjcwxy.supabase.co:5432/postgres
```

---

## Step-by-Step Instructions

### Step 1: Go to Your Streamlit Cloud App

1. Open your browser and go to: **https://share.streamlit.io**
2. Sign in with your GitHub account
3. Find and click on your app: **app-hyqk59jfu8mjzbcack4aaj**
   - Or go directly to: https://share.streamlit.io/app-hyqk59jfu8mjzbcack4aaj

### Step 2: Access App Settings

1. On your app page, click the **⚙️ Settings** button (gear icon) in the top right
2. Or click the **⋮** (three dots menu) and select **"Settings"**

### Step 3: Add Database Secret

1. In the left sidebar, click on **"Secrets"**
2. Click the **"Edit secrets"** button
3. You'll see a text editor - add this exactly:

```toml
DATABASE_URL = "postgresql+psycopg2://postgres:Qx7hpacuJyMjcnm8@db.ypzycptidfpqxikjcwxy.supabase.co:5432/postgres"
```

**Important:** 
- Make sure you use **double quotes** around the connection string
- Make sure there are **no extra spaces** before or after the equals sign
- The format should be exactly as shown above

4. Click **"Save"** button at the bottom

### Step 4: Restart Your App

1. Go back to your app dashboard (click your app name or use the back button)
2. Click the **⋮** (three dots menu) next to your app
3. Click **"Restart app"**
4. Wait 30-60 seconds for the app to restart

### Step 5: Test Connection

1. Once restarted, open your app: https://app-hyqk59jfu8mjzbcack4aaj.streamlit.app/
2. The database error should be gone!
3. Tables will be created automatically on first run
4. Demo data will be seeded automatically

---

## ✅ Success Indicators

You'll know it worked when:
- ✅ No database connection error appears
- ✅ The app loads successfully
- ✅ You can see the dashboard with maps and reports
- ✅ Tables are created in your Supabase database

---

## 🔍 Troubleshooting

### Problem: Still seeing connection error

1. **Double-check the secret format**:
   - Make sure you used `postgresql+psycopg2://` (not just `postgresql://`)
   - Verify there are quotes around the connection string
   - Check for typos

2. **Verify the secret was saved**:
   - Go back to Settings → Secrets
   - Make sure `DATABASE_URL` appears in the list

3. **Check app logs**:
   - In Streamlit Cloud dashboard, click on "Logs" or "App logs"
   - Look for any error messages

4. **Try restarting again**:
   - Sometimes you need to restart multiple times
   - Wait at least 30 seconds between restarts

### Problem: "SSL required" error

If you see an SSL error, modify your connection string in secrets to:

```toml
DATABASE_URL = "postgresql+psycopg2://postgres:Qx7hpacuJyMjcnm8@db.ypzycptidfpqxikjcwxy.supabase.co:5432/postgres?sslmode=require"
```

(Add `?sslmode=require` at the end)

### Problem: Can't find the Secrets option

- Make sure you're the owner of the app (not just a viewer)
- Try refreshing the page
- Make sure you're logged in to the correct GitHub account

---

## 📸 Visual Guide

Your Secrets page should look like this:

```
┌─────────────────────────────────────┐
│ Streamlit Secrets                   │
├─────────────────────────────────────┤
│                                     │
│ DATABASE_URL = "postgresql+psycopg2 │
│ ://postgres:Qx7hpacuJyMjcnm8@db.ypz │
│ ycptidfpqxikjcwxy.supabase.co:5432/ │
│ postgres"                           │
│                                     │
│ [Save]  [Cancel]                    │
└─────────────────────────────────────┘
```

---

## 🎉 You're Done!

Once the app restarts successfully, your database connection will be active and your app will work perfectly on Streamlit Cloud!

