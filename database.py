
from fabric.api import *
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='ecommerce-app',
)

with connection.cursor() as cursor:
    sql = "CREATE TABLE IF NOT EXISTS `ecommerce-app`.`items1` ( `id` SMALLINT AUTO_INCREMENT , " \
          "`name` VARCHAR(30) NOT NULL , `price` SMALLINT NOT NULL , `quantity` SMALLINT  NOT NULL, " \
          "PRIMARY KEY (`id`)) ENGINE = InnoDB"
    cursor.execute(sql)

    sql = "CREATE TABLE IF NOT EXISTS `ecommerce-app`.`orders1` ( `id` SMALLINT AUTO_INCREMENT , " \
          "`itemid` SMALLINT NOT NULL , `quantity` SMALLINT  NOT NULL, `useremail` VARCHAR(30) NOT NULL, " \
          "PRIMARY KEY (`id`), FOREIGN KEY (`itemid`) REFERENCES items1(`id`)) ENGINE = InnoDB"
    cursor.execute(sql)
