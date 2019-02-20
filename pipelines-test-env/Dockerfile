# docker container description file for NEMO_Nowcast package testing environment
#
# Primarily intended for creation of a docker image for use by bitbucket-pipelines.yml.

FROM continuumio/miniconda3

# Create nemo-nowcast-test conda env
ADD ./environment-test.yaml /tmp/environment-test.yaml
RUN conda env create -f /tmp/environment-test.yaml
