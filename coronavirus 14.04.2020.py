#Pr0metheus
import xlrd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

""" The Function Take an xls file and a number [The number should be the column number (A=0,B=1 etc)] as an input 
& outputs the column as a list. """
def read_xls(filename,n):
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0)
    column = sheet.col_values(n)
    column.pop(0) #To remove text above data (Was used in a particular case)
    #del column[-1] #To remove text underneath data (Was used in a particular case)
    return column

filename = 'excel file path'

date = read_xls(filename,0)
total_cases = read_xls(filename,1)
new_cases = read_xls(filename,2)
days = read_xls(filename,3) #days from start of outbreak

#logistic function
def logistic(t,a,b,c):
    return c / (1+ a * np.exp(-b*t))

# curve_fit() function takes the test-function
# x-data and y-data as argument and returns
# the coefficients a and b in param and
# the estimated covariance of param in param_cov
param, param_cov = curve_fit(logistic,days,new_cases) # for new cases
param2, param_cov2 = curve_fit(logistic,days,total_cases) #if we assume logistic growth for total cases


dayarr= np.array(days)

# ans stores the new y-data according to the coefficients given by curve-fit() function
ans_logis2 = (param2[2]/ (1+ param2[0] * np.exp(-param2[1]*dayarr)))
ans_logis = (param[2]/ (1+ param[0] * np.exp(-param[1]*dayarr)))

plt.xlabel("Days Since Start of Outbreak (21.02)")
plt.ylabel("Number of People")
plt.plot(days,total_cases, 'o', color ='red', label ="total_cases data")
plt.plot(days, ans_logis2, '--', color ='green', label ="optimized data (logistic) for total cases")
plt.plot(days,new_cases, 'o', color = 'blue', label = "new cases data")
plt.plot(days, ans_logis, '--', color ='purple', label ="optimized data (logistic) for new cases")
plt.legend()
plt.show()

