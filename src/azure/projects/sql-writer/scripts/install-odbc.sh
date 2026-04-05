#!/bin/bash
set -e

# Ref: https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver17&tabs=alpine18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline
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
