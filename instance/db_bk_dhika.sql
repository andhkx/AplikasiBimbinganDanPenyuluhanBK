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
