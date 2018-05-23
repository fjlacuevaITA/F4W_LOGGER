#FROM bfranco1/syslog

FROM bobrik/syslog-ng

##FROM balabit/syslog-ng-dev:latest

COPY ./libs /opt/kafka/lib

COPY kong.log /var/log/kong.log

##RUN apt-get update

##RUN git clone https://github.com/balabit/syslog-ng.git

##COPY ./syslog-ng.conf /install/syslog/etc/syslog-ng.conf
##WORKDIR ./syslog-ng

##RUN pip install -r requirements.txt

##RUN ./autogen.sh

##RUN mkdir build

##WORKDIR ./build

##RUN ../configure --enable-debug --prefix=/install/syslog-ng

##RUN make

##RUN make check

##RUN make install

#ENV SYSLOGNG_OPT=--no-caps

VOLUME ["/var/log" ,"/etc/syslog-ng/", "/etc/default/"]

