<<<<<<< HEAD
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 30 Mar 2026 pada 23.30
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
-- Struktur dari tabel `akun_dhika`
--

CREATE TABLE `akun_dhika` (
  `id_akun` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Siswa','Guru BK') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `akun_dhika`
--

INSERT INTO `akun_dhika` (`id_akun`, `username`, `password`, `role`, `created_at`) VALUES
(1, 'tini', 'tini123', 'Guru BK', '2026-03-28 08:55:06'),
(2, 'anom', 'anom123', 'Guru BK', '2026-03-28 08:55:06'),
(3, 'dudu', 'dudu123', 'Guru BK', '2026-03-28 08:55:06'),
(4, 'andhika', 'andhika123', 'Siswa', '2026-03-28 08:55:06'),
(5, 'fika', 'fika123', 'Siswa', '2026-03-28 08:55:06');

-- --------------------------------------------------------

--
-- Struktur dari tabel `chat_dhika`
--

CREATE TABLE `chat_dhika` (
  `id_chat` int(11) NOT NULL,
  `pengirim_akun_id` int(11) NOT NULL,
  `penerima_akun_id` int(11) NOT NULL,
  `pesan` text NOT NULL,
  `waktu` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `chat_dhika`
--

INSERT INTO `chat_dhika` (`id_chat`, `pengirim_akun_id`, `penerima_akun_id`, `pesan`, `waktu`) VALUES
(6, 4, 1, 'assalamualaikum ibu', '2026-03-29 14:38:49'),
(7, 4, 1, 'Halo, saya telah mengajukan konseling (Sosial) pada 2026-03-30 pukul 07:00-08:00. Mohon konfirmasinya. Terima kasih.', '2026-03-29 14:39:44'),
(8, 1, 4, 'oke nak', '2026-03-29 14:42:02'),
(9, 5, 2, 'terimakasih pak', '2026-03-29 15:15:24'),
(10, 2, 5, 'sama sama nak', '2026-03-29 15:16:38'),
(11, 4, 1, 'Halo, saya telah mengajukan konseling (Karir) pada 2026-03-30 pukul 11:00-12:00. Mohon konfirmasinya. Terima kasih.', '2026-03-30 01:21:19'),
(12, 4, 1, 'bu saya mau konseling', '2026-03-30 01:21:41'),
(13, 1, 4, 'selesai ya nak', '2026-03-30 01:24:07'),
(14, 4, 1, 'halo bu', '2026-03-30 01:25:53'),
(15, 4, 1, 'p', '2026-03-30 01:25:56');

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
-- Struktur dari tabel `konseling_dhika`
--

CREATE TABLE `konseling_dhika` (
  `id_konseling` varchar(20) NOT NULL,
  `siswa_id` int(11) NOT NULL,
  `guru_id` int(11) NOT NULL,
  `jenis` enum('Pribadi','Sosial','Belajar','Karir') NOT NULL,
  `tanggal` date NOT NULL,
  `jam_mulai` time NOT NULL,
  `jam_selesai` time NOT NULL,
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
('KS0004', 1, 1, 'Karir', '2026-03-30', '11:00:00', '12:00:00', 'Selesai', 'cita cita masadepan', 'andhika sudah mendapatkan tujuan hidupnya', '2026-03-30 01:21:19');

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
(65, 4, 'Login ke sistem', '2026-03-30 22:18:30');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pelanggaran_dhika`
--

CREATE TABLE `pelanggaran_dhika` (
  `id_pelanggaran` int(11) NOT NULL,
  `nama_pelanggaran` varchar(100) NOT NULL,
  `poin` int(11) NOT NULL,
  `kategori` enum('Ringan','Sedang','Berat','Sangat Berat') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `pelanggaran_dhika`
--

INSERT INTO `pelanggaran_dhika` (`id_pelanggaran`, `nama_pelanggaran`, `poin`, `kategori`) VALUES
(1, 'Terlambat', 5, 'Ringan'),
(2, 'Tidak memakai atribut lengkap', 5, 'Ringan'),
(3, 'Rambut tidak rapi', 10, 'Ringan'),
(4, 'Tidak mengerjakan tugas', 10, 'Sedang'),
(5, 'Keluar kelas tanpa izin', 10, 'Sedang'),
(6, 'Bolos 1 jam', 15, 'Sedang'),
(7, 'Bolos 1 hari', 30, 'Berat'),
(8, 'Berkelahi', 50, 'Berat'),
(9, 'Merokok', 50, 'Berat'),
(10, 'Membawa barang terlarang', 75, 'Sangat Berat'),
(11, 'Narkoba', 100, 'Sangat Berat');

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
  `total_poin` int(11) DEFAULT 0,
  `no_ortu` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data untuk tabel `siswa_dhika`
--

INSERT INTO `siswa_dhika` (`id_siswa`, `akun_id`, `nis`, `nama`, `kelas`, `jurusan`, `rombel`, `email`, `total_poin`, `no_ortu`) VALUES
(1, 4, '10243252', 'Andhika Andriana Putra', 'XI', 'RPL', 'A', 'andhika@gmail.com', 10, NULL),
(2, 5, '10245407', 'Fika Indah Lestari', 'XI', 'Kimia', 'A', 'fika@gmail.com', 0, NULL);

--
-- Indexes for dumped tables
--

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
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `akun_dhika`
--
ALTER TABLE `akun_dhika`
  MODIFY `id_akun` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `chat_dhika`
--
ALTER TABLE `chat_dhika`
  MODIFY `id_chat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT untuk tabel `guru_dhika`
--
ALTER TABLE `guru_dhika`
  MODIFY `id_guru` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `log_aktivitas_dhika`
--
ALTER TABLE `log_aktivitas_dhika`
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- AUTO_INCREMENT untuk tabel `pelanggaran_dhika`
--
ALTER TABLE `pelanggaran_dhika`
  MODIFY `id_pelanggaran` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT untuk tabel `riwayat_pelanggaran_dhika`
--
ALTER TABLE `riwayat_pelanggaran_dhika`
  MODIFY `id_riwayat` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `siswa_dhika`
--
ALTER TABLE `siswa_dhika`
  MODIFY `id_siswa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

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
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
=======
-- Database untuk Aplikasi Bimbingan dan Penyuluhan / BK
-- Dibuat oleh: Andhika Andriana Putra
-- SMK Negeri 2 Cimahi

-- Buat database
CREATE DATABASE IF NOT EXISTS db_bk_dhika;
USE db_bk_dhika;

-- Tabel 1: akun_dhika
CREATE TABLE akun_dhika (
    id_akun INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('Siswa', 'Guru BK', 'Admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert 5 data akun_dhika
INSERT INTO akun_dhika (username, password, role) VALUES
('admin_dhika', 'admin123', 'Admin'),
('guru_bk1', 'guru123', 'Guru BK'),
('guru_bk2', 'guru123', 'Guru BK'),
('siswa001', 'siswa123', 'Siswa'),
('siswa002', 'siswa123', 'Siswa');

-- Tabel 2: siswa_dhika
CREATE TABLE siswa_dhika (
    id_siswa INT PRIMARY KEY AUTO_INCREMENT,
    akun_id INT NOT NULL,
    nis VARCHAR(20) NOT NULL UNIQUE,
    nama VARCHAR(100) NOT NULL,
    kelas VARCHAR(10) NOT NULL,
    jurusan VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    FOREIGN KEY (akun_id) REFERENCES akun_dhika(id_akun) ON DELETE CASCADE
);

-- Insert 5 data siswa_dhika
INSERT INTO siswa_dhika (akun_id, nis, nama, kelas, jurusan, email) VALUES
(4, '2024001', 'Budi Santoso', 'XI RPL A', 'Rekayasa Perangkat Lunak', 'budi@student.smkn2cimahi.sch.id'),
(5, '2024002', 'Siti Nurhaliza', 'XI RPL A', 'Rekayasa Perangkat Lunak', 'siti@student.smkn2cimahi.sch.id'),
(4, '2024003', 'Dimas Prasetyo', 'XI TKJ B', 'Teknik Komputer Jaringan', 'dimas@student.smkn2cimahi.sch.id'),
(5, '2024004', 'Rina Wijaya', 'XI MM A', 'Multimedia', 'rina@student.smkn2cimahi.sch.id'),
(4, '2024005', 'Ahmad Fauzi', 'XI RPL B', 'Rekayasa Perangkat Lunak', 'ahmad@student.smkn2cimahi.sch.id');

-- Tabel 3: guru_dhika
CREATE TABLE guru_dhika (
    id_guru INT PRIMARY KEY AUTO_INCREMENT,
    akun_id INT NOT NULL,
    nip VARCHAR(20) NOT NULL UNIQUE,
    nama VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    FOREIGN KEY (akun_id) REFERENCES akun_dhika(id_akun) ON DELETE CASCADE
);

-- Insert 5 data guru_dhika
INSERT INTO guru_dhika (akun_id, nip, nama, email) VALUES
(2, '197801012006041001', 'Dra. Siti Aminah, M.Pd', 'siti.aminah@smkn2cimahi.sch.id'),
(3, '198505152010122002', 'Drs. Bambang Sudrajat', 'bambang.sudrajat@smkn2cimahi.sch.id'),
(2, '199002282015031003', 'Rina Marlina, S.Pd', 'rina.marlina@smkn2cimahi.sch.id'),
(3, '198712102012121004', 'Agus Setiawan, S.Psi', 'agus.setiawan@smkn2cimahi.sch.id'),
(2, '199306192018032005', 'Fitri Handayani, M.Psi', 'fitri.handayani@smkn2cimahi.sch.id');

-- Tabel 4: konseling_dhika
CREATE TABLE konseling_dhika (
    id_konseling VARCHAR(20) PRIMARY KEY,
    siswa_id INT NOT NULL,
    guru_id INT NOT NULL,
    jenis ENUM('Pribadi', 'Sosial', 'Belajar', 'Karir') NOT NULL,
    tanggal DATE NOT NULL,
    jam_mulai TIME NOT NULL,
    jam_selesai TIME NOT NULL,
    status ENUM('Pending', 'Disetujui', 'Selesai', 'Dibatalkan') DEFAULT 'Pending',
    alasan TEXT NOT NULL,
    hasil TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (siswa_id) REFERENCES siswa_dhika(id_siswa) ON DELETE CASCADE,
    FOREIGN KEY (guru_id) REFERENCES guru_dhika(id_guru) ON DELETE CASCADE
);

-- Insert 5 data konseling_dhika
INSERT INTO konseling_dhika (id_konseling, siswa_id, guru_id, jenis, tanggal, jam_mulai, jam_selesai, status, alasan, hasil) VALUES
('KSL001', 1, 1, 'Belajar', '2026-02-08', '08:00:00', '09:00:00', 'Selesai', 'Kesulitan memahami materi pemrograman Python', 'Diberikan metode belajar step by step dan latihan tambahan'),
('KSL002', 2, 2, 'Pribadi', '2026-02-09', '10:00:00', '11:00:00', 'Selesai', 'Masalah kepercayaan diri saat presentasi', 'Diberikan tips public speaking dan latihan mental'),
('KSL003', 3, 1, 'Sosial', '2026-02-10', '13:00:00', '14:00:00', 'Disetujui', 'Kesulitan beradaptasi dengan teman sekelas', NULL),
('KSL004', 4, 3, 'Karir', '2026-02-11', '09:00:00', '10:00:00', 'Pending', 'Konsultasi pemilihan jurusan kuliah', NULL),
('KSL005', 5, 2, 'Belajar', '2026-02-12', '14:00:00', '15:00:00', 'Pending', 'Kesulitan manajemen waktu belajar', NULL);

-- Tabel 5: chat_dhika
CREATE TABLE chat_dhika (
    id_chat INT PRIMARY KEY AUTO_INCREMENT,
    pengirim_akun_id INT NOT NULL,
    penerima_akun_id INT NOT NULL,
    pesan TEXT NOT NULL,
    waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pengirim_akun_id) REFERENCES akun_dhika(id_akun) ON DELETE CASCADE,
    FOREIGN KEY (penerima_akun_id) REFERENCES akun_dhika(id_akun) ON DELETE CASCADE
);

-- Insert 5 data chat_dhika
INSERT INTO chat_dhika (pengirim_akun_id, penerima_akun_id, pesan, waktu) VALUES
(4, 2, 'Selamat pagi Bu, saya ingin konsultasi mengenai kesulitan belajar', '2026-02-08 07:30:00'),
(2, 4, 'Baik, silahkan ajukan jadwal konseling melalui sistem', '2026-02-08 07:45:00'),
(5, 3, 'Pak, kapan jadwal konseling saya?', '2026-02-09 09:00:00'),
(3, 5, 'Jadwal konseling kamu sudah disetujui untuk besok jam 10:00', '2026-02-09 09:15:00'),
(4, 2, 'Terima kasih Bu atas bimbingannya kemarin', '2026-02-08 15:00:00');

-- Tabel 6: log_aktivitas_dhika
CREATE TABLE log_aktivitas_dhika (
    id_log INT PRIMARY KEY AUTO_INCREMENT,
    akun_id INT NOT NULL,
    aktivitas VARCHAR(255) NOT NULL,
    waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (akun_id) REFERENCES akun_dhika(id_akun) ON DELETE CASCADE
);

-- Insert 5 data log_aktivitas_dhika
INSERT INTO log_aktivitas_dhika (akun_id, aktivitas, waktu) VALUES
(4, 'Login ke sistem', '2026-02-08 07:25:00'),
(4, 'Mengajukan konseling baru - KSL001', '2026-02-08 07:35:00'),
(2, 'Login ke sistem', '2026-02-08 07:40:00'),
(2, 'Menyetujui konseling - KSL001', '2026-02-08 07:50:00'),
(4, 'Menyelesaikan konseling - KSL001', '2026-02-08 09:05:00');
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
