FROM python:3.8-slim

RUN apt-get update -y
RUN apt-get install -y libcurl4-openssl-dev libssl-dev \
    libnetcdf-dev libfontconfig1-dev libharfbuzz-dev libfribidi-dev \
    libnetcdf-dev r-base git
RUN R -e "install.packages('remotes')"
RUN R -e "install.packages('textshaping')"
RUN R -e "install.packages('systemfonts')"
RUN R -e "install.packages('ncdf4')"
RUN R -e "remotes::install_github('IDEMSInternational/cdms.products')"

RUN mkdir /opt/project
WORKDIR /opt/project

COPY requirements.txt requirements.txt
COPY requirements_dev.txt requirements_dev.txt

RUN pip install -r requirements_dev.txt
