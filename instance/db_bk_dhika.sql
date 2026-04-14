-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 14 Apr 2026 pada 04.06
-- Versi server: 10.4.6-MariaDB
-- Versi PHP: 7.3.10

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
  `nama` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `admin_dhika`
--

INSERT INTO `admin_dhika` (`id_admin`, `akun_id`, `nama`) VALUES
(1, 9, 'Admin');

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `akun_dhika`
--

INSERT INTO `akun_dhika` (`id_akun`, `username`, `password`, `role`, `created_at`, `status_akun`) VALUES
(1, 'tini', 'tini123', 'Guru BK', '2026-03-28 08:55:06', 'Aktif'),
(2, 'anom', 'anom123', 'Guru BK', '2026-03-28 08:55:06', 'Aktif'),
(3, 'dudu', 'dudu123', 'Guru BK', '2026-03-28 08:55:06', 'Aktif'),
(4, 'andhika', 'andhika123', 'Siswa', '2026-03-28 08:55:06', 'Aktif'),
(5, 'fika', 'fika123', 'Siswa', '2026-03-28 08:55:06', 'Aktif'),
(6, 'adit', 'adit123', 'Siswa', '2026-04-07 05:03:57', 'Aktif'),
(7, 'ismita', '123', 'Kesiswaan', '2026-04-12 04:03:52', 'Aktif'),
(8, 'gigin', '123', 'Wali Kelas', '2026-04-12 04:03:52', 'Aktif'),
(9, 'admin', '123', 'Admin', '2026-04-12 04:04:16', 'Aktif');

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `chat_dhika`
--

INSERT INTO `chat_dhika` (`id_chat`, `pengirim_akun_id`, `penerima_akun_id`, `pesan`, `waktu`, `dibaca`) VALUES
(6, 4, 1, 'assalamualaikum ibu', '2026-03-29 14:38:49', 1),
(7, 4, 1, 'Halo, saya telah mengajukan konseling (Sosial) pada 2026-03-30 pukul 07:00-08:00. Mohon konfirmasinya. Terima kasih.', '2026-03-29 14:39:44', 1),
(8, 1, 4, 'oke nak', '2026-03-29 14:42:02', 1),
(9, 5, 2, 'terimakasih pak', '2026-03-29 15:15:24', 0),
(10, 2, 5, 'sama sama nak', '2026-03-29 15:16:38', 0),
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
(26, 8, 4, 'nak', '2026-04-12 11:12:43', 0),
(27, 4, 1, 'bu', '2026-04-12 11:34:36', 1),
(28, 7, 1, 'bu', '2026-04-12 11:36:24', 0);

-- --------------------------------------------------------

--
-- Struktur dari tabel `guru_dhika`
--

