FROM docker.io/centos:latest

RUN mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup

RUN curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.163.com/.help/CentOS7-Base-163.repo

RUN yum --enablerepo=extras install -y epel-release

RUN yum install -y gcc

RUN yum -y install python-devel.x86_64

RUN curl -o psutil.tar https://pypi.python.org/packages/source/p/psutil/psutil-2.1.3.tar.gz

RUN tar zxvf psutil.tar

RUN cd psutil-2.1.3/

RUN python setup.py install

EXPOSE 8080

#RUN cp 

#RUN yum install -y python-psutil

#CMD ["python"]
