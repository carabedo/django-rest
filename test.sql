ALTER TABLE movimientos
  ADD ID INTEGER

-- https://stackoverflow.com/questions/36852745/add-an-autoincrementing-id-column-to-an-existing-table-with-sqlite
-- deberia crearme una nueva tabla agregando pk id autoincrement

ALTER TABLE clientes
  ADD ID INTEGER



ALTER TABLE prestamos
  ADD ID INTEGER


CREATE TABLE dni (
    PersonID int,
    LastName varchar(255),
    FirstName varchar(255),
    Address varchar(255),
    City varchar(255) 
);


DROP TABLE sucursales;


#### OBTENER DATOS DE UN CLIENTE

Un cliente autenticado puede consultar sus propios datos

GET con permisos de lectura y escritura a la tabla de CLIENTES
  
#### OBTENER SALDO DE CUENTA DE UN CLIENTE

Un cliente autenticado puede obtener el tipo de cuenta y su saldo.

GET con permiso de lectura a la tabla CUENTAS

#### OBTENER MONTO DE PRESTAMOS DE UN CLIENTE

Un cliente autenticado puede obtener el tipo de préstamo y total del mismo.

GET con permiso de lectura a la tabla PRESTAMOS


#### OBTENER MONTO DE PRESTAMOS DE UNA SUCURSAL

Un empleado autenticado puede obtener el listado de préstamos otorgados de una sucursal determinada.

GET LISTVIEW de PRESTAMOS por sucursal.

#### OBTENER TARJETAS ASOCIADAS A UN CLIENTE
 
Un empleado autenticado puede obtener el listado de tarjetas de crédito de un cliente determinado


GET LISTVIEW de TARJETAS por CLIENTES.

#### GENERAR UNA SOLICITUD DE PRESTAMO PARA UN CLIENTE

Un empleado autenticado puede solicitar un préstamo para un cliente, registrado el mismo y acreditando el saldo en su cuenta

POST a PRESTAMOS

#### ANULAR SOLICITUD DE PRESTAMO DE CLIENTE

Un empleado autenticado puede anular un préstamo para un cliente, revirtiendo el monto correspondiente

DELETE a PRESTAMOS

#### MODIFICAR DIRECCION DE UN CLIENTE

El propio cliente autenticado o un empleado puede modificar las direcciones.

UPDATE a DIRECCIONES

#### LISTADO DE TODAS LAS SUCURSALES

Un endpoint público que devuelve el listado todas las sucursales con la información correspondiente.

GET LIST/DETAILS de la tabla de sucursales.