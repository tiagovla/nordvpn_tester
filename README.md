# Nordvpn Tester
This script tests a file with nordvpn credentials.

#### Input:
A file containing the credentials in the following format.

nordvpnlist.txt:

```
email0@example.com:password0
email1@example.com:password1
email2@example.com:password2
```
#### Output:
A file containinig the working the credentials, time in seconds to expire and number of users logged in.

working_accs.txt:
```
email0@example.com:password0 41234 0/6
email2@example.com:password2 34122 1/6
```


