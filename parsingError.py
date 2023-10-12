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
