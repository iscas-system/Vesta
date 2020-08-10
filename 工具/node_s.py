'''
    Created on Jul 26, 2020
    @author: frank
'''

import csv
import os
import json

DATA = []

workload_eum = {}
framework_eum = {}
datasize_eum = {}
vmtype_eum = {}

def show_files(path):
    file_list = os.listdir(path)
    for file in file_list:
        cur_path = os.path.join(path, file)
        if os.path.isdir(cur_path):
            show_files(cur_path)
        else:
            datafile.append(cur_path)


def show_files_1(path, all_files):
    for root,dirs,files in os.walk(path):
        for file in files:
            all_files.append(os.path.join(root,file))
    return all_files

def main():
    path = "/Users/huyi/Desktop/scout/dataset/osr_single_node"
    json_files = show_files_1(path, [])
    #show_files(path)
    #json_files = datafile
    workload = []
    framework = []
    vm_type = []
    for json_file in json_files:
        one_data = []
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
                    one_data.append('%.2f' % float(contents.get('elapsed_time')))
                    
                    wl = contents.get('workload')
                    if wl not in workload_eum.keys():
                        workload_eum[wl] = len(workload_eum)
                    one_data.append( workload_eum[wl])
                    
                    fw = contents.get('framework')
                    if fw not in framework_eum.keys():
                        framework_eum[fw] = len(framework_eum)
                    one_data.append(framework_eum[fw])
                    
                    ds = contents.get('datasize')
                    if ds not in datasize_eum.keys():
                        datasize_eum[ds] = len(datasize_eum)
                    one_data.append(datasize_eum[ds])
                    
                    vt = base_dir_name.split('_')[0]
                    if vt not in vmtype_eum.keys():
                        vmtype_eum[vt] = len(vmtype_eum)
                    one_data.append(vmtype_eum[vt])
                    
                    vm_type.append(base_dir_name.split('_')[0])
                    workload.append(contents.get('workload'))
                    framework.append(contents.get('framework'))
            if os.path.exists(os.path.join(dir_name, 'sar.csv')):
                with open(os.path.join(dir_name, 'sar.csv'), 'r') as load_f:
                    reader = csv.DictReader(load_f)
                    count = 0
                    total_cpu, total_mem, total_disk = 0.0, 0.0, 0.0
                    for i in reader:
                        #                     print i.get('cpu.%usr')
                        total_cpu += float(i.get('cpu.%usr'))
                        total_mem += float(i.get('memory.%memused'))
                        total_disk += float(i.get('disk.%util'))
                        count += 1
                    average_cpu = total_cpu / count
                    average_mem = total_mem / count
                    average_disk = total_disk / count
                    one_data.append('%.2f' % average_cpu)
                    one_data.append('%.2f' % average_mem)
                    one_data.append('%.2f' % average_disk)
            if len(one_data) < 6:
                continue
            #for i in one_data:
            one_data_str = ",".join(str(i) for i in one_data)
            with open("data.txt","a") as fo:
                fo.write(one_data_str+'\n')


    with open("tag.txt","w") as fo:
        for key in workload_eum.keys():
            fo.write(key+':'+str(workload_eum[key])+'\n')
        fo.write("-----\n")
        for key in framework_eum.keys():
            fo.write(key+':'+str(framework_eum[key])+'\n')
        fo.write("-----\n")
        for key in datasize_eum.keys():
            fo.write(key+':'+str(datasize_eum[key])+'\n')
        fo.write("-----\n")
        for key in vmtype_eum.keys():
            fo.write(key+':'+str(vmtype_eum[key])+'\n')

'''
    workload_li = list(set(workload))
    #for i in workload_li:
    workload_li_str = ",".join(str(i) for i in workload_li)
    print (workload_li_str)
    framework_li = list(set(framework))
    #for i in framework_li:
    framework_li_str = ",".join(str(i) for i in framework_li)
    print (framework_li_str)
    vm_type_li = list(set(vm_type))
    #for i in vm_type_li:
    vm_type_li_str = ",".join(str(i) for i in vm_type_li)
    print (vm_type_li_str)
'''

if __name__ == '__main__':
    main()
