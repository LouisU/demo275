FROM centos:latest

# LABAL 
# ENV 
RUN yum upgrade \
&& yum install httpd httpd-devel -y \
&& yum -y install epel-release \
&& yum -y install python-pip \
&& pip install --upgrade pip \
&& yum install mod_wsgi \
&& yum clean all 

# modify settings in httpd.conf


EXPOSE 80
CMD []
