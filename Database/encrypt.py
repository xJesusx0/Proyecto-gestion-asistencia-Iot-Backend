import bcrypt

def encrypt(password):
    salt = bcrypt.gensalt().decode('utf-8')  # Generar y almacenar la sal
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
    return hashed_password

def decrypt(password,hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
