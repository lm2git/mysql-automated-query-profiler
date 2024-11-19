FROM mysql:5.7


ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=testdb
ENV MYSQL_USER=testuser
ENV MYSQL_PASSWORD=testpassword

COPY my.cnf /etc/mysql/my.cnf


COPY ./init-scripts /docker-entrypoint-initdb.d/


EXPOSE 3306
