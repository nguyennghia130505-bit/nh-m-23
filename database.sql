-- phpMyAdmin SQL Dump
-- Host: 127.0.0.1
-- Database: dien_khu_dan_cu

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- Tạo Database
CREATE DATABASE IF NOT EXISTS `dien_khu_dan_cu` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `dien_khu_dan_cu`;

-- Xóa các bảng cũ nếu tồn tại (theo thứ tự khóa ngoại để tránh lỗi)
DROP TABLE IF EXISTS `invoices`;
DROP TABLE IF EXISTS `electricity_readings`;
DROP TABLE IF EXISTS `meters`;
DROP TABLE IF EXISTS `customers`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `electricity_tiers`;

-- --------------------------------------------------------
-- Cấu trúc bảng `users`
CREATE TABLE `users` (
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `ho_ten` varchar(100) NOT NULL,
  `role` varchar(20) NOT NULL DEFAULT 'staff'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `users` (`username`, `password`, `ho_ten`, `role`) VALUES
('admin', '123', 'Quản trị viên', 'admin'),
('nhanvien', 'abc', 'Nhân Viên A', 'staff');

-- --------------------------------------------------------
-- Cấu trúc bảng `customers`
CREATE TABLE `customers` (
  `ma_kh` varchar(20) NOT NULL,
  `ten` varchar(100) NOT NULL,
  `dia_chi` varchar(255) NOT NULL,
  `sdt` varchar(20) NOT NULL,
  `trang_thai` varchar(50) NOT NULL DEFAULT 'Đang hoạt động'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `customers` (`ma_kh`, `ten`, `dia_chi`, `sdt`, `trang_thai`) VALUES
('KH001', 'Nguyễn Văn An', '12 Lý Tự Trọng, P.1, Q.1', '0901234567', 'Đang hoạt động'),
('KH002', 'Trần Thị Bình', '45 Nguyễn Huệ, P.2, Q.1', '0912345678', 'Đang hoạt động'),
('KH003', 'Lê Minh Cường', '78 Hai Bà Trưng, P.3, Q.3', '0923456789', 'Đang hoạt động'),
('KH004', 'Phạm Thị Dung', '23 Đinh Tiên Hoàng, P.4, Q.Bình Thạnh', '0934567890', 'Tạm ngừng'),
('KH005', 'Hoàng Văn Em', '56 Lê Văn Sỹ, P.12, Q.3', '0945678901', 'Đang hoạt động'),
('KH006', 'Vũ Thị Phương', '89 Cách Mạng Tháng 8, P.5, Q.Tân Bình', '0956789012', 'Đang hoạt động'),
('KH007', 'Đặng Quốc Hùng', '34 Nam Kỳ Khởi Nghĩa, P.7, Q.3', '0967890123', 'Đang hoạt động'),
('KH008', 'Bùi Thị Lan', '67 Trần Phú, P.8, Q.5', '0978901234', 'Đang hoạt động');

-- --------------------------------------------------------
-- Cấu trúc bảng `meters`
CREATE TABLE `meters` (
  `ma_cong_to` varchar(20) NOT NULL,
  `ma_kh` varchar(20) NOT NULL,
  `vi_tri` varchar(255) NOT NULL,
  `trang_thai` varchar(50) NOT NULL DEFAULT 'Hoạt động'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `meters` (`ma_cong_to`, `ma_kh`, `vi_tri`, `trang_thai`) VALUES
('CT001', 'KH001', 'Cột điện A1', 'Hoạt động'),
('CT002', 'KH002', 'Cột điện A2', 'Hoạt động'),
('CT003', 'KH003', 'Cột điện B1', 'Hoạt động'),
('CT004', 'KH004', 'Cột điện B2', 'Hỏng'),
('CT005', 'KH005', 'Cột điện C1', 'Hoạt động'),
('CT006', 'KH006', 'Cột điện C2', 'Hoạt động'),
('CT007', 'KH007', 'Cột điện D1', 'Hoạt động'),
('CT008', 'KH008', 'Cột điện D2', 'Hoạt động');

-- --------------------------------------------------------
-- Cấu trúc bảng `electricity_readings`
CREATE TABLE `electricity_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ma_kh` varchar(20) NOT NULL,
  `ma_cong_to` varchar(20) NOT NULL,
  `thang` varchar(20) NOT NULL,
  `chi_so_cu` int(11) NOT NULL,
  `chi_so_moi` int(11) NOT NULL,
  `tieu_thu` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `electricity_readings` (`ma_kh`, `ma_cong_to`, `thang`, `chi_so_cu`, `chi_so_moi`, `tieu_thu`) VALUES
('KH001', 'CT001', '04/2026', 1200, 1285, 85),
('KH002', 'CT002', '04/2026', 800, 860, 60),
('KH003', 'CT003', '04/2026', 2100, 2245, 145),
('KH005', 'CT005', '04/2026', 450, 498, 48),
('KH006', 'CT006', '04/2026', 1500, 1620, 120);

-- --------------------------------------------------------
-- Cấu trúc bảng `invoices`
CREATE TABLE `invoices` (
  `ma_hd` varchar(50) NOT NULL,
  `ma_kh` varchar(20) NOT NULL,
  `ma_cong_to` varchar(20) NOT NULL,
  `thang` varchar(20) NOT NULL,
  `tieu_thu` int(11) NOT NULL,
  `tong_tien` int(11) NOT NULL,
  `trang_thai` varchar(50) NOT NULL DEFAULT 'Chưa thanh toán',
  `ngay_tt` varchar(20) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `invoices` (`ma_hd`, `ma_kh`, `ma_cong_to`, `thang`, `tieu_thu`, `tong_tien`, `trang_thai`, `ngay_tt`) VALUES
('H2601001', 'KH001', 'CT001', '01/2026', 78, 131000, 'Đã thanh toán', '05/01/2026'),
('H2601002', 'KH002', 'CT002', '01/2026', 55, 97500, 'Đã thanh toán', '07/01/2026'),
('H2601003', 'KH003', 'CT003', '01/2026', 130, 257500, 'Đã thanh toán', '08/01/2026'),
('H2601004', 'KH005', 'CT005', '01/2026', 42, 63000, 'Đã thanh toán', '10/01/2026'),
('H2601005', 'KH006', 'CT006', '01/2026', 110, 207500, 'Đã thanh toán', '12/01/2026'),
('H2601006', 'KH007', 'CT007', '01/2026', 95, 172500, 'Đã thanh toán', '14/01/2026'),
('H2601007', 'KH008', 'CT008', '01/2026', 63, 114500, 'Đã thanh toán', '15/01/2026'),
('H2602001', 'KH001', 'CT001', '02/2026', 82, 139000, 'Đã thanh toán', '06/02/2026'),
('H2602002', 'KH002', 'CT002', '02/2026', 58, 103500, 'Đã thanh toán', '08/02/2026'),
('H2602003', 'KH003', 'CT003', '02/2026', 140, 277500, 'Đã thanh toán', '10/02/2026'),
('H2602004', 'KH005', 'CT005', '02/2026', 45, 67500, 'Chưa thanh toán', ''),
('H2602005', 'KH006', 'CT006', '02/2026', 115, 220000, 'Đã thanh toán', '11/02/2026'),
('H2602006', 'KH007', 'CT007', '02/2026', 88, 160000, 'Đã thanh toán', '13/02/2026'),
('H2602007', 'KH008', 'CT008', '02/2026', 70, 127500, 'Chưa thanh toán', ''),
('H2603001', 'KH001', 'CT001', '03/2026', 90, 157500, 'Đã thanh toán', '04/03/2026'),
('H2603002', 'KH002', 'CT002', '03/2026', 62, 112000, 'Đã thanh toán', '06/03/2026'),
('H2603003', 'KH003', 'CT003', '03/2026', 155, 307500, 'Đã thanh toán', '07/03/2026'),
('H2603004', 'KH005', 'CT005', '03/2026', 50, 75000, 'Đã thanh toán', '09/03/2026'),
('H2603005', 'KH006', 'CT006', '03/2026', 118, 225000, 'Chưa thanh toán', ''),
('H2603006', 'KH007', 'CT007', '03/2026', 100, 182500, 'Đã thanh toán', '11/03/2026'),
('H2603007', 'KH008', 'CT008', '03/2026', 68, 123000, 'Đã thanh toán', '12/03/2026'),
('HD001', 'KH001', 'CT001', '04/2026', 85, 147500, 'Chưa thanh toán', ''),
('HD002', 'KH002', 'CT002', '04/2026', 60, 107500, 'Đã thanh toán', '18/04/2026'),
('HD003', 'KH003', 'CT003', '04/2026', 145, 286250, 'Chưa thanh toán', ''),
('HD004', 'KH005', 'CT005', '04/2026', 48, 72000, 'Đã thanh toán', '20/04/2026'),
('HD005', 'KH006', 'CT006', '04/2026', 120, 232500, 'Chưa thanh toán', '');

-- --------------------------------------------------------
-- Cấu trúc bảng `electricity_tiers`
CREATE TABLE `electricity_tiers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bac` varchar(20) NOT NULL,
  `tu` int(11) NOT NULL,
  `den` int(11) NOT NULL,
  `don_gia` int(11) NOT NULL,
  `mo_ta` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `electricity_tiers` (`bac`, `tu`, `den`, `don_gia`, `mo_ta`) VALUES
('Bậc 1', 0, 50, 1500, '0 - 50 kWh'),
('Bậc 2', 51, 100, 2000, '51 - 100 kWh'),
('Bậc 3', 101, 999999, 2500, '> 100 kWh');

-- --------------------------------------------------------
-- Đặt khóa chính & khóa ngoại
ALTER TABLE `users` ADD PRIMARY KEY (`username`);
ALTER TABLE `customers` ADD PRIMARY KEY (`ma_kh`);
ALTER TABLE `meters` ADD PRIMARY KEY (`ma_cong_to`), ADD KEY `ma_kh` (`ma_kh`);
ALTER TABLE `invoices` ADD PRIMARY KEY (`ma_hd`), ADD KEY `ma_kh` (`ma_kh`);
ALTER TABLE `electricity_readings` ADD KEY `ma_kh` (`ma_kh`);

ALTER TABLE `meters` ADD CONSTRAINT `fk_meters_kh` FOREIGN KEY (`ma_kh`) REFERENCES `customers` (`ma_kh`) ON DELETE CASCADE;
ALTER TABLE `electricity_readings` ADD CONSTRAINT `fk_readings_kh` FOREIGN KEY (`ma_kh`) REFERENCES `customers` (`ma_kh`) ON DELETE CASCADE;
ALTER TABLE `invoices` ADD CONSTRAINT `fk_invoices_kh` FOREIGN KEY (`ma_kh`) REFERENCES `customers` (`ma_kh`) ON DELETE CASCADE;

COMMIT;
