-- CREAR BASE DE DATOS DE TIENDA ONLINE
CREATE DATABASE tienda_online;
USE tienda_online;
-- TABLAS
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    ciudad VARCHAR(50),
    pais VARCHAR(50),
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'activo'
);
CREATE TABLE categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);
CREATE TABLE productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    categoria_id INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT DEFAULT 0,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'activo',
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);
CREATE TABLE pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT NOT NULL,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega DATE,
    estado VARCHAR(30) DEFAULT 'pendiente',
    total DECIMAL(10, 2),
    direccion_envio VARCHAR(200),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
CREATE TABLE detalles_pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
CREATE TABLE empleados (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    puesto VARCHAR(50),
    salario DECIMAL(10, 2),
    fecha_contratacion DATE,
    departamento VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE
);
-- ÍNDICES
CREATE INDEX idx_clientes_ciudad ON clientes(ciudad);
CREATE INDEX idx_clientes_email ON clientes(email);
CREATE INDEX idx_productos_categoria ON productos(categoria_id);
CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
CREATE INDEX idx_pedidos_estado ON pedidos(estado);
CREATE INDEX idx_detalles_pedido ON detalles_pedidos(pedido_id);
-- DATOS: CATEGORIAS
INSERT INTO categorias (nombre, descripcion) VALUES
('Electrónica', 'Productos electrónicos y dispositivos'),
('Ropa', 'Prendas de vestir para hombres y mujeres'),
('Libros', 'Libros de diversos géneros'),
('Deportes', 'Equipamiento y artículos deportivos'),
('Hogar', 'Artículos y accesorios para el hogar'),
('Belleza', 'Productos de belleza y cuidado personal');
-- DATOS: CLIENTES
INSERT INTO clientes (nombre, email, telefono, ciudad, pais) VALUES
('Juan García', 'juan.garcia@email.com', '3101234567', 'Bogotá', 'Colombia'),
('María López', 'maria.lopez@email.com', '3107654321', 'Medellín', 'Colombia'),
('Carlos Rodríguez', 'carlos.rod@email.com', '3109876543', 'Cali', 'Colombia'),
('Ana Martínez', 'ana.martinez@email.com', '3102223333', 'Bogotá', 'Colombia'),
('Luis Fernández', 'luis.fernandez@email.com', '3104445555', 'Cartagena', 'Colombia'),
('Sofia Gómez', 'sofia.gomez@email.com', '3106667777', 'Bogotá', 'Colombia'),
('Pedro Sánchez', 'pedro.sanchez@email.com', '3108889999', 'Barranquilla', 'Colombia'),
('Laura Díaz', 'laura.diaz@email.com', '3100001111', 'Bogotá', 'Colombia'),
('Miguel Torres', 'miguel.torres@email.com', '3102225555', 'Santa Marta', 'Colombia'),
('Daniela Cruz', 'daniela.cruz@email.com', '3103337777', 'Bogotá', 'Colombia');
-- DATOS: PRODUCTOS
INSERT INTO productos (nombre, descripcion, categoria_id, precio, stock) VALUES
('Laptop HP 15', 'Laptop con procesador Intel i7, 16GB RAM', 1, 1200000, 5),
('Mouse Logitech', 'Mouse inalámbrico con batería', 1, 45000, 20),
('Teclado Mecánico', 'Teclado mecánico RGB', 1, 350000, 8),
('Monitor LG 27"', 'Monitor 4K UHD 27 pulgadas', 1, 800000, 3),
('Camisa Casual', 'Camisa de algodón para hombre', 2, 89000, 15),
('Pantalón Jeans', 'Pantalón jeans azul oscuro', 2, 120000, 25),
('Zapatos Deportivos', 'Zapatillas para correr', 2, 250000, 12),
('Harry Potter y la Piedra Filosofal', 'Novela de fantasía', 3, 35000, 10),
('El Quijote', 'Clásico de la literatura española', 3, 45000, 8),
('Balon de Fútbol', 'Balón profesional de fútbol', 4, 150000, 20),
('Bicicleta de Montaña', 'Bicicleta 21 velocidades', 4, 1500000, 2),
('Lámpara LED', 'Lámpara de escritorio LED', 5, 85000, 18),
('Almohada Ergonómica', 'Almohada para mejor descanso', 5, 120000, 12),
('Crema Facial', 'Crema hidratante para todo tipo de piel', 6, 65000, 30),
('Perfume', 'Perfume de lujo para hombre', 6, 250000, 10);
-- DATOS: EMPLEADOS
INSERT INTO empleados (nombre, email, puesto, salario, fecha_contratacion, departamento) VALUES
('Roberto Jiménez', 'roberto.jimenez@tienda.com', 'Gerente General', 5000000, '2022-01-15', 'Administración'),
('Jennifer García', 'jennifer.garcia@tienda.com', 'Gerente de Ventas', 4000000, '2022-03-20', 'Ventas'),
('David López', 'david.lopez@tienda.com', 'Vendedor', 2000000, '2023-06-10', 'Ventas'),
('Patricia Morales', 'patricia.morales@tienda.com', 'Vendedora', 2000000, '2023-07-15', 'Ventas'),
('Ricardo Suárez', 'ricardo.suarez@tienda.com', 'Administrador de BD', 3500000, '2022-02-01', 'Tecnología'),
('Katrina Pérez', 'katrina.perez@tienda.com', 'Gerente de Logística', 3800000, '2022-04-05', 'Logística'),
('Javier Castillo', 'javier.castillo@tienda.com', 'Operario Almacén', 1800000, '2023-01-20', 'Logística');
-- DATOS: PEDIDOS
INSERT INTO pedidos (cliente_id, fecha_pedido, fecha_entrega, estado, total, direccion_envio) VALUES
(1, '2024-01-10 14:30:00', '2024-01-15', 'entregado', 1245000, 'Cra 7 #125-40, Bogotá'),
(2, '2024-01-12 10:15:00', '2024-01-18', 'entregado', 89000, 'Cra 45 #20-30, Medellín'),
(3, '2024-01-15 09:00:00', '2024-01-22', 'en_transito', 2950000, 'Cra 3 #80-45, Cali'),
(4, '2024-01-18 16:45:00', NULL, 'pendiente', 535000, 'Cra 10 #95-20, Bogotá'),
(5, '2024-01-20 11:30:00', '2024-01-26', 'entregado', 250000, 'Cra 2 #15-60, Cartagena'),
(6, '2024-02-02 13:00:00', '2024-02-08', 'entregado', 150000, 'Cra 8 #110-30, Bogotá'),
(1, '2024-02-05 10:20:00', NULL, 'procesando', 1500000, 'Cra 7 #125-40, Bogotá'),
(7, '2024-02-08 15:10:00', '2024-02-14', 'entregado', 350000, 'Cra 20 #50-70, Barranquilla'),
(8, '2024-02-10 12:40:00', NULL, 'pendiente', 465000, 'Cra 15 #120-50, Bogotá'),
(9, '2024-02-12 09:30:00', '2024-02-18', 'entregado', 800000, 'Cra 5 #30-20, Santa Marta');
-- DATOS: DETALLES PEDIDOS
INSERT INTO detalles_pedidos (pedido_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 1, 1200000, 1200000),
(1, 2, 1, 45000, 45000),
(2, 5, 1, 89000, 89000),
(3, 7, 1, 250000, 250000),
(3, 12, 2, 85000, 170000),
(3, 14, 3, 65000, 195000),
(3, 11, 1, 1500000, 1500000),
(4, 6, 2, 120000, 240000),
(4, 10, 1, 150000, 150000),
(4, 15, 1, 250000, 250000),
(5, 8, 1, 35000, 35000),
(5, 3, 1, 350000, 350000),
(6, 4, 2, 150000, 300000),
(7, 9, 1, 45000, 45000),
(7, 1, 1, 1200000, 1200000),
(7, 11, 1, 1500000, 1500000),
(8, 5, 2, 89000, 178000),
(8, 13, 1, 120000, 120000),
(9, 12, 3, 85000, 255000),
(9, 14, 2, 65000, 130000);
-- VERIFICAR REGISTROS
SELECT 'Clientes' as tabla, COUNT(*) as registros FROM clientes UNION ALL
SELECT 'Categorías', COUNT(*) FROM categorias UNION ALL
SELECT 'Productos', COUNT(*) FROM productos UNION ALL
SELECT 'Pedidos', COUNT(*) FROM pedidos UNION ALL
SELECT 'Detalles Pedidos', COUNT(*) FROM detalles_pedidos UNION ALL
SELECT 'Empleados', COUNT(*) FROM empleados;
