#FROM python:3-alpine
FROM kernelci/build-base

RUN apt-get update && apt-get install -y python3-pip python3-setuptools
RUN python3 -m pip install --upgrade pip setuptools
RUN python3 -m pip install --upgrade kernelci

# custom concourse resouurce
ADD setup.py app/
ADD kci_resource app/kci_resource
RUN python3 -m pip install --no-cache-dir app/
#RUN python3 -m pip install --no-cache-dir app/  --install-option="--install-scripts=/opt/resource"

RUN mkdir /opt/resource
RUN ln -s /usr/local/bin/check /opt/resource/check
RUN ln -s /usr/local/bin/in /opt/resource/in
RUN ln -s /usr/local/bin/out /opt/resource/out

# also need local copy of kernelci-core for config yaml files
RUN git clone -b staging.kernelci.org https://github.com/kernelci/kernelci-core.git /kci/kernelci-core
