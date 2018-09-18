DROP DATABASE Modulo2;
CREATE DATABASE Modulo2;
USE Modulo2;
DROP TABLE verificentro;
CREATE TABLE verificentro (
       Placa		VARCHAR(10),
       VIN		VARCHAR(30),
       Marca		VARCHAR(50),
       Submarca		VARCHAR(50),
       Modelo		VARCHAR(60),
       CertificadoId	VARCHAR(30),
       VerificentroId	VARCHAR(30),
       Linea		VARCHAR(5),
       Fecha            DATE,
       Hora		TIME,
       Resultado	VARCHAR(30),
       CausaRechazo	VARCHAR(50));

