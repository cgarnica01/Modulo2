# Modulo2
Pasos para cargar el archivo en MYSQL
1 .- Con root copiar el archivo CSV 201411.csv al directorio /var/lib/mysql-files
2. - Cambiar los permisos del directorio a 755, chmod 755 /var/lib/mysql-files

Correr los arhivos con linea de comando de MYSQL en el siguiente orden:

mysql -u root -p "Cic1234*" -f < crea_tabla_verificentro.sql
mysql -u root -p "Cic1234*" Modulo2 < carga_datos.sql


Si no manda error entonces conectarse a mysql y verificar que se cargaron los datos

mysql -u root -p Modulo2
mysql> show tables;
mysql> desc verificentro;
mysql> select count(*) verificentro;


Nota: En este caso la BD se llama Modulo2 y la Tabla verificentro
