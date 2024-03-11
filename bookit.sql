-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 11, 2024 at 12:21 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bookit`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('81226e916f7d');

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `guest_count` int(11) NOT NULL,
  `additional_notes` varchar(1024) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `all_day` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `event_type` varchar(255) DEFAULT NULL,
  `cancelled` tinyint(1) DEFAULT NULL,
  `extra_facility_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`id`, `event_id`, `user_id`, `full_name`, `email`, `guest_count`, `additional_notes`, `start_date`, `end_date`, `start_time`, `end_time`, `all_day`, `created_at`, `event_type`, `cancelled`, `extra_facility_id`) VALUES
(1, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2025-06-18', '2025-06-19', '00:00:00', '23:59:59', 1, '2023-12-04 12:57:32', 'Birthday', 0, NULL),
(2, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2022-06-18', '2022-06-19', '14:00:00', '15:00:00', 0, '2023-12-04 12:58:51', 'Birthday', 0, NULL),
(3, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2021-06-18', '2021-06-19', '14:00:00', '15:00:00', 1, '2023-12-04 12:59:25', 'Wedding', 0, NULL),
(4, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2021-06-18', '2021-06-20', '14:00:00', '15:00:00', 0, '2023-12-04 12:59:57', 'Wedding', 0, NULL),
(5, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2020-06-18', '2020-06-20', '14:00:00', '15:00:00', 0, '2023-12-04 13:00:54', 'Business', 0, NULL),
(6, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2019-06-18', '2019-06-20', '14:00:00', '15:00:00', 0, '2023-12-04 13:01:01', 'Business', 0, NULL),
(7, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2018-06-18', '2018-06-20', '14:00:00', '15:00:00', 0, '2023-12-04 13:01:11', 'Charity', 0, NULL),
(8, 1, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-18', '2005-06-20', '14:00:00', '15:00:00', 0, '2023-12-04 13:26:24', 'Charity', 0, NULL),
(9, 1, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-21', '2005-06-22', '14:00:00', '15:00:00', 0, '2023-12-04 13:26:40', 'Workshop', 0, NULL),
(10, 1, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-23', '2005-06-24', '14:00:00', '15:00:00', 0, '2023-12-04 13:26:46', 'Workshop', 0, NULL),
(11, 1, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-25', '2005-06-26', '14:00:00', '15:00:00', 0, '2023-12-04 13:26:56', 'Wedding', 0, NULL),
(12, 1, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-04 13:27:04', 'Network', 0, NULL),
(13, 2, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 1, '2023-12-06 08:25:35', 'Network', 0, NULL),
(14, 3, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:15', 'Workshop', 1, NULL),
(15, 4, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:21', 'Network', 0, NULL),
(16, 5, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:27', 'Workshop', 0, NULL),
(17, 6, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2022-12-21', '2022-12-22', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:32', 'Charity', 0, NULL),
(18, 7, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:38', 'Network', 0, NULL),
(19, 8, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:44', 'Wedding', 0, NULL),
(20, 9, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:50', 'Wedding', 0, NULL),
(21, 10, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:56', 'Wedding', 0, NULL),
(22, 11, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:01', 'Workshop', 0, NULL),
(23, 12, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:05', 'Wedding', 0, NULL),
(24, 13, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2023-12-22', '2023-12-22', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:09', 'Network', 0, NULL),
(25, 14, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:13', 'Wedding', 0, NULL),
(26, 15, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:17', 'Charity', 0, NULL),
(27, 16, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:22', 'Charity', 0, NULL),
(28, 17, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:25', 'Network', 0, NULL),
(29, 18, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:41', 'Wedding', 0, NULL),
(31, 20, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:51', 'Network', 0, NULL),
(32, 21, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:54', 'Wedding', 0, NULL),
(33, 22, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2024-01-08', '2024-01-08', '14:00:00', '22:00:00', 0, '2023-12-06 08:27:58', 'Wedding', 0, NULL),
(35, 21, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:47:33', 'Wedding', 0, NULL),
(36, 20, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:47:47', 'Network', 0, NULL),
(37, 19, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2024-01-08', '2024-01-08', '12:00:00', '13:00:00', 0, '2023-12-06 08:48:53', 'Wedding', 0, NULL),
(38, 18, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:09', 'Network', 0, NULL),
(39, 17, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:15', 'Wedding', 0, NULL),
(40, 16, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:20', 'Network', 0, NULL),
(41, 15, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:24', 'Birthday', 0, NULL),
(42, 14, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:29', 'Birthday', 0, NULL),
(43, 13, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:34', 'Birthday', 0, NULL),
(44, 12, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:39', 'Network', 0, NULL),
(45, 11, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:42', 'Network', 0, NULL),
(46, 10, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:46', 'Network', 0, NULL),
(47, 9, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:50', 'Birthday', 0, NULL),
(48, 8, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:55', 'Birthday', 0, NULL),
(49, 7, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:00', 'Function', 0, NULL),
(50, 6, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2023-12-11', '2023-12-01', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:06', 'Birthday', 0, NULL),
(51, 5, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:10', 'Function', 0, NULL),
(52, 4, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:14', 'Function', 0, NULL),
(53, 3, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:18', 'Charity', 1, NULL),
(54, 2, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:21', 'Function', 0, NULL),
(55, 1, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:25', 'Function', 1, NULL),
(56, 26, 51, 'Abdul Rafay Atiq 124', 'just1.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-07 11:41:07', 'Function', 1, NULL),
(57, 27, 51, 'Abdul Rafay Atiq 124', 'just1.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-29', '2004-06-30', '14:00:00', '15:00:00', 1, '2023-12-07 11:41:19', 'Function', 0, NULL),
(58, 27, 51, 'Muhammad Ahsan Bin Abdul Aziz', 'nothing.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-20 08:16:43', 'Birthday', 0, NULL),
(59, 27, 51, 'Muhammad Ahsan Bin Abdul Aziz', 'nothing.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-29', '2004-06-30', '16:00:00', '17:00:00', 0, '2023-12-20 08:19:14', 'Birthday', 0, NULL),
(60, 27, 51, 'Muhammad Ahsan Bin Abdul Aziz', 'nothing.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-01', '2004-06-02', '16:00:00', '17:00:00', 0, '2023-12-20 08:24:04', 'Wedding', 1, NULL),
(85, 27, 51, 'Muhammad Ahsan Bin Abdul Aziz', 'nothing.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2024-01-08', '2024-01-08', '14:00:00', '18:00:00', 1, '2023-12-20 11:27:28', 'NeTwOrk', 1, NULL),
(106, 89, 55, 'Rafay and Rafay', 'johndoe@example.com', 5, 'Special requests for the event.', '2024-01-12', '2024-01-12', '12:00:00', '13:20:23', 0, '2024-01-17 13:13:07', 'Bussiness Meeting', 0, NULL),
(107, 89, 55, 'Rafay and Rafay', 'johndoe@example.com', 5, 'Special requests for the event.', '2024-02-12', '2024-02-12', '12:00:00', '13:20:23', 0, '2024-01-17 13:14:21', 'Bussiness Meeting', 0, NULL),
(110, 89, 55, 'Rafay and Rafay', 'johndoe@example.com', 5, 'Special requests for the event.', '2024-03-12', '2024-03-12', '12:00:00', '13:20:23', 0, '2024-01-17 13:17:50', 'Bussiness Meeting', 0, NULL),
(153, 88, 55, 'Rafay and Rafay', 'johndoe@example.com', 5, 'Special requests for the event.', '2025-06-09', '2025-06-09', '12:00:00', '15:00:00', 0, '2024-01-18 14:59:00', 'Business Meeting', 0, NULL),
(156, 109, 55, 'Alice Smith', 'alicesmith@example.com', 8, 'Special requests for the event.', '2024-01-19', '2024-01-19', '20:00:00', '22:00:00', 0, '2024-01-18 15:06:28', 'Business Meeting', 0, NULL),
(189, 118, 55, 'Jane Smith', 'jane.smith@example.com', 10, 'Nothing', '2024-02-06', '2024-02-06', '15:00:00', '17:00:00', 0, '2024-01-30 14:44:56', 'Wedding', 0, NULL),
(212, 123, 55, 'Jane Smith', 'jane.smith@example.com', 52, 'Nothing', '2024-02-07', '2024-02-07', '15:00:00', '17:00:00', 0, '2024-02-20 12:09:12', 'Wedding', 0, NULL),
(220, 123, 55, 'Jane Smith', 'jane.smith@example.com', 50, '', '2034-02-27', '2034-02-27', '10:00:00', '13:00:00', 0, '2024-03-05 10:02:18', 'Wedding', 0, NULL),
(221, 124, 55, 'Jane Smith', 'jane.smith@example.com', 50, '', '2034-02-27', '2034-02-27', '10:00:00', '11:00:00', 0, '2024-03-05 10:02:36', 'Wedding', 0, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `booking_extra_facility`
--

CREATE TABLE `booking_extra_facility` (
  `id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `extra_facility_id` int(11) NOT NULL,
  `unit` varchar(10) NOT NULL,
  `quantity` float NOT NULL,
  `image` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`image`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking_extra_facility`
--

INSERT INTO `booking_extra_facility` (`id`, `booking_id`, `extra_facility_id`, `unit`, `quantity`, `image`) VALUES
(6, 189, 19, 'unit', 2, NULL),
(7, 189, 20, 'hour', 2, NULL),
(8, 212, 47, 'unit', 2, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `id` int(11) NOT NULL,
  `thumbnail` varchar(255) NOT NULL,
  `other_images` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`other_images`)),
  `video_showcase` varchar(255) DEFAULT NULL,
  `address` varchar(255) NOT NULL,
  `rate` float NOT NULL,
  `fixed_price` tinyint(1) DEFAULT NULL,
  `details` varchar(1024) DEFAULT NULL,
  `facilities` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`facilities`)),
  `description` varchar(1024) DEFAULT NULL,
  `event_type` varchar(255) DEFAULT NULL,
  `vendor_id` int(11) NOT NULL,
  `services` varchar(1024) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `location_name` varchar(255) NOT NULL,
  `custom_event_name` varchar(255) DEFAULT NULL,
  `guest_capacity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`id`, `thumbnail`, `other_images`, `video_showcase`, `address`, `rate`, `fixed_price`, `details`, `facilities`, `description`, `event_type`, `vendor_id`, `services`, `latitude`, `longitude`, `location_name`, `custom_event_name`, `guest_capacity`) VALUES
(1, '18fabf02-221b-401c-90a6-dc5d012b73ab.png', '[\"9b056398-ec4a-4522-8dce-0b6e4ee650da.png\", \"db1c10fd-e7b9-466a-a5af-0112824c36c6.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 10, 1, 'details', '[\"06ad8829-280d-43b6-9483-1a097ad48e33.png\"]', 'description', 'Birthday', 10, NULL, 24.929, 67.0971, 'Delizia', NULL, NULL),
(2, 'b0af4b12-aa95-4218-a9a5-13d36579180b.png', '[\"69166b02-97f6-411b-b6f2-bd4e57b520c6.png\", \"cd836160-67b0-4813-beac-b5009264a378.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"4007c72c-be69-4fc9-b41f-6f3882a463f2.png\"]', 'description', 'wedding', 10, NULL, 24.9289, 67.097, 'Pieinthesky', NULL, NULL),
(3, '629ff76a-073d-45a0-92ff-87610a85cb4e.png', '[\"30efaa63-18fc-4bba-b8a2-41cfe88ccb96.png\", \"53f520a1-e644-42d7-824f-79d1074820df.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 10000, 1, 'details', '[\"3ed2dadc-3829-4f11-86e6-3a41b495e70f.png\"]', 'Birthday', 'Lounge', 10, NULL, 24.9288, 67.0969, 'Kaybees', NULL, NULL),
(4, '5b49050f-167f-4218-a1f6-6d88580549ec.png', '[\"5214eb22-c75a-42fd-af1a-ed39694fc7b5.png\", \"5b57d947-c14d-486d-8ecd-444715395d3b.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"0b0ae605-cdff-4c74-85de-0635975db9cf.png\"]', 'Its a shop', 'Workshop', 10, NULL, 24.9287, 67.0968, 'Kababjees', NULL, NULL),
(5, '749e744c-6b1b-4415-9c8c-a0d4a3c8dcd7.png', '[\"009ffe35-818c-4ef3-8c1c-22877797d546.png\", \"1091ac8c-414a-4973-bc50-10357985cc1b.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 1000, 1, 'details', '[\"decf26e4-bfa3-4fc4-8c36-c7de3855677b.png\"]', 'Birthday', 'House', 10, NULL, 24.9286, 67.0967, 'The Bakers', NULL, NULL),
(6, '45a3259a-6963-488a-9164-23d294c3af28.png', '[\"b05fbba7-d0d7-4a5b-8b9f-e87092493880.png\", \"b8f23972-4a41-45e5-ad0f-927464abd858.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"1b643bb6-3537-4d5c-b220-d1480c1fcca1.png\"]', 'Meeting', 'Bar', 10, NULL, 24.9285, 67.0966, 'Delicacy', NULL, NULL),
(7, '7a9d4ecf-6861-4ba4-aa04-594c365e9665.png', '[\"4ff2ae06-a1f9-4912-94f8-6ea073961e0f.png\", \"3858aea0-ae4f-48bd-b5d0-a030fa8e5d29.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 1000, 1, 'details', '[\"7cd2599c-0ad7-4bc7-be80-572c602e02a4.png\"]', 'Birthday', 'Restaurant', 10, NULL, 24.9284, 67.0965, 'Delizia', NULL, NULL),
(8, '7a8ec041-ec14-4885-aee3-7ec282b4f09a.png', '[\"ce7ece10-aa97-418e-b999-0c92ce5f15e0.png\", \"a83681a6-3d58-46a1-8e2e-bd8b11f78b05.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"0b2957d2-fa5d-452e-b022-15b6f216f0b1.png\"]', 'Birthday', 'Wedding', 10, NULL, 24.9283, 67.0964, 'Pieinthesky', NULL, NULL),
(9, 'ba0f8d0a-bded-429b-8b7b-240bf8bd2c9c.png', '[\"fa3ce8ff-93d6-479c-a8de-64fe2b77928e.png\", \"cb45790d-b17e-40fe-93d9-bfe2daf79759.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"9100c354-957b-43c7-8a16-9fd249b40b69.png\"]', 'Birthday', 'Event Space', 10, NULL, 24.9282, 67.0963, 'The Bakers', NULL, NULL),
(10, '20b49afa-f623-4a96-af57-587a42ab7aeb.png', '[\"e2eb7bc0-4336-4546-a2b3-644133263bb3.png\", \"4ae0480a-7b73-49cb-836e-d4cc743357ae.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"9197f633-784b-41e3-b75d-51cfea8e2678.png\"]', 'Birthday', 'Wedding', 10, NULL, 24.9281, 67.0962, 'Delicacy', NULL, NULL),
(11, '1ec67c4f-248c-44e6-9c3c-383e639bbf14.png', '[\"c08d3a06-3be1-4c16-862a-d2025c303098.png\", \"7fa9945c-a061-481b-a648-c6f1d9538223.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100000, 1, 'details', '[\"a6315cab-15a6-4037-865d-48f3bc01ce91.png\"]', 'Birthday', 'Wedding', 10, NULL, 24.928, 67.0961, 'Kababjees', NULL, NULL),
(12, 'd9613205-0dfc-4b33-afa1-99685d5d632f.png', '[\"d05367b8-0fb1-45af-87f1-84e3f4f55055.png\", \"bf2859fe-d4b3-45b6-b499-cd38f3a2696b.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"85d61838-c292-47e2-9f09-186bbc263a20.png\"]', 'Birthday', 'Studio', 10, NULL, 24.9279, 67.096, 'The sweets', NULL, NULL),
(13, 'dba59259-f5eb-4ac2-9065-064dfd2b7b00.png', '[\"e04f0374-5263-4e79-be9f-38e66ed6d258.png\", \"b0b83840-172e-4929-a5aa-cae2e82b8e81.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"bfee9161-7a20-4044-910e-78cb002ace5e.png\"]', 'Birthday', 'Wedding1', 6, NULL, 24.9278, 67.0959, 'KFC', NULL, NULL),
(14, 'cc6245d4-ad5c-4705-bcdd-403e8a5c12e2.png', '[\"d371dc37-3c08-43f3-867b-8af51879ff14.png\", \"d17d4d39-d24c-47ad-b8fb-f339ee9b2277.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"cf0c295a-9444-4f51-a8a4-4087d4f4c9e4.png\"]', 'Testing Birthday', 'Meeting', 11, NULL, 24.9277, 67.0958, 'Mc Donald', NULL, NULL),
(15, 'a1869d44-adbd-46fa-ba9a-4377a21c8f28.png', '[\"e055ac08-98dc-42bc-af7b-ea06d47cab1f.png\", \"f4e2e5ce-9655-4026-9ba5-9b253c3b13c0.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"2bd0ebe3-9532-4078-a195-9e35b06f47a5.png\"]', 'Testing Birthday', 'Test Wedding', 11, NULL, 24.9276, 67.0957, 'Delizia', NULL, NULL),
(16, '6416f843-cecf-4928-a582-edd0d89734ba.png', '[\"596984ea-94c5-41ab-bb49-47f65f620e9e.png\", \"9dfd7d0b-0720-47ef-aefc-c7512b4e6294.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"0e4fbc35-34c1-4122-a2f2-2a7f474b288a.png\"]', 'Testing Birthday', 'Test Wedding', 11, 'bn das', 24.9275, 67.0956, 'Kababjees', NULL, NULL),
(17, '4a91a0bc-8215-4418-a185-0201bcde6f88.png', '[\"e857f928-257a-4919-ace8-a31171a7a35d.png\", \"b468da9b-e5aa-4dd2-ac50-15be0d534083.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"4cde4a15-9d54-447a-880a-c3578f9d478d.png\"]', 'Testing Birthday', 'Test Wedding', 11, 'serepuveicew', 24.9274, 67.0955, 'KFC', NULL, NULL),
(18, 'a4ee942e-fb7e-4862-a36d-06d550d05ad3.png', '[\"2cd0cc40-c86b-40d7-957a-e9687be0556e.png\", \"bd9c0f25-aa41-4aeb-951c-eac506280ae5.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"957c2666-81ba-4ca8-8954-e2261e1e3dc0.png\"]', 'Testing Birthday', 'Test Wedding', 11, 'servicenas', 24.9273, 67.0955, 'Broadway Pizza', NULL, NULL),
(19, '92393fa7-5f78-4f00-80c3-5c5b5a6f8f0a.png', '[\"066142a0-27a6-4bd4-a2ab-49c8fe821e29.png\", \"9fae2664-b447-484b-b801-679e57b89654.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"7194f8ba-7ca4-45f5-9c3b-9b7d255556eb.png\"]', 'Testing Birthday', 'Test Wedding', 11, 'n fafhbfkd', 24.9272, 66.954, 'Pizzeria', NULL, NULL),
(20, '28df872a-7ef8-498a-8d49-a9d9260c7d36.png', '[\"29f33dd7-e16b-4440-986f-6e42c295bf61.png\", \"ba6297f9-de35-493e-858c-30fade31b458.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 10, 1, 'details', '[\"1ae10cb7-e473-4fbb-9e3c-77b54eea7c68.png\"]', 'Testing Birthday', 'Test Wedding', 11, 'nas f sdk', 24.9271, 67.0953, 'Burger o  clock', NULL, NULL),
(21, 'f1e0a15b-bc89-4258-b36a-f92b5d2c73cf.png', '[\"fa4b5430-af8d-4fc8-b0bc-a2832c3abc49.png\", \"1e52ab04-bdcc-49b4-9b6d-cbaa66345759.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"6b2b535c-1c3c-4630-a039-24e4ce9f9c6a.png\"]', 'Testing Birthday', 'Test Birthday', 11, 'nsjidfb', 24.927, 67.0952, 'Subway', NULL, NULL),
(22, 'bafa61f0-4dcd-4d73-96dd-19f92e9b13a8.png', '[\"dc8a689e-4cf4-4c08-9a72-c8d1d3bd42db.png\", \"7696a7dc-798d-48c1-aec5-4acffc038cce.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"5c803a90-c387-487b-8d37-f3b81560858d.png\"]', 'Testing Birthday', 'Birthday', 11, 'Wow !!', 24.9268, 67.095, 'Delizia', NULL, NULL),
(26, 'd7d929e3-48c8-42f6-895c-86f971f9a5e4.png', '[\"92487783-1796-47cd-9a1d-007521fff100.png\", \"1887b593-4d46-4a58-b6f1-454b430c2729.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"30385e1c-c3fb-4b91-8097-1b72f02f0834.png\"]', 'Birthday', 'concert', 6, 'A class service', 24.0123, 67.0123, 'the maze', NULL, NULL),
(27, '4db7cc10-36e5-4b89-b9e4-d1b19c7b3648.png', '[\"7f4ee5ba-534f-4a8e-815a-55973d41fe79.png\", \"9061c89e-7031-4340-bf22-f66f9f5a57e1.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"2d82d838-acbd-43f0-9874-3a69a209a6ca.png\"]', 'Birthday', 'concert', 6, 'A class service', 24, 67, 'The maze', NULL, NULL),
(28, '54a2033b-f307-4028-8fa6-a6edea487f73.png', '[\"eafdd5ad-31e6-44d7-9399-92e764e8a403.png\", \"cd731e9c-8ca7-4cb8-b634-f41010666c01.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 10000000, 1, 'details', '[\"4cd0f039-cb39-4042-8b2a-cd722ea54950.png\"]', 'Birthday', 'Birthday', 6, 'A class service', 24.927, 67.0951, 'Delizia', NULL, NULL),
(31, '57258934-a0f0-4ded-94fe-db0abc7f2639.png', '[\"58697109-9ab4-469e-b687-5d379dadf748.png\", \"0cfe7348-1720-4348-a4e0-65e835a5ea4c.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"4eb19179-aa37-4416-b174-8e3daf6ce66f.png\"]', 'Birthday', 'Testing Birthday', 15, 'A class service', 24.6, 64.2, 'Kababjees Bakers', NULL, NULL),
(35, 'd9aa7422-40f6-4f09-8da4-f188679e98b9.png', '[\"61f70f88-1019-4f78-9325-8c5d0510944c.png\", \"a66d1336-ed79-46bc-b7d9-7f73d51d7fd9.png\"]', 'base64_encoded_video', 'Sample Address', 1000000, 1, 'Event details...', '[\"4ce57aaf-183c-4e00-993c-bd30f839815d.png\"]', 'Event description...', 'Birthday', 15, 'A class service', 123.456, 78.9, 'Tassaract', NULL, NULL),
(57, 'b37c97f1-c011-4f4a-84fa-4ad07b329b9c.png', '[\"0fc9501e-bba8-4396-b7f6-9568d80a26fd.png\", \"d3d5a31e-9a4e-41c8-b53c-22f635b96331.png\"]', 'youtube.com', 'Gulshan block 6', 50, 1, 'Event details 123123', '[\"5b2d257a-1702-48c2-95b4-f8d4ea41eaeb.png\", \"dc1ad8e0-fdc0-4a0f-b8c2-6c6582a43d25.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(58, '2567eb1b-35e4-4dcd-93ff-6abf00f4fa01.png', '[\"929b5602-7b17-4dcc-aac3-3ded0c70c960.png\", \"51c75bc8-8b3d-470b-9a79-a48034aa5df6.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"5616d729-e317-4aa0-968d-3d6692d420fe.png\", \"b260cad2-3726-408c-824e-bb3f0ee60226.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(59, '2cf6c14a-f1a5-45f5-9713-14b1c46cc934.png', '[\"adae9f03-dabb-4059-8905-c26561663129.png\", \"c9e1d265-6929-42f8-ba4d-da807957a050.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"d188da07-5307-4b48-b208-060f97a00c92.png\", \"32789744-7700-46e0-9372-65e35c847309.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(60, 'bc610554-225a-4b03-ae41-4e2aa13192a7.png', '[\"8b0777df-adc7-4b17-a455-93cdf9110fe3.png\", \"130017d8-2492-4779-b3e7-0523397d8fdc.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"659ef286-cd03-45bb-91db-38b5ec78a49f.png\", \"0fc1558d-6362-4d59-ac6a-141c526b2742.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(61, '5f00fef3-3abf-4a71-9ba7-ff7ef0232ed2.png', '[\"a278eef5-ca3d-4ae5-bdea-0999fc0ffaa3.png\", \"3301ff72-fdba-4394-bcea-1fdf3d2e8be1.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"9fa0f89b-3d16-48d3-807c-4c344660f41e.png\", \"686ac33d-914e-46c2-bc82-0eb11834703c.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(62, 'ef6be7c1-e869-457b-a56d-be7814144750.png', '[\"304ee178-35c2-489e-bbd7-2967ff138e18.png\", \"a29dd544-1ccb-4ed9-814c-e3b3c3db4fe2.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"9b7560d4-c8e8-4c2a-a959-45c6b24d4660.png\", \"e5a35f9e-9539-4f97-8a25-2483d6e0d523.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(63, '13a43530-02e6-4a85-9e17-5c7fd5ab9576.png', '[\"a4962fa8-2b5f-4b4d-b070-5078adfe3893.png\", \"f1b94a9b-8927-449a-969a-0592ea62f10f.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"35101962-58b1-42a0-8740-be3960e85496.png\", \"bdafa16e-211f-49bf-87ad-fc1628c23549.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(64, '16ac297f-b705-48d4-90fe-12f508506e00.png', '[\"772807e1-6d8a-4bde-b14d-7d4c5ed60938.png\", \"33432356-1b1f-49d1-9528-d2851827785b.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"903062ae-9c5c-4e54-b520-86fd176a0c3e.png\", \"dc70829b-d986-4e39-a602-55534cb15d68.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(65, 'fa91da15-3fdd-4b9f-bf5f-1165a838f1cf.png', '[\"8e3505ba-f33c-438d-8896-2631981802b5.png\", \"b8163bcd-e903-42e2-a115-00e7195c49d8.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"f9a47477-9558-44c9-8f10-305f433e593b.png\", \"c9e16b7e-45fd-4c36-9805-29fbffd806fc.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(66, 'c5f47585-ca9a-49d5-921b-f8d88a3720f4.png', '[\"eafd8dec-5891-4235-a646-46d5d250bfa4.png\", \"4f1fa2bd-f32d-423a-a64a-1512fdb14521.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"76deeb43-0771-47b3-a5bf-cfed6809946f.png\", \"8e8cd11a-35f0-4f4d-a1c4-2a543a77df7e.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(67, '5a08084b-66ee-4283-9ed9-e1337b14888b.png', '[\"548287ed-aab1-402c-b329-b6cb6300738e.png\", \"5132b8d0-9c7b-42dc-9ac0-2fd4aa87c8ab.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"57f1b4ae-c8bf-4ead-9e08-7bbc59125e2b.png\", \"4b00c6d6-085a-4ada-94eb-d86fb9e42c37.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(68, 'ef9e58b9-fee5-473f-a6e8-ff8891a32ff0.png', '[\"ca8e32eb-43de-4a2d-8137-f20f3f823ffd.png\", \"4d4b66fe-b30a-499a-805a-8ca9aa55a6dd.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"0dfd141d-1356-4fce-bd55-27514f2193bd.png\", \"46fdb0e0-a9f7-48c9-b95a-2914c72e61f6.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(69, '35ff3611-65dd-456a-aca0-ee3912f59e08.png', '[\"81e4010a-97f9-494c-8604-c3f3d8ef3a33.png\", \"35a1ddb4-f12e-43b5-826e-fea1e6a565c4.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"b79e486e-8f74-46ee-95c4-4301aa7d31f8.png\", \"68f136ee-8081-4e66-8b12-05aa8bb24df2.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(70, '9d017ee3-1abe-4a2b-9d5e-cc67ac7021f2.png', '[\"2067ce7e-8977-42ea-88a8-cb202f720ae1.png\", \"cba83637-4425-4440-9266-4b9b9e3757e7.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"f0a6b122-0d44-47b6-9c0a-5e9d8260d2dc.png\", \"124fdbdf-fedd-4822-b6d5-1b8d810ddb64.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(71, 'cd9fe236-be55-4171-b0fe-f4b26c8533a8.png', '[\"4f76be94-c983-4732-933a-5eb8a4e4b226.png\", \"16a8a930-6405-423c-8ccc-148981d0afaf.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"59c04d5d-e589-408a-a805-74862a1a0ea1.png\", \"284b7bba-aa57-4db9-8ae5-b4088c38d768.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(72, 'ff59826c-0ac2-4c0f-97af-88f44317b17d.png', '[\"9741c7e9-4f87-47c3-a555-02cf186ad087.png\", \"8ff955ce-04ff-4fe9-9588-ccb09bddbde8.png\"]', 'youtube.com', 'Gulshan block 6', 500, 1, 'Event details 123123', '[\"c04e601c-68ff-493b-8384-167afb8853c7.png\", \"72bb1dcc-6c34-4d32-adf6-e8e8d7eda953.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(73, 'b85515d5-de73-459e-bf4a-a36daf015f14.png', '[\"65a4b7a0-5628-4666-92d7-cef8f038f1bb.png\", \"4c0d3e2f-818f-4bf8-9a27-fcc89557b5a6.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"9d2f159f-227d-4715-950c-b50a0d9bee0b.png\", \"79b93c2d-2c9c-478b-a78a-a5dd9d575430.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(74, '281815d8-c9eb-4ca3-bf93-ec1a72a6a62e.png', '[\"2cd9ba04-d0cd-4a53-a186-aa5ffbdd81f1.png\", \"0275eafb-9246-412e-bfec-ad1991adeba0.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"06171d05-d071-4322-ae29-cdfd8efb1478.png\", \"55dd68a4-d318-48a3-82b1-2dd4de83f2c7.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(75, '508320a5-5275-4433-a46a-1e10ff9b4c66.png', '[\"11dcf68e-984a-4c02-b9d5-6cde81441b55.png\", \"e415f6fc-3341-46d2-bd65-c02e80d79b7a.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"51f8d573-eba6-4cc1-9419-6c583dc60030.png\", \"761aa657-aa85-4324-b0e7-343881bc7f4f.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(76, '19da535f-f3cb-4af2-9eac-3ab2f2e12ce5.png', '[\"17d039ce-7f95-4c79-b1b2-c2d0c5d79270.png\", \"89b2d7ae-3424-417f-ab63-19f03448f6fa.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"0ef1839b-ed06-4dcc-9cae-032e099164f8.png\", \"00ea1ce6-2d3a-44a8-b368-fc9de6b06a5d.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(77, 'c4eadc7a-faa7-40bb-8dad-c20624f2b1a3.png', '[\"4e3f623b-1fc8-460c-9640-a0d36ed32e35.png\", \"a8a2941c-8fdb-4ed8-a351-64e9141850a2.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"2885ace8-9201-4722-b63d-1d2514faae62.png\", \"f755d9ee-7951-4a7f-ac46-6e87c43dd8fd.png\"]', 'Event description', 'Event Type', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(78, 'f5851b9c-b6ce-47b9-905f-8a25254624ee.png', '[\"559bdc86-4cfc-474b-8711-de3dbcc5bf91.png\", \"2e7baa7e-d100-4d76-8a30-868cc195cf7b.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"e6dd4765-939b-4f45-bf5f-4386383daad4.png\", \"f1c708b9-6f88-4592-9f78-482621d69bc2.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(79, 'eee89261-0d6a-4972-ab0e-5b9311313fda.png', '[\"e8c9f42a-48fb-42b1-b10d-b16b491bd773.png\", \"67a6dcce-7b87-4b99-868c-157d1d514cef.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"fb344021-d972-45d5-9445-7deb2ab88e4d.png\", \"0e9f5ce9-093f-4d0b-9da7-cc9ce5100c17.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(80, '2a2277ef-b2fd-4347-a882-d787f5308e38.png', '[\"1bf21bfb-3fbc-49cc-971e-2e84f96b3bb0.png\", \"5743932d-5e09-4fcf-b09a-b00f969467cf.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"0e9f74cc-8bc6-4748-9b77-f7d0890a94be.png\", \"78e4224a-3650-468a-90a8-cb3a8a61df22.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(81, '67ca1db4-726d-4dd4-8fdb-c1ec44ec1ab0.png', '[\"846223f9-e690-4371-adcf-891a507270f6.png\", \"8813619c-d686-4ead-8b50-b5d07a08a0d1.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"ced6a109-25ed-4e63-9ab5-1926e80bcb0e.png\", \"1a470ce2-fcc5-4d5e-b29c-e8018540cb98.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(88, 'c6499078-9004-4541-b61e-88405003a0e8.png', '[\"9f234295-00db-437b-9788-917e034700e4.png\", \"8eed25f7-8cbe-4f98-91b5-ec339c49f060.png\"]', 'youtube112312312312.com', 'Gulshan block 1', 500, 1, 'Event details 123123', '[\"09780920-1aef-438e-8467-9b89b2448bda.png\", \"a7496042-6fb1-48d8-97dd-4856a1bdb8b1.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(89, 'c1936860-691a-4416-9040-2f8dfec2d9ff.png', '[\"ab0fb002-db90-4ff0-b962-24ea0ede90a4.png\", \"e8177fbe-78bb-471a-abb3-cced92004991.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"4df643a8-60b5-4393-ab0d-fc4173a6b209.png\", \"2508ac62-7336-4464-9e32-ea04923499ea.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(90, 'b519dee5-42a0-4b83-b184-fbe51ece182a.png', '[\"f94a03f2-ec64-42f6-8ce8-b153944855a1.png\", \"1dfe8cb5-3c47-4d98-9199-1d028e753131.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"ebfc5050-96e4-425a-b749-533493caa86a.png\", \"6496f1bf-746a-4705-ac55-840a02a929fa.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(91, 'eb136ce9-b2b0-496c-8c33-c8ed15a46bb2.png', '[\"b5ec7406-1210-4785-b488-798d5335406e.png\", \"5df3e277-2ebb-4b1b-b76e-cbef5ef34ff4.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"3fe0a1b9-100a-4f91-8173-69a4f3dbb0f2.png\", \"c977f023-7eae-4372-8618-1bec31a92ba9.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(92, 'f009db8d-f83c-4286-b08f-4502eac0280b.png', '[\"978a0c24-847e-4fdd-bd84-0c73bfef74ae.png\", \"fdd78bfa-84d0-46de-825b-3aa18c9299e2.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"0074fc93-e4e2-4fd3-b3a9-c171307444e2.png\", \"00ec510c-b897-45a5-be38-15f9bbdcf4db.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(93, '250c8f17-ff39-493e-b5ca-b3faec1bc89a.png', '[\"c143feae-d952-4ad1-85f5-13c727f4c478.png\", \"dbc836ba-cefe-4a26-88a1-b409a3c0febd.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"3a8e6be1-4f6b-4a39-80c7-d8afeceb67c4.png\", \"b6205e84-a619-42a8-8a8b-bd0b32adb30f.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(94, 'c3c56b61-cb28-43a4-923c-4c32f27e2df1.png', '[\"3f0e3afb-d2ab-4113-8914-9ecef2efe23e.png\", \"a97f287a-fa49-4af9-9186-3176e2f81f9d.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"2c1a1044-7f21-410d-8f36-0c987165e445.png\", \"4bd6d042-b37e-42d6-81cd-cb36f8f00460.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(95, 'dcfdb331-e3be-4b1f-9cd1-d33c6a6aace1.png', '[\"a33ade92-e523-4274-8f88-0a344aa73a2f.png\", \"3b140c89-db64-4a7b-8751-4316f2dbcee9.png\"]', 'youtube.com', 'Gulshan block 7', 200, 1, 'Event details 123123', '[\"04aacce9-54f7-430e-9d64-2c28654e43b7.png\", \"838b31af-ee6f-4fd4-ade3-50adc1a37f37.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(96, 'c4434531-e1d3-4b01-ae40-ac734405eaba.png', '[\"5bab3e4b-d8f1-4232-aa1a-75fe3fe2d6ea.png\", \"81bbf65f-c8ee-4794-b85b-fadba3a3bca8.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"1ab0fe80-472f-485e-bf38-456949d06093.png\", \"0b46a00a-df65-4dad-a52c-c65f54ab9016.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(97, 'f1db03a2-dc6e-4352-8bf5-77da96b4bdf5.png', '[\"268c3a37-108b-4f5c-ad95-f0ed0e686311.png\", \"7b3277aa-c556-4439-aa23-5a652cec9c32.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"fe0eec55-b899-4272-b441-8d57e618e002.png\", \"6c8893d5-c0dc-4e75-89db-bd1fb1173976.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(98, '7846ea78-8c13-43fd-9673-aa4ebc7a2a16.png', '[\"fbc7112b-cffe-4ce6-af82-e26cb1d1509c.png\", \"d02a28ae-4ac7-4071-96c3-f09624cef4b8.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"a2285dec-9d85-4ba6-aa13-e2fa87a59401.png\", \"e8255571-c2c8-43ad-99ad-30b02922ce48.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(99, '84226ea2-76e5-4c9c-b4da-5b30bc6a227f.png', '[\"48f8fa7b-4900-462d-9f71-8d1ba2043aca.png\", \"4a4815e0-140b-41e8-91d8-85c9dc2c7705.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"d067bd32-ccfd-4b80-8428-caa6a24ebbac.png\", \"d886d0cf-44d1-490b-a460-993a66e7382f.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(109, '68c0adfc-d69c-4a3f-af89-5d2780350b08.png', '[\"f2fd9651-b550-4822-a732-dd3952053f87.png\", \"39b84b81-9fbd-4bae-84fa-5a646d54026b.png\"]', 'youtube.com', 'Gulshan block 7', 500, 1, 'Event details 123123', '[\"d8fdc413-4f1b-4748-b0f8-148c8a888d47.png\", \"be9a7bc6-9f58-47dc-a702-8a7b5a43e34a.png\"]', 'Event description', 'Anything', 16, 'General', 24.11, 67.11, 'Tassaract', NULL, NULL),
(118, '33cfeba6-5178-472f-a88c-1c8165e00dd5.png', '[\"88fc8730-c741-4793-9e51-17c24048e6d0.png\", \"59aba01f-dab1-4f83-abb7-9168adc0958a.png\"]', 'base64_encoded_video', '123 Main Street, City...', 50, 1, 'Event details go here', '[\"feff347b-7b7b-420f-acdc-2a1016adddbb.png\", \"7057a55a-f109-4b98-851c-894db5968c45.png\"]', 'Event description goes here', 'Party', 16, 'Service details go here', 40.7128, -74.006, 'Sample Location', NULL, NULL),
(119, '99723a29-5d99-4ecd-b8a5-9bed7727e013.png', '[\"1cb20e73-7358-4fa1-ae32-3b9b119e5dc1.png\", \"b394fba6-48bf-42d8-a85f-1e37afb12640.png\"]', 'base64_encoded_video', '123 Main Street, City', 50, 1, 'Event details go here', '[\"2b1e517b-aa2d-4080-b3d2-e43937ecc7cb.png\", \"b4699e4b-67a2-47a1-865d-c56a1dc32fdd.png\"]', 'Event description goes here', 'Party', 16, 'Service details go here', 40.7128, -74.006, 'Sample Location', NULL, NULL),
(120, 'ae4703d0-a9fd-4c00-8ed9-76aeef10f525.png', '[\"73f58d4a-0f85-44ae-9afa-00497f2c3ebf.png\", \"e2c805d7-8415-4020-bdaf-4c4a1765ee9e.png\"]', 'base64_encoded_video', '123 Main Street, City', 50, 1, 'Event details go here', '[\"0af26236-c753-4058-a1f1-b9d980f609ab.png\", \"9452de49-fecd-4be1-b9aa-fc8e9a767965.png\"]', 'Event description goes here', 'Party', 16, 'Service details go here', 40.7128, -74.006, 'Sample Location', NULL, NULL),
(121, '0d465097-1861-4a8d-ac69-857ca857509a.png', '[\"e5c89fdd-750a-45fb-bd1d-2d994ea30f54.png\", \"62d00178-4980-4616-9314-942299d8ceb0.png\"]', 'base64_encoded_video', '123 Main Street, City', 50, 1, 'Event details go here', '[\"7e66e40a-fc61-46de-9faf-cbd0ebe7b119.png\", \"1648d427-9645-4ad9-bdb2-8e47af25bd82.png\"]', 'Event description goes here', 'Party', 16, 'Service details go here', 40.7128, -74.006, 'Sample Location', NULL, NULL),
(122, '9e863a4e-5d6b-492e-8fcd-418307bcce8c.png', '[\"bafe97d8-59c1-42f1-8304-30b1a27ea31f.png\", \"cf9c2b05-e182-4a79-a381-c094ecaeb307.png\"]', 'base64_encoded_video', '123 Main Street, City', 50, 1, 'Event details go here', '[\"30af555b-75db-42b8-a5f9-be2be22bc564.png\", \"2c50dff1-d9db-4c42-8368-eba817acd78d.png\"]', 'Event description goes here', 'Party', 16, 'Service details go here', 40.7128, -74.006, 'Sample Location', NULL, NULL),
(123, '4354fe92-744d-41d9-80af-d4bf2df64c66.png', '[\"d97cafb4-2461-4382-a262-101f9e15dc03.png\", \"08fab056-1295-4c97-826b-0e31d8341765.png\"]', 'base64_encoded_video', '123 Main Street, City', 50, 1, 'Event details go here', '[\"1041ca43-0873-4cc1-8fcf-6003f3be828d.png\", \"6770e0b7-9315-478a-9c45-2025b8c92c94.png\"]', 'Event description goes here', 'Party', 16, 'Service details go here', 40.7128, -74.006, 'Sample Location', 'Something', 50),
(124, 'fa543f8f-9f8d-49e7-9e32-29d01a7ef73c.png', '[\"4dd27cfd-d894-44db-be3a-b2b8c6f80af8.png\", \"f879035d-f32f-48cd-af2a-76bb8027357f.png\"]', 'base64_encoded_video', '123 Main Street, City', 50, 1, 'Event details go here', '[\"824b51a5-d4bd-4049-81b6-f216fd369477.png\", \"64c3036e-34e8-484c-ba53-45e3a5d1a254.png\"]', 'Event description goes here', 'Party', 16, 'Service details go here', 40.7128, -74.006, 'Sample Location', 'Something', 50);

-- --------------------------------------------------------

--
-- Table structure for table `eventtiming`
--

CREATE TABLE `eventtiming` (
  `id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `day_of_week` varchar(10) DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `available` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `eventtiming`
--

INSERT INTO `eventtiming` (`id`, `event_id`, `day_of_week`, `start_time`, `end_time`, `available`) VALUES
(35, 70, 'Monday', '12:00:00', '23:00:00', 1),
(36, 70, 'Tuesday', '12:00:00', '23:00:00', 1),
(37, 70, 'Wednesday', '12:00:00', '23:00:00', 1),
(38, 70, 'Thursday', '12:00:00', '23:00:00', 1),
(39, 70, 'Friday', '11:00:00', '19:00:00', 0),
(40, 70, 'Saturday', '12:00:00', '23:00:00', 1),
(41, 70, 'Sunday', '12:00:00', '23:00:00', 1),
(42, 71, 'Monday', '12:00:00', '23:00:00', 1),
(43, 71, 'Tuesday', '12:00:00', '23:00:00', 1),
(44, 71, 'Wednesday', '12:00:00', '23:00:00', 1),
(45, 71, 'Thursday', '12:00:00', '23:00:00', 1),
(46, 71, 'Saturday', '12:00:00', '23:00:00', 1),
(47, 71, 'Sunday', '12:00:00', '23:00:00', 1),
(48, 72, 'Monday', '12:00:00', '23:00:00', 1),
(49, 72, 'Tuesday', '12:00:00', '23:00:00', 1),
(50, 72, 'Wednesday', '12:00:00', '23:00:00', 1),
(51, 72, 'Thursday', '12:00:00', '23:00:00', 1),
(52, 72, 'Saturday', '12:00:00', '23:00:00', 1),
(53, 72, 'Sunday', '12:00:00', '23:00:00', 1),
(54, 73, 'Monday', '12:00:00', '23:00:00', 1),
(55, 73, 'Tuesday', '12:00:00', '23:00:00', 1),
(56, 73, 'Wednesday', '12:00:00', '23:00:00', 1),
(57, 73, 'Thursday', '12:00:00', '23:00:00', 1),
(58, 73, 'Saturday', '12:00:00', '23:00:00', 1),
(59, 73, 'Sunday', '12:00:00', '23:00:00', 1),
(60, 74, 'Monday', '10:00:00', '18:00:00', 1),
(61, 74, 'Tuesday', '11:00:00', '19:00:00', 1),
(62, 75, 'Monday', '10:00:00', '18:00:00', 1),
(63, 75, 'Tuesday', '11:00:00', '19:00:00', 1),
(64, 76, 'Monday', '10:00:00', '18:00:00', 1),
(65, 76, 'Tuesday', '11:00:00', '19:00:00', 1),
(66, 77, 'Monday', '10:00:00', '18:00:00', 1),
(67, 77, 'Tuesday', '11:00:00', '19:00:00', 1),
(68, 78, 'Monday', '10:00:00', '18:00:00', 1),
(69, 78, 'Tuesday', '11:00:00', '19:00:00', 1),
(70, 79, 'Monday', '10:00:00', '18:00:00', 1),
(71, 79, 'Tuesday', '11:00:00', '19:00:00', 1),
(72, 80, 'Monday', '10:00:00', '18:00:00', 1),
(73, 80, 'Tuesday', '11:00:00', '19:00:00', 1),
(74, 81, 'Monday', '10:00:00', '18:00:00', 1),
(75, 81, 'Tuesday', '11:00:00', '19:00:00', 1),
(88, 88, 'Monday', '10:00:00', '18:00:00', 1),
(89, 88, 'Tuesday', '11:00:00', '19:00:00', 1),
(90, 89, 'Monday', '10:00:00', '18:00:00', 1),
(91, 89, 'Tuesday', '11:00:00', '19:00:00', 1),
(92, 89, 'Wednesday', '08:00:00', '23:59:59', 1),
(93, 89, 'Thursday', '08:00:00', '23:59:59', 1),
(94, 89, 'Friday', '08:00:00', '23:59:59', 1),
(95, 89, 'Saturday', '08:00:00', '23:59:59', 1),
(96, 89, 'Sunday', '08:00:00', '23:59:59', 1),
(97, 90, 'Monday', '10:00:00', '18:00:00', 1),
(98, 90, 'Tuesday', '11:00:00', '19:00:00', 1),
(99, 91, 'Monday', '10:00:00', '18:00:00', 1),
(100, 91, 'Tuesday', '11:00:00', '19:00:00', 1),
(101, 92, 'Monday', '10:00:00', '18:00:00', 1),
(102, 92, 'Tuesday', '11:00:00', '19:00:00', 1),
(103, 93, 'Monday', '10:00:00', '18:00:00', 1),
(104, 93, 'Tuesday', '11:00:00', '19:00:00', 1),
(105, 94, 'Monday', '10:00:00', '18:00:00', 1),
(106, 94, 'Tuesday', '11:00:00', '19:00:00', 1),
(107, 95, 'Monday', '10:00:00', '18:00:00', 1),
(108, 95, 'Tuesday', '11:00:00', '19:00:00', 1),
(109, 96, 'Monday', '10:00:00', '18:00:00', 1),
(110, 96, 'Tuesday', '11:00:00', '19:00:00', 1),
(111, 97, 'Monday', '10:00:00', '18:00:00', 1),
(112, 97, 'Tuesday', '11:00:00', '19:00:00', 1),
(113, 98, 'Monday', '10:00:00', '18:00:00', 1),
(114, 98, 'Tuesday', '11:00:00', '19:00:00', 1),
(115, 99, 'Monday', '10:00:00', '18:00:00', 1),
(116, 99, 'Tuesday', '11:00:00', '19:00:00', 1),
(135, 109, 'Monday', '10:00:00', '18:00:00', 1),
(136, 109, 'Tuesday', '11:00:00', '19:00:00', 1),
(137, 118, 'Monday', '10:00:00', '18:00:00', 1),
(138, 118, 'Tuesday', '09:00:00', '17:00:00', 1),
(139, 119, 'Monday', '10:00:00', '18:00:00', 1),
(140, 119, 'Tuesday', '09:00:00', '17:00:00', 1),
(141, 120, 'Monday', '10:00:00', '18:00:00', 1),
(142, 120, 'Tuesday', '09:00:00', '17:00:00', 1),
(143, 120, 'Wednesday', '10:00:00', '18:00:00', 1),
(144, 120, 'Thursday', '09:00:00', '17:00:00', 1),
(145, 121, 'Monday', '10:00:00', '18:00:00', 1),
(146, 121, 'Tuesday', '09:00:00', '17:00:00', 1),
(147, 121, 'Wednesday', '10:00:00', '18:00:00', 1),
(148, 121, 'Thursday', '09:00:00', '17:00:00', 1),
(149, 122, 'Monday', '10:00:00', '18:00:00', 1),
(150, 122, 'Tuesday', '09:00:00', '17:00:00', 1),
(151, 122, 'Wednesday', '10:00:00', '18:00:00', 1),
(152, 122, 'Thursday', '09:00:00', '17:00:00', 1),
(153, 123, 'Monday', '10:00:00', '18:00:00', 1),
(154, 123, 'Tuesday', '09:00:00', '17:00:00', 1),
(155, 123, 'Wednesday', '10:00:00', '18:00:00', 1),
(156, 123, 'Thursday', '09:00:00', '17:00:00', 1),
(157, 124, 'Monday', '10:00:00', '18:00:00', 1),
(158, 124, 'Tuesday', '09:00:00', '17:00:00', 1),
(159, 124, 'Wednesday', '10:00:00', '18:00:00', 1),
(160, 124, 'Thursday', '09:00:00', '17:00:00', 1);

-- --------------------------------------------------------

--
-- Table structure for table `extra_facility`
--

CREATE TABLE `extra_facility` (
  `id` int(11) NOT NULL,
  `name` varchar(1024) DEFAULT NULL,
  `image` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`image`)),
  `event_id` int(11) NOT NULL,
  `rate` float DEFAULT 0,
  `unit` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `extra_facility`
--

INSERT INTO `extra_facility` (`id`, `name`, `image`, `event_id`, `rate`, `unit`) VALUES
(5, 'Valet Parking', '[\"9727f52f-8dc4-416a-bc24-a643022e5fd6.png\", \"9b378a69-71ea-41fb-bd36-db159b9b7f31.png\"]', 88, 100, 'hour'),
(6, 'water bottle', '[\"a5d272fc-2c4f-408e-b5b9-6c574c2ac615.png\", \"e32c8129-de25-4234-a69a-3a42d35f0bc6.png\"]', 88, 200, 'unit'),
(17, 'art galleries', '[\"61404a80-035d-4873-897d-b1fb1814229b.png\", \"956a2671-cfb9-420c-adcf-d99cceaf0b01.png\"]', 109, 50, 'hour'),
(18, 'museums', '[\"94da3696-c2b9-42ed-b012-2258117a041b.png\", \"5d255696-ee8a-4397-a8e9-0bcec1870ec1.png\"]', 109, 80, 'hour'),
(19, 'extra 112', '[\"1554b9e9-8a11-42c5-9ac4-0ee225489060.png\", \"61691640-234a-42b0-8a11-4095a21982d9.png\"]', 118, 100, 'hour'),
(20, 'tissue massdkjngjsdngsdingisbghibsibgsdigbsage', '[\"d315a4bf-8dc7-4270-882e-4ebcbd81b8f8.png\", \"7d0837c9-d50e-43f8-92f6-4ad39e7ed01b.png\"]', 118, 200000, 'item'),
(21, 'Extra Facility 1', '[\"8e172ca6-9957-49e7-a783-915bf9b5dab4.png\", \"f56a2020-b598-4d0c-a15f-7a10cb9ce995.png\"]', 119, 20, 'hour'),
(22, 'Extra Facility 2', '[\"fc4c5779-c2e0-4412-bcfb-4bf6d15436b8.png\", \"4da4b467-8696-4204-a40b-5101d9a0deda.png\"]', 119, 15, 'unit'),
(23, 'Extra Facility 1', '[\"f8e2d6c9-d3c7-4dbe-b829-daad5cc7b8aa.png\", \"ad9d3d21-b89f-4032-8439-0242acba4bae.png\"]', 120, 2000000, 'unit'),
(24, 'Extra Facility 2', '[\"c9546fce-fc05-4efb-824c-4a30244d4080.png\", \"2badb4ce-9b57-4303-b7ea-587c21f8acf3.png\"]', 120, 2000000, 'unit'),
(25, 'extra 3', '[\"bc7ef704-0246-48cf-b6fa-e52be5fa53cf.png\", \"6cbc9060-8dec-4323-96d6-4567ff7eca26.png\"]', 118, 20, 'hour'),
(26, 'extra asdas1', '[\"b8bba6a2-48a5-4d33-8767-9b93d0f91883.png\", \"e8a7281b-c0a7-4625-bc8c-10d3d7416e03.png\"]', 118, 20, 'hour'),
(27, 'extra 3', '[\"cc4c5603-d297-4568-831a-0e6a5f7175e8.png\", \"9fb0d10c-06f5-4009-aa12-7aee87fae3e4.png\"]', 118, 20, 'hour'),
(28, 'extra 3', '[\"72796baa-ed9c-4543-bbb7-340bc786624b.png\", \"b48f6e8d-5ff0-43da-8661-acb448c4a68b.png\"]', 118, 20, 'hour'),
(29, 'extra 3', '[\"7aa57144-2b40-4293-9cea-5acedbccb010.png\", \"663a91dc-7e6b-4277-a8c9-2f52f6e2f882.png\"]', 118, 20, 'hour'),
(30, 'extra 3', '[\"4d2335b6-f59f-485a-a0dd-8018cc0a0dea.png\", \"19d86b5d-38aa-420d-8797-16837219d34e.png\"]', 118, 20, 'hour'),
(31, 'extra 3', '[\"d9c3526d-69e2-4c88-a6ce-bddaa12c7a7a.png\", \"0ad8f161-ab64-4d06-bd0e-300b25f3e1e9.png\"]', 118, 20, 'hour'),
(36, 'extra 3', '[\"5dd2274b-204b-4339-91ff-1998343906df.png\", \"80bee430-e249-464a-a60a-abe29498cbe1.png\"]', 118, 20, 'hour'),
(37, 'extra 3', '[\"2f369cb8-b4a3-4f64-b069-fc3da6abb1f0.png\", \"c88b5474-9b4e-4607-bfcb-257023d93baa.png\"]', 118, 20, 'hour'),
(38, 'extra 3', '[\"be30ebcd-7544-4b48-b5b7-a01ed4bb45c6.png\", \"a2b64286-b066-4d9f-ab85-73842d6b644d.png\"]', 118, 20, 'hour'),
(39, 'extra 3', '[\"dfc76f73-2c48-458f-84a5-e659c71c128e.png\", \"cfff7fd4-a4c1-4ac1-8979-76ae7359b7aa.png\"]', 118, 20, 'hour'),
(40, 'extra 3', '[\"f9e57459-5242-40d1-9851-ba607b4fb052.png\", \"21733d31-84e2-4eb0-b4c3-de6ba116482b.png\"]', 118, 20, 'hour'),
(41, 'extra 3', '[\"129e0e54-5fc1-42ed-aa92-95d326fe5e0f.png\", \"a457aefe-236a-4ad6-998a-4e019af954be.png\"]', 118, 20, 'hour'),
(42, 'extra 3', '[\"6ca96465-9aa7-4b9a-8f9c-20e7e174876d.png\", \"496b3ec6-006f-4b69-a424-a38d6a00f3a6.png\"]', 118, 20, 'hour'),
(43, 'Extra Facility 1', '[\"cbc1403f-76a9-45ee-99c8-ea1b940a138e.png\", \"60c3e845-504a-4f86-8dbd-3fd9e4917f5f.png\"]', 121, 2000000, 'unit'),
(44, 'Extra Facility 2', '[\"b2bf424d-444e-4469-bcc8-bac3e56b0f74.png\", \"3aede321-d2c4-4594-ac26-d9a6a43eb2bd.png\"]', 121, 2000000, 'unit'),
(45, 'Extra Facility 1', '[\"69cd1204-03fc-4b3a-aef7-c44368375d95.png\", \"ec12d9a7-e86a-4c1d-b3fd-0a5e9f788c2a.png\"]', 122, 2000000, 'unit'),
(46, 'Extra Facility 2', '[\"dafd27d9-e502-4b38-9408-6bb734496585.png\", \"70ce2822-5175-4a37-a3f3-a592678e5fdf.png\"]', 122, 2000000, 'unit'),
(47, 'Extra Facility 1', '[\"613de6aa-001f-4388-a0c2-e26ed4b3f753.png\", \"51546b83-52d7-4dd1-9fd0-ce6ca8565b48.png\"]', 123, 2000000, 'item'),
(48, 'Extra Facility 2', '[\"21730151-e5a9-45ee-942d-321f05d80c7e.png\", \"4fc57303-5936-48b9-a834-ef5010cedd64.png\"]', 123, 2000000, 'item'),
(49, 'Extra Facility 1', '[\"16dcfd22-f9c2-4355-adf3-1888a4eaeaa7.png\", \"eebda6ac-a93c-4f85-bbf6-38871caa8e88.png\"]', 124, 2000000, 'unit'),
(50, 'Extra Facility 2', '[\"33481a86-c162-4333-89ca-350494d67bdf.png\", \"d8ee9c0a-e06b-495f-a7c5-91d98e7818e4.png\"]', 124, 2000000, 'unit'),
(51, 'extra 3', '[\"07fbc5b0-ed63-498f-a7c0-3c2b3e3b8cec.png\", \"c75bdc76-a2dc-4808-b932-391878cf208a.png\"]', 118, 20, 'hour'),
(52, 'extra 3', '[\"c5508b1d-46d8-4d91-9c61-f3943da3d8cc.png\", \"44885993-f84f-49bb-9fa5-4325cc36ef21.png\"]', 118, 20, 'hour'),
(53, 'extra 3', '[\"ba063590-23b5-4583-a2f9-3bc90a83a492.png\", \"d5884dc6-a7a8-47e3-90a7-de723a190835.png\"]', 118, 20, 'hour'),
(54, 'extra 3', '[\"bfb610b4-7ec0-41f0-aa4b-ca8d10e9e0ad.png\", \"de7dc946-2947-48fd-9ea1-e66ad2d423fa.png\"]', 118, 20, 'hour');

-- --------------------------------------------------------

--
-- Table structure for table `favorites`
--

CREATE TABLE `favorites` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `favorites`
--

INSERT INTO `favorites` (`id`, `user_id`, `event_id`) VALUES
(10, 55, 15),
(11, 55, 8),
(12, 55, 2);

-- --------------------------------------------------------

--
-- Table structure for table `inquiry`
--

CREATE TABLE `inquiry` (
  `id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `guest_count` int(11) NOT NULL,
  `additional_notes` varchar(1024) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `all_day` tinyint(1) DEFAULT NULL,
  `event_type` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `cancelled` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inquiry`
--

INSERT INTO `inquiry` (`id`, `event_id`, `user_id`, `full_name`, `email`, `guest_count`, `additional_notes`, `start_date`, `end_date`, `start_time`, `end_time`, `all_day`, `event_type`, `created_at`, `cancelled`) VALUES
(2, 70, 55, 'Rafay and Rafay', 'johndoe@example.com', 5, 'Special requests for the event.', '2024-01-12', '2024-01-12', '12:00:00', '13:20:23', 0, 'Bussiness Meeting', '2024-01-11 13:13:14', 0),
(3, 70, 55, 'Rafay and Rafay', 'asbfjkdnf@gmail.com', 5, 'Special requests for the event.', '2024-01-12', '2024-01-12', '12:00:00', '13:20:23', 0, 'Bussiness Meeting', '2024-01-11 13:13:32', 0),
(4, 123, 55, 'John Doe', 'john.doe@example.com', 5, 'We\'re celebrating a birthday!', '2024-03-15', '2024-03-16', '14:00:00', '18:00:00', 0, 'Birthday Party', '2024-02-20 10:52:46', 0);

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `message_type` varchar(255) DEFAULT NULL,
  `creation_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `readed` tinyint(1) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_token`
--

CREATE TABLE `password_reset_token` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `expired_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `password_reset_token`
--

INSERT INTO `password_reset_token` (`id`, `user_id`, `token`, `created_at`, `expired_at`) VALUES
(1, 1, 'smZZLThS2TVq_H-CjNMh18Fo3E3JhYAQAsmgd8n7ukI', '2023-10-06 15:32:46', '2023-10-06 16:32:46'),
(3, 5, 'mVoQS4QG9eABjvKNP1wrda1Nndrm-GiTMShMyp48KgA', '2023-10-06 15:52:04', '2023-10-06 16:52:04'),
(5, 45, 'KVWt3P5m71K47VOJ7jvB9I87esNMq_QIQqR02x8V5fo', '2023-11-08 10:14:44', '2023-11-08 11:14:44');

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

CREATE TABLE `review` (
  `id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `cleanliness_rating` float NOT NULL,
  `price_value_rating` float NOT NULL,
  `service_value_rating` float NOT NULL,
  `location_rating` float NOT NULL,
  `user_review` varchar(1024) DEFAULT NULL,
  `average_rating` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `review`
--

INSERT INTO `review` (`id`, `booking_id`, `event_id`, `user_id`, `cleanliness_rating`, `price_value_rating`, `service_value_rating`, `location_rating`, `user_review`, `average_rating`) VALUES
(1, 2, 1, 48, 1, 3, 1, 1, 'The event was very boring', 5),
(2, 3, 1, 48, 2.5, 1.5, 4, 5, 'The event was very boring', 5),
(4, 8, 1, 50, 1, 3, 1, 1, 'The event was very boring', 0),
(5, 9, 1, 50, 1, 3, 1, 1, 'The event was very boring', 0),
(9, 12, 1, 50, 1, 3, 1, 1, 'The event was very boring', 0),
(10, 13, 2, 50, 1.5, 3, 1.5, 4.5, 'The event was very boring', 5),
(11, 14, 3, 50, 2.5, 3.5, 1.5, 4.5, 'The event was very boring', 5),
(12, 15, 4, 50, 2.5, 1.5, 1.5, 4.5, 'The event was very boring', 5),
(13, 16, 5, 50, 4.5, 1.5, 1.5, 4.5, 'The event was very boring', 4.9),
(14, 17, 6, 50, 5, 5, 5, 5, 'The event was very boring', 5),
(15, 18, 7, 50, 5, 5, 5, 4.5, 'The event was very boring', 5),
(16, 19, 8, 50, 5, 5, 5, 0, 'The event was very boring', 5),
(17, 20, 9, 50, 5, 5, 5, 0, 'The event was very boring', 1.5),
(18, 21, 10, 50, 5, 5, 5, 0, 'The event was very boring', 1),
(19, 22, 11, 50, 5, 5, 5, 0.5, 'The event was very boring', 5),
(20, 35, 21, 51, 5, 5, 5, 0.5, 'The event was very boring', 5),
(21, 36, 20, 51, 0.5, 5, 5, 0.5, 'The event was very boring', 5),
(22, 37, 19, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 1),
(23, 38, 18, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 2),
(24, 39, 17, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 3),
(25, 40, 16, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 4),
(26, 41, 15, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(27, 42, 14, 51, 5, 5, 5, 5, 'The event was very boring', 5),
(28, 43, 13, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(29, 44, 12, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(30, 45, 11, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(31, 46, 10, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(32, 47, 9, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(33, 48, 8, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(34, 49, 7, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(35, 50, 6, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(36, 51, 5, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 4.9),
(37, 52, 4, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(38, 53, 3, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(39, 54, 2, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 3),
(40, 55, 1, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 0),
(41, 56, 26, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(42, 57, 27, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(43, 189, 118, 55, 4.5, 4, 5, 4.2, 'The event was fantastic! I really enjoyed the venue and the services provided.', 4.4);

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `user_type` varchar(10) NOT NULL,
  `transaction_time` datetime NOT NULL,
  `transaction_amount` float NOT NULL,
  `trans_id` varchar(255) NOT NULL,
  `transaction_type` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`id`, `user_id`, `user_type`, `transaction_time`, `transaction_amount`, `trans_id`, `transaction_type`) VALUES
(1, 54, 'vendor', '2024-01-19 15:02:51', 20, '', ''),
(2, 54, 'vendor', '2024-01-19 15:05:51', 20, '', ''),
(3, 54, 'vendor', '2024-01-19 15:06:52', 20, '', ''),
(4, 54, 'vendor', '2024-01-19 15:08:19', 31, '', ''),
(5, 54, 'vendor', '2024-01-19 15:08:19', 4954, '', ''),
(6, 55, 'user', '2024-02-22 14:03:54', 1099, 'pi_3OmcsSCvNBqAG6fP0rmfttNC', 'stripe'),
(7, 55, 'user', '2024-02-22 14:30:07', 1099, 'pi_3OmdHoCvNBqAG6fP0lpOTsuA', 'stripe');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `access_token` varchar(1024) DEFAULT NULL,
  `role` varchar(50) NOT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  `vendor_id` int(11) DEFAULT NULL,
  `verified` tinyint(1) NOT NULL,
  `otp` varchar(10) DEFAULT NULL,
  `device_token` text DEFAULT NULL,
  `google_token` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `email`, `password_hash`, `access_token`, `role`, `profile_image`, `vendor_id`, `verified`, `otp`, `device_token`, `google_token`) VALUES
(1, 'itsabdulrafay@gmail.com', '$2b$12$yhZ6bsGJW5rr3oi2fWlSPesvMRPkaUXbf8JUS1D2fUa1mibWn2.EK', NULL, 'user', NULL, NULL, 0, NULL, NULL, NULL),
(3, 'abdulrafayatiq1.03@gmail.com', '$2b$12$kKmu2/LrmF8LZoB9gpYqN.klByrmSa8ZpjypZiQc3v2djWWtRo/3W', NULL, 'user', NULL, NULL, 0, NULL, NULL, NULL),
(4, 'abdulrafayatiq12.03@gmail.com', '$2b$12$56QCfrAJ9guP2xsBbYbNcec2./sfLSeYToBKXLPa34AVoGTJyMOUm', NULL, 'user', NULL, NULL, 0, NULL, NULL, NULL),
(5, 'abdulrafaya213tiq12.03@gmail.com', '$2b$12$mspOXUAz9rESOe5b2WnDeONnJ0FEWq0b1sDyEjjubnm7ERO2jtwVy', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjYwNzUxOSwianRpIjoiY2Q0NzAzMDEtMDNlYy00OGJjLWFlY2MtMGJjYzc0YjhmYzE5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhMjEzdGlxMTIuMDNAZ21haWwuY29tIiwibmJmIjoxNjk2NjA3NTE5LCJleHAiOjE2OTY2MD', 'user', NULL, NULL, 0, NULL, NULL, NULL),
(6, 'mrrafayatiq.03@gmail.com', '$2b$12$Z7.4zmA.NDIZRj65j5mi/.k/f5WuNXukOyBCzv1AGhIguQ2gPsgkW', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjkyMTAxMSwianRpIjoiYWYyNTMzZGQtNDY3MS00MmU2LTg0MmItZjRjM2NiNGRhZTJkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im1ycmFmYXlhdGlxLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTY5NjkyMTAxMSwiZXhwIjoxNjk2OTIxOTExfQ.o25', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(8, 'vendor@example.com', '$2b$12$/pH1pXZnAI8D0RP0jwfDr.aTk0MZ0HsI4TqSc6bSNszXhMMvS2l5m', NULL, 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(9, 'rafayvendor@example.com', '$2b$12$d986ivB7fjQ2oGcQV8Zb8eyK2OPA9FbeWgm71p4Ondv1lq/KQA2C6', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjkzMTMyMCwianRpIjoiYjE1OTY2YjEtMTA2Mi00NjgyLThjYTUtMzRjYjVlYWM3MDA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5dmVuZG9yQGV4YW1wbGUuY29tIiwibmJmIjoxNjk2OTMxMzIwLCJleHAiOjE2OTY5MzIyMjB9.d1ys1', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(10, 'rafayvendor2003@example.com', '$2b$12$gXLEBmv8lU3hMhPsEEkj2ekkw8zihjgB15UkUnWT57p3gTcoipiai', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjkzNjg5MywianRpIjoiOTZhNzAxMWMtMGNlMS00ZDBlLWJkOTgtNTc3ZGIxZjc0ODA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5dmVuZG9yMjAwM0BleGFtcGxlLmNvbSIsIm5iZiI6MTY5NjkzNjg5MywiZXhwIjoxNjk2OTM3NzkzfQ', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(11, 'rafayvendor20003@example.com', '$2b$12$K.QXAC8imIVcq1sBWYVV7OGkY64PXHx2pZCTlak/Qsbh/fkjrVMBm', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjkzNzk5NywianRpIjoiZmZmZDhkYzAtZmQ4Mi00ZDBhLWJhZTYtNzZlYTAyOTkwZGUwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5dmVuZG9yMjAwMDNAZXhhbXBsZS5jb20iLCJuYmYiOjE2OTY5Mzc5OTcsImV4cCI6MTY5NjkzODg5N3', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(12, 'rafayvendor200003@example.com', '$2b$12$bk4TbuTHLo2OGI2iLE1/dOSpSloYrCJejcfP8cSOgXEu35JMODyNK', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5Njk0MjMzOSwianRpIjoiMGNmMWQzN2ItM2ExMS00M2FlLTlhYmEtNmQ5YTlmZjNkNmUyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5dmVuZG9yMjAwMDAzQGV4YW1wbGUuY29tIiwibmJmIjoxNjk2OTQyMzM5LCJleHAiOjE2OTY5NDMyMz', 'vendor', '?PNG\n\Z\n\0\0\0\nIHDR\0\0\0?\0\0\0\0\0tb?=\0\0APLTE?????\0?EB!)???y??\0??\0\0????\0/\0\0\0??\0??1\0\0?\0r\0?-+\0\0\0?3\'\0\0,\0\0???3\0\0????\0k??\0?9<\0\0\0\09\0?\0o?\0??????????????????:\0?????????7\0?xq??y????????K????ˠ???{jb?????WfQF???p]T?????~#\0\0?????????M?o\\?z??????\0\0{??U9*????????', NULL, 0, NULL, NULL, NULL),
(13, 'rafayvendor1@gmail.com', '$2b$12$7oXDBIZ/Uj8pO9bm0KYXN.5Lcw839mKMNFcIOXHlotHpmpaO.K/nK', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzQ0OTQ3NywianRpIjoiMDEwMGE2NjgtM2UxYS00NzgwLWI5YjktNDg1N2RjNjZlZDM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5dmVuZG9yMUBnbWFpbC5jb20iLCJuYmYiOjE2OTc0NDk0NzcsImV4cCI6MTY5NzQ1MDM3N30.OILBxx', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(15, 'abdulrafayatiq123123123.03@gmail.com', '$2b$12$NbddmYJCvaZZSIFJ38vFYO6LEnOoyUEfS8tKDNLai7mqxhDVS3tVO', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODA1Njc3MCwianRpIjoiMTg5ZWY1YWEtOGFmOS00YjVhLTg4NDEtMDc4YjVhYWZiMzIwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxMTIzMTIzMTIzLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTY5ODA1Njc3MCwiZXhwIjoxNj', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(16, 'abdulrafayatiq12312312345.03@gmail.com', '$2b$12$IgUD6KVbmczhEleCF4KNK.2nnQnrJ.h5zcj8FIOjQVRBLyWWLY0O6', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODA1ODE3MywianRpIjoiYWZjMWY4YjctMjE5Yi00YWQwLWExNmItZTIyY2U1NzJjYWU5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxMTIzMTIzMTIzNDUuMDNAZ21haWwuY29tIiwibmJmIjoxNjk4MDU4MTczLCJleHAiOj', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(17, 'abdulrafayatiq1a.03@gmail.com', '$2b$12$CUGwmKX6WNtRlmWVOL6FPuK5ExkkvYlbxlzcWhjMas0KP1k9W/qTy', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODA2Mzg2OCwianRpIjoiNDMxMWFiMDQtNThjMC00ODhkLWE4MzYtN2FjNWJiODAxYTc1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxMWEuMDNAZ21haWwuY29tIiwibmJmIjoxNjk4MDYzODY4LCJleHAiOjE2OTgwNjQ3Nj', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(18, 'abdulrafayatiq11a.03@gmail.com', '$2b$12$zR80Qz5RO.211daR6hkPZeGQrh3TbK8a3i488q/pSYwar3OQN47ve', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODA2NDU3OCwianRpIjoiY2ZkNWNiMmYtZTA1MS00ZWFiLWI3NTktNDk5MWFmMmNkY2ZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxMTFhLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTY5ODA2NDU3OCwiZXhwIjoxNjk4MDY1ND', 'vendor', '33df98c4-34ec-414a-b3c3-689cc0c7fd01.png', NULL, 0, NULL, NULL, NULL),
(21, 'justrafay@gmail.com', '$2b$12$Qr5i/UxRLakF3ynvr69AE.tNBku/c9tXi0iV.cWq9DZR91q1glEKW', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODE0MDkzNCwianRpIjoiNmRmMjY0YjQtMzU4Yy00NjQ5LWEyN2ItMjMyZWQzYzBiZTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RyYWZheUBnbWFpbC5jb20iLCJuYmYiOjE2OTgxNDA5MzQsImV4cCI6MTY5ODE0MTgzNH0.RvPaPMpPX1', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(22, 'justrafay1@gmail.com', '$2b$12$c5G1F52/34UzZIlJY7gHR.1v46kdvpwHSL/q2E2r/erX5ifI4ZJlu', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODE0MTUwNiwianRpIjoiMDk1NmI3ZDEtYWYwOS00NDJiLTkxNGUtMTU0ODQzOTMxZGRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RyYWZheTFAZ21haWwuY29tIiwibmJmIjoxNjk4MTQxNTA2LCJleHAiOjE2OTgxNDI0MDZ9.MPGvkuyl2', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(33, 'justrafay5@gmail.com', '$2b$12$oUuFZYigfJDaHmTP0zUgH.oxtN9OHh9M8hCECYlxxcdA.VPN.iy1S', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzIzNzQ4OCwianRpIjoiODNkODkwMzUtNDYyZC00MmMwLTg1MzctNGQ2MjI2N2U5ODNlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RyYWZheTVAZ21haWwuY29tIiwibmJmIjoxNzAzMjM3NDg4LCJleHAiOjE3MDMyMzgzODh9.hLaxDnqMO', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 6, 0, NULL, NULL, NULL),
(34, 'justitsmerafay@gmail.com', '$2b$12$w0uEFtfx8I0uCUDP1hJqiOa8sZ3fwwahd92Tw3/lABqhHftqPnH2C', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODIyMTMyMywianRpIjoiZDQ2YWJkNjYtZmRkMy00ZDE3LTgzMjMtNWRlMThlNzIwZjQ5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RpdHNtZXJhZmF5QGdtYWlsLmNvbSIsIm5iZiI6MTY5ODIyMTMyMywiZXhwIjoxNjk4MjIyMjIzfQ.bGw', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 7, 0, NULL, NULL, NULL),
(35, 'justitsmerafay1@gmail.com', '$2b$12$9G/q3dDs2WUpl9VicjSQFesOnx6jdCcfjG2FLYkDi8an6na4iHA2y', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODIyMjMzNywianRpIjoiZDM4ZmE2OWYtYWMzNS00ZjI1LTg2NTgtYTg1ZmNhYjZjMzZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RpdHNtZXJhZmF5MUBnbWFpbC5jb20iLCJuYmYiOjE2OTgyMjIzMzcsImV4cCI6MTY5ODIyMzIzN30.7V', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 8, 0, NULL, NULL, NULL),
(36, 'justitsmerafay2@gmail.com', '$2b$12$vJq3CG84rq55kHem5MBaqev6l2SX24iEN6jGnkh.LsVbuMgz6DRK2', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODIyMzI2OCwianRpIjoiZDBlZjE0ZTEtN2Y3Yy00MjcyLWIwM2EtNGE3YWJjZWZhMDEyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RpdHNtZXJhZmF5MkBnbWFpbC5jb20iLCJuYmYiOjE2OTgyMjMyNjgsImV4cCI6MTY5ODIyNDE2OH0.IV', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(37, 'justitsmerafay3@gmail.com', '$2b$12$l5dHdXSRo7sD8kJ5tySrjuwllqF4vCN9.gW2VWPmh8mpR64VdnjU6', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODIyNjg5MCwianRpIjoiZjYzYzE2Y2QtNzNjMy00MmFhLThkODItYTdlYjgzOTk4NjhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RpdHNtZXJhZmF5M0BnbWFpbC5jb20iLCJuYmYiOjE2OTgyMjY4OTAsImV4cCI6MTY5ODIyNzc5MH0.7I', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(38, 'rafay@gmail.com', '$2b$12$1iKVhkbemNVTtLhw/xM5UObQ5nP0NQ/AyTWyUa.4mUUe8QIH/KBk.', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODIyNzc0NiwianRpIjoiZTViZjFhOWQtOTBjNy00ZDg2LTg5NGMtN2EwYmUxNmI4MWJiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5QGdtYWlsLmNvbSIsIm5iZiI6MTY5ODIyNzc0NiwiZXhwIjoxNjk4MjI4NjQ2fQ._ZmJ7Vlc9EWmo_V', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(39, 'rafay03@gmail.com', '$2b$12$Ibo6K6mDRs6n8UrDGEF9GuhYQEx9HHq9s5fpb7MEB8DiAhZUQiXwG', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODIyNzg3NiwianRpIjoiN2Q5ZDZjYTQtNzM2Mi00MTcxLTlkZTUtMDkxYjY0YmZhYTMwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5MDNAZ21haWwuY29tIiwibmJmIjoxNjk4MjI3ODc2LCJleHAiOjE2OTgyMjg3NzZ9.NivPo2qUBZRg3', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', NULL, 0, NULL, NULL, NULL),
(40, 'abdulrafayat1a.03@gmail.com', '$2b$12$uoaxmBKCQ0mL2dSRsIefhuiv6Kk3XuXS2H5WLwjRbVlu6pBr60wQa', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODI0MDE5MiwianRpIjoiZDNmM2M0OTAtMmUxYy00YmJkLWI4YTgtMWQzMDczNjQ5YzNhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdDFhLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTY5ODI0MDE5MiwiZXhwIjoxNjk4MjQxMDkyfQ', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 9, 0, NULL, NULL, NULL),
(41, 'abdulrafayat1aa.03@gmail.com', '$2b$12$eYfno2gsa4aiRcT9qvZjt.rUrXvDSuYd9uFvrTmhqHV/dvvBdx.9u', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODI0MTUyOCwianRpIjoiODhlYmI0YmUtM2NmZS00OGZhLWFlZjMtYmU1OTcyZjhjM2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdDFhYS4wM0BnbWFpbC5jb20iLCJuYmYiOjE2OTgyNDE1MjgsImV4cCI6MTY5ODI0MjQyOH', 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(42, 'abdulrafayataaaaaaaaa.03@gmail.com', '$2b$12$xBxr1gbilc94UFcYla7Kgu3j41UTtGzF846DR9/uqbm/n8lpMD2MC', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODQwNTkzNCwianRpIjoiMjE3YzliMmYtMGZhOC00YzM1LWI0YTAtZGQxNzVkYmUxZjNhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGFhYWFhYWFhYS4wM0BnbWFpbC5jb20iLCJuYmYiOjE2OTg0MDU5MzQsImV4cCI6MTY5OD', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 10, 0, NULL, NULL, NULL),
(43, 'pythondeveloper@gmail.com', '$2b$12$CaV7ORxnVaY.T3sp/jWM0.eIFKOSzsLy4HEe6dSy3STs0UuozjMGW', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMjQ2OTY3NywianRpIjoiMTBkNGJiMGYtNmVhNi00NjUzLWJhMWMtOGNiZWQ1ODM2MTIwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InB5dGhvbmRldmVsb3BlckBnbWFpbC5jb20iLCJuYmYiOjE3MDI0Njk2NzcsImV4cCI6MTcwMjQ3MDU3N30.Gt', 'user', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', NULL, 0, NULL, NULL, NULL),
(44, 'heyrafay@gmail.com', '$2b$12$sp3oNuyjnZhhQgRJQv8zmOZT1/M7kmmjKdNHzDaeaBbSozJcpejCy', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTI2NjI2MiwianRpIjoiMjE2MTE3N2QtMTlkNi00YmFiLTkyODYtYTNmMjVlNWUyYWEwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImhleXJhZmF5QGdtYWlsLmNvbSIsIm5iZiI6MTY5OTI2NjI2MiwiZXhwIjoxNjk5MjY3MTYyfQ.zibNFm2nigG', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', NULL, 0, NULL, NULL, NULL),
(45, 'testing@example.com', '$2b$12$O7e0.hh0Ls/I7E3uHDebpuCvRcPYvpz029dNvpWthBbUICmD.z4Nm', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTQzODI5NSwianRpIjoiZmY1YmU3YmYtMWM4Mi00NjQyLTlmNmItODUwOTU1MjEwMmE3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3RpbmdAZXhhbXBsZS5jb20iLCJuYmYiOjE2OTk0MzgyOTUsImV4cCI6MTY5OTQzOTE5NX0.s4zr6ufXyE', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 11, 0, NULL, NULL, NULL),
(46, 'abdulrafayatiq.03@example.com', '$2b$12$Pck7CLu3cfqii/FpnECcvO8aeu9EGFFMntW9ft.J4NZ7WOprR6HAC', NULL, 'vendor', NULL, NULL, 0, NULL, NULL, NULL),
(48, 'abdulrafayatiq.03@gmail.com', '$2b$12$Jg9mGzEYi6FI8eiBRDt18u8pBZ3ZG8AJSrSYl307SBRI9bJCFAv02', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMTY5NTMzMSwianRpIjoiZjlmYTI3OWItNjIxMy00Y2U5LTlhMTYtZmRjYWU5ODFiYjMwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTcwMTY5NTMzMSwiZXhwIjoxNzAxNjk2MjMxfQ', 'user', NULL, NULL, 0, NULL, NULL, NULL),
(49, 'abdulrafayatiqvendor.03@gmail.com', '$2b$12$K42Loxqxmdc.V/yM01a07eqkFAexDOAtRG6Wvfk8UKohNICRSQqhO', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMjQ2OTU2NCwianRpIjoiNjE1MDhlYTQtZTE5MC00MzcwLWJjMjgtMDcyZjdhMTZhNDBlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxdmVuZG9yLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTcwMjQ2OTU2NCwiZXhwIjoxNzAyND', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 13, 0, NULL, NULL, NULL),
(50, 'just.03@gmail.com', '$2b$12$a78hShATy819L7uX3QO2s.By24/3b2Ymp9hA22QZ1EyODuBVSO/Km', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMTg1MTkwMywianRpIjoiMDY3ZmE0MjMtYWIxOS00ODZiLTgwYTktZTU1NjJmYjQzOTJiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3QuMDNAZ21haWwuY29tIiwibmJmIjoxNzAxODUxOTAzLCJleHAiOjE3MDE4NTI4MDN9.NTRvqStH8RdPp', 'user', NULL, NULL, 0, NULL, NULL, NULL),
(51, 'just1.03@gmail.com', '$2b$12$nqXV2GHiaT9DodRwnNoEwe16cAPGh0K5/hy4CMSzPUrOM8f2M9jIG', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMzIzOTU5MCwianRpIjoiZDliZDI2OGYtMTM3Zi00ZDAzLTk5MzgtMDM0YWExNTY5ZTY5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3QxLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTcwMzIzOTU5MCwiZXhwIjoxNzAzMjQwNDkwfQ.6YEevXnKorm', 'user', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', NULL, 0, NULL, NULL, NULL),
(52, 'abdulrafayatiq@gmail.com.com', '$2b$12$6tmvlYLzyYiZtllws6mCwOHOK/gS3p1xkzyNWA1ZHDHKMJrwtUXBK', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMTk0ODc1MywianRpIjoiZDY1ZjQxY2UtMzgyZS00NDZjLWJmZDYtYTE0OTk0ZWMxZDhiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxQGdtYWlsLmNvbS5jb20iLCJuYmYiOjE3MDE5NDg3NTMsImV4cCI6MTcwMTk0OTY1M3', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 14, 0, NULL, NULL, NULL),
(53, 'justvendor.03@gmail.com', '$2b$12$45f9pZi8ic2dUAErRFN5CuLXd1AEuUkPhgr8f3K6zn6VUZ9aJqhaO', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMjQ2NzQ1NCwianRpIjoiZTJlNTQ5NTEtODZjZS00MDIxLThkYTAtZjJhNmQ2YjJhOTYzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3R2ZW5kb3IuMDNAZ21haWwuY29tIiwibmJmIjoxNzAyNDY3NDU0LCJleHAiOjE3MDI0NjgzNTR9.TNPyj', 'vendor', NULL, 15, 0, NULL, NULL, NULL),
(54, 'abdulrafayatiq123.03@gmail.com', '$2b$12$U4aqywc9wSvbZkoqa/7dc.te5z.YXu00HLeSP4.OnYQ2n38Ls5dRG', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODU5NzAxOSwianRpIjoiNjJlMTcwYjItZTdmMC00MjMwLTlmZTItZWU5YjkxMDQ5Yjg3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxMTIzLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTcwODU5NzAxOSwiZXhwIjoxNzA4NTk3OT', 'vendor', NULL, 16, 0, NULL, NULL, NULL),
(55, 'abdulrafayatiq123456.03@gmail.com', '$2b$12$09vHC2/suja0qn8kbJ.hmeNJLz9MCkiqOyCwlIn79XnxE7FSMVDAy', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMDE1NTM4NCwianRpIjoiN2RiODU0ZjItMjQ4MC00NjkyLWFiNjktMDY5NmJmMzQ4ZjU1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxMTIzNDU2LjAzQGdtYWlsLmNvbSIsIm5iZiI6MTcxMDE1NTM4NCwiZXhwIjoxNzEwMTU2Mjg0fQ.3iEmV__qVuacrUFtnvc0FurrWl-fkYj_d5tfRsibx80', 'user', NULL, NULL, 0, NULL, NULL, NULL),
(56, 'abdulrafayatiq10.03@gmail.com', '$2b$12$pAcd4u8i/MDQPF.9PE2XBOUV7q1ol8opER87g5UZ45L2gHFUIv8dK', NULL, 'vendor', NULL, 20, 0, '9102', NULL, NULL),
(57, 'samscoutt.03@gmail.com', '$2b$12$6Rll0VLJ1nFnHzkOZ4P2a..lw9Y9v3QVhKb9gvNKlIzapiVLU.ntS', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODA4Nzk5OSwianRpIjoiNzkwZjM2YzAtM2MzYi00Y2JhLTkzY2UtZmEzZWNkMDMzNmU1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InNhbXNjb3V0dC4wM0BnbWFpbC5jb20iLCJuYmYiOjE3MDgwODc5OTksImV4cCI6MTcwODA4ODg5OX0.UHUlj5', 'vendor', NULL, 21, 0, '3019', NULL, NULL),
(59, 'abdulrafayatiq123alfnsk.03@gmail.com', '$2b$12$5IfaRl.R4/FsvFGrylyqr.nP1MaqvABV0jjRnhqnSay7vOVPVtN36', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwODYwODk2NywianRpIjoiNjkyMmYyN2QtN2MyMC00MzA5LWIwMTctNDk3OTAyNTZmMDk4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxMTIzYWxmbnNrLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTcwODYwODk2NywiZXhwIjoxNzA4NjA5ODY3fQ.OW1lshbYmyMdaaue_48rnozhYWVZBzEKfufwEaoUeGo', 'vendor', NULL, 22, 0, NULL, NULL, NULL),
(61, 'asklfnasklmdas.03@gmail.com', '$2b$12$bxBSIQ9ZlhNtMW.gZkh4i.3nGzaWI2Uyyosv1NupAMzL30g2M0K7e', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwOTYzMjcwNiwianRpIjoiYzU2MDgyOWEtMjA1Zi00MDUyLTliNGUtN2M3MTQ3MGJjNmZmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFza2xmbmFza2xtZGFzLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTcwOTYzMjcwNiwiZXhwIjoxNzA5NjMzNjA2fQ.Pfimkvdj8Tui5n_aHIZSubrZu_8KcARQBEYHakWG-ww', 'vendor', NULL, 23, 0, NULL, NULL, NULL),
(71, 'mylaptophp10se@gmail.com', '$2b$12$QgQAvgSidblUNrNcuVWq1utFxD5jOQ7DzVV72wXJtiMQ8jH7RaguC', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwOTcyOTY0NSwianRpIjoiOThmZmNiYjEtODJkMS00ZDU3LTk3YWItZWVjNDI1MTUyNzRiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im15bGFwdG9waHAxMHNlQGdtYWlsLmNvbSIsIm5iZiI6MTcwOTcyOTY0NX0.Y2c0Fjhu7yQVB2n3U-dve-mTsYaAjz0xWQuzw_qlf2c', 'user', 'https://lh3.googleusercontent.com/a/ACg8ocLx6lBx_M-0QqlRN06o1BlQFYAIQFPmby0v9aSqVrnO=s96-c', NULL, 0, NULL, NULL, 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjZmOTc3N2E2ODU5MDc3OThlZjc5NDA2MmMwMGI2NWQ2NmMyNDBiMWIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzNjIzNDczODM3NTUtNGw2dHVyc2dlZ3BxbjF0NHE5MG9sdWxucGxjdTR1dG4uYXBwcy5nb29nbGV1c2VyY29udGVudC5j');

-- --------------------------------------------------------

--
-- Table structure for table `vendor`
--

CREATE TABLE `vendor` (
  `id` int(11) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `phone_number` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `biography` varchar(1024) NOT NULL,
  `wallet` float DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vendor`
--

INSERT INTO `vendor` (`id`, `full_name`, `phone_number`, `location`, `biography`, `wallet`) VALUES
(6, 'Abdul Rafay Atiq', '090078601', 'Karachi', 'Luxury Wedding Celebration Venue', 0),
(7, 'Just Itsmerafay', '123-456-7890', 'Karachi', 'I am a talented vendor.', 0),
(8, 'Just Itsmerafay', '123-456-7890', 'Karachi', 'I am a talented vendor.', 0),
(9, 'djkgnsdkglsd Doe', '123-456-7890', 'Karachi', 'A short biography about the vendor', 0),
(10, 'Abdul Rafay Atiq 123', '090078601', 'Karachi', 'Luxury Wedding Celebration Venue 1', 0),
(11, 'NO testing', '0823572347059237', 'Karachi', 'Testing Biography 12312312312', 0),
(13, 'Rafay The Vendor', '0900833922', 'Karachi', 'Testing Biography', 0),
(14, 'Bob The Builder', '090078601', 'Karachi', 'Luxury Wedding Celebration Venue 123124nfsd', 0),
(15, 'Just Vendor', '1234567890', 'Karachi', 'Just a simple vendor.', 0),
(16, 'John Doe', '1234567890', 'Some Location', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 47498),
(20, '', '', '', '', 0),
(21, '', '', '', '', 0),
(22, '', '', '', '', 0),
(23, '', '', '', '', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `extra_facility_id` (`extra_facility_id`);

--
-- Indexes for table `booking_extra_facility`
--
ALTER TABLE `booking_extra_facility`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_id` (`booking_id`),
  ADD KEY `extra_facility_id` (`extra_facility_id`);

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vendor_id` (`vendor_id`);

--
-- Indexes for table `eventtiming`
--
ALTER TABLE `eventtiming`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`);

--
-- Indexes for table `extra_facility`
--
ALTER TABLE `extra_facility`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`);

--
-- Indexes for table `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `inquiry`
--
ALTER TABLE `inquiry`
  ADD PRIMARY KEY (`id`),
  ADD KEY `event_id` (`event_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `password_reset_token`
--
ALTER TABLE `password_reset_token`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_id` (`booking_id`),
  ADD KEY `event_id` (`event_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `access_token` (`access_token`) USING HASH,
  ADD UNIQUE KEY `vendor_id` (`vendor_id`);

--
-- Indexes for table `vendor`
--
ALTER TABLE `vendor`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=222;

--
-- AUTO_INCREMENT for table `booking_extra_facility`
--
ALTER TABLE `booking_extra_facility`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=125;

--
-- AUTO_INCREMENT for table `eventtiming`
--
ALTER TABLE `eventtiming`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=161;

--
-- AUTO_INCREMENT for table `extra_facility`
--
ALTER TABLE `extra_facility`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT for table `favorites`
--
ALTER TABLE `favorites`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `inquiry`
--
ALTER TABLE `inquiry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `password_reset_token`
--
ALTER TABLE `password_reset_token`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `review`
--
ALTER TABLE `review`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- AUTO_INCREMENT for table `vendor`
--
ALTER TABLE `vendor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `booking_ibfk_3` FOREIGN KEY (`extra_facility_id`) REFERENCES `extra_facility` (`id`);

--
-- Constraints for table `booking_extra_facility`
--
ALTER TABLE `booking_extra_facility`
  ADD CONSTRAINT `booking_extra_facility_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `booking` (`id`),
  ADD CONSTRAINT `booking_extra_facility_ibfk_2` FOREIGN KEY (`extra_facility_id`) REFERENCES `extra_facility` (`id`);

--
-- Constraints for table `event`
--
ALTER TABLE `event`
  ADD CONSTRAINT `event_ibfk_1` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`id`);

--
-- Constraints for table `eventtiming`
--
ALTER TABLE `eventtiming`
  ADD CONSTRAINT `eventtiming_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`);

--
-- Constraints for table `extra_facility`
--
ALTER TABLE `extra_facility`
  ADD CONSTRAINT `extra_facility_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`);

--
-- Constraints for table `favorites`
--
ALTER TABLE `favorites`
  ADD CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  ADD CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `inquiry`
--
ALTER TABLE `inquiry`
  ADD CONSTRAINT `inquiry_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  ADD CONSTRAINT `inquiry_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `password_reset_token`
--
ALTER TABLE `password_reset_token`
  ADD CONSTRAINT `password_reset_token_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `booking` (`id`),
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  ADD CONSTRAINT `review_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
