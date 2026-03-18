#!/bin/bash
set -e

# Support for Debian 9, 10, 11, 12, 13
if ! [[ "9 10 11 12 13" == *"$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2 | cut -d '.' -f 1)"* ]];
then
    echo "Debian $(grep VERSION_ID /etc/os-release | cut -d '"' -f 2 | cut -d '.' -f 1) is not currently supported.";
    exit;
fi

# Download the package to configure the Microsoft repo
curl -sSL -O https://packages.microsoft.com/config/debian/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2 | cut -d '.' -f 1)/packages-microsoft-prod.deb
# Install the package
sudo dpkg -i packages-microsoft-prod.deb
# Delete the file
rm packages-microsoft-prod.deb

# Install dependencies and the driver
sudo apt-get update
sudo apt-get install -y unixodbc-dev
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
