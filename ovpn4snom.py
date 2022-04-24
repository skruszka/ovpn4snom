#!/usr/bin/python3
####################################################################
# Requirements:
# /usr/bin/python3
# pip3 install python-gnupg
####################################################################
import argparse
import getpass
import os, sys, stat
import tarfile

# Create Argparse arguments
parser = argparse.ArgumentParser(description='Create openvpn configuration, certificates, key and tarball for snom VoIP phones with OpenVPN firmware')
parser.add_argument('-A', '--auth', help='Create file for user credential for authentication', action='store_true')
parser.add_argument('-p', '--passwd', help='Password of the authentication user', type=str, nargs=1)
parser.add_argument('-u', '--username', help='Username of the authentication user', type=str, nargs=1)
parser.add_argument('-f', '--file', help='Filename of the ovpn file, default file is client.ovpn', nargs=1, type=str, default="client.ovpn")
parser.add_argument('-v', '--verbose', help='Enables verbose output', action='store_true')
args = parser.parse_args()

# Define functions
################################################################
# Read certificates block out of the ovpn file
def readcertfromovpn(file, start, stop):
    doprint = False
    file = open(file, 'r')
    lines = file.readlines()
    for line in lines:
        if line.startswith(start):
            doprint = True
        elif line.startswith(stop):
            doprint = False
        elif doprint:
            yield line

# Read certificates informations out of the certificates block of the ovpn file
def writecert(lines, start, stop, filename):
    file = open(filename, "w")
    # Defined trigger
    doprint = False
    for line in lines:
        if line.startswith(start):
            doprint = True
            file.write(line)
        elif line.startswith(stop):
            doprint = False
            file.write(line)
        elif doprint:
            file.write(line)
    file.close()
    # Set root only priviliges to file
    rootonly('./' + filename)

# create vpn.cnf out of the ovpn file
def createconf(file, auth):
    # Defined some trigger
    dowrite = True
    authset = False
    caset = False
    certset = False
    keyset = False
    pingset = False
    pingrestartset = False
    # Read ovpn file
    file = open(file, 'r')
    # Create vpn.cnf file
    conf = open('vpn.cnf', 'w')
    lines = file.readlines()
    for line in lines:
        if line.startswith('<'):
            dowrite = False
        # Set auth-user-pass to /penvpn/login if defined in ovpn file
        elif line.startswith('auth-user-pass'):
            if auth:
                # Write to fie if -A/--auth is set
                conf.write('auth-user-pass /openvpn/login.cnf' + "\n")
                # Set trigger to True
                authset = True
        # Set ping to 10 if defined in ovpn file
        elif line.startswith('ping '):
            conf.write('ping 10' + "\n")
            pingset = True
        # Set ping-restart to 60 if defined in ovpn file
        elif line.startswith('ping-restart'):
            conf.write('ping-restart 60' + "\n")
            pingrestartset = True
        # Set ca to /openvpn/ca.crt if defined in ovpn file
        elif line.startswith('ca'):
            conf.write('ca /openvpn/ca.crt' + "\n")
            caset = True
        # Set cert to /openvpn/client.crt if defined in ovpn file
        elif line.startswith('cert'):
            conf.write('cert /openvpn/client.crt' + "\n")
            certset = True
        # Set key to /openvpn/client.key if defined in ovpn file
        elif line.startswith('key'):
            conf.write('key /openvpn/client.key' + "\n")
            keyset = True
        # Withdraw this line in configuration
        elif line.startswith(' '):
            pass
        # Withdraw this line in configuration
        elif line.startswith('reneg-sec'):
            pass
        # Withdraw this line in configuration
        elif line.startswith('verify-x509-name'):
            pass
        # Withdraw this line in configuration
        elif line.startswith('route remote_host 255.255.255.255 net_gateway'):
            pass
        elif dowrite:
            conf.write(line)
    # Create this configuration if not present and argument -A/--auth is set
    if auth and not authset:
        conf.write('auth-user-pass /openvpn/login.cnf' + "\n")
    # Create this configuration if not present
    if not caset:
        conf.write('ca /openvpn/ca.crt' + "\n")
    # Create this configuration if not present
    if not certset:
        conf.write('cert /openvpn/client.crt' + "\n")
    # Create this configuration if not present
    if not keyset:
        conf.write('key /openvpn/client.key' + "\n")
    # Create this configuration if not present
    if not pingset:
        conf.write('ping 10' + "\n")
    # Create this configuration if not present
    if not pingrestartset:
        conf.write('ping-restart 60' + "\n")
    conf.close()
    file.close()
    # Set root only priviliges to file
    rootonly('./vpn.cnf')

# Function to set root only priviliges to file
def rootonly(file):
    # Set permission to 0700
    os.chmod(file, stat.S_IRWXU)
    # Set owner and group to root
    os.chown(file, 0, 0)

# Function to create the tarball for snom phones
def createtarball(username):
    if not username == 'client':
        # Use username as filename for tarball if set
        tarfilename = str(username + ".tar")
    else:
        # Use client.tar as default file name for tarball
        tarfilename = 'client.tar'
    file = tarfile.open(tarfilename, "w")
    # Add all necessary files to tarball
    files = ['vpn.cnf', 'ca.crt', 'client.crt', 'client.key']
    for item in files:
        file.add(item)
    # Add login.cnf to tarball if -A/--auth is set
    if not username == 'client':
        file.add('login.cnf')
    file.close()

# Function to cleanup files not needed anymore
def cleanup():
    files = ['vpn.cnf', 'ca.crt', 'client.crt', 'client.key', 'login.cnf']
    for item in files:
        if os.path.exists(item):
            # ↓ Delete file, ↑ if exists
            os.remove(item)

# Main
################################################################
# Check if argument -A/-auth is set, get credentials and write to login.cnf
if args.auth and not args.username:
    print("error on dependency: the argument -u/--username is depended by argument -A/--auth")
    sys.exit(1)
elif args.auth:
    # Check if password is set via -p/--passwd
    if args.passwd:
        password = args.passwd
    # Get password if argument -p/--passwd is missing
    else:
        pswd = getpass.getpass('Enter passphrase:')
        password = pswd
    # Write credentials to login.cnf
    with open('login.cnf', "w") as login:
        for item in args.username:
            login.write(item + "\n")
        if args.passwd:
            for item in password:
                login.write(item + "\n")
        else:
            login.write(password)
    login.close()
    # Set root only priviliges to file
    rootonly('./login.cnf')

# Create all certificates, keys and configuration files
# Create vpn.cnf file
createconf(args.file, args.auth)
# Create ca.crt file
writecert(readcertfromovpn(args.file, '<ca>', '</ca>'), '-----BEGIN CERTIFICATE-----', '-----END CERTIFICATE-----', "ca.crt")
# Create client.crt file
writecert(readcertfromovpn(args.file, '<cert>', '</cert>'), '-----BEGIN CERTIFICATE-----', '-----END CERTIFICATE-----', "client.crt")
# Create client.key file
writecert(readcertfromovpn(args.file, '<key>', '</key>'), '-----BEGIN PRIVATE KEY-----', '-----END PRIVATE KEY-----', "client.key")

# Create tarball, set username as filename for tarball if set
if args.auth:
    for item in args.username:
        createtarball(item)
else:
    createtarball('client')

# Delete all unnecessary files
cleanup()
