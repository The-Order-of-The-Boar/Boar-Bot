class boarPostgre():
    """Python wrapper class created using psycopg2 library to connect to a PostgreSQL server and 
    executes basic operations in a simplified way.
    """

    import psycopg2

    credentials = {}
    def __init__(self,host:str,database:str,user:str,password:str,port:int):
        """Saves the database credentials and tests the connection"""
        self.credentials["host"] = host
        self.credentials["dabatase"] = database
        self.credentials["user"] = user
        self.credentials["passworld"] = password
        self.credentials["port"] = port
        
        if self._get_connection() != None:
            print("Sucessful database connection")


###############################INTERNAL  FUNCTIONS###########################################
    def _get_connection(self):
        """Returns a open connection with the database"""
        try:
            con = self.psycopg2.connect(
                host=    self.credentials["host"],
                database=self.credentials["dabatase"],
                user=    self.credentials["user"],
                password=self.credentials["passworld"],
                port=    self.credentials["port"])
            return con
        except Exception as  error:
            print(error)
            return None

    def _cursor_execute(self,com,request=False):
        """Connects to the databse and execute the string 'com'"""
        db = self._get_connection()
        cursor = db.cursor()
        cursor.execute(com)
        request_data = None
        if request:
            request_data = cursor.fetchall()
        cursor.close()
        db.commit()
        db.close()
        return request_data
########################CUSTOM FUNCTIONS#################################################

    def custom_insert(self,query:str):
        """Executes the query you send without return
        Usage:custom_insert(String:query text)
        Example:custom_insert(INSERT INTO User VALUES(Leonardo,32,"lalalal") ON CONFLICT DO SET Age=User.Age+1) 
        """
        self._cursor_execute(query)

    def custom_retrieve(self,query:str):
        """Executes the query you send with return
        Usage:custom_retrieve(String:query text)
        Exemple:custom_retrieve(SELECT Name FROM User ORDER BY Age ASC LIMIT 10)
        """
        return self._cursor_execute(query,True)


########################Crud - 'CREATE' FUNCTIONS#################################################

    def create_table(self,name:str,colluns:list):
        """Creates a new table\n
        Usage: create_table(String:"name of the table",List:[Colluns of the table]) \n
        Example: create_table("User",[["Name","VARCHAR(255) PRIMARY KEY"],["Age", INTEGER"],["Password", "VARCHAR(33)"]])\n
        The first argument is the table name;the second argument is a list of strings, 
        each string representing one collum of the new table\n
        """
        #String command formatting
        command = f"Create table {name}("
        for collum in colluns:
            command += f"{collum[0]} {collum[1]},"
        command = command[:-1] + ")"
        print(command)

        #Connection to database and command execution via cursor
        self._cursor_execute(command)


    def insert_value(self,table:str,values:list,ignore_on_conflicts:bool=False,additional:str=""):
        """Inserts a new row in a given table\n
        Usage: insert_value("name of the table",["value1","value2","value3"....])\n
        Example: insert_value("User",["Leonardo","38","pass123"])\n
        The first argument is a string with the name of the table where the values will be inserted;
        The second argument is a list, containing the one value for each of the table's colluns;
        The third argument is optional, it adds the "ON CONFLICT IGNORE" that is used to avoid errors in duplicated
        primary keys 
        """
        #String command formatting
        command = f"Insert into {table}"

        #Concatenates the list of values
        values_data = "("
        for value in values:
            values_data+= f"'{value}',"
        values_data = f" {values_data[:-1]} )" 

        command += f" VALUES {values_data}"
        if ignore_on_conflicts:
            command += " ON CONFLICT DO NOTHING"
        
        command+= additional

        #Connection to database and command execution via cursor
        self._cursor_execute(command)


########################cRud - 'READ' FUNCTIONS#################################################
    def retrieve_table(self,name):
        """Returns an entire table\n
        Usage: retrieve_table("String:"name of the table")\n
        Example: retrieve_table("User")\n
        The only argument is the table name\n
        """
        #String command formatting
        command = f"Select * from {name}"

        #Connection to database,command execution via cursor and requisition return
        query = self._cursor_execute(command,request=True)
        return query
    
    def retrieve_collum(self,table:str,collum:str):
        """Returns an entire collum from a especific table\n
        Usage: retrieve_collum(String:"name of the table",String:"name of the collum")\n
        Example: retrieve_collum("User","Age")\n
        The first argument is the table name;The second argument is the collum name\n
        """
        #String command formatting
        command = f"Select * from {table}"

        #Connection to database,command execution via cursor and requisition return
        query = self._cursor_execute(command,request=True)
        return query

    def retrieve_value(self,table:str,collum:str,condition:list):
        """Returns all values inside the given table and collum that satisfies the condition \n
        Usage: retrieve_value(String:"name of the table",String: "name of the collum",
        List["condition collum name","condition row value"]) \n
        Example: retrieve_value("User","Password",["Age","38"])\n
        The first argument is the table name;The second argument is the collum name;
        The third argument is the value and his corresponding collum that will be searched
        """
        

        #String command formatting
        command = f"Select {collum} from {table} where {condition[0]} = '{condition[1]}'"

        #Connection to database,command execution via cursor and requisition return
        query = self._cursor_execute(command,request=True)
        return query

########################crUd - 'UPDATE' FUNCTIONS#################################################


    def update_value(self,table:str,old_value:list,new_value:list):
        """Updates specific values from a given row\n
        Usage: update_value(String:"name of the table",List["condition collum name","condition row value"],
        List["collum to be updated","value to be inserted"])\n
        Example: update_value("User",["name","Leonardo"],["Age","45"])\n
        The first argument is the table name;the second argument is a list,index 0 being  the name of the
        collum which the value will be searched, index 1 being the value that will be updated;
        the third argument is a list, index 0 being the collum where the new value will be placed,index 1 being the 
        new value that will replace the old value
        """
        
        #String command formatting
        command = f"Update {table} set {new_value[0]} = '{new_value[1]}' Where {old_value[0]} = '{old_value[1]}'"
        
        #Connection to database and command execution via cursor
        self._cursor_execute(command)
    
        


########################cruD - 'DELETE' FUNCTIONS##################################################
    def delete_value(self,table:str,collum:str,value:str):
        """Deletes a row in a specific collum where the value is equal the given one\n
        Usage: delete_value(String:"name of the table","condition collum name","condition row value)\n
        Example: delete_value("User","Age","45")
        The first argument is the table name; the second argument is the collum where the value will be searched;
        the third argument is the value that identificies the row that will be deleted
        """
        #String command formatting
        command = f"Delete from {table} where {collum} = '{value}'"

        #Connection to database and command execution via cursor
        self._cursor_execute(command)

########################CRUD Object########################################################################

db = boarPostgre("SECRET",5432)
####################################################################################################################