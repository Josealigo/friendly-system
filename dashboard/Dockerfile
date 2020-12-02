FROM rocker/shiny:latest

RUN apt-get update \
  && apt-get install -y --no-install-recomends libmysqlclient-dev

RUN R -e "install.packages(c('RMySQL','dplyr'))"
