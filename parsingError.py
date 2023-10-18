import os 
def load_report(filename):
    file = open(filename, 'r')
    error_modes = {}
    for line in file:
        if ':' in line and "AUTOMATED REPORT PERIOD" not in line and "OPERATION NOTES" not in line:
            segments = line.split(':')
            error_modes[segments[0].strip()] = int(segments[1].strip())
    file.close()
    return error_modes      

data_centers = {}
for file in os.listdir('reports/'):
    data_centers[file.strip('.dat')] = load_report('reports/' + file)  
# %%

data_center_total_error = {}
total_errors = 0
abnormal_tag = []
for key in data_centers.keys():
    if len(key) != 6 or not key.isdigit():
        abnormal_tag.append(key)
    errors = sum(data_centers[key].values())
    data_center_total_error[key] = errors
    total_errors += errors
most_errors = sorted(data_center_total_error.items(), key=lambda error: error[1], reverse=True)
error_type_totals = {}
for key in data_centers.keys():
    for error in data_centers[key].keys():
        if error not in error_type_totals:
            error_type_totals[error] = data_centers[key][error]
        else:
            error_type_totals[error] += data_centers[key][error]


top_10_errors = sorted(error_type_totals.items(), key=lambda error: error[1], reverse=True)
print('Files in Reports Directory:'.format(), len(os.listdir('reports/')))
print('Size of the Data Centers Dictionary:'.format(), len(data_centers))
# %%
flood_values = {}
for key in data_centers.keys():
    flood_values[key] = data_centers[key]['Physical intrusion (water)']
most_floods = sorted(flood_values.items(), key=lambda flood: flood[1], reverse=True)
