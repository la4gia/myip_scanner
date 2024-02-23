# myip_scanner

run with ```python3 myip_scanner.py```

## flow
Script runs "curl ifconfig.me" for the current IP address. If the pulled IP address is different from what is stored in ip_address.txt or if the file does not exist, the file is updated/created and the new IP address is emailed via gmail.

## prerequisites
* Need to configure gmail app password
* store both the email and password as environment variables
