import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file_path = r'C:\Users\simde\Downloads\Cell_discharge_SOC.csv'
try:
    data = pd.read_csv(file_path, on_bad_lines='skip')  # Skip malformed rows
except Exception as e:
    print(f"Error reading the file: {e}")
    exit()

voltage_array = np.array(data['V'])  # Voltage data as numpy array
min_voltage = np.min(voltage_array)
max_voltage = np.max(voltage_array)
num_values = len(voltage_array)
soc_array = np.array(data['SOC'])    # SOC data as numpy array
x = voltage_array.flatten() 
y = soc_array.flatten() 
xTest = np.linspace(min_voltage, max_voltage, num_values)

# 1st degree
A1st = np.column_stack((x, np.ones_like(x)))  
A_pseudo1st = np.linalg.pinv(A1st)  
theta1st = A_pseudo1st @ y  
a1, b1 = theta1st
y1st = a1 * xTest + b1 
err1st = np.linalg.norm(y - y1st) 

# 2nd degree
A2nd = np.column_stack((x**2, x, np.ones_like(x)))  
A_pseudo2nd = np.linalg.pinv(A2nd)  
theta2nd = A_pseudo2nd @ y  
a2, b2, c2 = theta2nd  
y2nd = a2 * xTest**2 + b2 * xTest + c2  
err2nd = np.linalg.norm(y - y2nd) 

# 3rd degree
A3rd = np.column_stack((x**3, x**2, x, np.ones_like(x)))  
A_pseudo3rd = np.linalg.pinv(A3rd)
theta3rd = A_pseudo3rd @ y  
a3, b3, c3, d3 = theta3rd
y3rd = a3 * xTest**3 + b3 * xTest**2 + c3 * xTest + d3 
err3rd = np.linalg.norm(y - y3rd)  

# 4th degree
A4th = np.column_stack((x**4, x**3, x**2, x, np.ones_like(x)))  
A_pseudo4th = np.linalg.pinv(A4th)
theta4th = A_pseudo4th @ y
a4, b4, c4, d4, e4 = theta4th
y4th = a4 * xTest**4 + b4 * xTest**3 + c4 * xTest**2 + d4 * xTest + e4
err4th = np.linalg.norm(y - y4th)   

# 5th degree
A5th = np.column_stack((x**5, x**4, x**3, x**2, x, np.ones_like(x)))  
A_pseudo5th = np.linalg.pinv(A5th)
theta5th = A_pseudo5th @ y
a5, b5, c5, d5, e5, f5 = theta5th
y5th = a5 * xTest**5 + b5 * xTest**4 + c5 * xTest**3 + d5 * xTest**2 + e5 * xTest + f5
err5th = np.linalg.norm(y - y5th)  

# 6th degree
A6th = np.column_stack((x**6, x**5, x**4, x**3, x**2, x, np.ones_like(x)))  
A_pseudo6th = np.linalg.pinv(A6th)
theta6th = A_pseudo6th @ y
a6, b6, c6, d6, e6, f6, g6 = theta6th
y6th = a6 * xTest**6 + b6 * xTest**5 + c6 * xTest**4 + d6 * xTest**3 + e6 * xTest**2 + f6 * xTest + g6
err6th = np.linalg.norm(y - y6th)   

plt.plot(x, y, color='black', label='Original Data')

# Plot all polynomial fits
plt.plot(xTest, y1st, label=f'1st Degree Fit (Error: {err1st:.2f})', color='blue')
plt.plot(xTest, y2nd, label=f'2nd Degree Fit (Error: {err2nd:.2f})', color='green')
plt.plot(xTest, y3rd, label=f'3rd Degree Fit (Error: {err3rd:.2f})', color='red')
plt.plot(xTest, y4th, label=f'4th Degree Fit (Error: {err4th:.2f})', color='purple')
plt.plot(xTest, y5th, label=f'5th Degree Fit (Error: {err5th:.2f})', color='orange')
plt.plot(xTest, y6th, label=f'6th Degree Fit (Error: {err6th:.2f})', color='cyan')

# Labels and legend
plt.xlabel('Cell Voltage (V)')
plt.ylabel('SOC (%)')
plt.legend()

# Add title to the plot
plt.title('Polynomial Fits for Voltage vs SOC')

# Show plot
plt.show()
