#!/bin/bash -e

# set up zap options
mkdir -p jenkins_home/scripts jenkins_home/.ZAP/scripts/scripts/authentication
cp zap_option/login.zst   jenkins_home/.ZAP/scripts/scripts/authentication/
cp zap_option/sendJson.py jenkins_home/scripts/
cp zap_option/com.cloudbees.jenkins.plugins.customtools.CustomTool.xml jenkins_home/
chown -R 1000 jenkins_home/.ZAP
chown -R 1000 jenkins_home/scripts
chown -R 1000 jenkins_home/com.cloudbees.jenkins.plugins.customtools.CustomTool.xml

# create job
docker exec -i jenkins_zap java -jar /var/jenkins_home/war/WEB-INF/jenkins-cli.jar -s http://localhost:8080 create-job ZAP_EXAMPLE_JOB < zap_option/config.xml
docker exec -i jenkins_zap java -jar /var/jenkins_home/war/WEB-INF/jenkins-cli.jar -s http://localhost:8080 create-job SEND_ES < zap_option/config_sendes.xml
cp zap_option/config.xml jenkins_home/jobs/ZAP_EXAMPLE_JOB/config.xml
cp zap_option/config_sendes.xml jenkins_home/jobs/SEND_ES/config.xml

# restart for reload configuration files
docker restart jenkins_zap
