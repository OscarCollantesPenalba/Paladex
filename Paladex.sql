USE Paladex;


DROP TABLE IF EXISTS Participantes;
DROP TABLE IF EXISTS Modera_Mazo;
DROP TABLE IF EXISTS Mazo_Carta;
DROP TABLE IF EXISTS Mazos;
DROP TABLE IF EXISTS Habilidades;
DROP TABLE IF EXISTS Cartas;
DROP TABLE IF EXISTS Campeon;
DROP TABLE IF EXISTS Clase_campeon;
DROP TABLE IF EXISTS Usuario;
DROP TABLE IF EXISTS Rol;
DROP TABLE IF EXISTS secciones;
DROP TABLE IF EXISTS Torneos;


CREATE TABLE Rol (
    id_rol INT PRIMARY KEY,    
    nombre_rol VARCHAR(50) NOT NULL 
);

CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(100) NOT NULL, 
    correo VARCHAR(150) UNIQUE NOT NULL,  
    contrasena VARCHAR(255) NOT NULL,
    puntos_experiencia INT DEFAULT 0,     
    id_rol INT NOT NULL,                  
    
    CONSTRAINT fk_rol                     
        FOREIGN KEY (id_rol) 
        REFERENCES Rol(id_rol)
);

CREATE TABLE Clase_campeon (
    id_clase INT PRIMARY KEY,
    nombre_clase VARCHAR(50) NOT NULL
);

CREATE TABLE Campeon(
    id_campeon INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    titulo VARCHAR(100),
    salud INT DEFAULT 100,
    daño FLOAT DEFAULT 100,
    velocidad FLOAT DEFAULT 100,
    id_clase INT NOT NULL,

    CONSTRAINT fk_clase
        FOREIGN KEY (id_clase)
        REFERENCES Clase_campeon(id_clase)
);

CREATE TABLE Habilidades(
    id_habilidad INT PRIMARY KEY,
    nombre VARCHAR(50),
    tipo VARCHAR(50),
    descripcion VARCHAR(200),
    id_campeon INT NOT NULL,

    CONSTRAINT fk_campeon
        FOREIGN KEY (id_campeon)
        REFERENCES  Campeon(id_campeon)
);

CREATE TABLE Cartas (
    id_carta INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(200),
    categoria VARCHAR(50),
    id_campeon INT NOT NULL,
    
    CONSTRAINT fk_cartas_campeon 
        FOREIGN KEY (id_campeon) 
        REFERENCES Campeon(id_campeon) 
        ON DELETE CASCADE
);

CREATE TABLE Mazos(
    id_mazo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_mazo VARCHAR(100),
    descripcion VARCHAR(200),
    estado VARCHAR(50),      
    id_usuario INT NOT NULL,  
    id_campeon INT NOT NULL,  

    CONSTRAINT fk_usuario 
        FOREIGN KEY (id_usuario) 
        REFERENCES Usuario(id_usuario),
    CONSTRAINT fk_campeon_2 
        FOREIGN KEY (id_campeon) 
        REFERENCES Campeon(id_campeon)
);

CREATE TABLE Mazo_Carta (
    id_mazo INT,             
    id_carta INT,                 
    nivel_carta INT NOT NULL,    
    PRIMARY KEY (id_mazo, id_carta),

    CONSTRAINT fk_mazo
        FOREIGN KEY (id_mazo) 
        REFERENCES Mazos(id_mazo) ON DELETE CASCADE,
    CONSTRAINT fk_carta
        FOREIGN KEY (id_carta) 
        REFERENCES Cartas(id_carta)
);

CREATE TABLE Modera_Mazo(
    id_moderacion INT PRIMARY KEY,
    accion VARCHAR(50),
    comentario VARCHAR(200) NULL,
    fecha DATE,
    id_usuario INT NOT NULL,
    id_mazo INT NOT NULL,

    CONSTRAINT fk_usuario_2
        FOREIGN KEY (id_usuario)
        REFERENCES Usuario(id_usuario),
    CONSTRAINT fk_mazo_2
        FOREIGN KEY (id_mazo)
        REFERENCES Mazos(id_mazo)
);

CREATE TABLE secciones(
    id_seccion INT PRIMARY KEY,
    titulo VARCHAR(100),
    contenido VARCHAR(200)
);

CREATE TABLE Torneos(
    id_torneo INT PRIMARY KEY,
    nombre VARCHAR(100),
    ubicacion VARCHAR(150),
    descripcion VARCHAR(200),
    reglas VARCHAR (200)
);

CREATE TABLE Participantes(
    id_usuario INT,
    id_torneo INT,
    alias VARCHAR(100), 
    equipo VARCHAR(100),
    win INT DEFAULT 0,
    loss INT DEFAULT 0,
    PRIMARY KEY (id_usuario, id_torneo),

    CONSTRAINT fk_usuario_3
        FOREIGN KEY (id_usuario) 
        REFERENCES Usuario(id_usuario),
    CONSTRAINT fk_torneo 
        FOREIGN KEY (id_torneo) 
        REFERENCES Torneos(id_torneo)
);
