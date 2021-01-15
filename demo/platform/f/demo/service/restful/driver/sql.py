import pymysql
import psycopg2
import os
import json

def main(isf):
    data = []
    dir_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dir_path, "metrics")
    with open(filename, 'r') as f:
        cnt = 0
        for eachline in f:
            if cnt != 0:
                eachline = eachline.split(os.linesep)[0]
                line = eachline.split(',')
                data.append({})
                data[cnt-1]['name'] = line[0]
                data[cnt-1]['kind'] = line[-1]
                l = len(line)
                num = 0
                data[cnt-1]['list'] = []
                for j in range(1,l-1):
                    if j % 2 == 1:
                        tmp = line[j][2:]
                        n = int(tmp)
                        data[cnt - 1]['list'].append([])
                        data[cnt - 1]['list'][num].append(n)
                    if j % 2 == 0:
                        tmp = line[j][2:-3]
                        n = float(tmp)
                        data[cnt - 1]['list'][num].append(n)
                        num += 1
            cnt += 1
    #connect to database
    db = psycopg2.connect(host="39.106.40.190",user="postgres",password="onceas",database='postgres',port=30306)
    cursor = db.cursor()
    if isf == True:
        cursor.execute("DROP TABLE IF EXISTS CONTAINERDATA")
        '''
        sql = """CREATE TABLE CONTAINERDATA (
                POD_NAME  CHAR(30) NOT NULL,
                METRIC_NAME CHAR(10),
                TIMES INT,
                VALUEC FLOAT )"""
        '''
        sql = """CREATE TABLE CONTAINERDATA (
                POD_NAME  CHAR(30) NOT NULL,
                TIMES CHAR(30),
                JSDATA CHAR(100) )"""
        cursor.execute(sql)
        db.commit()

    data_l = len(data)
    jsdata = {}
    for i in range(data_l):
        pod_name = data[i]['name']
        metric_name = data[i]['kind']
        list_l = len(data[i]['list'])
        for j in range(list_l):
            time = data[i]['list'][j][0]
            time = str(time)
            ttmp = pod_name + ',' + time
            if ttmp not in jsdata.keys():
                jsdata[ttmp] = {}
            values = data[i]['list'][j][1]
            jsdata[ttmp][metric_name] = str(values)
            '''
            sql = "INSERT INTO CONTAINERDATA(POD_NAME, \
                METRIC_NAME, TIMES, VALUEC) \
                VALUES ('%s', '%s', %s, %s)" % \
                (pod_name, metric_name,time,values)
            '''
    for key in jsdata.keys():
        arr = key.split(',')
        pod_name = arr[0]
        time = arr[1]
        sql = "INSERT INTO CONTAINERDATA(POD_NAME, \
            TIMES, JSDATA ) \
            VALUES ('%s', '%s', '%s')" % \
            (pod_name, time, json.dumps(jsdata[key]))
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

    db.close()

if __name__ == '__main__':
    main(True)
