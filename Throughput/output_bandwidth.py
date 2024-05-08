import re
import glob
import csv

number_re = re.compile(r'\d+\.\d+')
sealfs_re = re.compile(r'^.+?(?:\d+\.\d+\s+[MkKBb]\/s)\s+(\d+\.\d+\s+[MkKBb]\/s).+ros1sealfs.+$', re.MULTILINE)

files = glob.glob("./TiAGo/*_io_*.txt")

for file_path in files:
    filename = re.split(r'[/\.]', file_path)[-2]
    filename_w_ext = re.split(r'[/]', file_path)[-1]
    path = file_path[:-len(filename_w_ext)]
    file = open(file_path, "r")
        
    output_file_path = path + filename + "_parsed.csv"
    output_file = open(output_file_path, "w")
    csv_writer = csv.writer(output_file)
    
    file_type = 'sealfs' if 'sealfs' in filename else 'ext4'
    
    total, count = 0, 0
    
    all_text = file.read()
    matches = sealfs_re.findall(all_text)
    
    for time in matches:
        unit = time.split(' ')[-1]
        cur_time = 0
        
        if unit == 'M/s':
            cur_time = float(time.split(' ')[0]) * 1024
        elif unit == 'K/s':
            cur_time = float(time.split(' ')[0])
        
        total += cur_time
        csv_writer.writerow([file_type, cur_time])
        count += 1
    
        
    # csv_writer.writerow(['bandwidth_logs', total / float(count)])
