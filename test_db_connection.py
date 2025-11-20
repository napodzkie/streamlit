"""
Test script to diagnose PostgreSQL connection issues.
Run this to check if your database connection is working.
"""
import sys
import os

print("=" * 60)
print("PostgreSQL Connection Diagnostic Tool")
print("=" * 60)
print()

# Check if required packages are installed
print("1. Checking required packages...")
try:
    import psycopg2
    print("   ✅ psycopg2 is installed")
except ImportError:
    print("   ❌ psycopg2 is NOT installed")
    print("   Install it with: pip install psycopg2-binary")
    sys.exit(1)

try:
    from sqlalchemy import create_engine
    print("   ✅ SQLAlchemy is installed")
except ImportError:
    print("   ❌ SQLAlchemy is NOT installed")
    print("   Install it with: pip install SQLAlchemy")
    sys.exit(1)

print()

# Get connection details
print("2. Connection details:")
database_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/civicguardian")
print(f"   Connection string: {database_url.replace('postgres:', 'postgres:***')}")

# Parse connection details (basic)
if "@" in database_url:
    parts = database_url.split("@")
    if "://" in parts[0]:
        auth_part = parts[0].split("://")[1]
        if ":" in auth_part:
            user, password = auth_part.split(":", 1)
            print(f"   Username: {user}")
            print(f"   Password: {'*' * len(password)}")
    
    if "/" in parts[1]:
        host_port = parts[1].split("/")[0]
        if ":" in host_port:
            host, port = host_port.split(":")
            print(f"   Host: {host}")
            print(f"   Port: {port}")
        else:
            print(f"   Host: {host_port}")
            print(f"   Port: 5432 (default)")
        
        database = parts[1].split("/")[1].split("?")[0] if "/" in parts[1] else None
        if database:
            print(f"   Database: {database}")

print()

# Test basic connection (using psycopg2 directly)
print("3. Testing basic connection...")
try:
    import psycopg2.extras
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        connect_timeout=5
    )
    print("   ✅ Successfully connected to PostgreSQL server!")
    print(f"   PostgreSQL version: {conn.server_version}")
    conn.close()
except psycopg2.OperationalError as e:
    print(f"   ❌ Connection failed: {e}")
    print()
    print("   Possible causes:")
    print("   - PostgreSQL server is not running")
    print("   - Wrong host/port (check if PostgreSQL is on a different port)")
    print("   - Wrong username/password")
    print("   - Firewall blocking the connection")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ Unexpected error: {e}")
    sys.exit(1)

print()

# Test if database exists
print("4. Checking if database 'civicguardian' exists...")
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        database="postgres",  # Connect to default database first
        connect_timeout=5
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'civicguardian'")
    exists = cursor.fetchone()
    
    if exists:
        print("   ✅ Database 'civicguardian' exists")
    else:
        print("   ❌ Database 'civicguardian' does NOT exist")
        print("   Creating database...")
        cursor.execute('CREATE DATABASE civicguardian')
        print("   ✅ Database 'civicguardian' created!")
    
    cursor.close()
    conn.close()
except psycopg2.OperationalError as e:
    print(f"   ❌ Could not check database: {e}")
except psycopg2.errors.DuplicateDatabase:
    print("   ✅ Database 'civicguardian' already exists")
except Exception as e:
    print(f"   ❌ Unexpected error: {e}")

print()

# Test SQLAlchemy connection
print("5. Testing SQLAlchemy connection...")
try:
    from sqlalchemy import create_engine, text
    engine = create_engine(database_url, pool_pre_ping=True, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print("   ✅ SQLAlchemy connection successful!")
        print(f"   {version}")
except Exception as e:
    print(f"   ❌ SQLAlchemy connection failed: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("✅ All connection tests passed!")
print("=" * 60)
print()
print("Your Streamlit app should be able to connect to the database now.")
print("If you still see errors, check the PostgreSQL configuration files:")
print("  - postgresql.conf (check 'listen_addresses')")
print("  - pg_hba.conf (check authentication settings)")

