
# Import the appropriate library here

# You can define a customized query class here and an abstract method query().

class MysqlBase:
    """
    This database is a palantir database
    """
    id = "" # source uuid
    credential = {
        "host": "",
        "port": "",
        "username": "",
        "password": "",
        "database_name": "",      
    } # credential to connect to source

    def connect(self)-> any:
        """
        return customize query class
        """
        print("connect to", self.credential["host"])
        return "connected"

    def disconnect(self) -> bool:
        return True   

    def connect_orm(self, isPoolConnection: bool):
        """
        return orm library connection to client
        """
        return "lib_connection_here"    
    
    def get_info(self) -> str:
        """
        get source information from sdk server, low priority
        """
        return ""
