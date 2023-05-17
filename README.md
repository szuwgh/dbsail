# dbsail
This tool is used to connect to mysql or postgresql and insert data of customizable size


##  User Guide

#### insert mysql data
```
$ ./dbsail mysql -h 127.0.0.1 -u root -p 123456 -s 10M
This tool is used to connect to mysql or postgresql and insert data of customizable size, power by wgh

 ____    ____     ____    ______  ______   __
/\  _`\ /\  _`\  /\  _`\ /\  _  \/\__  _\ /\ \
\ \ \/\ \ \ \L\ \\ \,\L\_\ \ \L\ \/_/\ \/ \ \ \
 \ \ \ \ \ \  _ <'\/_\__ \\ \  __ \ \ \ \  \ \ \  __
  \ \ \_\ \ \ \L\ \ /\ \L\ \ \ \/\ \ \_\ \__\ \ \L\ \
   \ \____/\ \____/ \ `\____\ \_\ \_\/\_____\\ \____/
    \/___/  \/___/   \/_____/\/_/\/_/\/_____/ \/___/

running dbsail mysql model

connect mysql success 192.168.255.128:3306
create data base testdbbase
use data base testdbbase
create table test1

you will insert 10240 rows of data

Processing ████████████████████████████████████████████████████████████████ 100%
finish insert 10240 rows data, usage time 00:00:03
```

#### insert postgresql data

```
$ ./dbsail pg -h 127.0.0.1 -u test -p 123456 -s 10M
This tool is used to connect to mysql or postgresql and insert data of customizable size, power by wgh

 ____    ____     ____    ______  ______   __
/\  _`\ /\  _`\  /\  _`\ /\  _  \/\__  _\ /\ \
\ \ \/\ \ \ \L\ \\ \,\L\_\ \ \L\ \/_/\ \/ \ \ \
 \ \ \ \ \ \  _ <'\/_\__ \\ \  __ \ \ \ \  \ \ \  __
  \ \ \_\ \ \ \L\ \ /\ \L\ \ \ \/\ \ \_\ \__\ \ \L\ \
   \ \____/\ \____/ \ `\____\ \_\ \_\/\_____\\ \____/
    \/___/  \/___/   \/_____/\/_/\/_/\/_____/ \/___/

running dbsail postgresql model

connect postgresql success 127.0.0.1:5432 postgres
create data base testdbbase
connect postgresql success 127.0.0.1:5432 testdbbase
create table test1

you will insert 10240 rows of data

Processing ████████████████████████████████████████████████████████████████ 100%
finish insert 10240 rows data, usage time 00:00:02
```

#### clean data
```
$ ./dbsail mysql clean -h 127.0.0.1 -u test -p 123456
$ ./dbsail pg clean -h 127.0.0.1 -u test -p 123456
This tool is used to connect to mysql or postgresql and insert data of customizable size, power by wgh

 ____    ____     ____    ______  ______   __
/\  _`\ /\  _`\  /\  _`\ /\  _  \/\__  _\ /\ \
\ \ \/\ \ \ \L\ \\ \,\L\_\ \ \L\ \/_/\ \/ \ \ \
 \ \ \ \ \ \  _ <'\/_\__ \\ \  __ \ \ \ \  \ \ \  __
  \ \ \_\ \ \ \L\ \ /\ \L\ \ \ \/\ \ \_\ \__\ \ \L\ \
   \ \____/\ \____/ \ `\____\ \_\ \_\/\_____\\ \____/
    \/___/  \/___/   \/_____/\/_/\/_/\/_____/ \/___/

connect postgresql success 127.0.0.1:5432 postgres
drop data base testdbbase
```


Commands:
* `version`: show version
* `pg`: use postgresql model
* `mysql`: use mysql model
* `clean`: drop database

Common options

* `-help`: Show dbsail's condensed help output.
* `-h/--host`: database host address
* `-u/--user`: database user account
* `-P/--port`: database port
* `-P/--password`: database user passport
* `-b/--batch`: the number of rows inserted into the database at a time, e.g.: 10
* `-c/--count`: the total number of rows inserted into the database, e.g.: 1000
* `-s/--size`: total size of inserts into the database, e.g.:1K,1M,1G defalut:10M
* `-d/--database`: select the database to insert, e.g.:testdbbase