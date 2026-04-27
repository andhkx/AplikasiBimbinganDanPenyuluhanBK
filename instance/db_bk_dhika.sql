-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 21 Apr 2026 pada 09.59
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_bk_dhika`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `admin_dhika`
--

CREATE TABLE `admin_dhika` (
  `id_admin` int(11) NOT NULL,
  `akun_id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `no_hp` varchar(20) DEFAULT NULL,
  `foto_profil` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `admin_dhika`
--

INSERT INTO `admin_dhika` (`id_admin`, `akun_id`, `nama`, `email`, `no_hp`, `foto_profil`) VALUES
(1, 9, 'Admin', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `akun_dhika`
--

CREATE TABLE `akun_dhika` (
  `id_akun` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Siswa','Guru BK','Wali Kelas','Kesiswaan','Admin') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `status_akun` enum('Aktif','Pending','Nonaktif') DEFAULT 'Aktif'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `akun_dhika`
--

INSERT INTO `akun_dhika` (`id_akun`, `username`, `password`, `role`, `created_at`, `status_akun`) VALUES
(1, 'tini', 'scrypt:32768:8:1$HIJtdu9z8NmN17bP$ac2eb8566fe4dfe195de2fc4abb03a7e83fec151c80ca3ba0eda99c4b31a12602e177f9e39fe8389b37b81e58a25b8efb7d08e450a82ae0f2770d9bbac9d43ed', 'Guru BK', '2026-03-28 08:55:06', 'Aktif'),
(2, 'anom', 'scrypt:32768:8:1$Z7ODOm0wysSXrsUC$f632f9446e30eb30bf3d9b1d876507a1843c6b298014fa0b260b14f03066a659628930b13d1907aa6e942aea0f509bd51bedcd2773f5dec32a6b0908c8d3c704', 'Guru BK', '2026-03-28 08:55:06', 'Aktif'),
(3, 'dudu', 'scrypt:32768:8:1$qFqDQqBVjIzMsSD1$4b36d9d32f88a2cdd64486b3321d7fe172d59f0820209ef4e12c1e9d14db441ad584f3300d046970c2d94722b11ce1276c628e6df887ac0cef09792f8e6d3e0b', 'Guru BK', '2026-03-28 08:55:06', 'Aktif'),
(4, 'andhika', 'scrypt:32768:8:1$Y3VVczzuR9xA9b7s$94099e0e5d43ec2e9395170c69a732dcb78522636e7877ed22b6f9349b66fbd8005ae9ca582c33a0b91686857763f764a675ef299d53adf0c11966d8577828c3', 'Siswa', '2026-03-28 08:55:06', 'Aktif'),
(5, 'fika', 'scrypt:32768:8:1$8LukVurlyRW0Sgpj$5354f7f56be4bf909b8e1ec345242b7fd29996d867637577f518769d302d26463c1f2f21a358f56c1e201fabf56a8fbe3e82a7e8eb36f5b7a9da3cbf1fd3a1f3', 'Siswa', '2026-03-28 08:55:06', 'Aktif'),
(6, 'adit', 'scrypt:32768:8:1$smpqZ7Ru2SOe2oZ3$c5efc18cf3642c31e0c60290fba4ce2b16c52f018d99c01c40d7317d2de8a5fce6bd283ceee4f8667d3f61bda834b23b88b15de5ad2583e14622c9ab3594c86a', 'Siswa', '2026-04-07 05:03:57', 'Aktif'),
(7, 'ismita', 'scrypt:32768:8:1$ETBBEWXPH4Yr5qHG$1c979345ed1c30cd35227ca1bfef03d6bfd27791638ead54b4ca85a3b98fed4fbc75b61872c7a9427ca3b5c0dff64ffa749257fdb53302a6a0941a9b50ea133d', 'Kesiswaan', '2026-04-12 04:03:52', 'Aktif'),
(8, 'gigin', 'scrypt:32768:8:1$fOhiTtB3lCeKGyOn$8e93e167272cd6609f1c1c38796f7dba59b30199f40d03b52703b26fae9c8949d828d598b4512b98ea0d6dd6e9e6d755e9eff89482bba980acc7944b9c849059', 'Wali Kelas', '2026-04-12 04:03:52', 'Aktif'),
(9, 'admin', 'scrypt:32768:8:1$6ULxr6UA65AYNBOE$55c716400d969b0d2e4bf2390ae3f594a737c8f6fc49addfbb4bb341f8c766c60abad6b3b7cfe65e084dc5a82274f403356f8f3add10712a4a4641c0bd31edcd', 'Admin', '2026-04-12 04:04:16', 'Aktif'),
(10, 'haidar', 'scrypt:32768:8:1$LMkd36fdhMe1bXIT$c72c6e9c48b780d1f0d156e6c87249f3669b7f286eace7d52a24bc1d142a7ca5f7da4a896600eccebc40e7614093fa47eafc127e49d477d5008357d6742195c3', 'Siswa', '2026-04-21 03:25:02', 'Aktif');

-- --------------------------------------------------------

--
-- Struktur dari tabel `chat_dhika`
--

CREATE TABLE `chat_dhika` (
  `id_chat` int(11) NOT NULL,
  `pengirim_akun_id` int(11) NOT NULL,
  `penerima_akun_id` int(11) NOT NULL,
  `pesan` text NOT NULL,
  `waktu` timestamp NOT NULL DEFAULT current_timestamp(),
  `dibaca` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `chat_dhika`
--

INSERT INTO `chat_dhika` (`id_chat`, `pengirim_akun_id`, `penerima_akun_id`, `pesan`, `waktu`, `dibaca`) VALUES
(6, 4, 1, 'assalamualaikum ibu', '2026-03-29 14:38:49', 1),
(7, 4, 1, 'Halo, saya telah mengajukan konseling (Sosial) pada 2026-03-30 pukul 07:00-08:00. Mohon konfirmasinya. Terima kasih.', '2026-03-29 14:39:44', 1),
(8, 1, 4, 'oke nak', '2026-03-29 14:42:02', 1),
(9, 5, 2, 'terimakasih pak', '2026-03-29 15:15:24', 0),
(10, 2, 5, 'sama sama nak', '2026-03-29 15:16:38', 1),
(11, 4, 1, 'Halo, saya telah mengajukan konseling (Karir) pada 2026-03-30 pukul 11:00-12:00. Mohon konfirmasinya. Terima kasih.', '2026-03-30 01:21:19', 1),
(12, 4, 1, 'bu saya mau konseling', '2026-03-30 01:21:41', 1),
(13, 1, 4, 'selesai ya nak', '2026-03-30 01:24:07', 1),
(14, 4, 1, 'halo bu', '2026-03-30 01:25:53', 1),
(15, 4, 1, 'p', '2026-03-30 01:25:56', 1),
(16, 4, 1, 'Halo, saya telah mengajukan konseling (Belajar) pada 2026-04-05 pukul 08:06-09:06. Mohon konfirmasinya. Terima kasih.', '2026-04-05 01:06:35', 1),
(17, 4, 1, 'bu', '2026-04-07 05:06:22', 1),
(18, 4, 1, 'ko diatas ya', '2026-04-07 05:06:46', 1),
(19, 4, 1, 'assalamualaikum by', '2026-04-08 12:57:24', 1),
(20, 4, 1, 'bu', '2026-04-08 12:57:29', 1),
(21, 4, 1, 'Halo, saya telah mengajukan konseling (Pribadi) pada 2026-04-09 pukul 11:15-13:15. Mohon konfirmasinya.', '2026-04-09 04:15:52', 1),
(22, 1, 4, 'test', '2026-04-09 04:16:52', 1),
(23, 4, 1, 'halo Bu', '2026-04-09 23:53:19', 1),
(24, 4, 1, 'buu', '2026-04-12 04:07:00', 1),
(25, 1, 4, 'ya', '2026-04-12 09:47:05', 1),
(26, 8, 4, 'nak', '2026-04-12 11:12:43', 1),
(27, 4, 1, 'bu', '2026-04-12 11:34:36', 1),
(28, 7, 1, 'bu', '2026-04-12 11:36:24', 0),
(29, 4, 1, 'buuuuu', '2026-04-15 12:57:55', 1),
(30, 1, 4, 'hai', '2026-04-15 12:59:16', 1),
(31, 1, 4, 'oi', '2026-04-15 13:18:45', 1),
(32, 1, 4, 'nak', '2026-04-15 13:48:51', 1),
(33, 1, 4, 'jan begadang ya', '2026-04-15 13:49:12', 1),
(34, 4, 1, 'siap bu', '2026-04-15 13:49:55', 1),
(35, 5, 2, 'Halo, saya telah mengajukan konseling (Karir) pada 2026-04-21 pukul 15:00. Mohon konfirmasinya.', '2026-04-21 06:23:46', 0);

-- --------------------------------------------------------

--
-- Struktur dari tabel `guru_dhika`
--

CREATE TABLE `guru_dhika` (
  `id_guru` int(11) NOT NULL,
  `akun_id` int(11) NOT NULL,
  `nip` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `no_hp` varchar(20) DEFAULT NULL,
  `foto_profil` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `guru_dhika`
--

INSERT INTO `guru_dhika` (`id_guru`, `akun_id`, `nip`, `nama`, `email`, `no_hp`, `foto_profil`) VALUES
(1, 1, '197512302005012003', 'Tini Hermawati, S.Pd', 'tinihermawati@gmail.com', NULL, NULL),
(2, 2, '196805121994031002', 'Anom Jati Kusumo, S.Psi', 'anom@gmail.com', NULL, NULL),
(3, 3, '197908172006041005', 'Durahman, S.Psi', 'dudu@gmail.com', NULL, NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `kesiswaan_dhika`
--

CREATE TABLE `kesiswaan_dhika` (
  `id_kesiswaan` int(11) NOT NULL,
  `akun_id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `nip` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `no_hp` varchar(20) DEFAULT NULL,
  `foto_profil` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `kesiswaan_dhika`
--

INSERT INTO `kesiswaan_dhika` (`id_kesiswaan`, `akun_id`, `nama`, `nip`, `email`, `no_hp`, `foto_profil`) VALUES
(1, 7, 'Ismita Ratnasari, S.ST, M.M', '297328910101', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `konseling_dhika`
--

CREATE TABLE `konseling_dhika` (
  `id_konseling` varchar(20) NOT NULL,
  `siswa_id` int(11) NOT NULL,
  `guru_id` int(11) NOT NULL,
  `jenis` enum('Pribadi','Sosial','Belajar','Karir') NOT NULL,
  `tanggal` date NOT NULL,
  `jam_mulai` time NOT NULL,
  `jam_selesai` time DEFAULT NULL,
  `status` enum('Pending','Disetujui','Selesai','Dibatalkan') DEFAULT 'Pending',
  `alasan` text NOT NULL,
  `hasil` text DEFAULT NULL,
  `tindak_lanjut` text DEFAULT NULL,
  `foto_surat` varchar(255) DEFAULT NULL,
  `foto_dokumentasi` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `konseling_dhika`
--

INSERT INTO `konseling_dhika` (`id_konseling`, `siswa_id`, `guru_id`, `jenis`, `tanggal`, `jam_mulai`, `jam_selesai`, `status`, `alasan`, `hasil`, `tindak_lanjut`, `foto_surat`, `foto_dokumentasi`, `created_at`) VALUES
('KS0001', 1, 1, 'Karir', '2026-03-30', '11:00:00', '12:00:00', 'Disetujui', 'konsultasi tentang apa yang terjadi setelah lulus sekolah', '', NULL, NULL, NULL, '2026-03-28 11:32:39'),
('KS0002', 2, 2, 'Belajar', '2026-03-28', '12:00:00', '13:00:00', 'Selesai', 'konsultasi jurnal kimia', 'fika sudah lancar mengerjakan jurnal', NULL, NULL, NULL, '2026-03-28 12:00:10'),
('KS0003', 1, 1, 'Sosial', '2026-03-30', '07:00:00', '14:50:00', 'Selesai', 'teman', 'andhika sudah bisa bersosialisasi dan menambah eq nya', 'perlu bimbingan lagi jika belum terbiasa dengan perilaku yg baru', NULL, NULL, '2026-03-29 14:39:44'),
('KS0004', 1, 1, 'Karir', '2026-03-30', '11:00:00', '12:00:00', 'Selesai', 'cita cita masadepan', 'andhika sudah mendapatkan tujuan hidupnya', NULL, NULL, NULL, '2026-03-30 01:21:19'),
('KS0006', 1, 1, 'Pribadi', '2026-04-09', '11:15:00', '13:15:00', 'Disetujui', 'aaaa', '', NULL, NULL, NULL, '2026-04-09 04:15:52'),
('KS0007', 1, 1, 'Pribadi', '2026-04-13', '12:00:00', NULL, 'Disetujui', 'jangan lupa hadir ya nak', NULL, NULL, NULL, NULL, '2026-04-12 09:50:20'),
('KS0008', 11, 1, 'Pribadi', '2026-04-20', '13:43:00', NULL, 'Disetujui', 'Panggilan dari Guru BK', NULL, NULL, NULL, NULL, '2026-04-20 06:43:30'),
('KS0009', 2, 2, 'Karir', '2026-04-21', '15:00:00', NULL, 'Selesai', 'ingin bimbingan tentang kehidupan setelah lulus smk', '', NULL, NULL, NULL, '2026-04-21 06:23:46');

-- --------------------------------------------------------

--
-- Struktur dari tabel `log_aktivitas_dhika`
--

CREATE TABLE `log_aktivitas_dhika` (
  `id_log` int(11) NOT NULL,
  `akun_id` int(11) NOT NULL,
  `aktivitas` varchar(255) NOT NULL,
  `waktu` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `log_aktivitas_dhika`
--

INSERT INTO `log_aktivitas_dhika` (`id_log`, `akun_id`, `aktivitas`, `waktu`) VALUES
(1, 4, 'Login ke sistem', '2026-02-08 00:25:00'),
(2, 4, 'Mengajukan konseling baru - KSL001', '2026-02-08 00:35:00'),
(3, 2, 'Login ke sistem', '2026-02-08 00:40:00'),
(4, 2, 'Menyetujui konseling - KSL001', '2026-02-08 00:50:00'),
(5, 4, 'Menyelesaikan konseling - KSL001', '2026-02-08 02:05:00'),
(6, 4, 'Login ke sistem', '2026-03-28 09:59:15'),
(7, 4, 'Login ke sistem', '2026-03-28 10:00:55'),
(8, 4, 'Login ke sistem', '2026-03-28 10:02:22'),
(9, 4, 'Mengajukan konseling KS0001', '2026-03-28 11:32:39'),
(10, 4, 'Logout dari sistem', '2026-03-28 11:32:50'),
(11, 4, 'Login ke sistem', '2026-03-28 11:33:00'),
(12, 4, 'Logout dari sistem', '2026-03-28 11:55:56'),
(13, 1, 'Login ke sistem', '2026-03-28 11:56:11'),
(14, 1, 'Logout dari sistem', '2026-03-28 11:57:52'),
(15, 4, 'Login ke sistem', '2026-03-28 11:58:06'),
(16, 4, 'Logout dari sistem', '2026-03-28 11:58:35'),
(17, 5, 'Login ke sistem', '2026-03-28 11:59:16'),
(18, 5, 'Mengajukan konseling KS0002', '2026-03-28 12:00:10'),
(19, 5, 'Logout dari sistem', '2026-03-28 12:00:16'),
(20, 2, 'Login ke sistem', '2026-03-28 12:00:26'),
(21, 1, 'Login ke sistem', '2026-03-29 14:37:05'),
(22, 4, 'Login ke sistem', '2026-03-29 14:38:34'),
(23, 4, 'Mengajukan konseling KS0003', '2026-03-29 14:39:44'),
(24, 4, 'Logout dari sistem', '2026-03-29 14:40:12'),
(25, 1, 'Login ke sistem', '2026-03-29 14:40:24'),
(26, 1, 'Update konseling KS0001 ke status disetujui', '2026-03-29 14:52:31'),
(27, 1, 'Update konseling KS0001 ke status disetujui', '2026-03-29 14:53:18'),
(28, 1, 'Update konseling KS0003 ke status disetujui', '2026-03-29 14:53:25'),
(29, 1, 'Update konseling KS0001 ke status disetujui', '2026-03-29 14:54:34'),
(30, 1, 'Logout dari sistem', '2026-03-29 14:55:13'),
(31, 2, 'Login ke sistem', '2026-03-29 14:55:24'),
(32, 2, 'Update konseling KS0002 ke status disetujui', '2026-03-29 14:55:34'),
(33, 2, 'Update konseling KS0002 ke status pending', '2026-03-29 14:56:48'),
(34, 2, 'Update konseling KS0002 ke status pending', '2026-03-29 14:57:01'),
(35, 2, 'Update konseling KS0002 ke status Disetujui', '2026-03-29 15:04:49'),
(36, 2, 'Update konseling KS0002 ke status Selesai', '2026-03-29 15:05:39'),
(37, 2, 'Logout dari sistem', '2026-03-29 15:05:52'),
(38, 5, 'Login ke sistem', '2026-03-29 15:05:59'),
(39, 5, 'Logout dari sistem', '2026-03-29 15:15:40'),
(40, 2, 'Login ke sistem', '2026-03-29 15:16:07'),
(41, 2, 'Login ke sistem', '2026-03-29 15:16:23'),
(42, 2, 'Logout dari sistem', '2026-03-29 15:19:22'),
(43, 2, 'Login ke sistem', '2026-03-29 15:19:34'),
(44, 2, 'Logout dari sistem', '2026-03-29 15:20:13'),
(45, 4, 'Login ke sistem', '2026-03-29 15:20:26'),
(46, 4, 'Login ke sistem', '2026-03-29 22:01:49'),
(47, 4, 'Logout dari sistem', '2026-03-29 22:03:12'),
(48, 1, 'Login ke sistem', '2026-03-29 22:03:26'),
(49, 4, 'Login ke sistem', '2026-03-30 01:20:52'),
(50, 4, 'Mengajukan konseling KS0004', '2026-03-30 01:21:19'),
(51, 4, 'Logout dari sistem', '2026-03-30 01:22:31'),
(52, 1, 'Login ke sistem', '2026-03-30 01:22:39'),
(53, 1, 'Update konseling KS0004 ke status Disetujui', '2026-03-30 01:23:00'),
(54, 1, 'Update konseling KS0004 ke status Selesai', '2026-03-30 01:23:20'),
(55, 1, 'Logout dari sistem', '2026-03-30 01:24:32'),
(56, 4, 'Login ke sistem', '2026-03-30 01:24:41'),
(57, 1, 'Login ke sistem', '2026-03-30 21:50:39'),
(58, 1, 'Logout dari sistem', '2026-03-30 21:52:56'),
(59, 4, 'Login ke sistem', '2026-03-30 21:53:10'),
(60, 4, 'Logout dari sistem', '2026-03-30 21:53:53'),
(61, 1, 'Login ke sistem', '2026-03-30 21:54:03'),
(62, 1, 'Login ke sistem', '2026-03-30 21:54:26'),
(63, 1, 'Input pelanggaran siswa id 1, poin +10', '2026-03-30 22:16:18'),
(64, 1, 'Logout dari sistem', '2026-03-30 22:18:14'),
(65, 4, 'Login ke sistem', '2026-03-30 22:18:30'),
(66, 4, 'Login ke sistem', '2026-04-05 01:05:18'),
(67, 4, 'Login ke sistem', '2026-04-05 01:05:46'),
(68, 4, 'Mengajukan konseling KS0005', '2026-04-05 01:06:35'),
(69, 4, 'Login ke sistem', '2026-04-05 01:07:18'),
(70, 4, 'Logout dari sistem', '2026-04-05 01:07:27'),
(71, 4, 'Login ke sistem', '2026-04-05 01:07:56'),
(72, 4, 'Login ke sistem', '2026-04-07 00:00:10'),
(73, 4, 'Logout dari sistem', '2026-04-07 00:02:00'),
(74, 1, 'Login ke sistem', '2026-04-07 00:02:11'),
(75, 1, 'Logout dari sistem', '2026-04-07 00:02:54'),
(76, 1, 'Login ke sistem', '2026-04-07 00:05:59'),
(77, 4, 'Login ke sistem', '2026-04-07 00:22:28'),
(78, 4, 'Logout dari sistem', '2026-04-07 00:24:12'),
(79, 1, 'Login ke sistem', '2026-04-07 00:24:20'),
(80, 1, 'Login ke sistem', '2026-04-07 05:03:42'),
(81, 1, 'Menyetujui pendaftaran Aditya Firmansyah Andira', '2026-04-07 05:03:57'),
(82, 1, 'Logout dari sistem', '2026-04-07 05:04:58'),
(83, 4, 'Login ke sistem', '2026-04-07 05:05:08'),
(84, 1, 'Login ke sistem', '2026-04-08 12:30:56'),
(85, 1, 'Login ke sistem', '2026-04-08 12:31:16'),
(86, 4, 'Login ke sistem', '2026-04-08 12:32:07'),
(87, 4, 'Login ke sistem', '2026-04-08 12:33:43'),
(88, 4, 'Login ke sistem', '2026-04-08 12:45:14'),
(89, 4, 'Login ke sistem', '2026-04-09 04:14:52'),
(90, 4, 'Mengajukan konseling KS0006', '2026-04-09 04:15:52'),
(91, 4, 'Logout dari sistem', '2026-04-09 04:16:03'),
(92, 1, 'Login ke sistem', '2026-04-09 04:16:11'),
(93, 1, 'Update konseling KS0006 ke Disetujui', '2026-04-09 04:16:35'),
(94, 1, 'Logout dari sistem', '2026-04-09 04:16:57'),
(95, 4, 'Login ke sistem', '2026-04-09 04:17:06'),
(96, 4, 'Login ke sistem', '2026-04-09 23:51:34'),
(97, 4, 'Logout dari sistem', '2026-04-09 23:53:24'),
(98, 1, 'Login ke sistem', '2026-04-09 23:53:32'),
(99, 4, 'Login ke sistem', '2026-04-12 04:06:40'),
(100, 4, 'Logout dari sistem', '2026-04-12 04:07:43'),
(101, 7, 'Login ke sistem', '2026-04-12 04:07:50'),
(102, 7, 'Logout dari sistem', '2026-04-12 04:08:37'),
(103, 8, 'Login ke sistem', '2026-04-12 04:08:43'),
(104, 8, 'Logout dari sistem', '2026-04-12 04:08:56'),
(105, 1, 'Login ke sistem', '2026-04-12 04:09:02'),
(106, 4, 'Login ke sistem', '2026-04-12 09:45:37'),
(107, 4, 'Logout dari sistem', '2026-04-12 09:46:30'),
(108, 1, 'Login ke sistem', '2026-04-12 09:46:38'),
(109, 1, 'Logout dari sistem', '2026-04-12 09:47:53'),
(110, 7, 'Login ke sistem', '2026-04-12 09:48:02'),
(111, 7, 'Membuat pengaduan untuk siswa id 1', '2026-04-12 09:48:36'),
(112, 7, 'Logout dari sistem', '2026-04-12 09:49:19'),
(113, 8, 'Login ke sistem', '2026-04-12 09:49:27'),
(114, 8, 'Logout dari sistem', '2026-04-12 09:49:47'),
(115, 1, 'Login ke sistem', '2026-04-12 09:49:54'),
(116, 1, 'Memanggil siswa id 1 untuk konseling KS0007', '2026-04-12 09:50:20'),
(117, 1, 'Logout dari sistem', '2026-04-12 09:50:31'),
(118, 4, 'Login ke sistem', '2026-04-12 09:50:43'),
(119, 4, 'Logout dari sistem', '2026-04-12 09:52:42'),
(120, 7, 'Login ke sistem', '2026-04-12 09:52:57'),
(121, 7, 'Logout dari sistem', '2026-04-12 09:55:39'),
(122, 9, 'Login ke sistem', '2026-04-12 09:55:45'),
(123, 4, 'Login ke sistem', '2026-04-12 11:02:57'),
(124, 4, 'Login ke sistem', '2026-04-12 11:04:30'),
(125, 4, 'Login ke sistem', '2026-04-12 11:10:58'),
(126, 7, 'Login ke sistem', '2026-04-12 11:11:39'),
(127, 7, 'Logout dari sistem', '2026-04-12 11:12:22'),
(128, 8, 'Login ke sistem', '2026-04-12 11:12:28'),
(129, 8, 'Logout dari sistem', '2026-04-12 11:12:48'),
(130, 4, 'Login ke sistem', '2026-04-12 11:13:04'),
(131, 4, 'Login ke sistem', '2026-04-12 11:19:10'),
(132, 4, 'Login ke sistem', '2026-04-12 11:25:39'),
(133, 4, 'Login ke sistem', '2026-04-12 11:29:19'),
(134, 4, 'Login ke sistem', '2026-04-12 11:29:36'),
(135, 4, 'Login ke sistem', '2026-04-12 11:30:47'),
(136, 4, 'Login ke sistem', '2026-04-12 11:33:15'),
(137, 4, 'Logout dari sistem', '2026-04-12 11:34:51'),
(138, 1, 'Login ke sistem', '2026-04-12 11:34:59'),
(139, 1, 'Logout dari sistem', '2026-04-12 11:36:09'),
(140, 7, 'Login ke sistem', '2026-04-12 11:36:15'),
(141, 4, 'Login ke sistem', '2026-04-15 12:41:04'),
(142, 4, 'Login ke sistem', '2026-04-15 12:57:37'),
(143, 4, 'Logout dari sistem', '2026-04-15 12:58:03'),
(144, 1, 'Login ke sistem', '2026-04-15 12:58:06'),
(145, 1, 'Membuat pemanggilan orang tua siswa id 1', '2026-04-15 13:02:37'),
(146, 1, 'Membuat pemanggilan orang tua siswa id 2', '2026-04-15 13:12:57'),
(147, 4, 'Login ke sistem', '2026-04-15 13:47:15'),
(148, 1, 'Login ke sistem', '2026-04-15 13:48:24'),
(149, 4, 'Logout dari sistem', '2026-04-15 13:52:01'),
(150, 1, 'Login ke sistem', '2026-04-15 13:52:03'),
(151, 1, 'Logout dari sistem', '2026-04-15 13:52:53'),
(152, 7, 'Login ke sistem', '2026-04-15 13:52:56'),
(153, 4, 'Login ke sistem', '2026-04-20 04:06:44'),
(154, 4, 'Logout dari sistem', '2026-04-20 04:06:55'),
(155, 1, 'Login ke sistem', '2026-04-20 04:06:57'),
(156, 1, 'Logout dari sistem', '2026-04-20 06:28:38'),
(157, 8, 'Login ke sistem', '2026-04-20 06:28:54'),
(158, 8, 'Logout dari sistem', '2026-04-20 06:29:08'),
(159, 7, 'Login ke sistem', '2026-04-20 06:29:11'),
(160, 7, 'Input pelanggaran siswa id 11', '2026-04-20 06:41:43'),
(161, 7, 'Logout dari sistem', '2026-04-20 06:41:58'),
(162, 7, 'Login ke sistem', '2026-04-20 06:42:02'),
(163, 7, 'Membuat pengaduan untuk siswa id 11', '2026-04-20 06:43:01'),
(164, 7, 'Logout dari sistem', '2026-04-20 06:43:03'),
(165, 1, 'Login ke sistem', '2026-04-20 06:43:06'),
(166, 1, 'Update pengaduan #2 ke Diproses', '2026-04-20 06:43:18'),
(167, 1, 'Memanggil siswa id 11 untuk konseling KS0008', '2026-04-20 06:43:30'),
(168, 1, 'Membuat pemanggilan orang tua siswa id 11', '2026-04-20 06:43:48'),
(169, 1, 'Logout dari sistem', '2026-04-20 07:10:39'),
(170, 4, 'Login ke sistem', '2026-04-20 07:10:42'),
(171, 4, 'Logout dari sistem', '2026-04-20 07:10:53'),
(172, 8, 'Login ke sistem', '2026-04-20 07:10:56'),
(173, 8, 'Logout dari sistem', '2026-04-20 07:11:04'),
(174, 7, 'Login ke sistem', '2026-04-20 07:11:12'),
(175, 7, 'Logout dari sistem', '2026-04-20 07:11:31'),
(176, 9, 'Login ke sistem', '2026-04-20 07:11:36'),
(177, 9, 'Logout dari sistem', '2026-04-20 07:11:48'),
(178, 4, 'Login ke sistem', '2026-04-20 07:17:24'),
(179, 4, 'Logout dari sistem', '2026-04-20 07:17:32'),
(180, 1, 'Login ke sistem', '2026-04-20 07:17:34'),
(181, 1, 'Logout dari sistem', '2026-04-20 07:17:54'),
(182, 8, 'Login ke sistem', '2026-04-20 07:17:58'),
(183, 8, 'Logout dari sistem', '2026-04-20 07:18:29'),
(184, 4, 'Login ke sistem', '2026-04-20 07:18:31'),
(185, 4, 'Logout dari sistem', '2026-04-20 07:18:37'),
(186, 1, 'Login ke sistem', '2026-04-20 07:18:38'),
(187, 1, 'Logout dari sistem', '2026-04-20 07:18:40'),
(188, 8, 'Login ke sistem', '2026-04-20 07:18:43'),
(189, 8, 'Logout dari sistem', '2026-04-20 07:18:50'),
(190, 4, 'Login ke sistem', '2026-04-20 07:18:52'),
(191, 4, 'Logout dari sistem', '2026-04-20 07:29:23'),
(192, 1, 'Login ke sistem', '2026-04-20 07:29:25'),
(193, 1, 'Logout dari sistem', '2026-04-20 07:32:49'),
(194, 4, 'Login ke sistem', '2026-04-20 07:32:51'),
(195, 4, 'Logout dari sistem', '2026-04-20 07:36:48'),
(196, 4, 'Login ke sistem', '2026-04-21 02:54:27'),
(197, 4, 'Logout dari sistem', '2026-04-21 03:21:28'),
(198, 4, 'Login ke sistem', '2026-04-21 03:21:31'),
(199, 4, 'Logout dari sistem', '2026-04-21 03:21:34'),
(200, 1, 'Login ke sistem', '2026-04-21 03:21:36'),
(201, 1, 'Logout dari sistem', '2026-04-21 03:21:38'),
(202, 9, 'Login ke sistem', '2026-04-21 03:23:31'),
(203, 9, 'Login ke sistem', '2026-04-21 03:23:51'),
(204, 9, 'Login ke sistem', '2026-04-21 03:24:25'),
(205, 9, 'Membuat akun Siswa: haidar', '2026-04-21 03:25:02'),
(206, 9, 'Update status akun #10 ke Nonaktif', '2026-04-21 03:25:19'),
(207, 9, 'Logout dari sistem', '2026-04-21 03:25:25'),
(208, 9, 'Login ke sistem', '2026-04-21 03:25:34'),
(209, 9, 'Update status akun #10 ke Aktif', '2026-04-21 03:25:35'),
(210, 9, 'Logout dari sistem', '2026-04-21 03:43:26'),
(211, 4, 'Login ke sistem', '2026-04-21 03:43:28'),
(212, 4, 'Logout dari sistem', '2026-04-21 03:52:34'),
(213, 1, 'Login ke sistem', '2026-04-21 03:52:37'),
(214, 1, 'Logout dari sistem', '2026-04-21 03:59:50'),
(215, 4, 'Login ke sistem', '2026-04-21 03:59:52'),
(216, 4, 'Login ke sistem', '2026-04-21 03:59:58'),
(217, 4, 'Login ke sistem', '2026-04-21 04:01:04'),
(218, 4, 'Login ke sistem', '2026-04-21 04:02:28'),
(219, 4, 'Login ke sistem', '2026-04-21 04:02:42'),
(220, 4, 'Logout dari sistem', '2026-04-21 04:11:45'),
(221, 4, 'Login ke sistem', '2026-04-21 04:18:36'),
(222, 4, 'Logout dari sistem', '2026-04-21 04:18:50'),
(223, 1, 'Login ke sistem', '2026-04-21 04:18:52'),
(224, 1, 'Logout dari sistem', '2026-04-21 04:19:03'),
(225, 4, 'Login ke sistem', '2026-04-21 04:50:32'),
(226, 4, 'Memperbarui profil akun', '2026-04-21 04:53:24'),
(227, 4, 'Logout dari sistem', '2026-04-21 05:00:34'),
(228, 1, 'Login ke sistem', '2026-04-21 05:00:36'),
(229, 1, 'Logout dari sistem', '2026-04-21 05:01:40'),
(230, 1, 'Login ke sistem', '2026-04-21 05:40:23'),
(231, 1, 'Logout dari sistem', '2026-04-21 05:40:49'),
(232, 4, 'Login ke sistem', '2026-04-21 05:40:51'),
(233, 4, 'Logout dari sistem', '2026-04-21 05:55:23'),
(234, 1, 'Login ke sistem', '2026-04-21 05:55:27'),
(235, 1, 'Logout dari sistem', '2026-04-21 05:55:28'),
(236, 1, 'Login ke sistem', '2026-04-21 05:55:31'),
(237, 1, 'Logout dari sistem', '2026-04-21 05:55:33'),
(238, 1, 'Login ke sistem', '2026-04-21 05:55:39'),
(239, 1, 'Logout dari sistem', '2026-04-21 06:09:52'),
(240, 4, 'Login ke sistem', '2026-04-21 06:09:56'),
(241, 4, 'Logout dari sistem', '2026-04-21 06:10:01'),
(242, 1, 'Login ke sistem', '2026-04-21 06:10:06'),
(243, 1, 'Logout dari sistem', '2026-04-21 06:10:41'),
(244, 8, 'Login ke sistem', '2026-04-21 06:10:44'),
(245, 8, 'Logout dari sistem', '2026-04-21 06:10:48'),
(246, 7, 'Login ke sistem', '2026-04-21 06:10:51'),
(247, 7, 'Logout dari sistem', '2026-04-21 06:11:24'),
(248, 1, 'Login ke sistem', '2026-04-21 06:12:06'),
(249, 1, 'Logout dari sistem', '2026-04-21 06:15:27'),
(250, 4, 'Login ke sistem', '2026-04-21 06:15:30'),
(251, 4, 'Logout dari sistem', '2026-04-21 06:15:31'),
(252, 1, 'Login ke sistem', '2026-04-21 06:15:34'),
(253, 1, 'Logout dari sistem', '2026-04-21 06:15:49'),
(254, 4, 'Login ke sistem', '2026-04-21 06:15:52'),
(255, 4, 'Logout dari sistem', '2026-04-21 06:15:54'),
(256, 4, 'Login ke sistem', '2026-04-21 06:16:21'),
(257, 4, 'Logout dari sistem', '2026-04-21 06:19:57'),
(258, 1, 'Login ke sistem', '2026-04-21 06:20:00'),
(259, 1, 'Logout dari sistem', '2026-04-21 06:21:51'),
(260, 1, 'Login ke sistem', '2026-04-21 06:21:54'),
(261, 1, 'Logout dari sistem', '2026-04-21 06:22:25'),
(262, 5, 'Login ke sistem', '2026-04-21 06:22:45'),
(263, 5, 'Mengajukan konseling KS0009', '2026-04-21 06:23:46'),
(264, 5, 'Logout dari sistem', '2026-04-21 06:24:03'),
(265, 4, 'Login ke sistem', '2026-04-21 06:24:07'),
(266, 4, 'Logout dari sistem', '2026-04-21 06:24:09'),
(267, 2, 'Login ke sistem', '2026-04-21 06:24:21'),
(268, 2, 'Update konseling KS0009 ke Selesai', '2026-04-21 06:24:53'),
(269, 2, 'Logout dari sistem', '2026-04-21 06:25:03'),
(270, 9, 'Login ke sistem', '2026-04-21 06:25:06'),
(271, 9, 'Logout dari sistem', '2026-04-21 06:33:27'),
(272, 1, 'Login ke sistem', '2026-04-21 06:33:30'),
(273, 1, 'Logout dari sistem', '2026-04-21 06:34:13'),
(274, 8, 'Login ke sistem', '2026-04-21 06:34:16'),
(275, 8, 'Logout dari sistem', '2026-04-21 06:36:45'),
(276, 4, 'Login ke sistem', '2026-04-21 06:36:48'),
(277, 4, 'Logout dari sistem', '2026-04-21 06:42:58'),
(278, 1, 'Login ke sistem', '2026-04-21 06:43:02'),
(279, 1, 'Logout dari sistem', '2026-04-21 06:43:12'),
(280, 9, 'Login ke sistem', '2026-04-21 06:43:15'),
(281, 9, 'Logout dari sistem', '2026-04-21 06:44:04'),
(282, 1, 'Login ke sistem', '2026-04-21 06:44:07'),
(283, 1, 'Logout dari sistem', '2026-04-21 06:44:54'),
(284, 4, 'Login ke sistem', '2026-04-21 06:44:57'),
(285, 4, 'Logout dari sistem', '2026-04-21 06:46:19'),
(286, 1, 'Login ke sistem', '2026-04-21 06:46:22'),
(287, 1, 'Logout dari sistem', '2026-04-21 06:53:13'),
(288, 9, 'Login ke sistem', '2026-04-21 06:53:17'),
(289, 9, 'Logout dari sistem', '2026-04-21 06:56:03'),
(290, 4, 'Login ke sistem', '2026-04-21 06:56:09'),
(291, 4, 'Logout dari sistem', '2026-04-21 06:57:26'),
(292, 9, 'Login ke sistem', '2026-04-21 06:57:29'),
(293, 9, 'Logout dari sistem', '2026-04-21 06:58:40'),
(294, 4, 'Login ke sistem', '2026-04-21 06:58:44'),
(295, 4, 'Logout dari sistem', '2026-04-21 07:09:49'),
(296, 8, 'Login ke sistem', '2026-04-21 07:09:58'),
(297, 8, 'Logout dari sistem', '2026-04-21 07:10:09'),
(298, 4, 'Login ke sistem', '2026-04-21 07:10:11'),
(299, 4, 'Logout dari sistem', '2026-04-21 07:10:20'),
(300, 8, 'Login ke sistem', '2026-04-21 07:10:26'),
(301, 8, 'Logout dari sistem', '2026-04-21 07:12:38'),
(302, 4, 'Login ke sistem', '2026-04-21 07:12:48'),
(303, 4, 'Logout dari sistem', '2026-04-21 07:13:57'),
(304, 8, 'Login ke sistem', '2026-04-21 07:14:00'),
(305, 8, 'Logout dari sistem', '2026-04-21 07:14:42'),
(306, 1, 'Login ke sistem', '2026-04-21 07:14:45'),
(307, 1, 'Logout dari sistem', '2026-04-21 07:15:46'),
(308, 8, 'Login ke sistem', '2026-04-21 07:15:49'),
(309, 8, 'Logout dari sistem', '2026-04-21 07:16:24'),
(310, 7, 'Login ke sistem', '2026-04-21 07:16:32'),
(311, 7, 'Input pelanggaran siswa id 1', '2026-04-21 07:17:36'),
(312, 7, 'Logout dari sistem', '2026-04-21 07:17:52'),
(313, 4, 'Login ke sistem', '2026-04-21 07:17:55'),
(314, 4, 'Logout dari sistem', '2026-04-21 07:18:34'),
(315, 7, 'Login ke sistem', '2026-04-21 07:18:38'),
(316, 7, 'Logout dari sistem', '2026-04-21 07:20:00'),
(317, 1, 'Login ke sistem', '2026-04-21 07:20:03'),
(318, 1, 'Logout dari sistem', '2026-04-21 07:40:59'),
(319, 8, 'Login ke sistem', '2026-04-21 07:41:03'),
(320, 8, 'Logout dari sistem', '2026-04-21 07:42:32'),
(321, 4, 'Login ke sistem', '2026-04-21 07:42:35'),
(322, 4, 'Logout dari sistem', '2026-04-21 07:48:23'),
(323, 4, 'Login ke sistem', '2026-04-21 07:48:32'),
(324, 4, 'Logout dari sistem', '2026-04-21 07:49:07'),
(325, 1, 'Login ke sistem', '2026-04-21 07:49:13'),
(326, 1, 'Update konseling KS0003 ke Selesai', '2026-04-21 07:51:28'),
(327, 1, 'Logout dari sistem', '2026-04-21 07:51:35'),
(328, 8, 'Login ke sistem', '2026-04-21 07:51:38'),
(329, 8, 'Logout dari sistem', '2026-04-21 07:52:18'),
(330, 4, 'Login ke sistem', '2026-04-21 07:52:21'),
(331, 4, 'Logout dari sistem', '2026-04-21 07:52:52'),
(332, 4, 'Login ke sistem', '2026-04-21 07:53:17');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pelanggaran_dhika`
--

CREATE TABLE `pelanggaran_dhika` (
  `id_pelanggaran` int(11) NOT NULL,
  `nama_pelanggaran` varchar(100) NOT NULL,
  `kategori` enum('Ringan','Sedang','Berat','Sangat Berat') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `pelanggaran_dhika`
--

INSERT INTO `pelanggaran_dhika` (`id_pelanggaran`, `nama_pelanggaran`, `kategori`) VALUES
(1, 'Terlambat', 'Ringan'),
(2, 'Tidak memakai atribut lengkap', 'Ringan'),
(3, 'Rambut tidak rapi', 'Ringan'),
(4, 'Tidak mengerjakan tugas', 'Sedang'),
(5, 'Keluar kelas tanpa izin', 'Sedang'),
(6, 'Bolos 1 jam', 'Sedang'),
(7, 'Bolos 1 hari', 'Berat'),
(8, 'Berkelahi', 'Berat'),
(9, 'Merokok', 'Berat'),
(10, 'Membawa barang terlarang', 'Sangat Berat'),
(11, 'Narkoba', 'Sangat Berat');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pemanggilan_ortu_dhika`
--

CREATE TABLE `pemanggilan_ortu_dhika` (
  `id_pemanggilan` int(11) NOT NULL,
  `siswa_id` int(11) NOT NULL,
  `guru_id` int(11) NOT NULL,
  `tujuan` text NOT NULL,
  `tanggal` date NOT NULL,
  `status` enum('Dijadwalkan','Sudah Hadir','Tidak Hadir') DEFAULT 'Dijadwalkan',
  `catatan` text DEFAULT NULL,
  `foto_surat` varchar(255) DEFAULT NULL,
  `foto_dokumentasi` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `pemanggilan_ortu_dhika`
--

INSERT INTO `pemanggilan_ortu_dhika` (`id_pemanggilan`, `siswa_id`, `guru_id`, `tujuan`, `tanggal`, `status`, `catatan`, `foto_surat`, `foto_dokumentasi`, `created_at`) VALUES
(1, 1, 1, 'andhika tidak menaati peraturan sekolah', '2026-04-15', 'Sudah Hadir', 'orang tua andhika menyetujui surat perjanjian ', NULL, NULL, '2026-04-15 13:02:37'),
(2, 2, 1, 'membahas prestasi fika yg mempunyai potensi besar untuk lebih berkembang', '2026-04-16', 'Dijadwalkan', NULL, NULL, NULL, '2026-04-15 13:12:57'),
(3, 11, 1, 'merokok di warjo', '2026-04-20', 'Dijadwalkan', NULL, NULL, NULL, '2026-04-20 06:43:48');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pengaduan_dhika`
--

CREATE TABLE `pengaduan_dhika` (
  `id_pengaduan` int(11) NOT NULL,
  `kesiswaan_id` int(11) NOT NULL,
  `siswa_id` int(11) NOT NULL,
  `judul` varchar(200) NOT NULL,
  `deskripsi` text NOT NULL,
  `status` enum('Baru','Diproses','Selesai') DEFAULT 'Baru',
  `catatan` text DEFAULT NULL,
  `tanggal` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `pengaduan_dhika`
--

INSERT INTO `pengaduan_dhika` (`id_pengaduan`, `kesiswaan_id`, `siswa_id`, `judul`, `deskripsi`, `status`, `catatan`, `tanggal`) VALUES
(1, 1, 1, 'sering bolos', '2x bolos dalam seminggu', 'Diproses', NULL, '2026-04-12 09:48:36'),
(2, 1, 11, 'merokok', 'harus dibimbing agar tidak merokok lagi', 'Diproses', '', '2026-04-20 06:43:01');

-- --------------------------------------------------------

--
-- Struktur dari tabel `riwayat_pelanggaran_dhika`
--

CREATE TABLE `riwayat_pelanggaran_dhika` (
  `id_riwayat` int(11) NOT NULL,
  `siswa_id` int(11) NOT NULL,
  `pelanggaran_id` int(11) NOT NULL,
  `tanggal` date NOT NULL,
  `keterangan` text DEFAULT NULL,
  `tindakan_guru` text DEFAULT NULL,
  `tindak_lanjut` text DEFAULT NULL,
  `foto_surat` varchar(255) DEFAULT NULL,
  `foto_dokumentasi` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `riwayat_pelanggaran_dhika`
--

INSERT INTO `riwayat_pelanggaran_dhika` (`id_riwayat`, `siswa_id`, `pelanggaran_id`, `tanggal`, `keterangan`, `tindakan_guru`, `tindak_lanjut`, `foto_surat`, `foto_dokumentasi`) VALUES
(1, 1, 3, '2026-03-30', '', NULL, NULL, NULL, NULL),
(2, 11, 9, '2026-04-20', 'merokok di warjo', 'diberi surat perjanjian', 'harus dibimbing oleh bk', NULL, NULL),
(3, 1, 3, '2026-04-21', 'tes', 'tes', 'tes', NULL, '4dabe842e6df43f989031e4a2ff1bd2e.jpg');

-- --------------------------------------------------------

--
-- Struktur dari tabel `siswa_dhika`
--

CREATE TABLE `siswa_dhika` (
  `id_siswa` int(11) NOT NULL,
  `akun_id` int(11) NOT NULL,
  `nis` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `kelas` enum('X','XI','XII') NOT NULL,
  `jurusan` enum('RPL','Meka','Mesin','Kimia','Animasi','DKV') NOT NULL,
  `rombel` enum('A','B','C','D') NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `no_hp` varchar(20) DEFAULT NULL,
  `no_ortu` varchar(20) DEFAULT NULL,
  `foto_profil` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `siswa_dhika`
--

INSERT INTO `siswa_dhika` (`id_siswa`, `akun_id`, `nis`, `nama`, `kelas`, `jurusan`, `rombel`, `email`, `no_hp`, `no_ortu`, `foto_profil`) VALUES
(1, 4, '10243252', 'Andhika Andriana Putra', 'XI', 'RPL', 'A', 'andhika@gmail.com', '62895627174900', '6281223530650', '90a5056273b343e8af3a0c5bacb22ebd.jpg'),
(2, 5, '10245407', 'Fika Indah Lestari', 'XI', 'Kimia', 'A', 'fika@gmail.com', NULL, '62895631922002', NULL),
(11, 6, '10243249', 'Aditya Firmansyah Andira', 'XI', 'RPL', 'A', NULL, NULL, NULL, NULL),
(12, 10, '10243266', 'Haidar Alif Fajar Maulana', 'XI', 'RPL', 'A', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `wali_kelas_dhika`
--

CREATE TABLE `wali_kelas_dhika` (
  `id_walikelas` int(11) NOT NULL,
  `akun_id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `nip` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `no_hp` varchar(20) DEFAULT NULL,
  `foto_profil` varchar(255) DEFAULT NULL,
  `kelas` enum('X','XI','XII') NOT NULL,
  `jurusan` enum('RPL','Animasi','DKV','Kimia','Mesin','Meka') NOT NULL,
  `rombel` enum('A','B','C','D') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `wali_kelas_dhika`
--

INSERT INTO `wali_kelas_dhika` (`id_walikelas`, `akun_id`, `nama`, `nip`, `email`, `no_hp`, `foto_profil`, `kelas`, `jurusan`, `rombel`) VALUES
(1, 8, 'Gigin Gantini Putri', '271918363829119', NULL, NULL, NULL, 'XI', 'RPL', 'A');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `admin_dhika`
--
ALTER TABLE `admin_dhika`
  ADD PRIMARY KEY (`id_admin`),
  ADD KEY `akun_id` (`akun_id`);

--
-- Indeks untuk tabel `akun_dhika`
--
ALTER TABLE `akun_dhika`
  ADD PRIMARY KEY (`id_akun`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indeks untuk tabel `chat_dhika`
--
ALTER TABLE `chat_dhika`
  ADD PRIMARY KEY (`id_chat`),
  ADD KEY `pengirim_akun_id` (`pengirim_akun_id`),
  ADD KEY `penerima_akun_id` (`penerima_akun_id`);

--
-- Indeks untuk tabel `guru_dhika`
--
ALTER TABLE `guru_dhika`
  ADD PRIMARY KEY (`id_guru`),
  ADD UNIQUE KEY `nip` (`nip`),
  ADD KEY `akun_id` (`akun_id`);

--
-- Indeks untuk tabel `kesiswaan_dhika`
--
ALTER TABLE `kesiswaan_dhika`
  ADD PRIMARY KEY (`id_kesiswaan`),
  ADD KEY `akun_id` (`akun_id`);

--
-- Indeks untuk tabel `konseling_dhika`
--
ALTER TABLE `konseling_dhika`
  ADD PRIMARY KEY (`id_konseling`),
  ADD KEY `siswa_id` (`siswa_id`),
  ADD KEY `guru_id` (`guru_id`);

--
-- Indeks untuk tabel `log_aktivitas_dhika`
--
ALTER TABLE `log_aktivitas_dhika`
  ADD PRIMARY KEY (`id_log`),
  ADD KEY `akun_id` (`akun_id`);

--
-- Indeks untuk tabel `pelanggaran_dhika`
--
ALTER TABLE `pelanggaran_dhika`
  ADD PRIMARY KEY (`id_pelanggaran`);

--
-- Indeks untuk tabel `pemanggilan_ortu_dhika`
--
ALTER TABLE `pemanggilan_ortu_dhika`
  ADD PRIMARY KEY (`id_pemanggilan`),
  ADD KEY `siswa_id` (`siswa_id`),
  ADD KEY `guru_id` (`guru_id`);

--
-- Indeks untuk tabel `pengaduan_dhika`
--
ALTER TABLE `pengaduan_dhika`
  ADD PRIMARY KEY (`id_pengaduan`),
  ADD KEY `kesiswaan_id` (`kesiswaan_id`),
  ADD KEY `siswa_id` (`siswa_id`);

--
-- Indeks untuk tabel `riwayat_pelanggaran_dhika`
--
ALTER TABLE `riwayat_pelanggaran_dhika`
  ADD PRIMARY KEY (`id_riwayat`),
  ADD KEY `siswa_id` (`siswa_id`),
  ADD KEY `pelanggaran_id` (`pelanggaran_id`);

--
-- Indeks untuk tabel `siswa_dhika`
--
ALTER TABLE `siswa_dhika`
  ADD PRIMARY KEY (`id_siswa`),
  ADD UNIQUE KEY `nis` (`nis`),
  ADD KEY `akun_id` (`akun_id`);

--
-- Indeks untuk tabel `wali_kelas_dhika`
--
ALTER TABLE `wali_kelas_dhika`
  ADD PRIMARY KEY (`id_walikelas`),
  ADD KEY `akun_id` (`akun_id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `admin_dhika`
--
ALTER TABLE `admin_dhika`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `akun_dhika`
--
ALTER TABLE `akun_dhika`
  MODIFY `id_akun` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT untuk tabel `chat_dhika`
--
ALTER TABLE `chat_dhika`
  MODIFY `id_chat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT untuk tabel `guru_dhika`
--
ALTER TABLE `guru_dhika`
  MODIFY `id_guru` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `kesiswaan_dhika`
--
ALTER TABLE `kesiswaan_dhika`
  MODIFY `id_kesiswaan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `log_aktivitas_dhika`
--
ALTER TABLE `log_aktivitas_dhika`
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=333;

--
-- AUTO_INCREMENT untuk tabel `pelanggaran_dhika`
--
ALTER TABLE `pelanggaran_dhika`
  MODIFY `id_pelanggaran` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT untuk tabel `pemanggilan_ortu_dhika`
--
ALTER TABLE `pemanggilan_ortu_dhika`
  MODIFY `id_pemanggilan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `pengaduan_dhika`
--
ALTER TABLE `pengaduan_dhika`
  MODIFY `id_pengaduan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `riwayat_pelanggaran_dhika`
--
ALTER TABLE `riwayat_pelanggaran_dhika`
  MODIFY `id_riwayat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `siswa_dhika`
--
ALTER TABLE `siswa_dhika`
  MODIFY `id_siswa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT untuk tabel `wali_kelas_dhika`
--
ALTER TABLE `wali_kelas_dhika`
  MODIFY `id_walikelas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `admin_dhika`
--
ALTER TABLE `admin_dhika`
  ADD CONSTRAINT `admin_dhika_ibfk_1` FOREIGN KEY (`akun_id`) REFERENCES `akun_dhika` (`id_akun`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `chat_dhika`
--
ALTER TABLE `chat_dhika`
  ADD CONSTRAINT `chat_dhika_ibfk_1` FOREIGN KEY (`pengirim_akun_id`) REFERENCES `akun_dhika` (`id_akun`) ON DELETE CASCADE,
  ADD CONSTRAINT `chat_dhika_ibfk_2` FOREIGN KEY (`penerima_akun_id`) REFERENCES `akun_dhika` (`id_akun`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `guru_dhika`
--
ALTER TABLE `guru_dhika`
  ADD CONSTRAINT `guru_dhika_ibfk_1` FOREIGN KEY (`akun_id`) REFERENCES `akun_dhika` (`id_akun`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `kesiswaan_dhika`
--
ALTER TABLE `kesiswaan_dhika`
  ADD CONSTRAINT `kesiswaan_dhika_ibfk_1` FOREIGN KEY (`akun_id`) REFERENCES `akun_dhika` (`id_akun`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `konseling_dhika`
--
ALTER TABLE `konseling_dhika`
  ADD CONSTRAINT `konseling_dhika_ibfk_1` FOREIGN KEY (`siswa_id`) REFERENCES `siswa_dhika` (`id_siswa`) ON DELETE CASCADE,
  ADD CONSTRAINT `konseling_dhika_ibfk_2` FOREIGN KEY (`guru_id`) REFERENCES `guru_dhika` (`id_guru`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `log_aktivitas_dhika`
--
ALTER TABLE `log_aktivitas_dhika`
  ADD CONSTRAINT `log_aktivitas_dhika_ibfk_1` FOREIGN KEY (`akun_id`) REFERENCES `akun_dhika` (`id_akun`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `pemanggilan_ortu_dhika`
--
ALTER TABLE `pemanggilan_ortu_dhika`
  ADD CONSTRAINT `pemanggilan_ortu_dhika_ibfk_1` FOREIGN KEY (`siswa_id`) REFERENCES `siswa_dhika` (`id_siswa`) ON DELETE CASCADE,
  ADD CONSTRAINT `pemanggilan_ortu_dhika_ibfk_2` FOREIGN KEY (`guru_id`) REFERENCES `guru_dhika` (`id_guru`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `pengaduan_dhika`
--
ALTER TABLE `pengaduan_dhika`
  ADD CONSTRAINT `pengaduan_dhika_ibfk_1` FOREIGN KEY (`kesiswaan_id`) REFERENCES `kesiswaan_dhika` (`id_kesiswaan`) ON DELETE CASCADE,
  ADD CONSTRAINT `pengaduan_dhika_ibfk_2` FOREIGN KEY (`siswa_id`) REFERENCES `siswa_dhika` (`id_siswa`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `riwayat_pelanggaran_dhika`
--
ALTER TABLE `riwayat_pelanggaran_dhika`
  ADD CONSTRAINT `riwayat_pelanggaran_dhika_ibfk_1` FOREIGN KEY (`siswa_id`) REFERENCES `siswa_dhika` (`id_siswa`) ON DELETE CASCADE,
  ADD CONSTRAINT `riwayat_pelanggaran_dhika_ibfk_2` FOREIGN KEY (`pelanggaran_id`) REFERENCES `pelanggaran_dhika` (`id_pelanggaran`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `siswa_dhika`
--
ALTER TABLE `siswa_dhika`
  ADD CONSTRAINT `siswa_dhika_ibfk_1` FOREIGN KEY (`akun_id`) REFERENCES `akun_dhika` (`id_akun`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `wali_kelas_dhika`
--
ALTER TABLE `wali_kelas_dhika`
  ADD CONSTRAINT `wali_kelas_dhika_ibfk_1` FOREIGN KEY (`akun_id`) REFERENCES `akun_dhika` (`id_akun`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
