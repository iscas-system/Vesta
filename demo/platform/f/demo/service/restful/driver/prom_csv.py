import csv
import requests
import sys
import time
import datetime
import os
import service.restful.driver.sql as mysql


def GetMetrixNames(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    names = response.json()['data']
    # Return metrix names
    return names

def main(env_t,pret,t):
    """
    command = ['sum(rate(container_cpu_usage_seconds_total{pod=~"spark.*"}[5s])) by (pod, namespace) / (sum(container_spec_cpu_quota{pod=~"spark.*"}/100000) by (pod, namespace)) * 100',\
               'sum(container_memory_rss{pod=~"spark.*"}) by(pod, namespace) / sum(container_spec_memory_limit_bytes{pod=~"spark.*"}) by(pod, namespace) * 100 != +inf',\
               'sum(container_fs_usage_bytes{pod=~"spark.*"}) by(pod, namespace) / 1024 / 1024 / 1024']
    """
    command = ['sum(container_cpu_usage_seconds_total{pod=~"myspark.*"}) by (pod, namespace) / 100',\
               'sum(container_memory_rss{pod=~"spark.*"}) by(pod, namespace) / 100 != +inf',\
               'sum(container_fs_usage_bytes{pod=~"spark.*"}) by(pod, namespace) / 1024 / 1024 / 1024']
    metricname = ['cpu','memory','fs']

    """
    Prometheus hourly data as csv.
    """
    dir_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dir_path,"metrics")
    data = []
    with open (filename,'a') as f:
        writer = csv.writer(f)
        """
        if len(sys.argv) != 2:
            print('Usage: {0} http://localhost:9090'.format(sys.argv[0]))
            sys.exit(1)
        """
        argv = "http://39.106.40.190:31001"
        metrixNames=GetMetrixNames(argv)
        writeHeader=True
        for i in range(3):
             #now its hardcoded for hourly
            '''
            t = time.time()
            today = datetime.datetime.now()
            oneday = datetime.timedelta(hours=1)
            pret = today - oneday
            pret = int(time.mktime(pret.timetuple()))
            '''
            response = requests.get('{0}/api/v1/query_range'.format(argv),
            params={'query': command[i],'start': str(pret),'end':str(t),'step': '5s'})
            results = response.json()['data']['result']
              # Build a list of all labelnames used.
              #gets all keys and discard __name__
            labelnames = set()
            for result in results:
                labelnames.update(result['metric'].keys())
              # Canonicalize
            labelnames.discard('__name__')
            labelnames = sorted(labelnames)
              # Write the samples.
            if writeHeader:
                writer.writerow(['name', 'timestamp', 'value'] + labelnames)
                writeHeader=False
            for result in results:
                l = [result['metric'].get('pod', '')] + result['values']
                l.append(metricname[i])
                # for label in labelnames:
                #     l.append(result['metric'].get(label, ''))
                writer.writerow(l)
                cnt = 0
                res = 0
                for item in result['values']:
                    res += float(item[1])
                    cnt += 1
                data.append(res / cnt)
    filename_d = os.path.join(dir_path, "data.txt")
    with open(filename_d, 'a') as fd:
        content = []
        content.append(t - pret)
        for item in env_t:
            content.append(item)
        for item in data:
            content.append(item)
        content_str = ",".join(str(tmpt) for tmpt in content)
        fd.write(content_str+'\n')
    mysql.main(False)
