from werkzeug.security import generate_password_hash
# --- CHOOSE YOUR NEW, FINAL PASSWORD ---
password_to_use = "NewCapstonePass2024!"
# -------------------------------------
hashed_password = generate_password_hash(password_to_use, method='pbkdf2:sha256')
print(f"Your new password is: {password_to_use}")
print(f"Your new hash is: {hashed_password}")