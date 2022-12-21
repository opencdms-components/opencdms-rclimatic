FROM python:3.8-slim

RUN apt-get update -y
RUN apt-get install -y libcurl4-openssl-dev libssl-dev libxml2 libxml2-dev\
    libnetcdf-dev libfontconfig1-dev libharfbuzz-dev libfribidi-dev \
    libnetcdf-dev r-base git libpq-dev python3-dev default-mysql-client default-libmysqlclient-dev
RUN R -e "install.packages(c('remotes','textshaping', 'systemfonts', 'ncdf4'))"
RUN R -e "remotes::install_github('IDEMSInternational/cdms.products')"

RUN mkdir /opt/project
WORKDIR /opt/project

COPY requirements.txt requirements.txt
COPY requirements_dev.txt requirements_dev.txt

RUN pip install -r requirements_dev.txt
