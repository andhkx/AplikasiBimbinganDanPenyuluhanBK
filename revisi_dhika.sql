ALTER TABLE akun_dhika MODIFY COLUMN role ENUM('Siswa','Guru BK','Wali Kelas','Kesiswaan','Admin') NOT NULL;

ALTER TABLE siswa_dhika DROP COLUMN IF EXISTS total_poin;

ALTER TABLE pelanggaran_dhika DROP COLUMN IF EXISTS poin;

ALTER TABLE konseling_dhika MODIFY COLUMN jam_selesai TIME NULL DEFAULT NULL;

CREATE TABLE IF NOT EXISTS wali_kelas_dhika (
    id_walikelas INT AUTO_INCREMENT PRIMARY KEY,
    akun_id INT NOT NULL,
    nama VARCHAR(100) NOT NULL,
    nip VARCHAR(20),
    kelas ENUM('X','XI','XII') NOT NULL,
    jurusan ENUM('RPL','Animasi','DKV','Kimia','Mesin','Meka') NOT NULL,
    rombel ENUM('A','B','C','D') NOT NULL,
    FOREIGN KEY (akun_id) REFERENCES akun_dhika(id_akun) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS kesiswaan_dhika (
    id_kesiswaan INT AUTO_INCREMENT PRIMARY KEY,
    akun_id INT NOT NULL,
    nama VARCHAR(100) NOT NULL,
    nip VARCHAR(20),
    FOREIGN KEY (akun_id) REFERENCES akun_dhika(id_akun) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS admin_dhika (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    akun_id INT NOT NULL,
    nama VARCHAR(100) NOT NULL,
    FOREIGN KEY (akun_id) REFERENCES akun_dhika(id_akun) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pengaduan_dhika (
    id_pengaduan INT AUTO_INCREMENT PRIMARY KEY,
    guru_id INT NOT NULL,
    siswa_id INT NOT NULL,
    judul VARCHAR(200) NOT NULL,
    deskripsi TEXT NOT NULL,
    status ENUM('Baru','Diproses','Selesai') DEFAULT 'Baru',
    catatan_kesiswaan TEXT,
    tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guru_id) REFERENCES guru_dhika(id_guru) ON DELETE CASCADE,
    FOREIGN KEY (siswa_id) REFERENCES siswa_dhika(id_siswa) ON DELETE CASCADE
);

DROP TABLE IF EXISTS pendaftaran_dhika;

ALTER TABLE riwayat_pelanggaran_dhika DROP COLUMN IF EXISTS poin;

ALTER TABLE chat_dhika ADD COLUMN IF NOT EXISTS dibaca TINYINT(1) DEFAULT 0;

DROP TABLE IF EXISTS pengaduan_dhika;
CREATE TABLE pengaduan_dhika (
    id_pengaduan INT AUTO_INCREMENT PRIMARY KEY,
    kesiswaan_id INT NOT NULL,
    siswa_id INT NOT NULL,
    judul VARCHAR(200) NOT NULL,
    deskripsi TEXT NOT NULL,
    status ENUM('Baru','Diproses','Selesai') DEFAULT 'Baru',
    catatan TEXT,
    tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kesiswaan_id) REFERENCES kesiswaan_dhika(id_kesiswaan) ON DELETE CASCADE,
    FOREIGN KEY (siswa_id) REFERENCES siswa_dhika(id_siswa) ON DELETE CASCADE
);
