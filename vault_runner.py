#!/usr/bin/python
"""
:maintainer: 
    :maturity: 2017.6.0
    :requires: hvac
    :platform: centOS
"""
from __future__ import absolute_import

import salt.config
import salt.wheel
import salt.client
import hvac
import crypt
import logging

opts = salt.config.master_config('/etc/salt/master')
salt_wheel = salt.wheel.WheelClient(opts)
salt_client = salt.client.LocalClient()
salt_caller = salt.client.Caller()

up_to_date = []
updated = []
failed = []


def __virtual__():
    return 'vault_runner'


log = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
log.addHandler(ch)


def my_log(msg, level):
    message = 'VAULT_RUNNER: ' + msg
    if level == 'error':
        log.error(message)
    else:
        log.warning(message)


def get_vault_password():
    vault_token = salt_caller.cmd('pillar.get', 'vault_read_root')['read_root_token']
    vault_token = vault_token.split('\n')[0]
    client = hvac.Client(url='https://vault', token=vault_token)
    password = client.read('secret/root/plain')['data']['password']
    return password


def get_pw_hashes(user):
    '''
    Gets the password hash of the user for each minion and returns them to
    the saltmaster
    Actually returns the entire line for the user from the shadow file
    '''
    minion_passwd = {}
    accepted_minions = salt_wheel.cmd('key.list', ['accepted'])
    for accepted, minions in accepted_minions.iteritems():
        for minion in minions:
            minion_hash = salt_client.cmd(minion, 'shadow.info', [user])
            if bool(minion_hash) == True:
                hashstring = minion_hash[minion]['passwd']
                minion_passwd[minion] = hashstring
            else:
                result = salt_client.cmd(minion, 'test.ping')
                if bool(result) == True:
                    result = "Unknown error"
                    my_log("Password for {0} was not updated. Result: {1}".format(minion, result), "error")
                    failed.append(minion)
                else:
                    result = "Minion did not return test.ping"
                    my_log("Password for {0} was not updated. Result: {1}".format(minion, result), "error")
                    failed.append(minion)
    return minion_passwd

def compare_hash(minion, hashstring, password):
    '''
    (for each minion)
    Hashes the password pulled from vault, and compares that with the hash
    from the minion
    If hashes are different, call state to update password to the one from the
    external pillar and return output from the minion
    '''
    hash_array = hashstring.split('$')
    if hash_array[0] == "*LOCK*":
        result = "Minion returned a locked shadow file, please remediate."
        my_log("Password for {0} was not updated. Result: {1}".format(minion, result), "error")
        failed.append(minion)
    else:
        algorithm_identifier = hash_array[1]
        # supported algoritm identifiers are 1, 5, and 6
        if algorithm_identifier not in ['1', '5', '6']:
            failed.append(minion)
            my_log("{0} uses an unsupported hashing algorithm".format(minion), "error")
        else:
            salt = hash_array[2]

            # outputs entire password section of line in shadow file
            hashed_password = crypt.crypt(password, '${0}${1}$'.format(algorithm_identifier, salt))

            if hashstring == hashed_password:
                up_to_date.append(minion)
            else:
                # generates new salt for the new password hash, based on minion hashing algorithm
                if algorithm_identifier == '6':
                    newsalt = crypt.mksalt(crypt.METHOD_SHA512)
                elif algorithm_identifier == '5':
                    newsalt = crypt.mksalt(crypt.METHOD_SHA256)
                else:  # only remaining option is that algorithm_identifier = 1
                    newsalt = crypt.mksalt(crypt.METHOD_MD5)
                new_password_hash = crypt.crypt(password, newsalt)
                # run salt command to update password, collect output
                result = salt_client.cmd(minion, 'shadow.set_password', ['root', hashed_password])
                if result[minion] is True:
                    updated.append(minion)
                else:
                    my_log("Password for {0} was not updated. Result: {1}".format(minion, result[minion]), "error")
                    failed.append(minion)


def update_password():
    # run with `salt-run vault_runner.update_password` on saltmaster
    password = get_vault_password()
    user = 'root'
    minionDict = get_pw_hashes(user)
    for minion in minionDict:
        compare_hash(minion, minionDict[minion], password)
    my_log("Password already up-to-date on the following minions: {0}".format(up_to_date), "log")
    my_log("Password updated on the following minions: {0}".format(updated), "log")
    my_log("\nPassword update FAILED on the following minions: {0}".format(failed), "error")
    return True
