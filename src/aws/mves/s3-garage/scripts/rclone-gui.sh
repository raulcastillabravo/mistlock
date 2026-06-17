#!/usr/bin/env bash
mise exec -- rclone --config="config/rclone.conf" rcd --rc-web-gui --rc-no-auth --rc-web-gui-no-open-browser
