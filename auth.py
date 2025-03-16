import hashlib
import psycopg2
import streamlit as st
from db import connect_to_postgresql


def get_all_users():
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password_hash, role FROM users')
    users = cursor.fetchall()
    conn.close()
    return users


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password, role):
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    try:
        hashed_password = hash_password(password)
        cursor.execute(
            'INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)',
            (username, hashed_password, role)
        )
        conn.commit()
        st.success("User created successfully!")
    except psycopg2.IntegrityError:
        st.error("Username already exists.")
    finally:
        conn.close()

def validate_user(username, password, role):
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute(
        'SELECT id FROM users WHERE username = %s AND password_hash = %s AND role = %s',
        (username, hashed_password, role)
    )
    user = cursor.fetchone()
    conn.close()
    return user


def update_user(username, new_password, new_role):
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    try:
        hashed_password = hash_password(new_password)
        cursor.execute(
            "UPDATE users SET password_hash = %s , role = %s WHERE username = %s",
            (hashed_password, new_role, username)
        )
        conn.commit()
        st.success(f"User '{username}' updated successfully!")
    except Exception as e:
        st.error(f"Error updating user: {e}")
    finally:
        cursor.close()
        conn.close()


def delete_user(username):
    conn = connect_to_postgresql()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
        st.success("User deleted successfully!")
    except Exception as e:
        st.error(f"Error deleting user: {e}")
    finally:
        conn.close()



