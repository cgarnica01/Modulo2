LOAD DATA INFILE "/var/lib/mysql-files/201411.csv"
INTO TABLE Modulo2.verificentro
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(Placa,VIN,Marca,Submarca,Modelo,CertificadoId,VerificentroId,Linea,@Var_Fecha,@Var_Hora,Resultado,CausaRechazo)
SET Fecha = STR_TO_DATE(TRIM(@Var_Fecha),'%Y/%c/%d'),
    Hora = TRIM(@Var_Hora);
