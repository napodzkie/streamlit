# Streamlit Cloud Deployment Guide

## 🔴 Problem: Database Connection Error

If you see this error on Streamlit Cloud:
```
connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
```

This is because **Streamlit Cloud cannot connect to localhost** - your app runs on Streamlit's servers, not your local machine. You need a **cloud-hosted PostgreSQL database**.

---

## ✅ Solution: Set Up a Cloud Database

You have several options for free cloud PostgreSQL databases:

### Option 1: Supabase (Recommended - Easy & Free)

1. **Sign up**: Go to [https://supabase.com](https://supabase.com) and create a free account
2. **Create a new project**:
   - Click "New Project"
   - Choose a name (e.g., "civicguardian")
   - Set a database password (save this!)
   - Select a region close to you
3. **Get your connection string**:
   - Go to **Settings** → **Database**
   - Scroll down to **Connection string** section
   - Copy the **URI** connection string
   - It will look like: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`
   - **Important**: Replace `postgresql://` with `postgresql+psycopg2://` for SQLAlchemy

### Option 2: ElephantSQL (Also Free)

1. **Sign up**: Go to [https://www.elephantsql.com](https://www.elephantsql.com)
2. **Create a free instance**:
   - Click "Create New Instance"
   - Select "Tiny Turtle" (free tier)
   - Choose a region
   - Click "Select Plan" and confirm
3. **Get your connection string**:
   - Click on your instance
   - Copy the **URL** from the details page
   - It will look like: `postgres://user:password@host:5432/database`
   - **Important**: Replace `postgres://` with `postgresql+psycopg2://` for SQLAlchemy

### Option 3: Neon (Serverless PostgreSQL)

1. **Sign up**: Go to [https://neon.tech](https://neon.tech)
2. **Create a project**:
   - Click "Create Project"
   - Choose settings and create
3. **Get connection string**:
   - Go to "Connection Details"
   - Copy the connection string
   - Format it as: `postgresql+psycopg2://user:password@host/database`

### Option 4: Railway (Easy Setup)

1. **Sign up**: Go to [https://railway.app](https://railway.app)
2. **Create PostgreSQL service**:
   - Click "New Project"
   - Select "PostgreSQL"
3. **Get connection string**:
   - Go to "Variables" tab
   - Copy the `DATABASE_URL` value
   - Already formatted correctly!

---

## 🔧 Configure Streamlit Cloud Secrets

Once you have your cloud database connection string:

### Step 1: Go to Streamlit Cloud Dashboard

1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click on your app (or create a new one)

### Step 2: Add Database Secret

1. Click **"⚙️ Settings"** (gear icon) in the app menu
2. Click **"Secrets"** in the left sidebar
3. Click **"Edit secrets"**
4. Add your database URL in this format:

```toml
DATABASE_URL = "postgresql+psycopg2://username:password@host:5432/database_name"
```

**Example for Supabase:**
```toml
DATABASE_URL = "postgresql+psycopg2://postgres:YourPassword123@db.abcdefghijk.supabase.co:5432/postgres"
```

**Example for ElephantSQL:**
```toml
DATABASE_URL = "postgresql+psycopg2://user:pass@host.elephantsql.com:5432/dbname"
```

5. Click **"Save"**

### Step 3: Restart Your App

1. Go back to your app dashboard
2. Click **"⋮"** (three dots) → **"Restart app"**
3. Wait for the app to restart

---

## 📝 Example: Complete Setup with Supabase

Here's a step-by-step example:

### 1. Create Supabase Project
- Visit: https://supabase.com/dashboard
- Click "New Project"
- Name: `civicguardian`
- Password: `MySecurePassword123!`
- Region: `US East`
- Wait ~2 minutes for setup

### 2. Get Connection String
- Settings → Database
- Under "Connection string" → "URI"
- Copy: `postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres`
- **Convert to**: `postgresql+psycopg2://postgres.xxxxx:MySecurePassword123!@aws-0-us-east-1.pooler.supabase.com:6543/postgres`

### 3. Set in Streamlit Cloud
```toml
DATABASE_URL = "postgresql+psycopg2://postgres.xxxxx:MySecurePassword123!@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
```

### 4. Test Connection
- Your app should now connect successfully
- Tables will be created automatically on first run
- Demo data will be seeded

---

## 🔍 Troubleshooting

### Problem: Still getting connection errors

1. **Check your connection string format**:
   - Must start with `postgresql+psycopg2://` (not just `postgresql://`)
   - Must include username, password, host, port, and database name

2. **Verify database is accessible**:
   - Some databases have IP allowlists - make sure Streamlit Cloud IPs are allowed
   - Check if your database requires SSL connections

3. **Test the connection string locally first**:
   ```python
   # Create a test file
   import os
   from sqlalchemy import create_engine, text
   
   DATABASE_URL = "your-connection-string-here"
   engine = create_engine(DATABASE_URL)
   
   try:
       with engine.connect() as conn:
           result = conn.execute(text("SELECT version()"))
           print("✅ Connection successful!")
           print(result.fetchone()[0])
   except Exception as e:
       print(f"❌ Connection failed: {e}")
   ```

### Problem: "SSL required" error

Add SSL parameters to your connection string:
```toml
DATABASE_URL = "postgresql+psycopg2://user:pass@host:5432/db?sslmode=require"
```

### Problem: Tables not created

The app should auto-create tables on first run. If not:
1. Check Streamlit Cloud logs for errors
2. Ensure the database user has CREATE TABLE permissions
3. Try restarting the app

---

## 🎯 Quick Checklist

- [ ] Created account on cloud database provider (Supabase/ElephantSQL/etc.)
- [ ] Created database/project
- [ ] Copied connection string
- [ ] Converted `postgresql://` to `postgresql+psycopg2://`
- [ ] Added `DATABASE_URL` to Streamlit Cloud Secrets
- [ ] Restarted Streamlit app
- [ ] Verified app loads without errors

---

## 💡 Tips

1. **Keep your password secure** - Never commit secrets to GitHub
2. **Free tier limitations** - Free databases usually have size/time limits
3. **Connection pooling** - For production, consider connection pooling
4. **Backup your data** - Set up regular backups for important data

---

## 📚 Additional Resources

- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Supabase Documentation](https://supabase.com/docs)
- [ElephantSQL Documentation](https://www.elephantsql.com/docs/)
- [SQLAlchemy Connection Strings](https://docs.sqlalchemy.org/en/20/core/engines.html#database-urls)

