# A simple Python Based Mullvad Interface. 
------------------
Using commandline utils for interacting and using vpn

# How to use?
------------------
```py
from mullvad import MullvadCLI, AccountNotFound

connector = MullvadCLI()
###
try:
    connector.account_info()
except AccountNotFound:
    ### This means you aren't signed in
    connector.login(<Token>)

connector.connect() # Initialize the connection, will raise the AccountNotFound if you are not logged in.
connector.status() # Updates the status, it can report the wrong information if you call to soon after disconnecting/connecting
connector.disconnect() # Deconnect from the relay
```