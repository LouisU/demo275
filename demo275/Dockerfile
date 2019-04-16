FROM centos:latest
# part 1
# LABAL 
# ENV 

# part 2 install dependency of httpd and python
RUN yum upgrade -y
RUN yum install -y httpd httpd-devel 
RUN yum install -y mod_wsgi 
RUN yum install -y epel-release
RUN yum install -y python-pip
RUN yum clean all
RUN pip --version
RUN pip install --upgrade pip 


# part 3 modify settings in httpd.conf
WORKDIR /etc/httpd/conf
# This command just make sure that 127.0.0.1 can response right thing.
RUN sed -i '$a ServerName localhost:80' httpd.conf  
# more settings should be set.


EXPOSE 80
CMD []
