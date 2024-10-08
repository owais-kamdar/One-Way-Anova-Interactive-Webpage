import numpy as np
from scipy.stats import f

# ANOVA function
def myANOVA(grid, alpha):
    GM = np.mean(grid)
    groupMeans = np.zeros(len(grid))
    
    # Calculate group means
    for i in range(len(grid)):
        groupMeans[i] = np.mean(grid[i])
        
    # Initialize sum of squares
    SStotal = 0
    SSWG = 0
    SSBG = 0

    # Calculate sum of squares
    for i in range(len(grid)):
        SSBG += len(grid[i]) * (groupMeans[i] - GM) ** 2
        for j in range(len(grid[i])):
            SStotal += (grid[i, j] - GM) ** 2
            SSWG += (grid[i, j] - groupMeans[i]) ** 2

    # Degrees of freedom
    DFtotal = grid.size - 1
    DFBG = len(grid) - 1
    DFWG = grid.size - len(grid)

    # Variance between groups and within groups
    varBG = SSBG / DFBG
    varWG = SSWG / DFWG

    # Calculate the F-statistic
    myF = varBG / varWG

    # Get the critical F-value using the F-distribution
    Fstat = f.ppf(1 - alpha, DFBG, DFWG)

    # Decision based on F-statistic
    if myF > Fstat:
        result = "There is a statistically significant difference between the groups!"
    else:
        result = "There is no evidence for a significant difference between the groups."
    
    return result, myF, Fstat
