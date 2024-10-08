import sqlite3
import pandas as pd
import numpy as np
from scipy.stats import f

def myANOVA(grid, alpha):
    # Calculate the grand mean (GM)
    GM = np.mean(grid)

    # Calculate group means
    groupMeans = np.zeros(len(grid))
    for i in range(len(grid)):
        groupMeans[i] = np.mean(grid[i])
        
    # Initialize sum of squares
    SStotal = 0
    SSWG = 0
    SSBG = 0

    # Calculate sum of squares
    for i in range(len(grid)):
        SSBG += len(grid[i]) * (groupMeans[i] - GM)**2
        for j in range(len(grid[i])):
            SStotal += (grid[i, j] - GM)**2
            SSWG += (grid[i, j] - groupMeans[i])**2

    # Degrees of freedom
    DFtotal = grid.size - 1
    DFBG = len(grid) - 1
    DFWG = grid.size - len(grid)

    # Variance between groups and within groups
    varBG = SSBG / DFBG
    varWG = SSWG / DFWG

    # Calculate the F-statistic
    myF = varBG / varWG

    # Get the critical F-value using the F-distribution CDF (f.ppf)
    Fstat = f.ppf(1 - alpha, DFBG, DFWG)

    # Compare F-statistic with the critical F-value to make the decision
    if myF > Fstat:
        result = "There is a statistically significant difference between the groups!"
    else:
        result = "There is no evidence for a significant difference between the groups."
    
    # Return three values: result, F-statistic, and critical F-value
    return result, myF, Fstat


# define the sqlquery function to execute a given SQL query on a given SQL database connection

def sqlquery(connection,prompt):
    try:
        cur = connection.cursor() # try to create a cursor for an SQL query
        cur.execute(prompt) # prompt parameter is fed in as SQL query
        results = cur.fetchall() # store all results from the query in a variable
        if len(results) > 0: # if the query returned a nonzero number of results
            return results # return the results
        else:
            return "No results found." # return the message that no data entry matched the query
        
    except sqlite3.Error as e:
        print(f"SQL query execution error: {e}") # print error message if the SQL query cannot be performed

fileName = "/Users/owais/Desktop/aipi510-fall24/assignment 5/anovatest.csv"

try: 
    conn = sqlite3.connect("test1") # open the connection to an SQL database named test1
    print("Connected to the SQL Database! Executing all queries...\n")
    
    data = pd.read_csv(fileName) # store the data in this variable
    
    try:
        data.to_sql('table1',conn,index=False,if_exists='replace') # forms the SQL database
    except Exception as e:
        print(f"Data upload error: {e}") # print error message if data cannot be uploaded to the SQL database
    
    sql1 = sqlquery(conn,"SELECT * FROM table1")
    
except sqlite3.Error as e:
    print(f"Database connection error: {e}") # print error message if we cannot connect to the database
    
finally: # if everything in the "try" block is finished
    if conn: # and if the SQL connection still exists
        conn.close() # close the connection to the SQL database
        print("\nYour database connection has been closed.")

myGrid = (np.transpose(sql1)[1:,:]).astype(float)

# Run the ANOVA test and display the results
result, myF, Fstat = myANOVA(myGrid, 0.05)

# Print the ANOVA results
print(f"F-statistic: {myF}")
print(f"Critical F-value: {Fstat}")
