* La simulación consiste en un supermercado que tiene llegadas poisson que se entregan en un el parametro ARRIVAL_DATA.
    - Ej: `ARRIVAL_DATA = [[8, 11], [9, 30]]` sería una llegada en la hora 8 de 11 personas promedio y a las 9 de 30 personas promedio.
* A los clientes se le genera una cantidad aleatoria de productos usando los parámetros MIN_PRODS y MAX_PRODS.
* Se tiene un listado de cajeros con horas de entrada y salida, descritos en CASHIER_DATA.
    - Ej: `CASHIER_DATA = [[8, 16], [15, 24]]` serían dos cajeros, uno de 8 a 16 hrs., y otro de 15 a 24 hrs.
* El tiempo de proceso por producto se da en segundos en la variable PROC_TIME.
* SIM_TIME es la cantidad de minutos que va a correr la simulación.
