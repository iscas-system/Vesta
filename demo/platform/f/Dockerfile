FROM centos:7.6.1810

RUN yum -y install epel-release 

RUN yum install python3 python3-devel python3-pip libcurl-devel postgresql-devel gcc -y

RUN pip3 install --upgrade pip

RUN pip3 install flask flask_restful scikit-learn joblib numpy pandas flask-cors pymysql pydotplus psycopg2

RUN mkdir -p /home/test

ADD demo /home/test

ADD laji /home/test

WORKDIR /home/test

CMD ["python3","RunServer.py"]