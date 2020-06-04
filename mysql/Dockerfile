FROM mysql:5.7
ADD ./init/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf
COPY ./init/init.sql /docker-entrypoint-initdb.d
