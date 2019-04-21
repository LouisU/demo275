FROM python:2.7
# part 1
# LABAL
# ENV
COPY . /var/www/demo275
WORKDIR /var/www/demo275

# part 2 install dependency of httpd and python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8000
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
