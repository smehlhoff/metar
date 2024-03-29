#!/bin/bash

# Add user and set password
useradd -m $SERVER_USERNAME && \
    echo "$SERVER_USERNAME:$SERVER_PASSWORD" | chpasswd

# Make the user a root user
usermod -aG sudo $SERVER_USERNAME

# Change default shell for user
usermod -s /bin/bash $SERVER_USERNAME

# Start SSH daemon
/usr/sbin/sshd -D
