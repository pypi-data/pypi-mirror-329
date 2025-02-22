import smtplib
import random
from email.message import EmailMessage
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, Request, Header
from pydantic import BaseModel, EmailStr, Extra
from sqlalchemy import create_engine, Column, String, Integer, DateTime, or_, text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uuid import uuid4  # For generating unique API keys
from passlib.hash import argon2  # Using Argon2 for password hashing
from fastapi.security import APIKeyHeader
import json
import psycopg2
from psycopg2 import sql
from typing import Optional
from concurrent.futures import ThreadPoolExecutor


# =========================
# Global Configurations
# =========================
TESTING_MODE = True  # Toggle True (testing) or False (production)

# =========================
# SMTP / Email Settings
# =========================
SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 465
EMAIL_USERNAME = "otp@insights.fincept.in"
EMAIL_PASSWORD = "12Rjkrs34##"

# =========================
# Postgres / SQLAlchemy Config
# =========================
DATABASE_URL = "postgresql://postgres:12Rjkrs34##@localhost/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()

# =========================
# FastAPI App
# =========================
app = FastAPI()

# Define API Key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

# =========================
# Thread Pool for psycopg2 Queries
# =========================
thread_pool = ThreadPoolExecutor(max_workers=5)

def execute_db_query(query, params=(), dbname="FinanceDB"):
    """
    Connect to Postgres, execute the query with params, and return rows.
    Adjust the DB, user, password, host, etc. for your environment.
    """
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user="postgres",
            password="12Rjkrs34##",
            host="localhost",
            port=5432
        )
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
        conn.close()
        return rows
    except psycopg2.Error as e:
        raise e

# =========================
# Database Model (User)
# =========================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_verified = Column(Integer, default=0)
    registered_ip = Column(String, nullable=True)
    ip_whitelist = Column(JSON, default=[])
    temporary_ip = Column(String, nullable=True)
    temporary_ip_expiration = Column(DateTime, nullable=True)
    otp = Column(Integer, nullable=True)
    otp_expiration = Column(DateTime, nullable=True)
    api_key = Column(String, unique=True, nullable=True)
    rate_limit = Column(Integer, default=100)       # Daily rate limit
    subscriptions = Column(JSON, default=[])        # JSON column for subscribed databases
    usage_logs = Column(JSON, default=[])           # JSON column for storing usage logs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# =========================
# Utilities
# =========================

def log_usage(current_user: User, action: str, resource: str, db: SessionLocal, ip: str):
    """
    Logs API usage to the user's usage_logs JSON column.
    """
    log_entry = {
        "action": action,
        "resource": resource,
        "ip": ip,
        "timestamp": datetime.utcnow().isoformat(),
    }
    usage_logs = current_user.usage_logs or []
    if isinstance(usage_logs, str):
        usage_logs = json.loads(usage_logs)
    usage_logs.append(log_entry)
    current_user.usage_logs = json.dumps(usage_logs)
    db.commit()

rate_limits = {}  # maps IP addresses to an integer usage counter

def check_rate_limit(ip: str, current_user: User = None):
    """
    Checks if the requesting IP (or user) has exceeded the daily or per-IP rate limit.
    Decrements the user's or IP's limit if within bounds.
    """
    if current_user:  # user-based rate limit
        if current_user.rate_limit <= 0:
            raise HTTPException(status_code=429, detail="Rate limit exceeded for your account.")
        current_user.rate_limit -= 1
    else:  # IP-based rate limit
        global rate_limits
        rate_limits[ip] = rate_limits.get(ip, 10)  # default 10 if not present
        if rate_limits[ip] <= 0:
            raise HTTPException(status_code=429, detail="Rate limit exceeded for this IP.")
        rate_limits[ip] -= 1

# =========================
# Pydantic Models
# =========================
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    class Config:
        extra = Extra.ignore

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: int

