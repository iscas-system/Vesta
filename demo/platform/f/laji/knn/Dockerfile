FROM centos:7.6.1810

RUN yum -y install epel-release 

RUN yum install python3 python3-devel python3-pip libcurl-devel -y

RUN pip3 install --upgrade pip

RUN pip3 install scikit-learn numpy pandas 

RUN mkdir -p /home/test

ADD main /home/test

WORKDIR /home/test

CMD ["python3","knn.py"]
