print("Hello, World!")
def load_report(filename):
    file = open(filename, 'r')
    error_modes = {}
    for line in file:
        if ':' in line and "AUTOMATED REPORT PERIOD" not in line and "OPERATION NOTES" not in line:
            segments = line.split(':')
            error_modes[segments[0].strip()] = int(segments[1].strip())
    return error_modes      
    
error_modes = load_report("reports/reports/000000.dat")  