# =========================
# DB Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# Email / OTP Logic
# =========================
def send_otp_email(email: str, otp: int):
    """
    Sends an OTP email using Hostinger's SMTP.
    """
    try:
        msg = EmailMessage()
        msg["Subject"] = "Your OTP Verification Code"
        msg["From"] = EMAIL_USERNAME
        msg["To"] = email
        msg.set_content(f"Your OTP for registration is: {otp}. It is valid for 10 minutes.")

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"OTP email sent successfully to {email}!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send OTP email")


# =========================
# Get Current User (Protected Endpoints)
# =========================
def get_current_user(api_key: str = Depends(api_key_header), db: SessionLocal = Depends(get_db)):
    """
    Validate the API key and check that the user is verified.
    """
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or unauthorized API key")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Account is not verified. Please verify your email.")
    return user

# =========================
# Get Guest User (10 Request Limit)
# =========================

def get_user_or_guest(
        request: Request,
        db: SessionLocal = Depends(get_db),
        x_api_key: Optional[str] = Header(None)  # Grab "X-API-Key" if present
):
    """
    Tries to authenticate via API key. If missing or invalid, returns None (guest).
    If valid, returns the authenticated User object.
    """
    if x_api_key is None:
        # No API key present => treat as guest
        return None

    # If they provided an API key, try to get the user
    user = db.query(User).filter(User.api_key == x_api_key).first()
    if user and user.is_verified:
        return user
    # If invalid or unverified
    return None


def get_guest_usage_by_ip(ip: str, db: SessionLocal):
    """
    Returns the guest usage row for this IP, or None if not found.
    Using raw SQL for demonstration. You could do this with SQLAlchemy too.
    """
    query = text("SELECT id, ip, usage_count FROM guest_usage WHERE ip = :ip LIMIT 1")
    result = db.execute(query, {"ip": ip}).fetchone()
    return result


def create_or_increment_guest_usage(ip: str, db: SessionLocal):
    """
    If no record for this IP, insert. If existing, increment usage_count.
    Returns the updated usage_count.
    """
    # Try to fetch existing usage
    row = get_guest_usage_by_ip(ip, db)

    if row:
        usage_id, ip_val, current_count = row
        new_count = current_count + 1
        update_q = text("""
            UPDATE guest_usage
            SET usage_count = :new_count,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = :usage_id
        """)
        db.execute(update_q, {"new_count": new_count, "usage_id": usage_id})
        db.commit()
        return new_count
    else:
        insert_q = text("""
            INSERT INTO guest_usage (ip, usage_count)
            VALUES (:ip, 1)
            RETURNING usage_count
        """)
        result = db.execute(insert_q, {"ip": ip}).fetchone()
        db.commit()
        return result[0] if result else 1


# =========================
# Registration & OTP
# =========================
@app.post("/register")
def register(user: UserCreate, request: Request, db: SessionLocal = Depends(get_db)):
    """
    Register a new user, generate an OTP, and (optionally) send via email.
    """
    existing_user = db.query(User).filter(
        or_(User.username == user.username, User.email == user.email)
    ).first()

    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username is already registered")
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email is already registered")

    # Generate OTP
    otp = 111111 if TESTING_MODE else random.randint(100000, 999999)
    otp_expiration = datetime.utcnow() + timedelta(minutes=10)
    api_key = str(uuid4())
    registered_ip = request.client.host

    try:
        db.execute(
            text(
                """
                INSERT INTO users (username, email, password_hash, otp, otp_expiration, api_key, is_verified, registered_ip)
                VALUES (:username, :email, :password_hash, :otp, :otp_expiration, :api_key, :is_verified, :registered_ip)
                """
            ),
            {
                "username": user.username,
                "email": user.email,
                "password_hash": argon2.hash(user.password),
                "otp": otp,
                "otp_expiration": otp_expiration,
                "api_key": api_key,
                "is_verified": 0,
                "registered_ip": registered_ip,
            },
        )
        db.commit()

        # Send OTP only in production mode
        if not TESTING_MODE:
            send_otp_email(user.email, otp)
    except Exception as e:
        db.rollback()
        print(f"Error during registration: {e}")
        raise HTTPException(status_code=500, detail="Registration failed due to an internal error")

    return {
        "message": ("User registered successfully. Check your email for the OTP."
                    if not TESTING_MODE
                    else "User registered successfully."),
        "api_key": api_key,
    }


