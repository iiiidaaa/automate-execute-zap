FROM owasp/zap2docker-stable

USER root

RUN apt-get update \
      && apt-get -y upgrade  \
      && apt-get install -y python3-pip \
      && pip3 install elasticsearch \
      && pip3 install requests \
      && pip3 install python-owasp-zap-v2.4 \
      # clean up
      && apt-get clean

USER zap

ADD scripts/ /zap/zapscripts/