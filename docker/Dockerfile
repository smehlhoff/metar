FROM ubuntu:latest

# Install required packages
RUN apt-get update \
    && apt-get install -y \
        cron \
        sudo \
        nano \
        git \
        python3.11 \
        python3.11-venv \
        openssh-server \
        iputils-ping \
    && apt-get clean

# Configure SSH
RUN ssh-keygen -A \
    && mkdir -p /run/sshd

# Copy entrypoint script and set permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose SSH port
EXPOSE 22

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
