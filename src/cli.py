
from datetime import datetime
import logging
from os import popen
from typing import Literal

from src import AccountNotFound


class MullvadCLI:
    """A wrapper for the Mullvad CLI Api."""

    def __init__(self) -> None:
        self.path = "mullvad"
        self.log = logging.getLogger("mullvad.cli")
        self.__log__()
        self.status = popen(f"{self.path} status").read()
        self.is_connected = "Connected" in self.status


    def __log__(self):
        logformat = '%(asctime)s %(module)12s:%(lineno)-4s %(levelname)-9s %(message)s'
        loglevel = 'INFO'
        loghandler = logging.NullHandler()
        loghandler.setFormatter(logging.Formatter(logformat))
        self.log.addHandler(loghandler)
        self.log.setLevel(loglevel)
        self.log.info("Started Logging Mullvad.")


    def version(self) -> str:
        """Return the version of the mullvad client

        Returns:
            str: the version of the mullvad client
        """
        return popen("mullvad -V").read()


    def status(self) -> bool:
        """Get the status."""
        self.status = popen(f"{self.path} status").read()
        self.log.info(self.status)


############## Account Calls ###############
    def account_info(self) -> dict:
        """Get the account info

        Raises:
            AccountNotFound: If you aren't Logged in

        Returns:
            dict: {
                Mullvad account: <token>
                Expires at: <datetime_object>
                Device name: <client_name>
            }
        """
        temp = popen(f"{self.path} account get").read()
        if "Not logged in" in temp:
            raise AccountNotFound("Not logged in on any account")
        d = temp.splitlines()
        ret = {}
        for _ in d:
            tmp = _.split(":")
            if not _.startswith("Expir"):
                ret.update({tmp[0]: tmp[1].strip()})
            else:
                ret.update({tmp[0]: datetime.fromisoformat(tmp[1].strip())})
        return ret


    def login(self, token:int) -> str:
        """Log into the API

        Args:
            token (int): Your account token for mullvad

        Raises:
            AccountNotFound: If the account does not exist.

        Returns:
            str: returns the account it was added to in the format of `Mullvad account "<token>" set`
        """
        temp = popen(f"{self.path} account login {token}").read()
        if "Error: " in temp:
            raise AccountNotFound("Account Not Found, sorry")
        return temp


    def logout(self) -> str:
        """Logout of the Client

        Returns:
            str: Removed device from Mullvad account
        """
        return popen(f"{self.path} account logout").read()


############ Auto-connect Calls ############
    def get_auto_connect(self) -> str:
        """Gets the auto connect status

        Returns:
            str: Autoconnect: <status>
        """
        return popen("mullvad auto-connect get").read()


    def set_auto_connect(self, status:Literal["on","off"]) -> str:
        """Set the auto connect to On/Off

        Args:
            status (Literal[&quot;on&quot;,&quot;off&quot;]): what status to set the autoconnect to

        Returns:
            str: Successfully set the auto-connect to: <status>
        """
        popen(f"mullvad auto-connect set {status}")
        return f"Successfully set the auto-connect to: `{status.capitalize()}`"


############## Lockdown Calls ##############
    def get_lockdown_mode(self) -> str:
        """Block traffic when the VPN is disconnected?

        Returns:
            str: Block traffic when the VPN is disconnected: <status>
        """
        return popen("mullvad lockdown-mode get").read()


    def set_lockdown_mode(self, status:Literal["on","off"]) -> str:
        """Set the lockdown mode

        WARNING
        If you are on a remote server and trigger this, there will be NO way to turn 
        it off if you run the disconnect command, or are already disconnected
        This means you will be kicked out of the server.

        Args:
            status (Literal[&quot;on&quot;,&quot;off&quot;]): What you want to set lockdown mode too

        Returns:
            str: Successfully set the lockdown-mode to: <status>
            
        """
        popen(f"mullvad lockdown-mode set {status}")
        return f"Successfully set the lockdown-mode to: `{status.capitalize()}`"


################ DNS Calls #################
    def get_dns(self):
        ...
        # TODO: Implement this
    
    def set_dns(self, type, *dns_servers):
        ...
        # TODO: Implement this


################ LAN Calls #################
    def get_lan(self):
        ...
        # TODO: Implement this
    
    def set_lan(self, status: Literal["allow","block"]):
        ...
        # TODO: Implement this

############# Connection Calls #############
    def connect(self) -> bool:
        """Connect to the relay."""
        if self.is_connected:
            self.log.info("Already Connected")
            return False
        self.is_connected = True
        tmp = popen(f"{self.path} connect").read()
        if "Warning" in tmp:
            raise AccountNotFound(tmp)
        
        self.log.info("Connecting...")
        return True

    def reconnect(self) -> bool:
        """Connect to the relay."""
        if self.is_connected:
            self.log.info("Already Connected")
            return False
        self.is_connected = True
        tmp = popen(f"{self.path} connect").read()
        if "Warning" in tmp:
            raise AccountNotFound(tmp)
        
        self.log.info("Connecting...")
        return True


    def disconnect(self) -> bool:
        """Disconnect from the relay

        Returns:
            bool: If the connection **Changed**  if the server was already disconnected it returns False.
        """
        if not self.is_connected:
            self.log.info("Not connected")
            return False
        self.is_connected = False
        popen(f"{self.path} disconnect")
        self.log.info("Disconnecting...")
        return True


############### Bridge Calls ###############
    def get_bridge(self):
        ...
        # TODO: Implement this
        
    def set_bridge_state(self, type: Literal["auto","on","off"],):
        ...
        # TODO: Implement this

        # TODO The Rest: "location","custom-list","provider","ownership","custom"
        
    def set_bridge_location(self, location: Literal[""]):
        ...
        # TODO: everything

    def list_bridge(self):
        ...
        # TODO: Implement this

############### Relay Calls ################


################ API Access ################


############ Obfuscation Calls #############


############ Split Tunnel Calls ############


############### Tunnel Calls ###############


########### Factory Reset Calls ############


