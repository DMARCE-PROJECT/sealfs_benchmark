import re
import glob
import csv
import string

section_re = re.compile(r'(?:-+\s*\d\)\s+([\w-]+\s+=>\s+[\w-]+)\s+-+\s+)((?:\s*\d\)\s+\W*\s*\d+\.\d+\sus\s+\|\s+.+\(\);\s*)+)')
number_re = re.compile(r'\d+\.\d+')
openvpn_re = re.compile(r'openvpn')
ros1sea_re = re.compile(r'ros1sea')
multilo_re = re.compile(r'multilo')

files = glob.glob("./**/*ext4_ftrace*.txt")

for file_path in files:
    filename = re.split(r'[/\.]', file_path)[-2]
    filename_w_ext = re.split(r'[/]', file_path)[-1]
    path = file_path[:-len(filename_w_ext)]
        
    output_file_path = path + filename + "_parsed.csv"
    output_file = open(output_file_path, "w")
    csv_writer = csv.writer(output_file)
    
    
    file = open(file_path, "r")
    all_text = file.read()

    matches = section_re.findall(all_text)
    ref_count = {}
    
    print(filename)
    for match in matches:
        if openvpn_re.search(match[0]) is not None:
            continue
                
        n_lines = match[1].count('\n')
        times = number_re.findall(match[1])
        
        
        for time in times:
            if 'image' in filename:
                if float(time) > 600:
                    csv_writer.writerow(['ext4_write', time])
            else:
                if multilo_re.search(match[0]) is not None and ros1sea_re.search(match[0]) is not None:
                    csv_writer.writerow(['ext4_write', time])

        

    
