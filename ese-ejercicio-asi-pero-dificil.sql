Create table Tipos_de_movimientos(
	idTipo int not null,
	nombre varchar(20),
	tipo int
	constraint PK_idTipo primary key(idTipo)
)
 
create table Movimientos(
	idMovimiento int not null,
	fechaMovimiento date,
	idProveedor int,
	cantidadComprada int,
	precioCompra decimal(10,2),
	precioVenta decimal(10,2),
	idTipoMovimiento int not null,
	orderId int,
 
	constraint PK_idMovimiento primary key(idMovimiento),
	constraint FK_idTipoMovimientoMo foreign key (idTipoMovimiento) references Tipos_de_movimientos(idTipo),
	constraint FK_idProveedorMo foreign key (idProveedor) references Suppliers(SupplierID),
	constraint FK_orderIdMo foreign key (orderId) references Orders(OrderID)
)
 
declare @idproducto int
 
declare productos cursor scroll for
	select ProductID
	from Products
open products
fetch next from productos into @idProducto
 
	select p.ProductID, sum(p.UnitsInStock)
	from Products p
	group by p.ProductID
close productos
deallocate productos
 
create procedure sp_Ingreso_Poructo
@concepto varchar(50),


update Products set UnitsInStock = UnitsInStock + @cantidad where ProductID = @idproducto
 
 
while @contador < (select count(ProductID) from Products) begin

end
 
declare productos_totales cursor for
	select p.ProductID, p.UnitsInStock, od.Quantity, (p.UnitsInStock + od.Quantity) as suma
	from Products p, [Order Details] od
	where p.ProductID = od.ProductID
 
select * from Products
select * from [Order Details]
 
select * from Suppliers