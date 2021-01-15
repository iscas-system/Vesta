import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


benchmark1 = "Benchmark: Hadoop Kmeans"
# benchmark2 = "Benchmark: Hadoop WordCount"
# WordCount 18G18U CPU_overall
# t1 = ""
# time1 = ""  
# benchmark1_a1 = ""
# benchmark1_b1 = ""
# benchmark1_c1 = ""
# benchmark1_d1 = ""

num = 13
workers = 4

t1 = "Hadoop TeraSort"  
time1 = "27"
benchmark1_a1 = ""  
benchmark1_b1 = ""
benchmark1_c1 = ""
benchmark1_d1 = ""

t2 = "Spark TeraSort"
time2 = "31"  
benchmark2_a1 = ""  
benchmark2_b1 = ""
benchmark2_c1 = ""
benchmark2_d1 = ""

t3 = "Hadoop WordCount"
time3 = "27"
benchmark3_a1 = ""  
benchmark3_b1 = ""
benchmark3_c1 = ""
benchmark3_d1 = ""

t4 = "Spark WordCount"
time4 = "30"
benchmark4_a1 = ""  
benchmark4_b1 = ""
benchmark4_c1 = ""
benchmark4_d1 = ""

t5 = "Hadoop PageRank"
time5 = "48"
benchmark5_a1 = ""  
benchmark5_b1 = ""
benchmark5_c1 = ""
benchmark5_d1 = ""

t6 = "Spark PageRank"
time6 = "33"
benchmark6_a1 = ""  
benchmark6_b1 = ""
benchmark6_c1 = ""
benchmark6_d1 = ""

t7 = "Hadoop Bayes"
time7 = "268"
benchmark7_a1 = ""
benchmark7_b1 = ""
benchmark7_c1 = ""
benchmark7_d1 = ""

t8 = "Spark Bayes"
time8 = "44"
benchmark8_a1 = ""
benchmark8_b1 = ""
benchmark8_c1 = ""
benchmark8_d1 = ""

t9 = "Hadoop Kmeans"
time9 = "126"
benchmark9_a1 = ""  
benchmark9_b1 = ""
benchmark9_c1 = ""
benchmark9_d1 = ""

t10 = "Spark Kmeans"
time10 = "34"
benchmark10_a1 = ""  
benchmark10_b1 = ""
benchmark10_c1 = ""
benchmark10_d1 = ""

t11 = "Spark LDA"
time11 = "34"
benchmark11_a1 = ""  
benchmark11_b1 = ""
benchmark11_c1 = ""
benchmark11_d1 = ""

t12 = "Spark PCA"
time12 = "38"
benchmark12_a1 = ""  
benchmark12_b1 = ""
benchmark12_c1 = ""
benchmark12_d1 = ""

t13 = "Spark LR"
time13 = "41"
benchmark13_a1 = ""  
benchmark13_b1 = ""
benchmark13_c1 = ""
benchmark13_d1 = ""

t14 = "Spark LDA"
time14 = "54"
benchmark14_a1 = ""  
benchmark14_b1 = ""
benchmark14_c1 = ""
benchmark14_d1 = ""

t15 = "Spark SVM"
time15 = "40"
benchmark15_a1 = ""
benchmark15_b1 = ""
benchmark15_c1 = ""
benchmark15_d1 = ""

col_labels = []
row_labels = ['CPU mean(%)', 'CPU standard deviation(%)', 'RAM mean(%)', 'RAM standard deviation(%)', 'Disk read mean(Mbps)', 'Disk read standard deviation(Mbps)', \
              'Disk write mean(%)', 'Disk write standard deviation(Mbps)', 'Network receive mean(Mbps)', 'Network receive standard deviation(Mbps)', \
              'Network send mean(Mbps)', 'Network send standard deviation(Mbps)']
table_vals = []
col_value = []
mean_value = []
row_colors = ['gold']
for i in range(1,num+1):
    c = locals()['benchmark%s_c1' % str(i)].split(" ")
    x = []
    y_c1 = []
    y_c2 = []
    l = 0  
    for n in c:   
        l = l + 1        
        m = n.split(",")
        x.append(5*int(l))          
        y_c1.append(float('%.2f' % (float(m[1]))) / 1024 / 1024 / workers)
        y_c2.append(float('%.2f' % (float(m[2]))) / 1024 / 1024 / workers)
    print("Disk read mean: %sMbps" % ('%.2f' % (np.mean(np.array(y_c1)))))
    print("Disk read standard deviation: %sMbps" % ('%.2f' % (np.std(np.array(y_c1)))))
    print("Disk write mean: %sMbps" % ('%.2f' % (np.mean(np.array(y_c2)))))
    print("Disk write standard deviation: %sMbps" % ('%.2f' % (np.std(np.array(y_c2)))))
#     col_value_float.append(('%.2f' % (np.mean(np.array(y_a))))) 
#     col_value_float.append(('%.2f' % (np.std(np.array(y_a)))))
#     col_value_float.append(('%.2f' % (np.mean(np.array(y_b))))) 
#     col_value_float.append(('%.2f' % (np.std(np.array(y_b)))))
#     col_value_float.append(('%.2f' % (np.mean(np.array(y_c1)))))
#     col_value_float.append(('%.2f' % (np.std(np.array(y_c1))))) 
#     col_value_float.append(('%.2f' % (np.mean(np.array(y_c2))))) 
#     col_value_float.append(('%.2f' % (np.std(np.array(y_c2))))) 
#     col_value_float.append(('%.2f' % (np.mean(np.array(y_d1))))) 
#     col_value_float.append(('%.2f' % (np.std(np.array(y_d1))))) 
#     col_value_float.append(('%.2f' % (np.mean(np.array(y_d2))))) 
#     col_value_float.append(('%.2f' % (np.std(np.array(y_d2)))))
    mean_value.append([('%.2f' % (np.mean(np.array(y_c1)))), ('%.2f' % (np.mean(np.array(y_c2))))])
    

table_vals = []
tmp = []
for col in mean_value:
    print(np.array(col))
# for col in col_value:
#     print(np.array(col))
# for i in range(0,len(col_value[0])):
#     for col in col_value:
#         tmp.append(col[i])
#     table_vals.append(tmp)
# #     print(tmp)
#     tmp = []
# print(table_vals)
# print(col_labels)
# print(row_labels)
# my_table = plt.table(cellText=table_vals, colWidths=[0.2]*num, \
#                      rowLabels=row_labels, colLabels=col_labels, \
#                      loc='best')
# my_table.set_fontsize(20)
# plt.axis('off')

# plt.show()