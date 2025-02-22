# SLHP Data Warehousing

## database_connector
This module contains the connectors neccessary to connecto to either databricks or Sql Server. 

## environment_setup
This module contains a function which will setup a sample folder structure and files of how a flask application should interact. 

## active_directory
This module contains a class that can help you authenticate with the active directories associated with you SQL database. It reads the groups from the users associated to that database and looks up those AD groups then returns the usernames of those associated with the groups. To validate, check and see if the username of the user is in the returned list. If so, they are able to access the applcation. 