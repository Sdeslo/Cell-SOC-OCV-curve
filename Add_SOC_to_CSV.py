import pandas as pd

# Load the CSV file
file_path = r'C:\Users\simde\Downloads\Cell_discharge_100mA.csv'
data = pd.read_csv(file_path, on_bad_lines='skip')

if 'I' in data.columns and 'mAh' in data.columns:
    last_mah = data['mAh'].iloc[-1]  # Last capacity value
    # Initialize SOC to 100
    soc_values = [100]
    cumulative_discharge = 0  # Start with no discharge
    
    # Iterate through each row and calculate the cumulative discharge
    for i in range(1, len(data)):
        current = data['I'].iloc[i]  # Current (in A)
        time_delta = 0.001242  # Time step in hours
        discharge = current * 1000 * time_delta  # Discharge in mAh for this time step
        cumulative_discharge += discharge
        
        # Calculate the SOC for this step
        soc = ((last_mah - cumulative_discharge) / last_mah) * 100
        soc_values.append(soc)
    
    # Add the SOC values as a new column in the DataFrame
    data['SOC'] = soc_values
    # Save the updated data to a new CSV file with a header
    new_file_path = r'C:\Users\simde\Downloads\Cell_discharge_SOC.csv'
    data.to_csv(new_file_path, index=False)
    print(f"SOC added and file saved as {new_file_path}")
else:
    print("Error: Required columns ('current', 'time_delta', 'last_mah') not found.")
