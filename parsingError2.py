import os 
import matplotlib.pyplot as plt
import numpy as np

# Function to load data from a report file
def load_report(filename):
    file = open(filename, 'r')
    error_modes = {}
    for line in file:
        if ':' in line and "AUTOMATED REPORT PERIOD" not in line and "OPERATION NOTES" not in line:
            segments = line.split(':')
            error_modes[segments[0].strip()] = int(segments[1].strip())

        if any(value < 0 for value in error_modes.values()):
        file.close()
        raise ValueError("Error: Subdictionary contains negative values")
        
    file.close()
    return error_modes      
# Dictionary to store data center reports
data_centers = {}

# Read data from report files and store it in data_centers
for file in os.listdir('reports/'):
    data_centers[file.strip('.dat')] = load_report('reports/' + file)  
# %%

# Calculate total error counts for each data center
data_center_total_error = {}
abnormal_tag = []

# Loop through data centers
for key in data_centers.keys():
    if len(key) != 6 or not key.isdigit():
        abnormal_tag.append(key)
    errors = sum(data_centers[key].values())
    data_center_total_error[key] = errors

print('Files in Reports Directory:'.format(), len(os.listdir('reports/')))
print('Size of the Data Centers Dictionary:'.format(), len(data_centers))

total_errors = sum(data_center_total_error.values())

most_errors = sorted(data_center_total_error.items(), key=lambda error: error[1], reverse=True)

error_type_totals = {}
for key in data_centers.keys():
    for error in data_centers[key].keys():
        if error not in error_type_totals:
            error_type_totals[error] = data_centers[key][error]
        else:
            error_type_totals[error] += data_centers[key][error]

same_error = ['A/C', 'Air Con.', 'HVAC']
error_type_totals['combined A/C'] = 0
for i in same_error:
    error_type_totals['combined A/C'] += error_type_totals[i]
    del error_type_totals[i]

top_10_errors = sorted(error_type_totals.items(), key=lambda error: error[1], reverse=True)

# %%
flood_values = {}
for key in data_centers.keys():
    flood_values[key] = data_centers[key]['Physical intrusion (water)'] / data_center_total_error[key]

x = sorted(flood_values.values())
y = np.arange(len(flood_values))/len(flood_values)
flood_avg = np.mean([p for p in flood_values.values()])
flood_std = np.std([p for p in flood_values.values()])


plt.figure()
plt.plot(x, y, '.', markersize=20)
plt.plot(x, y, linewidth=2, c='r')
plt.xlabel("Flood Risk")
plt.ylabel("P<(x)")
plt.title('Cumulative Distribution Function for Flood Risk')
plt.savefig('CDF Flood Values.png')

most_floods = sorted(flood_values.items(), key=lambda flood: flood[1], reverse=True)
 
print("{:^15}{:^20}".format('Data Center ID', '% Flood Errors'))
print("   " + '-' * 27)
for i in most_floods[:10]:
    print(f'{i[0]:^15}  {i[1]:^19.4f}')


flood_class = {}
for key in flood_values.keys():
    percent = flood_values[key]
    if percent < .8 and percent >= .7:
        flood_class[key] = 1
    elif percent < .7 and percent >= .6:
        flood_class[key] = 2
    elif percent < .6 and percent >= .5:
        flood_class[key] = 3
    elif percent < .5 and percent >= .4:
        flood_class[key] = 4
    elif percent < .4 and percent >= .3:
        flood_class[key] = 5
    elif percent < .3 and percent >= .2:
        flood_class[key] = 6
    elif percent < .2 and percent >= .1:
        flood_class[key] = 7
    elif percent < .1 and percent >= 0:
        flood_class[key] = 8

plt.figure()
bins = np.arange(.5, 9.5, 1)
plt.hist(flood_class.values(), bins=bins)
plt.xlabel('Risk Class (1 high - 8 low)')
plt.ylabel('# of Centers')
plt.title('Distribution of Flood Risk Catagories')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('Flood Risk Catagories Hist.png')

margin_of_error = {}
for key in flood_values.keys():
    p = flood_values[key]
    n = data_center_total_error[key]
    margin_of_error[key] = 1.96 * np.sqrt(( p * (1-p))/ n)

full_moe_list = [moe for moe in margin_of_error.values()]
avg_moe_all = np.mean(full_moe_list)
margin_of_error_list = [moe for moe in margin_of_error.values() if moe != 0]

avg_moe = np.mean(margin_of_error_list)
std_moe = np.std(margin_of_error_list)

plt.figure()
plt.hist(margin_of_error_list, bins=15)
plt.title('Distribution of Margin of Error')
plt.xlabel('Margin of Error')
plt.ylabel('# of Data Centers')
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('Margin of Error Hist.png')
