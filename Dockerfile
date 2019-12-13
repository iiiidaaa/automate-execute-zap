FROM jenkins/jenkins:lts

# skip setup Wizard
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

USER root
COPY plugins.txt /usr/share/jenkins/ref/
RUN apt-get update \
      && apt-get -y upgrade  \
      && apt-get install -y python3 python3-pip \
      && pip3 install elasticsearch \
      # pre-install jenkins plugins
      && /usr/local/bin/install-plugins.sh $(cat /usr/share/jenkins/ref/plugins.txt) \
      # clean up
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

USER jenkins