CREATE TABLE `guru_dhika` (
  `id_guru` int(11) NOT NULL,
  `akun_id` int(11) NOT NULL,
  `nip` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `guru_dhika`
--

INSERT INTO `guru_dhika` (`id_guru`, `akun_id`, `nip`, `nama`, `email`) VALUES
(1, 1, '197512302005012003', 'Tini Hermawati, S.Pd', 'tinihermawati@gmail.com'),
(2, 2, '196805121994031002', 'Anom Jati Kusumo, S.Psi', 'anom@gmail.com'),
(3, 3, '197908172006041005', 'Durahman, S.Psi', 'dudu@gmail.com');

-- --------------------------------------------------------

--
-- Struktur dari tabel `kesiswaan_dhika`
--

CREATE TABLE `kesiswaan_dhika` (
  `id_kesiswaan` int(11) NOT NULL,
  `akun_id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `nip` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `kesiswaan_dhika`
--

INSERT INTO `kesiswaan_dhika` (`id_kesiswaan`, `akun_id`, `nama`, `nip`) VALUES
(1, 7, 'Ismita Ratnasari, S.ST, M.M', '297328910101');

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
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `konseling_dhika`
--

INSERT INTO `konseling_dhika` (`id_konseling`, `siswa_id`, `guru_id`, `jenis`, `tanggal`, `jam_mulai`, `jam_selesai`, `status`, `alasan`, `hasil`, `created_at`) VALUES
('KS0001', 1, 1, 'Karir', '2026-03-30', '11:00:00', '12:00:00', 'Disetujui', 'konsultasi tentang apa yang terjadi setelah lulus sekolah', '', '2026-03-28 11:32:39'),
('KS0002', 2, 2, 'Belajar', '2026-03-28', '12:00:00', '13:00:00', 'Selesai', 'konsultasi jurnal kimia', 'fika sudah lancar mengerjakan jurnal', '2026-03-28 12:00:10'),
('KS0003', 1, 1, 'Sosial', '2026-03-30', '07:00:00', '08:00:00', 'Disetujui', 'teman', '', '2026-03-29 14:39:44'),
('KS0004', 1, 1, 'Karir', '2026-03-30', '11:00:00', '12:00:00', 'Selesai', 'cita cita masadepan', 'andhika sudah mendapatkan tujuan hidupnya', '2026-03-30 01:21:19'),
('KS0006', 1, 1, 'Pribadi', '2026-04-09', '11:15:00', '13:15:00', 'Disetujui', 'aaaa', '', '2026-04-09 04:15:52'),
('KS0007', 1, 1, 'Pribadi', '2026-04-13', '12:00:00', NULL, 'Disetujui', 'jangan lupa hadir ya nak', NULL, '2026-04-12 09:50:20');

-- --------------------------------------------------------

--
-- Struktur dari tabel `log_aktivitas_dhika`
--

CREATE TABLE `log_aktivitas_dhika` (
  `id_log` int(11) NOT NULL,
  `akun_id` int(11) NOT NULL,
  `aktivitas` varchar(255) NOT NULL,
  `waktu` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
(140, 7, 'Login ke sistem', '2026-04-12 11:36:15');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pelanggaran_dhika`
--

CREATE TABLE `pelanggaran_dhika` (
  `id_pelanggaran` int(11) NOT NULL,
  `nama_pelanggaran` varchar(100) NOT NULL,
  `kategori` enum('Ringan','Sedang','Berat','Sangat Berat') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `pengaduan_dhika`
--

INSERT INTO `pengaduan_dhika` (`id_pengaduan`, `kesiswaan_id`, `siswa_id`, `judul`, `deskripsi`, `status`, `catatan`, `tanggal`) VALUES
(1, 1, 1, 'sering bolos', '2x bolos dalam seminggu', 'Diproses', NULL, '2026-04-12 09:48:36');

-- --------------------------------------------------------

--
-- Struktur dari tabel `riwayat_pelanggaran_dhika`
--

CREATE TABLE `riwayat_pelanggaran_dhika` (
  `id_riwayat` int(11) NOT NULL,
  `siswa_id` int(11) NOT NULL,
  `pelanggaran_id` int(11) NOT NULL,
  `tanggal` date NOT NULL,
  `keterangan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `riwayat_pelanggaran_dhika`
--

INSERT INTO `riwayat_pelanggaran_dhika` (`id_riwayat`, `siswa_id`, `pelanggaran_id`, `tanggal`, `keterangan`) VALUES
(1, 1, 3, '2026-03-30', '');

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
  `no_ortu` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `siswa_dhika`
--

INSERT INTO `siswa_dhika` (`id_siswa`, `akun_id`, `nis`, `nama`, `kelas`, `jurusan`, `rombel`, `email`, `no_ortu`) VALUES
(1, 4, '10243252', 'Andhika Andriana Putra', 'XI', 'RPL', 'A', 'andhika@gmail.com', '+6281223530650'),
(2, 5, '10245407', 'Fika Indah Lestari', 'XI', 'Kimia', 'A', 'fika@gmail.com', '+62895631922002'),
(11, 6, '10243249', 'Aditya Firmansyah Andira', 'XI', 'RPL', 'A', NULL, NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `wali_kelas_dhika`
--

CREATE TABLE `wali_kelas_dhika` (
  `id_walikelas` int(11) NOT NULL,
  `akun_id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `nip` varchar(20) DEFAULT NULL,
  `kelas` enum('X','XI','XII') NOT NULL,
  `jurusan` enum('RPL','Animasi','DKV','Kimia','Mesin','Meka') NOT NULL,
  `rombel` enum('A','B','C','D') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `wali_kelas_dhika`
--

INSERT INTO `wali_kelas_dhika` (`id_walikelas`, `akun_id`, `nama`, `nip`, `kelas`, `jurusan`, `rombel`) VALUES
(1, 8, 'Gigin Gantini Putri', '271918363829119', 'XI', 'RPL', 'A');

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
  MODIFY `id_akun` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT untuk tabel `chat_dhika`
--
ALTER TABLE `chat_dhika`
  MODIFY `id_chat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

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
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=141;

--
-- AUTO_INCREMENT untuk tabel `pelanggaran_dhika`
--
ALTER TABLE `pelanggaran_dhika`
  MODIFY `id_pelanggaran` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT untuk tabel `pengaduan_dhika`
--
ALTER TABLE `pengaduan_dhika`
  MODIFY `id_pengaduan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `riwayat_pelanggaran_dhika`
--
ALTER TABLE `riwayat_pelanggaran_dhika`
  MODIFY `id_riwayat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `siswa_dhika`
--
ALTER TABLE `siswa_dhika`
  MODIFY `id_siswa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

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
