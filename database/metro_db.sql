-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th10 19, 2025 lúc 11:33 AM
-- Phiên bản máy phục vụ: 8.0.41
-- Phiên bản PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `metro_db`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `entry_logs`
--

CREATE TABLE `entry_logs` (
  `log_id` int NOT NULL,
  `face_id` int NOT NULL,
  `station_id` int NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `action` enum('tap_in','tap_out') NOT NULL,
  `confidence` decimal(5,2) NOT NULL,
  `fee_charged` decimal(10,2) DEFAULT '0.00',
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `face_data`
--

CREATE TABLE `face_data` (
  `face_id` int NOT NULL,
  `user_id` int NOT NULL,
  `face_encoding` longblob NOT NULL,
  `photo_path` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `stations`
--

CREATE TABLE `stations` (
  `station_id` int NOT NULL,
  `station_name` varchar(100) NOT NULL,
  `line` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Đang đổ dữ liệu cho bảng `stations`
--

INSERT INTO `stations` (`station_id`, `station_name`, `line`, `created_at`) VALUES
(1, 'Bến Thành', 'Line 1', '2025-10-19 15:50:02'),
(2, 'Suối Tiên', 'Line 1', '2025-10-19 15:50:02'),
(3, 'Ngã Tư Sáng', 'Line 1', '2025-10-19 15:50:02'),
(4, 'Cầu Giấy', 'Line 2', '2025-10-19 15:50:02'),
(5, 'Hoan Kiếm', 'Line 2', '2025-10-19 15:50:02'),
(6, 'Long Biên', 'Line 2', '2025-10-19 15:50:02');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `tickets`
--

CREATE TABLE `tickets` (
  `ticket_id` int NOT NULL,
  `user_id` int NOT NULL,
  `station_from_id` int NOT NULL,
  `station_to_id` int NOT NULL,
  `valid_at_datetime` datetime NOT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'NEW',
  `purchase_price` decimal(10,2) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `users`
--

CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password_hash` varchar(256) NOT NULL,
  `wallet_balance` decimal(10,2) NOT NULL DEFAULT '0.00',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `entry_logs`
--
ALTER TABLE `entry_logs`
  ADD PRIMARY KEY (`log_id`),
  ADD KEY `face_id` (`face_id`),
  ADD KEY `station_id` (`station_id`),
  ADD KEY `idx_entry_logs_user` (`user_id`);

--
-- Chỉ mục cho bảng `face_data`
--
ALTER TABLE `face_data`
  ADD PRIMARY KEY (`face_id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `idx_face_user` (`user_id`);

--
-- Chỉ mục cho bảng `stations`
--
ALTER TABLE `stations`
  ADD PRIMARY KEY (`station_id`),
  ADD UNIQUE KEY `station_name` (`station_name`);

--
-- Chỉ mục cho bảng `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`ticket_id`),
  ADD KEY `station_from_id` (`station_from_id`),
  ADD KEY `station_to_id` (`station_to_id`),
  ADD KEY `idx_ticket_user` (`user_id`),
  ADD KEY `idx_ticket_datetime` (`valid_at_datetime`);

--
-- Chỉ mục cho bảng `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_user_id` (`user_id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `entry_logs`
--
ALTER TABLE `entry_logs`
  MODIFY `log_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `face_data`
--
ALTER TABLE `face_data`
  MODIFY `face_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `stations`
--
ALTER TABLE `stations`
  MODIFY `station_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT cho bảng `tickets`
--
ALTER TABLE `tickets`
  MODIFY `ticket_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `entry_logs`
--
ALTER TABLE `entry_logs`
  ADD CONSTRAINT `entry_logs_ibfk_1` FOREIGN KEY (`face_id`) REFERENCES `face_data` (`face_id`),
  ADD CONSTRAINT `entry_logs_ibfk_2` FOREIGN KEY (`station_id`) REFERENCES `stations` (`station_id`),
  ADD CONSTRAINT `entry_logs_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Các ràng buộc cho bảng `face_data`
--
ALTER TABLE `face_data`
  ADD CONSTRAINT `face_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Các ràng buộc cho bảng `tickets`
--
ALTER TABLE `tickets`
  ADD CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`station_from_id`) REFERENCES `stations` (`station_id`),
  ADD CONSTRAINT `tickets_ibfk_3` FOREIGN KEY (`station_to_id`) REFERENCES `stations` (`station_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
