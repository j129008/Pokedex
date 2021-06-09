FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y python3 python3-pip mysql-client python3-dev build-essential libssl-dev libffi-dev \
    && apt-get purge -y --auto-remove

# install python modules
COPY requirements.txt /root/
RUN pip3 install -r /root/requirements.txt

# setting ssh-server
RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd && \
    echo 'root:dockerpassword' | chpasswd && \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
