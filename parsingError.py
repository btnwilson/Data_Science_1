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
    data_centers[file.strip('.dat')] = load_report("reports/000000.dat") 
print('Files in Reports Directory:'.format(), len(os.listdir('reports/')))
print('Size of the Data Centers Dictionary:'.format(), len(data_centers))

data_center_error_avgs = {}
total_errors = 0
for key in data_centers.keys():
    errors = sum(data_centers[key].values())
    data_center_error_avgs[key] = errors
    total_errors += errors

error_type_totals = {}
for key in data_centers.keys():
    for error in data_centers[key].keys():
        if error not in error_type_totals:
            error_type_totals[error] = data_centers[key][error]
        else:
            error_type_totals[error] += data_centers[key][error]
top_2 = sorted(error_type_totals.items(), key=lambda error: error[1], reverse=True)[:2]
print(top_2)
