#!/bin/bash

# Ensure a virtual environment
if [ ! -d "env" ]; then
    python3 -m venv venv
fi

# Source the virtual environment
source ./venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npx -y pnpm install

# Install Go dependencies
# go install app/pocketbook.go
go mod tidy

# Add project bin to $PATH
if [ -d "./scripts" ] && [[ ":$PATH:" != *":./scripts:"* ]]; then
    PATH="${PATH:+"$PATH:"}./scripts"
    chmod ug+x ./scripts/*
fi

# Print message
echo -e "\033[38;5;48m(Done)\033[0m"