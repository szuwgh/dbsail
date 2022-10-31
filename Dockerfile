ARG CENTOS_VERSION=7
FROM centos:$CENTOS_VERSION

# Python 2.7.5 is installed with centos7 image
# Add repository for PIP
# 安装依赖
RUN yum install -y epel-release \
    && yum install -y libffi-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel zlib gcc make libpcap-devel xz-devel gdbm-devel

# 安装python3.x
RUN yum -y install wget \
    && wget https://www.python.org/ftp/python/3.9.2/Python-3.9.2.tgz \
    && tar -zxvf Python-3.9.2.tgz \
    && cd Python-3.9.2 && ./configure --prefix=/usr/local/python3 --enable-shared --with-threads \
    && make \
    && make install \ 
    && make clean \
    && rm -rf /Python-3.9.2* \
    && ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3 \
    && ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3


ENV LD_LIBRARY_PATH=/usr/local/python3/lib

#安装一些 pip包
RUN yum install -y postgresql-devel \
	&& pip3 install click && pip3 install psycopg2-binary && pip3 install pymysql && pip3 install progress && pip3 install pyinstaller

COPY ./dbsail.py /opt/dbdata/
RUN  cd /opt/dbdata/ && /usr/local/python3/bin/pyinstaller -F /opt/dbdata/dbsail.py
ENTRYPOINT [ "/bin/sh"]
