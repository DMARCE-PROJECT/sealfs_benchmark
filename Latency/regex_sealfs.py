import re
import glob
import csv

number_re = re.compile(r'\d+\.\d+')
openvpn_re = re.compile(r'openvpn')
sealfs_re = re.compile(r'^.+sealfs_write.+$', re.MULTILINE)

files = glob.glob("./**/*sealfs_ftrace*.txt")

for file_path in files:
    filename = re.split(r'[/\.]', file_path)[-2]
    filename_w_ext = re.split(r'[/]', file_path)[-1]
    path = file_path[:-len(filename_w_ext)]
        
    output_file_path = path + filename + "_parsed.csv"
    output_file = open(output_file_path, "w")
    csv_writer = csv.writer(output_file)
    
    
    file = open(file_path, "r")
    all_text = file.read()

    matches = sealfs_re.findall(all_text)
    
    for match in matches:
        if openvpn_re.search(match) is not None:
            continue
        
        time = number_re.findall(match)
        
        if len(time) == 0:
            continue
        
        csv_writer.writerow(['sealfs_write', time[0]])
            
    output_file.close()
    file.close()
    