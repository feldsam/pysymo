FROM ubuntu:14.04
MAINTAINER icoz

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get -y -q install software-properties-common python-software-properties
RUN add-apt-repository ppa:adiscon/v8-stable
RUN apt-get update && apt-get -y -q install rsyslog rsyslog-mongodb mongodb && apt-get clean

RUN sed 's/module(load="imklog")/#module(load="imklog")/' -i /etc/rsyslog.conf
RUN sed 's/#$ModLoad imudp/$ModLoad imudp/' -i /etc/rsyslog.conf
RUN sed 's/#$UDPServerRun 514/$UDPServerRun 514/' -i /etc/rsyslog.conf
RUN sed 's/#$ModLoad imtcp/$ModLoad imtcp/' -i /etc/rsyslog.conf
RUN sed 's/#$InputTCPServerRun 514/$InputTCPServerRun 514/' -i /etc/rsyslog.conf
RUN sed 's/$ModLoad imklog/#$ModLoad imklog/' -i /etc/rsyslog.conf

RUN mv /etc/rsyslog.d/50-default.conf /etc/rsyslog.d/50-default.old
ADD ./10-mongodb.conf /etc/rsyslog.d/10-mongodb.conf

EXPOSE 514/tcp 514/udp

ENTRYPOINT ["/usr/sbin/rsyslogd"]
CMD ["-n"]

