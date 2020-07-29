'''
Created on Jul 26, 2020

@author: frank
'''

import csv
import os
import json

DATA = []

def show_files(path, all_files):
    file_list = os.listdir(path)
    for file in file_list:
        cur_path = os.path.join(path, file)
        if os.path.isdir(cur_path):
            show_files(cur_path, all_files)
        else:
            all_files.append(file)

    return all_files

def show_files_1(path, all_files):
    for root,dirs,files in os.walk(path):
        for file in files:
            all_files.append(os.path.join(root,file))
    return all_files

def main():
    path = 'E:\wuyuewen\scout\dataset/osr_single_node'
    json_files = show_files_1(path, [])
#     workload = []
#     framework = []
#     vm_type = []
    for json_file in json_files:
        one_data = {}
#         print json_file
        base_name = os.path.basename(json_file)
        dir_name = os.path.dirname(json_file)
        base_dir_name = os.path.basename(dir_name)
        if base_name == 'report.json':
            with open(json_file, 'r') as load_f:
                contents = json.load(load_f)
                if contents.get('completed') == False:
                    continue
                else:
                    one_data['elapsed_time'] = '%.2f' % float(contents.get('elapsed_time'))
                    one_data['workload'] = contents.get('workload')
                    one_data['framework'] = contents.get('framework')
                    one_data['datasize'] = contents.get('datasize')
                    one_data['vm_type'] = base_dir_name.split('_')[0]
#                     vm_type.append(base_dir_name.split('_')[0])
#                     workload.append(contents.get('workload'))
#                     framework.append(contents.get('framework'))
            if os.path.exists(os.path.join(dir_name, 'sar.csv')):
                with open(os.path.join(dir_name, 'sar.csv'), 'r') as load_f:
                    reader = csv.DictReader(load_f)
                    count = 0
                    total_cpu, total_mem, total_disk,total_net = 0.0, 0.0, 0.0, 0.0
                    for i in reader:
    #                     print i.get('cpu.%usr')
                        total_cpu += float(i.get('cpu.%usr'))
                        total_mem += float(i.get('memory.%memused'))
                        total_disk += float(i.get('disk.%util'))
                        total_net += float(i.get('network.%ifutil'))
                        count += 1
                    average_cpu = total_cpu / count
                    average_mem = total_mem / count
                    average_disk = total_disk / count
                    average_net = total_net / count
                    one_data['cpu_usage'] = '%.2f' % average_cpu
                    one_data['mem_usage'] = '%.2f' % average_mem
                    one_data['disk_usage'] = '%.2f' % average_disk
                    one_data['net_usage'] = '%.2f' % average_net
            if len(one_data) < 6:
                continue
            with open(os.path.join(path, '%s.json' % base_dir_name), 'w') as f:
                json.dump(one_data, f)
#             for i in one_data:
#                 one_data_str = ",".join(str(i) for i in one_data)
#             print one_data_str
    print('------------------------------------------------------------------')
#     workload_li = list(set(workload))
#     for i in workload_li:
#         workload_li_str = ",".join(str(i) for i in workload_li)
#     print workload_li_str
#     framework_li = list(set(framework))
#     for i in framework_li:
#         framework_li_str = ",".join(str(i) for i in framework_li)
#     print framework_li_str
#     vm_type_li = list(set(vm_type))
#     for i in vm_type_li:
#         vm_type_li_str = ",".join(str(i) for i in vm_type_li)
#     print vm_type_li_str

if __name__ == '__main__':
    main()