-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 12, 2023 at 08:29 AM
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
('c3c3909fbc24');

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
  `cancelled` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`id`, `event_id`, `user_id`, `full_name`, `email`, `guest_count`, `additional_notes`, `start_date`, `end_date`, `start_time`, `end_time`, `all_day`, `created_at`, `event_type`, `cancelled`) VALUES
(1, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2025-06-18', '2025-06-19', '00:00:00', '23:59:59', 1, '2023-12-04 12:57:32', 'Birthday', 0),
(2, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2022-06-18', '2022-06-19', '14:00:00', '15:00:00', 0, '2023-12-04 12:58:51', 'Birthday', 0),
(3, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2021-06-18', '2021-06-19', '14:00:00', '15:00:00', 0, '2023-12-04 12:59:25', 'Wedding', 0),
(4, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2021-06-18', '2021-06-20', '14:00:00', '15:00:00', 0, '2023-12-04 12:59:57', 'Wedding', 0),
(5, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2020-06-18', '2020-06-20', '14:00:00', '15:00:00', 0, '2023-12-04 13:00:54', 'Bussiness Meeting', 0),
(6, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2019-06-18', '2019-06-20', '14:00:00', '15:00:00', 0, '2023-12-04 13:01:01', 'Bussiness Meeting', 0),
(7, 1, 48, 'Abdul Rafay Atiq', 'abdulrafayatiq.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2018-06-18', '2018-06-20', '14:00:00', '15:00:00', 0, '2023-12-04 13:01:11', 'Bussiness Meeting', 0),
(8, 1, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-18', '2005-06-20', '14:00:00', '15:00:00', 0, '2023-12-04 13:26:24', 'Wedding', 0),
(9, 1, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-21', '2005-06-22', '14:00:00', '15:00:00', 0, '2023-12-04 13:26:40', 'Bussiness Meeting', 0),
(10, 1, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-23', '2005-06-24', '14:00:00', '15:00:00', 0, '2023-12-04 13:26:46', 'Birthday', 0),
(11, 1, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-25', '2005-06-26', '14:00:00', '15:00:00', 0, '2023-12-04 13:26:56', 'Wedding', 0),
(12, 1, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-04 13:27:04', 'Bussiness MEeting', 0),
(13, 2, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:25:35', NULL, 0),
(14, 3, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:15', NULL, 0),
(15, 4, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:21', NULL, 0),
(16, 5, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:27', NULL, 0),
(17, 6, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:32', NULL, 0),
(18, 7, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:38', NULL, 0),
(19, 8, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:44', NULL, 0),
(20, 9, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:50', NULL, 0),
(21, 10, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:26:56', NULL, 0),
(22, 11, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:01', NULL, 0),
(23, 12, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:05', NULL, 0),
(24, 13, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:09', NULL, 0),
(25, 14, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:13', NULL, 0),
(26, 15, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:17', NULL, 0),
(27, 16, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:22', NULL, 0),
(28, 17, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:25', NULL, 0),
(29, 18, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:41', NULL, 0),
(30, 19, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:45', NULL, 0),
(31, 20, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:51', NULL, 0),
(32, 21, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:54', NULL, 0),
(33, 22, 50, 'Abdul Rafay Atiq 123', 'just.03@gmail.com', 10, 'Arrange birthday cakes and ballons', '2005-06-27', '2005-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:27:58', NULL, 0),
(34, 22, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2025-01-25', '2025-01-25', '14:00:00', '15:00:00', 0, '2023-12-06 08:47:28', NULL, 0),
(35, 21, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:47:33', NULL, 0),
(36, 20, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:47:47', NULL, 0),
(37, 19, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:48:53', NULL, 0),
(38, 18, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:09', NULL, 0),
(39, 17, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:15', NULL, 0),
(40, 16, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:20', NULL, 0),
(41, 15, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:24', NULL, 0),
(42, 14, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:29', NULL, 0),
(43, 13, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:34', NULL, 0),
(44, 12, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:39', NULL, 0),
(45, 11, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:42', NULL, 0),
(46, 10, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:46', NULL, 0),
(47, 9, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:50', NULL, 0),
(48, 8, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:49:55', NULL, 0),
(49, 7, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:00', NULL, 0),
(50, 6, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:06', NULL, 0),
(51, 5, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:10', NULL, 0),
(52, 4, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:14', NULL, 0),
(53, 3, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:18', NULL, 0),
(54, 2, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:21', NULL, 0),
(55, 1, 51, 'Abdul Rafay Atiq 124', 'just.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-06 08:50:25', NULL, 1),
(56, 26, 51, 'Abdul Rafay Atiq 124', 'just1.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-07 11:41:07', NULL, 0),
(57, 27, 51, 'Abdul Rafay Atiq 124', 'just1.03@gmail.com', 11, 'Arrange birthday cakes and ballons', '2004-06-27', '2004-06-28', '14:00:00', '15:00:00', 0, '2023-12-07 11:41:19', NULL, 0);

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
  `location_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`id`, `thumbnail`, `other_images`, `video_showcase`, `address`, `rate`, `fixed_price`, `details`, `facilities`, `description`, `event_type`, `vendor_id`, `services`, `latitude`, `longitude`, `location_name`) VALUES
(1, '18fabf02-221b-401c-90a6-dc5d012b73ab.png', '[\"9b056398-ec4a-4522-8dce-0b6e4ee650da.png\", \"db1c10fd-e7b9-466a-a5af-0112824c36c6.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"06ad8829-280d-43b6-9483-1a097ad48e33.png\"]', 'description', 'Birthday', 10, NULL, 24.929, 67.0971, 'Delizia'),
(2, 'b0af4b12-aa95-4218-a9a5-13d36579180b.png', '[\"69166b02-97f6-411b-b6f2-bd4e57b520c6.png\", \"cd836160-67b0-4813-beac-b5009264a378.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"4007c72c-be69-4fc9-b41f-6f3882a463f2.png\"]', 'description', 'wedding', 10, NULL, 24.9289, 67.097, 'Pieinthesky'),
(3, '629ff76a-073d-45a0-92ff-87610a85cb4e.png', '[\"30efaa63-18fc-4bba-b8a2-41cfe88ccb96.png\", \"53f520a1-e644-42d7-824f-79d1074820df.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"3ed2dadc-3829-4f11-86e6-3a41b495e70f.png\"]', 'Birthday', 'birthday', 10, NULL, 24.9288, 67.0969, 'Kaybees'),
(4, '5b49050f-167f-4218-a1f6-6d88580549ec.png', '[\"5214eb22-c75a-42fd-af1a-ed39694fc7b5.png\", \"5b57d947-c14d-486d-8ecd-444715395d3b.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"0b0ae605-cdff-4c74-85de-0635975db9cf.png\"]', 'Birthday', 'Wedding', 10, NULL, 24.9287, 67.0968, 'Kababjees'),
(5, '749e744c-6b1b-4415-9c8c-a0d4a3c8dcd7.png', '[\"009ffe35-818c-4ef3-8c1c-22877797d546.png\", \"1091ac8c-414a-4973-bc50-10357985cc1b.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 1000, 1, 'details', '[\"decf26e4-bfa3-4fc4-8c36-c7de3855677b.png\"]', 'Birthday', 'Wedding', 10, NULL, 24.9286, 67.0967, 'The Bakers'),
(6, '45a3259a-6963-488a-9164-23d294c3af28.png', '[\"b05fbba7-d0d7-4a5b-8b9f-e87092493880.png\", \"b8f23972-4a41-45e5-ad0f-927464abd858.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"1b643bb6-3537-4d5c-b220-d1480c1fcca1.png\"]', 'Meeting', 'Wedding', 10, NULL, 24.9285, 67.0966, 'Delicacy'),
(7, '7a9d4ecf-6861-4ba4-aa04-594c365e9665.png', '[\"4ff2ae06-a1f9-4912-94f8-6ea073961e0f.png\", \"3858aea0-ae4f-48bd-b5d0-a030fa8e5d29.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 1000, 1, 'details', '[\"7cd2599c-0ad7-4bc7-be80-572c602e02a4.png\"]', 'Birthday', 'Wedding', 10, NULL, 24.9284, 67.0965, 'Delizia'),
(8, '7a8ec041-ec14-4885-aee3-7ec282b4f09a.png', '[\"ce7ece10-aa97-418e-b999-0c92ce5f15e0.png\", \"a83681a6-3d58-46a1-8e2e-bd8b11f78b05.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"0b2957d2-fa5d-452e-b022-15b6f216f0b1.png\"]', 'Birthday', 'Wedding', 10, NULL, 24.9283, 67.0964, 'Pieinthesky'),
(9, 'ba0f8d0a-bded-429b-8b7b-240bf8bd2c9c.png', '[\"fa3ce8ff-93d6-479c-a8de-64fe2b77928e.png\", \"cb45790d-b17e-40fe-93d9-bfe2daf79759.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"9100c354-957b-43c7-8a16-9fd249b40b69.png\"]', 'Birthday', 'Wedding', 10, NULL, 24.9282, 67.0963, 'The Bakers'),
(10, '20b49afa-f623-4a96-af57-587a42ab7aeb.png', '[\"e2eb7bc0-4336-4546-a2b3-644133263bb3.png\", \"4ae0480a-7b73-49cb-836e-d4cc743357ae.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"9197f633-784b-41e3-b75d-51cfea8e2678.png\"]', 'Birthday', 'Wedding', 10, NULL, 24.9281, 67.0962, 'Delicacy'),
(11, '1ec67c4f-248c-44e6-9c3c-383e639bbf14.png', '[\"c08d3a06-3be1-4c16-862a-d2025c303098.png\", \"7fa9945c-a061-481b-a648-c6f1d9538223.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"a6315cab-15a6-4037-865d-48f3bc01ce91.png\"]', 'Birthday', 'Wedding', 10, NULL, 24.928, 67.0961, 'Kababjees'),
(12, 'd9613205-0dfc-4b33-afa1-99685d5d632f.png', '[\"d05367b8-0fb1-45af-87f1-84e3f4f55055.png\", \"bf2859fe-d4b3-45b6-b499-cd38f3a2696b.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"85d61838-c292-47e2-9f09-186bbc263a20.png\"]', 'Birthday', 'office meeting', 10, NULL, 24.9279, 67.096, 'The sweets'),
(13, 'dba59259-f5eb-4ac2-9065-064dfd2b7b00.png', '[\"e04f0374-5263-4e79-be9f-38e66ed6d258.png\", \"b0b83840-172e-4929-a5aa-cae2e82b8e81.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"bfee9161-7a20-4044-910e-78cb002ace5e.png\"]', 'Birthday', 'Wedding', 6, NULL, 24.9278, 67.0959, 'KFC'),
(14, 'cc6245d4-ad5c-4705-bcdd-403e8a5c12e2.png', '[\"d371dc37-3c08-43f3-867b-8af51879ff14.png\", \"d17d4d39-d24c-47ad-b8fb-f339ee9b2277.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"cf0c295a-9444-4f51-a8a4-4087d4f4c9e4.png\"]', 'Testing Birthday', 'Test Wedding', 11, NULL, 24.9277, 67.0958, 'Mc Donald'),
(15, 'a1869d44-adbd-46fa-ba9a-4377a21c8f28.png', '[\"e055ac08-98dc-42bc-af7b-ea06d47cab1f.png\", \"f4e2e5ce-9655-4026-9ba5-9b253c3b13c0.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"2bd0ebe3-9532-4078-a195-9e35b06f47a5.png\"]', 'Testing Birthday', 'Test Wedding', 11, NULL, 24.9276, 67.0957, 'Delizia'),
(16, '6416f843-cecf-4928-a582-edd0d89734ba.png', '[\"596984ea-94c5-41ab-bb49-47f65f620e9e.png\", \"9dfd7d0b-0720-47ef-aefc-c7512b4e6294.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"0e4fbc35-34c1-4122-a2f2-2a7f474b288a.png\"]', 'Testing Birthday', 'Test Wedding', 11, 'bn das', 24.9275, 67.0956, 'Kababjees'),
(17, '4a91a0bc-8215-4418-a185-0201bcde6f88.png', '[\"e857f928-257a-4919-ace8-a31171a7a35d.png\", \"b468da9b-e5aa-4dd2-ac50-15be0d534083.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"4cde4a15-9d54-447a-880a-c3578f9d478d.png\"]', 'Testing Birthday', 'Test Wedding', 11, 'serepuveicew', 24.9274, 67.0955, 'KFC'),
(18, 'a4ee942e-fb7e-4862-a36d-06d550d05ad3.png', '[\"2cd0cc40-c86b-40d7-957a-e9687be0556e.png\", \"bd9c0f25-aa41-4aeb-951c-eac506280ae5.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"957c2666-81ba-4ca8-8954-e2261e1e3dc0.png\"]', 'Testing Birthday', 'Test Wedding', 11, 'servicenas', 24.9273, 67.0955, 'Broadway Pizza'),
(19, '92393fa7-5f78-4f00-80c3-5c5b5a6f8f0a.png', '[\"066142a0-27a6-4bd4-a2ab-49c8fe821e29.png\", \"9fae2664-b447-484b-b801-679e57b89654.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"7194f8ba-7ca4-45f5-9c3b-9b7d255556eb.png\"]', 'Testing Birthday', 'Test Wedding', 11, 'n fafhbfkd', 24.9272, 66.954, 'Pizzeria'),
(20, '28df872a-7ef8-498a-8d49-a9d9260c7d36.png', '[\"29f33dd7-e16b-4440-986f-6e42c295bf61.png\", \"ba6297f9-de35-493e-858c-30fade31b458.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"1ae10cb7-e473-4fbb-9e3c-77b54eea7c68.png\"]', 'Testing Birthday', 'Test Wedding', 11, 'nas f sdk', 24.9271, 67.0953, 'Burger o  clock'),
(21, 'f1e0a15b-bc89-4258-b36a-f92b5d2c73cf.png', '[\"fa4b5430-af8d-4fc8-b0bc-a2832c3abc49.png\", \"1e52ab04-bdcc-49b4-9b6d-cbaa66345759.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"6b2b535c-1c3c-4630-a039-24e4ce9f9c6a.png\"]', 'Testing Birthday', 'Test Birthday', 11, 'nsjidfb', 24.927, 67.0952, 'Subway'),
(22, 'bafa61f0-4dcd-4d73-96dd-19f92e9b13a8.png', '[\"dc8a689e-4cf4-4c08-9a72-c8d1d3bd42db.png\", \"7696a7dc-798d-48c1-aec5-4acffc038cce.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"5c803a90-c387-487b-8d37-f3b81560858d.png\"]', 'Testing Birthday', 'Birthday', 11, 'Wow !!', 24.9268, 67.095, 'Delizia'),
(26, 'd7d929e3-48c8-42f6-895c-86f971f9a5e4.png', '[\"92487783-1796-47cd-9a1d-007521fff100.png\", \"1887b593-4d46-4a58-b6f1-454b430c2729.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"30385e1c-c3fb-4b91-8097-1b72f02f0834.png\"]', 'Birthday', 'Wedding', 6, 'A class service', 24.9266, 67.0949, 'Pieinthesky'),
(27, '4db7cc10-36e5-4b89-b9e4-d1b19c7b3648.png', '[\"7f4ee5ba-534f-4a8e-815a-55973d41fe79.png\", \"9061c89e-7031-4340-bf22-f66f9f5a57e1.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"2d82d838-acbd-43f0-9874-3a69a209a6ca.png\"]', 'Birthday', 'Test Birthday', 6, 'A class service', 24, 67, 'Burger o  clock'),
(28, '54a2033b-f307-4028-8fa6-a6edea487f73.png', '[\"eafdd5ad-31e6-44d7-9399-92e764e8a403.png\", \"cd731e9c-8ca7-4cb8-b634-f41010666c01.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"4cd0f039-cb39-4042-8b2a-cd722ea54950.png\"]', 'Birthday', 'Birthday', 6, 'A class service', 24.6, 64.1, 'Delizia'),
(31, '57258934-a0f0-4ded-94fe-db0abc7f2639.png', '[\"58697109-9ab4-469e-b687-5d379dadf748.png\", \"0cfe7348-1720-4348-a4e0-65e835a5ea4c.png\"]', 'Video ssjdnfsdjknsdgjkjsdnetails', 'Vendor Address', 100, 1, 'details', '[\"4eb19179-aa37-4416-b174-8e3daf6ce66f.png\"]', 'Birthday', 'Testing Birthday', 15, 'A class service', 24.6, 64.1, 'Kababjees Bakers'),
(35, 'd9aa7422-40f6-4f09-8da4-f188679e98b9.png', '[\"61f70f88-1019-4f78-9325-8c5d0510944c.png\", \"a66d1336-ed79-46bc-b7d9-7f73d51d7fd9.png\"]', 'base64_encoded_video', 'Sample Address', 100, 1, 'Event details...', '[\"4ce57aaf-183c-4e00-993c-bd30f839815d.png\"]', 'Event description...', 'Birthday', 15, 'A class service', 123.456, 78.9, 'Tassaract');

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
(4, 8, 1, 50, 1, 3, 1, 1, 'The event was very boring', 5),
(5, 9, 1, 50, 1, 3, 1, 1, 'The event was very boring', 4.9),
(9, 12, 1, 50, 1, 3, 1, 1, 'The event was very boring', 5),
(10, 13, 2, 50, 1.5, 3, 1.5, 4.5, 'The event was very boring', 5),
(11, 14, 3, 50, 2.5, 3.5, 1.5, 4.5, 'The event was very boring', 5),
(12, 15, 4, 50, 2.5, 1.5, 1.5, 4.5, 'The event was very boring', 5),
(13, 16, 5, 50, 4.5, 1.5, 1.5, 4.5, 'The event was very boring', 4.9),
(14, 17, 6, 50, 5, 5, 5, 5, 'The event was very boring', 5),
(15, 18, 7, 50, 5, 5, 5, 4.5, 'The event was very boring', 5),
(16, 19, 8, 50, 5, 5, 5, 0, 'The event was very boring', 5),
(17, 20, 9, 50, 5, 5, 5, 0, 'The event was very boring', 5),
(18, 21, 10, 50, 5, 5, 5, 0, 'The event was very boring', 5),
(19, 22, 11, 50, 5, 5, 5, 0.5, 'The event was very boring', 5),
(20, 35, 21, 51, 5, 5, 5, 0.5, 'The event was very boring', 5),
(21, 36, 20, 51, 0.5, 5, 5, 0.5, 'The event was very boring', 5),
(22, 37, 19, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(23, 38, 18, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(24, 39, 17, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(25, 40, 16, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(26, 41, 15, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(27, 42, 14, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
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
(39, 54, 2, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(40, 55, 1, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(41, 56, 26, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5),
(42, 57, 27, 51, 0.5, 4.5, 5, 0.5, 'The event was very boring', 5);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `access_token` text DEFAULT NULL,
  `role` varchar(50) NOT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  `vendor_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `email`, `password_hash`, `access_token`, `role`, `profile_image`, `vendor_id`) VALUES
(1, 'itsabdulrafay@gmail.com', '$2b$12$yhZ6bsGJW5rr3oi2fWlSPesvMRPkaUXbf8JUS1D2fUa1mibWn2.EK', NULL, 'user', NULL, NULL),
(3, 'abdulrafayatiq1.03@gmail.com', '$2b$12$kKmu2/LrmF8LZoB9gpYqN.klByrmSa8ZpjypZiQc3v2djWWtRo/3W', NULL, 'user', NULL, NULL),
(4, 'abdulrafayatiq12.03@gmail.com', '$2b$12$56QCfrAJ9guP2xsBbYbNcec2./sfLSeYToBKXLPa34AVoGTJyMOUm', NULL, 'user', NULL, NULL),
(5, 'abdulrafaya213tiq12.03@gmail.com', '$2b$12$mspOXUAz9rESOe5b2WnDeONnJ0FEWq0b1sDyEjjubnm7ERO2jtwVy', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjYwNzUxOSwianRpIjoiY2Q0NzAzMDEtMDNlYy00OGJjLWFlY2MtMGJjYzc0YjhmYzE5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhMjEzdGlxMTIuMDNAZ21haWwuY29tIiwibmJmIjoxNjk2NjA3NTE5LCJleHAiOjE2OTY2MD', 'user', NULL, NULL),
(6, 'mrrafayatiq.03@gmail.com', '$2b$12$Z7.4zmA.NDIZRj65j5mi/.k/f5WuNXukOyBCzv1AGhIguQ2gPsgkW', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjkyMTAxMSwianRpIjoiYWYyNTMzZGQtNDY3MS00MmU2LTg0MmItZjRjM2NiNGRhZTJkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im1ycmFmYXlhdGlxLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTY5NjkyMTAxMSwiZXhwIjoxNjk2OTIxOTExfQ.o25', 'vendor', NULL, NULL),
(8, 'vendor@example.com', '$2b$12$/pH1pXZnAI8D0RP0jwfDr.aTk0MZ0HsI4TqSc6bSNszXhMMvS2l5m', NULL, 'vendor', NULL, NULL),
(9, 'rafayvendor@example.com', '$2b$12$d986ivB7fjQ2oGcQV8Zb8eyK2OPA9FbeWgm71p4Ondv1lq/KQA2C6', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjkzMTMyMCwianRpIjoiYjE1OTY2YjEtMTA2Mi00NjgyLThjYTUtMzRjYjVlYWM3MDA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5dmVuZG9yQGV4YW1wbGUuY29tIiwibmJmIjoxNjk2OTMxMzIwLCJleHAiOjE2OTY5MzIyMjB9.d1ys1', 'vendor', NULL, NULL),
(10, 'rafayvendor2003@example.com', '$2b$12$gXLEBmv8lU3hMhPsEEkj2ekkw8zihjgB15UkUnWT57p3gTcoipiai', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjkzNjg5MywianRpIjoiOTZhNzAxMWMtMGNlMS00ZDBlLWJkOTgtNTc3ZGIxZjc0ODA1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5dmVuZG9yMjAwM0BleGFtcGxlLmNvbSIsIm5iZiI6MTY5NjkzNjg5MywiZXhwIjoxNjk2OTM3NzkzfQ', 'vendor', NULL, NULL),
(11, 'rafayvendor20003@example.com', '$2b$12$K.QXAC8imIVcq1sBWYVV7OGkY64PXHx2pZCTlak/Qsbh/fkjrVMBm', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NjkzNzk5NywianRpIjoiZmZmZDhkYzAtZmQ4Mi00ZDBhLWJhZTYtNzZlYTAyOTkwZGUwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5dmVuZG9yMjAwMDNAZXhhbXBsZS5jb20iLCJuYmYiOjE2OTY5Mzc5OTcsImV4cCI6MTY5NjkzODg5N3', 'vendor', NULL, NULL),
(12, 'rafayvendor200003@example.com', '$2b$12$bk4TbuTHLo2OGI2iLE1/dOSpSloYrCJejcfP8cSOgXEu35JMODyNK', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5Njk0MjMzOSwianRpIjoiMGNmMWQzN2ItM2ExMS00M2FlLTlhYmEtNmQ5YTlmZjNkNmUyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5dmVuZG9yMjAwMDAzQGV4YW1wbGUuY29tIiwibmJmIjoxNjk2OTQyMzM5LCJleHAiOjE2OTY5NDMyMz', 'vendor', '?PNG\n\Z\n\0\0\0\nIHDR\0\0\0?\0\0\0\0\0tb?=\0\0APLTE?????\0?EB!)???y??\0??\0\0????\0/\0\0\0??\0??1\0\0?\0r\0?-+\0\0\0?3\'\0\0,\0\0???3\0\0????\0k??\0?9<\0\0\0\09\0?\0o?\0??????????????????:\0?????????7\0?xq??y????????K????ˠ???{jb?????WfQF???p]T?????~#\0\0?????????M?o\\?z??????\0\0{??U9*????????', NULL),
(13, 'rafayvendor1@gmail.com', '$2b$12$7oXDBIZ/Uj8pO9bm0KYXN.5Lcw839mKMNFcIOXHlotHpmpaO.K/nK', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NzQ0OTQ3NywianRpIjoiMDEwMGE2NjgtM2UxYS00NzgwLWI5YjktNDg1N2RjNjZlZDM4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5dmVuZG9yMUBnbWFpbC5jb20iLCJuYmYiOjE2OTc0NDk0NzcsImV4cCI6MTY5NzQ1MDM3N30.OILBxx', 'vendor', NULL, NULL),
(15, 'abdulrafayatiq123123123.03@gmail.com', '$2b$12$NbddmYJCvaZZSIFJ38vFYO6LEnOoyUEfS8tKDNLai7mqxhDVS3tVO', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODA1Njc3MCwianRpIjoiMTg5ZWY1YWEtOGFmOS00YjVhLTg4NDEtMDc4YjVhYWZiMzIwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxMTIzMTIzMTIzLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTY5ODA1Njc3MCwiZXhwIjoxNj', 'vendor', NULL, NULL),
(16, 'abdulrafayatiq12312312345.03@gmail.com', '$2b$12$IgUD6KVbmczhEleCF4KNK.2nnQnrJ.h5zcj8FIOjQVRBLyWWLY0O6', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODA1ODE3MywianRpIjoiYWZjMWY4YjctMjE5Yi00YWQwLWExNmItZTIyY2U1NzJjYWU5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxMTIzMTIzMTIzNDUuMDNAZ21haWwuY29tIiwibmJmIjoxNjk4MDU4MTczLCJleHAiOj', 'vendor', NULL, NULL),
(17, 'abdulrafayatiq1a.03@gmail.com', '$2b$12$CUGwmKX6WNtRlmWVOL6FPuK5ExkkvYlbxlzcWhjMas0KP1k9W/qTy', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODA2Mzg2OCwianRpIjoiNDMxMWFiMDQtNThjMC00ODhkLWE4MzYtN2FjNWJiODAxYTc1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxMWEuMDNAZ21haWwuY29tIiwibmJmIjoxNjk4MDYzODY4LCJleHAiOjE2OTgwNjQ3Nj', 'vendor', NULL, NULL),
(18, 'abdulrafayatiq11a.03@gmail.com', '$2b$12$zR80Qz5RO.211daR6hkPZeGQrh3TbK8a3i488q/pSYwar3OQN47ve', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODA2NDU3OCwianRpIjoiY2ZkNWNiMmYtZTA1MS00ZWFiLWI3NTktNDk5MWFmMmNkY2ZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxMTFhLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTY5ODA2NDU3OCwiZXhwIjoxNjk4MDY1ND', 'vendor', '33df98c4-34ec-414a-b3c3-689cc0c7fd01.png', NULL),
(21, 'justrafay@gmail.com', '$2b$12$Qr5i/UxRLakF3ynvr69AE.tNBku/c9tXi0iV.cWq9DZR91q1glEKW', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODE0MDkzNCwianRpIjoiNmRmMjY0YjQtMzU4Yy00NjQ5LWEyN2ItMjMyZWQzYzBiZTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RyYWZheUBnbWFpbC5jb20iLCJuYmYiOjE2OTgxNDA5MzQsImV4cCI6MTY5ODE0MTgzNH0.RvPaPMpPX1', 'vendor', NULL, NULL),
(22, 'justrafay1@gmail.com', '$2b$12$c5G1F52/34UzZIlJY7gHR.1v46kdvpwHSL/q2E2r/erX5ifI4ZJlu', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODE0MTUwNiwianRpIjoiMDk1NmI3ZDEtYWYwOS00NDJiLTkxNGUtMTU0ODQzOTMxZGRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RyYWZheTFAZ21haWwuY29tIiwibmJmIjoxNjk4MTQxNTA2LCJleHAiOjE2OTgxNDI0MDZ9.MPGvkuyl2', 'vendor', NULL, NULL),
(33, 'justrafay5@gmail.com', '$2b$12$oUuFZYigfJDaHmTP0zUgH.oxtN9OHh9M8hCECYlxxcdA.VPN.iy1S', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMjI5MDkxMCwianRpIjoiOWU4ZWMyOTItZTVjMy00ZjM1LWE0NjAtYTllY2NhOTA2MzE5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RyYWZheTVAZ21haWwuY29tIiwibmJmIjoxNzAyMjkwOTEwLCJleHAiOjE3MDIyOTE4MTB9.MHj2bJRFEnlthNPiWhkBvaC_sCr6Vex5Sg1vszDQlEc', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 6),
(34, 'justitsmerafay@gmail.com', '$2b$12$w0uEFtfx8I0uCUDP1hJqiOa8sZ3fwwahd92Tw3/lABqhHftqPnH2C', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODIyMTMyMywianRpIjoiZDQ2YWJkNjYtZmRkMy00ZDE3LTgzMjMtNWRlMThlNzIwZjQ5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RpdHNtZXJhZmF5QGdtYWlsLmNvbSIsIm5iZiI6MTY5ODIyMTMyMywiZXhwIjoxNjk4MjIyMjIzfQ.bGw', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 7),
(35, 'justitsmerafay1@gmail.com', '$2b$12$9G/q3dDs2WUpl9VicjSQFesOnx6jdCcfjG2FLYkDi8an6na4iHA2y', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODIyMjMzNywianRpIjoiZDM4ZmE2OWYtYWMzNS00ZjI1LTg2NTgtYTg1ZmNhYjZjMzZhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RpdHNtZXJhZmF5MUBnbWFpbC5jb20iLCJuYmYiOjE2OTgyMjIzMzcsImV4cCI6MTY5ODIyMzIzN30.7V', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 8),
(36, 'justitsmerafay2@gmail.com', '$2b$12$vJq3CG84rq55kHem5MBaqev6l2SX24iEN6jGnkh.LsVbuMgz6DRK2', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODIyMzI2OCwianRpIjoiZDBlZjE0ZTEtN2Y3Yy00MjcyLWIwM2EtNGE3YWJjZWZhMDEyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RpdHNtZXJhZmF5MkBnbWFpbC5jb20iLCJuYmYiOjE2OTgyMjMyNjgsImV4cCI6MTY5ODIyNDE2OH0.IV', 'vendor', NULL, NULL),
(37, 'justitsmerafay3@gmail.com', '$2b$12$l5dHdXSRo7sD8kJ5tySrjuwllqF4vCN9.gW2VWPmh8mpR64VdnjU6', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODIyNjg5MCwianRpIjoiZjYzYzE2Y2QtNzNjMy00MmFhLThkODItYTdlYjgzOTk4NjhmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3RpdHNtZXJhZmF5M0BnbWFpbC5jb20iLCJuYmYiOjE2OTgyMjY4OTAsImV4cCI6MTY5ODIyNzc5MH0.7I', 'vendor', NULL, NULL),
(38, 'rafay@gmail.com', '$2b$12$1iKVhkbemNVTtLhw/xM5UObQ5nP0NQ/AyTWyUa.4mUUe8QIH/KBk.', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODIyNzc0NiwianRpIjoiZTViZjFhOWQtOTBjNy00ZDg2LTg5NGMtN2EwYmUxNmI4MWJiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5QGdtYWlsLmNvbSIsIm5iZiI6MTY5ODIyNzc0NiwiZXhwIjoxNjk4MjI4NjQ2fQ._ZmJ7Vlc9EWmo_V', 'vendor', NULL, NULL),
(39, 'rafay03@gmail.com', '$2b$12$Ibo6K6mDRs6n8UrDGEF9GuhYQEx9HHq9s5fpb7MEB8DiAhZUQiXwG', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODIyNzg3NiwianRpIjoiN2Q5ZDZjYTQtNzM2Mi00MTcxLTlkZTUtMDkxYjY0YmZhYTMwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJhZmF5MDNAZ21haWwuY29tIiwibmJmIjoxNjk4MjI3ODc2LCJleHAiOjE2OTgyMjg3NzZ9.NivPo2qUBZRg3', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', NULL),
(40, 'abdulrafayat1a.03@gmail.com', '$2b$12$uoaxmBKCQ0mL2dSRsIefhuiv6Kk3XuXS2H5WLwjRbVlu6pBr60wQa', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODI0MDE5MiwianRpIjoiZDNmM2M0OTAtMmUxYy00YmJkLWI4YTgtMWQzMDczNjQ5YzNhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdDFhLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTY5ODI0MDE5MiwiZXhwIjoxNjk4MjQxMDkyfQ', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 9),
(41, 'abdulrafayat1aa.03@gmail.com', '$2b$12$eYfno2gsa4aiRcT9qvZjt.rUrXvDSuYd9uFvrTmhqHV/dvvBdx.9u', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODI0MTUyOCwianRpIjoiODhlYmI0YmUtM2NmZS00OGZhLWFlZjMtYmU1OTcyZjhjM2I2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdDFhYS4wM0BnbWFpbC5jb20iLCJuYmYiOjE2OTgyNDE1MjgsImV4cCI6MTY5ODI0MjQyOH', 'vendor', NULL, NULL),
(42, 'abdulrafayataaaaaaaaa.03@gmail.com', '$2b$12$xBxr1gbilc94UFcYla7Kgu3j41UTtGzF846DR9/uqbm/n8lpMD2MC', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5ODQwNTkzNCwianRpIjoiMjE3YzliMmYtMGZhOC00YzM1LWI0YTAtZGQxNzVkYmUxZjNhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGFhYWFhYWFhYS4wM0BnbWFpbC5jb20iLCJuYmYiOjE2OTg0MDU5MzQsImV4cCI6MTY5OD', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 10),
(43, 'pythondeveloper@gmail.com', '$2b$12$CaV7ORxnVaY.T3sp/jWM0.eIFKOSzsLy4HEe6dSy3STs0UuozjMGW', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTM1MzkxMywianRpIjoiMWNiNDJjZTgtZDllNi00Mzg4LTkxYmYtODY1ODAxN2FlYjkyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InB5dGhvbmRldmVsb3BlckBnbWFpbC5jb20iLCJuYmYiOjE2OTkzNTM5MTMsImV4cCI6MTY5OTM1NDgxM30.jO', 'user', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', NULL),
(44, 'heyrafay@gmail.com', '$2b$12$sp3oNuyjnZhhQgRJQv8zmOZT1/M7kmmjKdNHzDaeaBbSozJcpejCy', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTI2NjI2MiwianRpIjoiMjE2MTE3N2QtMTlkNi00YmFiLTkyODYtYTNmMjVlNWUyYWEwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImhleXJhZmF5QGdtYWlsLmNvbSIsIm5iZiI6MTY5OTI2NjI2MiwiZXhwIjoxNjk5MjY3MTYyfQ.zibNFm2nigG', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', NULL),
(45, 'testing@example.com', '$2b$12$O7e0.hh0Ls/I7E3uHDebpuCvRcPYvpz029dNvpWthBbUICmD.z4Nm', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTQzODI5NSwianRpIjoiZmY1YmU3YmYtMWM4Mi00NjQyLTlmNmItODUwOTU1MjEwMmE3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3RpbmdAZXhhbXBsZS5jb20iLCJuYmYiOjE2OTk0MzgyOTUsImV4cCI6MTY5OTQzOTE5NX0.s4zr6ufXyE', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 11),
(46, 'abdulrafayatiq.03@example.com', '$2b$12$Pck7CLu3cfqii/FpnECcvO8aeu9EGFFMntW9ft.J4NZ7WOprR6HAC', NULL, 'vendor', NULL, NULL),
(48, 'abdulrafayatiq.03@gmail.com', '$2b$12$Jg9mGzEYi6FI8eiBRDt18u8pBZ3ZG8AJSrSYl307SBRI9bJCFAv02', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMTY5NTMzMSwianRpIjoiZjlmYTI3OWItNjIxMy00Y2U5LTlhMTYtZmRjYWU5ODFiYjMwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTcwMTY5NTMzMSwiZXhwIjoxNzAxNjk2MjMxfQ', 'user', NULL, NULL),
(49, 'abdulrafayatiqvendor.03@gmail.com', '$2b$12$K42Loxqxmdc.V/yM01a07eqkFAexDOAtRG6Wvfk8UKohNICRSQqhO', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMTY5NTA0OCwianRpIjoiODdhMTFiODctNzRhMS00ZmJhLWE0ZjMtYWE4NGE3NzQ1NWE5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxdmVuZG9yLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTcwMTY5NTA0OCwiZXhwIjoxNzAxNj', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 13),
(50, 'just.03@gmail.com', '$2b$12$a78hShATy819L7uX3QO2s.By24/3b2Ymp9hA22QZ1EyODuBVSO/Km', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMTg1MTkwMywianRpIjoiMDY3ZmE0MjMtYWIxOS00ODZiLTgwYTktZTU1NjJmYjQzOTJiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3QuMDNAZ21haWwuY29tIiwibmJmIjoxNzAxODUxOTAzLCJleHAiOjE3MDE4NTI4MDN9.NTRvqStH8RdPp', 'user', NULL, NULL),
(51, 'just1.03@gmail.com', '$2b$12$EDnoqZf1WGd/jhS2N0W6MeRt.G7RAImatJy8iXTemL6vwJGGlPlX2', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMjI5OTc1NiwianRpIjoiMGU5MDRmZTEtZDNkZC00ZWQxLTlhMjktN2NkYWQ3ZGEwOTc0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3QxLjAzQGdtYWlsLmNvbSIsIm5iZiI6MTcwMjI5OTc1NiwiZXhwIjoxNzAyMzAwNjU2fQ.XFGtid9-Nw9PUSpvREcwj0SUdl3um7zisZMIpRwGQz4', 'user', NULL, NULL),
(52, 'abdulrafayatiq@gmail.com.com', '$2b$12$6tmvlYLzyYiZtllws6mCwOHOK/gS3p1xkzyNWA1ZHDHKMJrwtUXBK', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMTk0ODc1MywianRpIjoiZDY1ZjQxY2UtMzgyZS00NDZjLWJmZDYtYTE0OTk0ZWMxZDhiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFiZHVscmFmYXlhdGlxQGdtYWlsLmNvbS5jb20iLCJuYmYiOjE3MDE5NDg3NTMsImV4cCI6MTcwMTk0OTY1M30.JZUjefQ0wz_uGzbZMISF8DV6a6huWpCi8UHZ0kXi6hQ', 'vendor', 'ab7ebf3d-c31f-4e69-aff2-f126a22a8578.png', 14),
(53, 'justvendor.03@gmail.com', '$2b$12$45f9pZi8ic2dUAErRFN5CuLXd1AEuUkPhgr8f3K6zn6VUZ9aJqhaO', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwMjI5NDE0NywianRpIjoiMDAzMjNhYjMtYzUyZi00NDhhLThjMjQtYzgzMjRiOTM0ZmJiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Imp1c3R2ZW5kb3IuMDNAZ21haWwuY29tIiwibmJmIjoxNzAyMjk0MTQ3LCJleHAiOjE3MDIyOTUwNDd9.eWwWWBMWVTySpaHCf-1TYEp_yBepC8UKEOEipdrF8hQ', 'vendor', NULL, 15);

-- --------------------------------------------------------

--
-- Table structure for table `vendor`
--

CREATE TABLE `vendor` (
  `id` int(11) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `phone_number` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `biography` varchar(1024) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vendor`
--

INSERT INTO `vendor` (`id`, `full_name`, `phone_number`, `location`, `biography`) VALUES
(6, 'Abdul Rafay Atiq', '090078601', 'Karachi', 'Luxury Wedding Celebration Venue'),
(7, 'Just Itsmerafay', '123-456-7890', 'City, Country', 'I am a talented vendor.'),
(8, 'Just Itsmerafay', '123-456-7890', 'City, Country', 'I am a talented vendor.'),
(9, 'djkgnsdkglsd Doe', '123-456-7890', 'Some Location', 'A short biography about the vendor'),
(10, 'Abdul Rafay Atiq 123', '090078601', 'Karachi', 'Luxury Wedding Celebration Venue 1'),
(11, 'NO testing', '0823572347059237', 'London', 'Testing Biography 12312312312'),
(13, 'Rafay The Vendor', '0900833922', 'Karachi', 'Just a common man'),
(14, '', '', '', ''),
(15, 'Just Vendor', '1234567890', 'NY, Newyork', 'Just a simple vendor.');

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
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vendor_id` (`vendor_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `password_reset_token`
--
ALTER TABLE `password_reset_token`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `review`
--
ALTER TABLE `review`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;

--
-- AUTO_INCREMENT for table `vendor`
--
ALTER TABLE `vendor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`),
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `event`
--
ALTER TABLE `event`
  ADD CONSTRAINT `event_ibfk_1` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`id`);

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
