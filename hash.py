import hashlib

# Of course, this file is on github only because project is for demonstration :)

def hashing(password):
    ''' Foo hashs password entered by user '''
    password = 'kn485' + password + 'bn12mzx09'
    password = password.encode('utf-8')
    password = hashlib.sha256((password)).hexdigest()
    salt = password[3:6]
    salt = salt.encode('utf-8')
    password = password.encode('utf-8')
    hashed_password = hashlib.pbkdf2_hmac(
        hash_name='sha256', password=password, salt=salt, iterations=100000)
    return(hashed_password.hex())

# Now hashing is "static", next step would be making hashing more dynamic: 
# personal salt for every password, that is not (!) depends on entered symbols (!).  