@app.post("/verify-otp")
def verify_otp(verification: VerifyOTP, db: SessionLocal = Depends(get_db)):
    """
    Verify the OTP for a newly registered account.
    """
    user = db.query(User).filter(User.email == verification.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")
    if user.otp != verification.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    if datetime.utcnow() > user.otp_expiration:
        raise HTTPException(status_code=400, detail="OTP has expired")

    user.is_verified = 1
    user.otp = None
    user.otp_expiration = None
    db.commit()

    return {"message": "Email verified successfully!"}


# =========================
# Secondary Email / MFA
# =========================
@app.post("/add-secondary-email")
def add_secondary_email(
    secondary_email: EmailStr,
    current_user: User = Depends(get_current_user),
    db: SessionLocal = Depends(get_db),
):
    """
    Add or update the secondary email address for the current user.
    """
    if current_user.secondary_email == secondary_email:
        raise HTTPException(status_code=400, detail="This email is already registered as your secondary email.")

    current_user.secondary_email = secondary_email
    current_user.secondary_email_verified = 0  # Mark as unverified
    db.commit()

    # Send verification OTP to the secondary email
    otp = random.randint(100000, 999999)
    current_user.otp = otp
    current_user.otp_expiration = datetime.utcnow() + timedelta(minutes=10)
    db.commit()

    send_otp_email(secondary_email, otp)

    return {"message": f"Verification OTP sent to {secondary_email}. Please verify."}


@app.post("/verify-secondary-email")
def verify_secondary_email(
    verification: VerifyOTP,
    current_user: User = Depends(get_current_user),
    db: SessionLocal = Depends(get_db),
):
    """
    Verify the secondary email address using an OTP.
    """
    if current_user.secondary_email != verification.email:
        raise HTTPException(status_code=400, detail="This email does not match your secondary email.")
    if current_user.otp != verification.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP.")
    if datetime.utcnow() > current_user.otp_expiration:
        raise HTTPException(status_code=400, detail="OTP has expired.")

    current_user.secondary_email_verified = 1
    current_user.otp = None
    current_user.otp_expiration = None
    db.commit()

    return {"message": "Secondary email verified successfully!"}


@app.post("/toggle-mfa")
def toggle_mfa(
    enable: bool,
    current_user: User = Depends(get_current_user),
    db: SessionLocal = Depends(get_db),
):
    """
    Enable or disable MFA using the secondary email.
    """
    if enable:
        if not current_user.secondary_email_verified:
            raise HTTPException(status_code=400, detail="Secondary email is not verified. Please verify it first.")
        current_user.mfa_enabled = True
        message = "MFA enabled successfully."
    else:
        current_user.mfa_enabled = False
        message = "MFA disabled successfully."

    db.commit()
    return {"message": message}


# =========================
# Subscriptions & Database Info
# =========================
@app.get("/databases")
def get_databases(current_user: User = Depends(get_current_user)):
    """
    Return all available databases (minus restricted ones) for the current user.
    """
    restricted_databases = {"postgres"}
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false;"))
            databases = [row[0] for row in result if row[0] not in restricted_databases]
        return {"databases": databases}
    except Exception as e:
        print(f"Error fetching databases: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch databases.")


@app.get("/{database_name}/tables")
def get_tables(database_name: str, request: Request, current_user: User = Depends(get_current_user)):
    """
    Return all tables in the given database if user is subscribed.
    Enforces rate limit and subscription check.
    """
    ip = request.client.host
    check_rate_limit(ip, current_user)

    # Check subscription
    subscriptions = current_user.subscriptions or "[]"
    if isinstance(subscriptions, str):
        try:
            subscriptions = json.loads(subscriptions)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid subscriptions format.")

    if database_name not in subscriptions:
        raise HTTPException(status_code=403, detail="Not subscribed to this database.")

    # Fetch tables
    database_url = f"postgresql://postgres:12Rjkrs34##@localhost/{database_name}"
    specific_engine = create_engine(database_url)

    try:
        with specific_engine.connect() as connection:
            result = connection.execute(text("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"))
            tables = [row[0] for row in result]
        return {"tables": tables}
    except Exception as e:
        print(f"Error fetching tables for {database_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch tables.")


@app.get("/usage-logs")
def get_usage_logs(current_user: User = Depends(get_current_user)):
    """
    Return the current user's usage logs (list of actions).
    """
    logs = current_user.usage_logs
    if isinstance(logs, str):
        logs = json.loads(logs)
    return {"usage_logs": logs}


@app.post("/subscribe/{database_name}")
def subscribe_database(
    database_name: str,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: SessionLocal = Depends(get_db),
):
    """
    Subscribe the current user to a specific database.
    """
    valid_databases = [
        "IndiaPriceData", "metaData", "IndiaStockExchange", "NSELiveSecData", "DataGovIN",
        "finceptapi", "LargeEconomicDatabase", "IndiaBondData", "FinanceDB", "IndiaMutualFund",
        "IndiaStockCal", "WorldForexData", "WorldNewsData", "IndiaStockData", "PressReleaseData",
        "WorldEventData", "MarineTradeData", "WorldIndexData", "stockFundamentals", "WorldCommodityData"
    ]

    if database_name not in valid_databases:
        raise HTTPException(status_code=400, detail="Invalid database name.")

    subscriptions = current_user.subscriptions or []
    if isinstance(subscriptions, str):
        subscriptions = json.loads(subscriptions)

    if database_name in subscriptions:
        raise HTTPException(status_code=400, detail="Already subscribed to this database.")

    # Add subscription
    subscriptions.append(database_name)
    current_user.subscriptions = json.dumps(subscriptions)

    # Log the subscription
    ip = request.client.host
    usage_logs = current_user.usage_logs or []
    if isinstance(usage_logs, str):
        usage_logs = json.loads(usage_logs)
    usage_logs.append({
        "action": "subscribe",
        "database": database_name,
        "ip": ip,
        "time": datetime.utcnow().isoformat(),
    })
    current_user.usage_logs = json.dumps(usage_logs)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Subscription failed: {e}")

    return {"message": f"Successfully subscribed to {database_name}."}


# =========================
# Protected Data Endpoint (Pagination)
# =========================

@app.get("/{database_name}/{table_name}/data")
def get_table_data_unified(
        database_name: str,
        table_name: str,
        request: Request,
        user_or_none=Depends(get_user_or_guest),  # Our new optional dependency
        db: SessionLocal = Depends(get_db)
):
    """
    Fetch data with fixed pagination.
    - Guests (no API key): page=1, limit=10
    - Registered users: page=1, limit=50
    """

    ip = request.client.host

    # Hardcoded pagination values
    guest_page, guest_limit = 1, 10  # Fixed for guests
    user_page, user_limit = 1, 50  # Fixed for registered users

    if user_or_none:
        # ====================
        # AUTHENTICATED USER
        # ====================
        current_user = user_or_none

        # 1) Rate limit for user
        if current_user.rate_limit <= 0:
            raise HTTPException(429, "Rate limit exceeded for your account.")
        current_user.rate_limit -= 1
        db.commit()

        # 2) Check subscription
        subscriptions = current_user.subscriptions or []
        if isinstance(subscriptions, str):
            try:
                subscriptions = json.loads(subscriptions)
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Invalid subscriptions format.")

        if database_name not in subscriptions:
            raise HTTPException(status_code=403, detail="Not subscribed to this database.")

        # 3) Connect to the DB
        try:
            db_url = f"postgresql://postgres:12Rjkrs34##@localhost/{database_name}"
            specific_engine = create_engine(db_url)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error connecting to database {database_name}: {e}")

        # 4) Paginated query (fixed values for registered users)
        offset = (user_page - 1) * user_limit
        query_str = f'SELECT * FROM "{table_name}" ORDER BY 1 LIMIT :limit OFFSET :offset'

        try:
            with specific_engine.connect() as conn:
                result = conn.execute(text(query_str), {"limit": user_limit, "offset": offset})
                rows = result.fetchall()
                columns = result.keys()
                data = [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching data from table {table_name}: {e}")

        return {
            "database": database_name,
            "table": table_name,
            "page": user_page,
            "limit": user_limit,
            "rows_returned": len(data),
            "data": data
        }

    else:
        # ====================
        # GUEST USER (No API key)
        # ====================

        # 1) Increment guest usage
        usage_count = create_or_increment_guest_usage(ip, db)

        # 2) Check if they exceed the 10-request limit
        if usage_count > 10:
            raise HTTPException(
                status_code=429,
                detail="You have exceeded the 10-request limit for guest usage. Please register for an account."
            )

        # 3) Connect to the DB
        try:
            db_url = f"postgresql://postgres:12Rjkrs34##@localhost/{database_name}"
            specific_engine = create_engine(db_url)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error connecting to database {database_name} as a guest: {e}"
            )

        # 4) Paginated query (fixed values for guests)
        offset = (guest_page - 1) * guest_limit
        query_str = f'SELECT * FROM "{table_name}" ORDER BY 1 LIMIT :limit OFFSET :offset'

        try:
            with specific_engine.connect() as conn:
                result = conn.execute(text(query_str), {"limit": guest_limit, "offset": offset})
                rows = result.fetchall()
                columns = result.keys()
                data = [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching data (guest): {e}")

        return {
            "database": database_name,
            "table": table_name,
            "page": guest_page,
            "limit": guest_limit,
            "rows_returned": len(data),
            "data": data
        }

# =========================
# PUBLIC (FREE) ENDPOINTS
# No API Key, No Subscriptions, No Rate Limit
# =========================

@app.get("/public/{dbname}/{table}/{column}/filter")
async def get_rows_by_column_value(dbname: str, table: str, column: str, value: str):
    """
    Return all rows from {table} in {dbname} where {column} == value.
    Publicly accessible; no API key or subscription required.
    """
    # Check if column exists
    columns_query = sql.SQL("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema='public'
          AND table_name={table_name}
    """).format(table_name=sql.Literal(table))

    columns_future = thread_pool.submit(execute_db_query, columns_query, dbname=dbname)
    columns = columns_future.result()

    actual_columns = [col[0] for col in columns]
    if column not in actual_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Column '{column}' does not exist in table '{table}'"
        )

    # Query rows
    data_query = sql.SQL("SELECT * FROM {table} WHERE {column} = %s").format(
        column=sql.Identifier(column),
        table=sql.Identifier(table)
    )

    try:
        data_future = thread_pool.submit(execute_db_query, data_query, (value,), dbname=dbname)
        rows = data_future.result()

        # Ensure correct column order from the actual table
        columns_order_query = sql.SQL("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema='public' 
              AND table_name={table_name}
            ORDER BY ordinal_position
        """).format(table_name=sql.Literal(table))
        columns_order_future = thread_pool.submit(execute_db_query, columns_order_query, dbname=dbname)
        ordered_cols = columns_order_future.result()
        ordered_cols_list = [c[0] for c in ordered_cols]

        # Convert to list of dicts
        data_out = [dict(zip(ordered_cols_list, row)) for row in rows]
        return data_out

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {e}")


@app.get("/public/{dbname}/{table}/countries")
async def get_distinct_countries(dbname: str, table: str, limit: int = 500, offset: int = 0):
    """
    Return all distinct countries in {table} (up to {limit}, skipping {offset}).
    Publicly accessible; no API key or subscription required.
    """
    # Check if 'country' column exists
    columns_query = sql.SQL("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema='public'
          AND table_name={table_name}
    """).format(table_name=sql.Literal(table))
    columns_future = thread_pool.submit(execute_db_query, columns_query, dbname=dbname)
    columns = columns_future.result()

    if 'country' not in [col[0] for col in columns]:
        raise HTTPException(
            status_code=400,
            detail=f"Column 'country' does not exist in table '{table}'"
        )

    query_str = """
        SELECT DISTINCT country
        FROM {table}
        WHERE country IS NOT NULL
        LIMIT %s OFFSET %s
    """
    data_query = sql.SQL(query_str).format(table=sql.Identifier(table))
    params = (limit, offset)

    try:
        data_future = thread_pool.submit(execute_db_query, data_query, params, dbname=dbname)
        rows = data_future.result()
        return [row[0] for row in rows]
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {e}")


@app.get("/public/{dbname}/{table}/sectors_and_industries_and_stocks")
async def get_sectors_industries_stocks(
    dbname: str,
    table: str,
    filter_column: str,
    filter_value: str,
    sector: Optional[str] = None,
    industry: Optional[str] = None,
    limit: int = 500,
    offset: int = 0
):
    """
    3-step logic to fetch sectors, then industries, then stocks for a given filter (e.g., country):
      1) If no sector & no industry -> distinct sectors
      2) If sector & no industry   -> distinct industries
      3) If sector & industry      -> list of stocks (with symbol, name, market_cap)
    Publicly accessible; no API key or subscription required.
    """
    # Check needed columns
    columns_query = sql.SQL("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema='public'
          AND table_name={table_name}
    """).format(table_name=sql.Literal(table))

    columns_future = thread_pool.submit(execute_db_query, columns_query, dbname=dbname)
    columns = columns_future.result()
    col_names = [col[0] for col in columns]

    required_cols = [filter_column, 'sector', 'industry', 'symbol', 'market_cap']
    for rc in required_cols:
        if rc not in col_names:
            raise HTTPException(
                status_code=400,
                detail=f"Column '{rc}' does not exist in table '{table}'. Required: {required_cols}"
            )

    # 1) Distinct sectors if sector and industry are not provided
    if not sector and not industry:
        query_str = """
            SELECT DISTINCT sector
            FROM {table}
            WHERE {filter_column} = %s
              AND sector IS NOT NULL
            LIMIT %s OFFSET %s
        """
        data_query = sql.SQL(query_str).format(
            table=sql.Identifier(table),
            filter_column=sql.Identifier(filter_column)
        )
        params = (filter_value, limit, offset)

        try:
            data_future = thread_pool.submit(execute_db_query, data_query, params, dbname=dbname)
            rows = data_future.result()
            return [row[0] for row in rows]  # distinct sectors
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Database query failed: {e}")

    # 2) Distinct industries if sector is provided but no industry
    elif sector and not industry:
        query_str = """
            SELECT DISTINCT industry
            FROM {table}
            WHERE {filter_column} = %s
              AND sector = %s
              AND industry IS NOT NULL
            LIMIT %s OFFSET %s
        """
        data_query = sql.SQL(query_str).format(
            table=sql.Identifier(table),
            filter_column=sql.Identifier(filter_column)
        )
        params = (filter_value, sector, limit, offset)

        try:
            data_future = thread_pool.submit(execute_db_query, data_query, params, dbname=dbname)
            rows = data_future.result()
            return [row[0] for row in rows]  # distinct industries
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Database query failed: {e}")

    # 3) List stocks if both sector & industry are provided
    elif sector and industry:
        query_str = """
            SELECT symbol, name, market_cap
            FROM {table}
            WHERE {filter_column} = %s
              AND sector = %s
              AND industry = %s
              AND symbol IS NOT NULL
            LIMIT %s OFFSET %s
        """
        data_query = sql.SQL(query_str).format(
            table=sql.Identifier(table),
            filter_column=sql.Identifier(filter_column)
        )
        params = (filter_value, sector, industry, limit, offset)

        try:
            data_future = thread_pool.submit(execute_db_query, data_query, params, dbname=dbname)
            rows = data_future.result()
            return [
                {"symbol": row[0], "name": row[1], "market_cap": row[2]}
                for row in rows
            ]
        except psycopg2.Error as e:
            raise HTTPException(status_code=500, detail=f"Database query failed: {e}")

    # Invalid combination
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid combination of parameters. Provide either none or both for sector/industry."
        )
