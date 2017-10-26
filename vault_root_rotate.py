#!/usr/bin/python

"""
:maintainer: 
    :maturity: 2017.7.0
    :requires: HVAC
    :platform: centOS

This module facilitates the generation of a new root token and writes it to the root path within Vault.
It also takes a hash of that root value and saves it at the kickstart path.
"""
try:
    import hvac
    import os
    import string
    import random
    from passlib.handlers.sha2_crypt import sha512_crypt
except ImportError, imperr:
    err_list = str(imperr).split(' ')
    print 'Unable to import module: ' + err_list[3]
    print 'Please install the ' + err_list[3] + ' module for Python.'
    sys.exit()

## PUBLIC FUNCTIONS ##
token_dir = os.getenv("HOME") + "/.vault-token"
vault_token = open(token_dir).read()
client = hvac.Client(url='https://vault', token=vault_token)

def root_rotate():
    '''
    Generates new root token with hash to be saved in vault.
    '''


    if  os.path.isfile(token_dir):
        vault_data = _getVaultData()
        current_passwords = vault_data[0]
        current_hashes = vault_data[1]
        new_root_value = _genRandom()
        hashed_current = _genHash(new_root_value)
        _updateVault(current_passwords, current_hashes, new_root_value, hashed_current)
        return "Password has been updated!"
    else:
        return "Please Authenticate with Vault before running this CLI tool."

## PRIVATE FUNCTIONS ##


def _genHash(secret):
    '''
    Generate a new hash for new root value.
    '''

    hash_secret = sha512_crypt.encrypt(secret, salt_size=16, rounds=5000)

    return hash_secret

def _genRandom():
    '''
    Generate a Random String of Characters
    '''

    chars = string.letters + string.digits + '!@#%^&'
    random.seed = (os.urandom(1024))
    random_string = ''.join(random.SystemRandom().choice(chars) for _ in xrange(32))

    return random_string

def _getVaultData():
    '''
    Get current vault data to be updated
    '''

    passwords = client.read('secret/root/plain')['data']
    hashes = client.read('secret/root/hash')['data']
    hashes_list = _parsePasswords(hashes)
    password_list = _parsePasswords(passwords)

    return [password_list, hashes_list]

def _parsePasswords(passwords):
    '''
    Check for the current password and all 5 last passwords.
    '''

    current = passwords['password']
    last = passwords['lastpass']
    last1 = passwords['lastpass1']
    last2 = passwords['lastpass2']
    last3 = passwords['lastpass3']
    last4 = passwords['lastpass4']
    parsed_values = [current, last, last1, last2, last3, last4]

    return parsed_values

def _updateVault(current_passwords, current_hashes, new_root_value, hashed_current):
    '''
    Update Vault with new values, moving old values to old slots.
    '''

    client.write('secret/root/plain', password=new_root_value, lastpass=current_passwords[0], lastpass1=current_passwords[1], lastpass2=current_passwords[2], lastpass3=current_passwords[3], lastpass4=current_passwords[4],)
    client.write('secret/root/hash', password=hashed_current, lastpass=current_hashes[0], lastpass1=current_hashes[1], lastpass2=current_hashes[2], lastpass3=current_hashes[3], lastpass4=current_hashes[4],)
    client.write('secret/kickstart/root_hash_prod', password_hash=hashed_current)

if __name__ == "__main__":
    print root_rotate()
