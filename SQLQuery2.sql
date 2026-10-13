Create DATABASE Inventarios_SQLyPython; 
USE Inventarios_SQLyPython;


CREATE TABLE Detalle_Venta
(
  ID_producto     VARCHAR(10)   NOT NULL,
  ID_VENTA        INT           NOT NULL,
  Cantidad        INT           NULL    ,
  Precio_Unitario DECIMAL(10,2) NULL    ,
  PRIMARY KEY (ID_producto, ID_VENTA)
);


CREATE TABLE Movimiento_Inventario
(
  ID_Movimiento     INT          NOT NULL IDENTITY(1,1),
  ID_producto       VARCHAR(10)  NOT NULL,
  Codigo_movimiento VARCHAR(9)   NULL    ,
  Tipo_movimiento   VARCHAR(100) NOT NULL,
  Cantidad          INT          NOT NULL,
  Fecha             DATETIME     NOT NULL,
  Motivo            VARCHAR(300) NULL    ,
  PRIMARY KEY (ID_Movimiento)
);

ALTER TABLE Movimiento_Inventario
  ADD CONSTRAINT UQ_ID_Movimiento UNIQUE (ID_Movimiento);

ALTER TABLE Movimiento_Inventario
  ADD CONSTRAINT UQ_Codigo_movimiento UNIQUE (Codigo_movimiento);

CREATE TABLE Producto
(
  ID_producto      INT           NOT NULL IDENTITY(1,1),
  Codigo_producto  VARCHAR(9)    NULL    ,
  nombre_P         VARCHAR(100)  NOT NULL,
  Codigo_barra_P   VARCHAR(13)   NOT NULL,
  Descripcion_P    VARCHAR(300)  NULL    ,
  Stock_disponible INT           NOT NULL,
  UnitPrice        DECIMAL(10,2) NOT NULL,
  TotalVendido     DECIMAL(10,2) NULL    ,
  PRIMARY KEY (ID_producto)
);

ALTER TABLE Producto
  ADD CONSTRAINT UQ_ID_producto UNIQUE (ID_producto);

ALTER TABLE Producto
  ADD CONSTRAINT UQ_Codigo_producto UNIQUE (Codigo_producto);

ALTER TABLE Producto
  ADD CONSTRAINT UQ_Codigo_barra_P UNIQUE (Codigo_barra_P);

CREATE TABLE Prove_Produc
(
  ID_provedor VARCHAR(10) NOT NULL,
  ID_producto VARCHAR(10) NOT NULL
);

CREATE TABLE Proveedor
(
  ID_provedor  VARCHAR(10)  NOT NULL,
  nombre_prove VARCHAR(100) NOT NULL,
  Email        VARCHAR(100) NOT NULL,
  Telefono     VARCHAR(14) NULL    ,
  PRIMARY KEY (ID_provedor)
);

ALTER TABLE Proveedor
  ADD CONSTRAINT UQ_ID_provedor UNIQUE (ID_provedor);

ALTER TABLE Proveedor
  ADD CONSTRAINT UQ_Email UNIQUE (Email);

CREATE TABLE Venta
(
  ID_VENTA     INT           NOT NULL IDENTITY(1,1),
  Codigo_venta VARCHAR(9)    NOT NULL,
  Fecha        DATETIME      NOT NULL,
  TOTAL        DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (ID_VENTA)
);

ALTER TABLE Venta
  ADD CONSTRAINT UQ_ID_VENTA UNIQUE (ID_VENTA);

ALTER TABLE Venta
  ADD CONSTRAINT UQ_Codigo_venta UNIQUE (Codigo_venta);

ALTER TABLE Prove_Produc
  ADD CONSTRAINT FK_Proveedor_TO_Prove_Produc
    FOREIGN KEY (ID_provedor)
    REFERENCES Proveedor (ID_provedor);

ALTER TABLE Prove_Produc
  ADD CONSTRAINT FK_Producto_TO_Prove_Produc
    FOREIGN KEY (ID_producto)
    REFERENCES Producto (ID_producto);

ALTER TABLE Movimiento_Inventario
  ADD CONSTRAINT FK_Producto_TO_Movimiento_Inventario
    FOREIGN KEY (ID_producto)
    REFERENCES Producto (ID_producto);

ALTER TABLE Detalle_Venta
  ADD CONSTRAINT FK_Producto_TO_Detalle_Venta
    FOREIGN KEY (ID_producto)
    REFERENCES Producto (ID_producto);

ALTER TABLE Detalle_Venta
  ADD CONSTRAINT FK_Venta_TO_Detalle_Venta
    FOREIGN KEY (ID_VENTA)
    REFERENCES Venta (ID_VENTA);