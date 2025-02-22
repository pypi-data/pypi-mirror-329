from ldap3 import Server, Connection, ALL, NTLM
from sqlalchemy import text

class ActiveDirectoryManager:
    def __init__(self, server, domain, sqlalchemy_engine,verbose:bool):
        '''
        Parameters:
            - server: the server where your AD groups are located
            - domain: domain in which to search for the AD groups
            - sqlalchemy_engine: used to run the query, use with app.context() to run this portion
            - verbose: if you want detailed logging of what is happening in the backend
        '''
        self.server = server
        self.domain = domain
        self.engine = sqlalchemy_engine
        self.username = None
        self.password = None
        self.verbose = verbose

    def set_unp(self, username, password):
        """
        Set the username and password for authentication.
        """
        self.username = username
        self.password = password

    def authenticate_user(self, username, password):
        """
        Authenticate a user against the Active Directory server.
        """
        try:
            # Connect to the LDAP server
            server = Server(self.server, get_info=ALL)
            conn = Connection(
                server,
                user=f"{self.domain}\\{username}",
                password=password,
                authentication=NTLM,
                auto_bind=True
            )
            conn.unbind()
            return True  # Authentication successful
        except Exception as e:
            print(f"Authentication Error: {e}")
            return False

    def get_user_security_groups(self):
        """
        Authenticate the user and get their security group memberships.
        """
        try:
            # Retrieve the list of security groups from the database
            db_groups = self._get_ad_groups_from_db()
            if not db_groups:
                print("No security groups retrieved from the database.")
                return []
            if self.verbose:
                print(f'Groups returned:{db_groups}')
            # Connect to the LDAP server
            server = Server(self.server, get_info=ALL)
            conn = Connection(
                server,
                user=f"{self.domain}\\{self.username}",
                password=self.password,
                authentication=NTLM,
                auto_bind=True
            )

            # Construct the search filter for multiple groups
            for group in db_groups:
                # Format the group names into the right format for 'memberOf' filter
                group = str(group).split('\\')[1]
                group_dn = f"OU=SL1 Security Groups,DC={self.domain.replace('.', ',DC=')}"
                if self.verbose:
                    print(group_dn, group)
                # Perform the search to find the group and its members
                conn.search(
                    search_base=group_dn,
                    search_filter=f"(CN={group})",  # Search for the group in AD
                    attributes=['member']  # Get the 'member' attribute (the list of users)
                )
                
                # If the group is found and contains members
                if self.verbose:
                    print(conn.entries)
                user_groups = []
                if conn.entries:
                    if self.verbose:
                        print('Entries: ',conn.entries[0])
                    members = conn.entries[0].member.values  # Extract all members from the 'member' attribute
                    
                    for member in members:
                        # Perform a search for each member to get their sAMAccountName
                        if self.verbose:
                            print('Searching for member: ',member)
                        member = member.split(',',1)
                        conn.search(
                            search_base=member[1],
                            search_filter=f"({member[0]})",
                            attributes=['sAMAccountName']
                        )
                        
                        # Collect the sAMAccountName for each member
                        if conn.entries:
                            user_groups.append(conn.entries[0].sAMAccountName.value)
                    
                    conn.unbind()  # Clean up connection after the search
               
                    
                return user_groups

        except Exception as e:
            print(f"LDAP Error: {e}")
            return []


    def _get_ad_groups_from_db(self):
        """
        Retrieve metadata about users and roles with access to the database.
        """
        metadata = []
        try:
            query = """
            SELECT distinct
                dp.name AS database_user
            FROM 
                sys.database_principals AS dp
            LEFT JOIN 
                sys.database_permissions AS p ON dp.principal_id = p.grantee_principal_id
            LEFT JOIN 
                sys.objects AS o ON p.major_id = o.object_id
            WHERE 
                dp.name like'sl1%' -- Exclude system users
                AND dp.type IN ('S', 'U', 'G') -- S: SQL user, U: Windows user, G: Database role
            ORDER BY 
                dp.name
            """
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                metadata = [row.database_user for row in result]
        except Exception as e:
            print(f"Error retrieving database metadata: {e}")
        return metadata
