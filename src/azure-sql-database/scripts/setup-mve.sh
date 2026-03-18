#!/bin/bash
set -e

# sudo apt-get update
# sudo apt-get install -y curl gnupg2 unixodbc-dev

# # Install Microsoft ODBC Driver 18 for SQL Server
# if ! dpkg -l | grep -q msodbcsql18; then
#     curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
#     curl https://packages.microsoft.com/config/debian/12/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
#     sudo apt-get update
#     sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
# fi


if ! [[ "18.04 20.04 22.04 24.04 25.10" == *"$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)"* ]];
then
    echo "Ubuntu $(grep VERSION_ID /etc/os-release | cut -d '"' -f 2) is not currently supported.";
    exit;
fi

# Download the package to configure the Microsoft repo
curl -sSL -O https://packages.microsoft.com/config/ubuntu/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)/packages-microsoft-prod.deb
# Install the package
sudo dpkg -i packages-microsoft-prod.deb
# Delete the file
rm packages-microsoft-prod.deb

# Install the driver
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18


(curl https://mise.run | sh)
export PATH="$HOME/.local/bin:$PATH"

mise install -y
mise run setup
mise run init-sql