<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
import mysql.connector
from fpdf import FPDF
from datetime import datetime, timedelta
=======
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
import mysql.connector
from fpdf import FPDF
from datetime import datetime, timedelta
import hashlib
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a

app = Flask(__name__)
app.secret_key = 'andhika_bk_smk2_2026'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

<<<<<<< HEAD

def get_db_connection_dhika():
    try:
        conn = mysql.connector.connect(
            host='192.168.100.8',
            port=3306,
            user='dhika',
            password='123',
            database='db_bk_dhika'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"DB error: {err}")
        return None


def flash_dhika(message, category='info'):
    session['flash_message'] = message
    session['flash_category'] = category


def get_flash_dhika():
    message = session.pop('flash_message', None)
    category = session.pop('flash_category', None)
    return message, category


def log_aktivitas_dhika(akun_id, aktivitas):
    try:
        conn = get_db_connection_dhika()
        if conn:
            cursor = conn.cursor(buffered=True)
            cursor.execute(
                "INSERT INTO log_aktivitas_dhika (akun_id, aktivitas) VALUES (%s, %s)",
                (akun_id, aktivitas)
            )
=======
# ==================== KONEKSI DATABASE ====================
def get_db_connection_dhika():
    """Fungsi untuk koneksi database"""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_bk_dhika',
            autocommit=True
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None

# ==================== FUNGSI HELPER ====================
def hash_password_dhika(password):
    """Hash password dengan SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_id_dhika(prefix, last_id):
    """Generate ID dengan format (prefix + 4 digit)"""
    if last_id and last_id[0].startswith(prefix):
        num = int(last_id[0][len(prefix):]) + 1
    else:
        num = 1
    return f"{prefix}{num:04d}"

def log_aktivitas_dhika(akun_id, aktivitas):
    """Fungsi untuk mencatat aktivitas pengguna"""
    try:
        conn = get_db_connection_dhika()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO log_aktivitas (akun_id, aktivitas) 
                VALUES (%s, %s)
            """, (akun_id, aktivitas))
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
<<<<<<< HEAD
        print(f"Log error: {e}")


def get_status_pelanggaran_dhika(total_poin):
    if total_poin <= 50:
        return 'Aman'
    elif total_poin <= 100:
        return 'Peringatan'
    elif total_poin <= 150:
        return 'SP1'
    elif total_poin <= 200:
        return 'SP2'
    return 'SP3'


def reset_poin_semester_dhika():
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        cursor.execute("UPDATE siswa_dhika SET total_poin = 0")
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


@app.template_filter('format_tanggal_dhika')
def format_tanggal_dhika(value):
    if isinstance(value, str):
        try:
            return datetime.strptime(value, '%Y-%m-%d').strftime('%d/%m/%Y')
        except Exception:
            return value
    return value


@app.template_filter('status_badge_dhika')
def status_badge_dhika(status):
    badges = {
        'Pending': 'warning',
        'Disetujui': 'success',
        'Selesai': 'primary',
        'Dibatalkan': 'danger'
    }
    return badges.get(status, 'secondary')


@app.context_processor
def inject_variables_dhika():
    return dict(get_flash_dhika=get_flash_dhika, now=datetime.now())


@app.errorhandler(404)
def page_not_found_dhika(e):
    return render_template('404_dhika.html'), 404


@app.errorhandler(500)
def server_error_dhika(e):
    return render_template('500_dhika.html'), 500


@app.route('/')
def home_dhika():
    return redirect(url_for('login_dhika'))


@app.route('/login', methods=['GET', 'POST'])
def login_dhika():
    if request.method == 'POST':
        username = request.form.get('username_dhika', '').strip()
        password = request.form.get('password_dhika', '').strip()
        if not username or not password:
            flash_dhika('Username dan password harus diisi!', 'error')
            return render_template('auth/login_dhika.html')
=======
        print(f"Error logging: {e}")

# ==================== ROUTE UTAMA ====================
@app.route('/')
def home_dhika():
    """Halaman utama - redirect ke login"""
    return redirect(url_for('login_dhika'))

@app.route('/login', methods=['GET', 'POST'])
def login_dhika():
    """Halaman login"""
    if request.method == 'POST':
        username = request.form.get('username_dhika', '').strip()
        password = request.form.get('password_dhika', '').strip()
        
        if not username or not password:
            flash_dhika('Username dan password harus diisi!', 'error')
            return render_template('login_dhika.html')
        
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
        try:
            conn = get_db_connection_dhika()
            if not conn:
                flash_dhika('Database connection error!', 'error')
<<<<<<< HEAD
                return render_template('auth/login_dhika.html')
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute("""
                SELECT a.*,
                       s.id_siswa, s.nama as nama_siswa, s.kelas, s.jurusan,
                       g.id_guru, g.nama as nama_guru
                FROM akun_dhika a
                LEFT JOIN siswa_dhika s ON a.id_akun = s.akun_id
                LEFT JOIN guru_dhika g ON a.id_akun = g.akun_id
                WHERE a.username = %s
            """, (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user and user['password'] == password:
                if user.get('status_akun') == 'Pending':
                    flash_dhika('Akun kamu masih menunggu persetujuan Guru BK.', 'error')
                    return render_template('auth/login_dhika.html')
                if user.get('status_akun') == 'Nonaktif':
                    flash_dhika('Akun kamu telah dinonaktifkan. Hubungi Guru BK.', 'error')
                    return render_template('auth/login_dhika.html')
=======
                return render_template('login_dhika.html')
            
            cursor = conn.cursor(dictionary=True)
            
            # Cari user berdasarkan username
            cursor.execute("""
                SELECT a.*, 
                       s.id_siswa, s.nama as nama_siswa, s.kelas, s.jurusan,
                       g.id_guru, g.nama as nama_guru
                FROM akun a
                LEFT JOIN siswa s ON a.id_akun = s.akun_id
                LEFT JOIN guru g ON a.id_akun = g.akun_id
                WHERE a.username = %s
            """, (username,))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user and user['password'] == hash_password_dhika(password):
                # Set session
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
                session.permanent = True
                session['logged_in'] = True
                session['id_akun'] = user['id_akun']
                session['username'] = user['username']
                session['role'] = user['role']
<<<<<<< HEAD
                session['nama'] = user['nama_siswa'] if user['role'] == 'Siswa' else user['nama_guru']
                log_aktivitas_dhika(user['id_akun'], 'Login ke sistem')
                if user['role'] == 'Siswa':
                    return redirect(url_for('dashboard_siswa_dhika'))
                return redirect(url_for('dashboard_guru_dhika'))
            else:
                flash_dhika('Username atau password salah!', 'error')
        except Exception as e:
            flash_dhika(f'Login error: {str(e)}', 'error')
    return render_template('auth/login_dhika.html')


@app.route('/logout')
def logout_dhika():
=======
                session['nama'] = user['nama_siswa'] if user['role'] == 'siswa' else user['nama_guru']
                
                # Log aktivitas
                log_aktivitas_dhika(user['id_akun'], 'Login ke sistem')
                
                # Redirect berdasarkan role
                if user['role'] == 'siswa':
                    return redirect(url_for('dashboard_siswa_dhika'))
                else:  # guru
                    return redirect(url_for('dashboard_guru_dhika'))
            else:
                flash_dhika('Username atau password salah!', 'error')
                
        except Exception as e:
            flash_dhika(f'Login error: {str(e)}', 'error')
    
    return render_template('login_dhika.html')

@app.route('/logout')
def logout_dhika():
    """Logout user"""
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
    if 'id_akun' in session:
        log_aktivitas_dhika(session['id_akun'], 'Logout dari sistem')
    session.clear()
    flash_dhika('Anda telah logout!', 'success')
    return redirect(url_for('login_dhika'))

<<<<<<< HEAD

@app.route('/register', methods=['GET', 'POST'])
def register_dhika():
    if request.method == 'POST':
        username = request.form.get('username_dhika', '').strip()
        password = request.form.get('password_dhika', '').strip()
        konfirmasi = request.form.get('konfirmasi_dhika', '').strip()
        nis = request.form.get('nis_dhika', '').strip()
        nama = request.form.get('nama_dhika', '').strip()
        kelas = request.form.get('kelas_dhika', '').strip()
        jurusan = request.form.get('jurusan_dhika', '').strip()
        rombel = request.form.get('rombel_dhika', '').strip()
        no_ortu = request.form.get('no_ortu_dhika', '').strip()
        if not all([username, password, konfirmasi, nis, nama, kelas, jurusan, rombel]):
            flash_dhika('Semua field wajib harus diisi!', 'error')
            return render_template('auth/register_dhika.html')
        if password != konfirmasi:
            flash_dhika('Password dan konfirmasi tidak sama!', 'error')
            return render_template('auth/register_dhika.html')
        if len(password) < 6:
            flash_dhika('Password minimal 6 karakter!', 'error')
            return render_template('auth/register_dhika.html')
        try:
            conn = get_db_connection_dhika()
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT id_akun FROM akun_dhika WHERE username = %s", (username,))
            if cursor.fetchone():
                flash_dhika('Username sudah dipakai!', 'error')
                cursor.close()
                conn.close()
                return render_template('auth/register_dhika.html')
            cursor.execute(
                "SELECT id_daftar FROM pendaftaran_dhika WHERE nis = %s AND status_daftar = 'Pending'",
                (nis,)
            )
            if cursor.fetchone():
                flash_dhika('NIS ini sudah memiliki pendaftaran yang sedang diproses!', 'error')
                cursor.close()
                conn.close()
                return render_template('auth/register_dhika.html')
            cursor.execute("""
                INSERT INTO pendaftaran_dhika (username, password, nis, nama, kelas, jurusan, rombel, no_ortu)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (username, password, nis, nama, kelas, jurusan, rombel, no_ortu or None))
            conn.commit()
            cursor.close()
            conn.close()
            flash_dhika('Pendaftaran berhasil! Tunggu persetujuan Guru BK.', 'success')
            return redirect(url_for('login_dhika'))
        except Exception as e:
            flash_dhika(f'Error: {str(e)}', 'error')
    return render_template('auth/register_dhika.html')


@app.route('/konseling/siswa')
def konseling_siswa_dhika():
    if 'logged_in' not in session or session.get('role') != 'Siswa':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_siswa FROM siswa_dhika WHERE akun_id = %s", (session['id_akun'],))
        siswa = cursor.fetchone()
        cursor.execute("""
            SELECT k.*, g.nama as nama_guru
            FROM konseling_dhika k
            JOIN guru_dhika g ON k.guru_id = g.id_guru
=======
# ==================== MANAJEMEN KONSELING ====================
@app.route('/konseling/siswa')
def konseling_siswa_dhika():
    """Halaman konseling untuk siswa"""
    if 'logged_in' not in session or session.get('role') != 'siswa':
        return redirect(url_for('login_dhika'))
    
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True)
        
        # Ambil id siswa
        cursor.execute("SELECT id_siswa FROM siswa WHERE akun_id = %s", (session['id_akun'],))
        siswa = cursor.fetchone()
        
        # Ambil daftar konseling
        cursor.execute("""
            SELECT k.*, g.nama as nama_guru 
            FROM konseling k
            JOIN guru g ON k.guru_id = g.id_guru
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
            WHERE k.siswa_id = %s
            ORDER BY k.tanggal DESC, k.jam_mulai DESC
        """, (siswa['id_siswa'],))
        konseling_list = cursor.fetchall()
<<<<<<< HEAD
        cursor.execute("SELECT id_guru, nama FROM guru_dhika")
        guru_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('konseling/konseling_siswa_dhika.html',
                               konseling_list=konseling_list,
                               guru_list=guru_list)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('konseling/konseling_siswa_dhika.html')


@app.route('/konseling/guru')
def konseling_guru_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_guru FROM guru_dhika WHERE akun_id = %s", (session['id_akun'],))
        guru = cursor.fetchone()
        cursor.execute("""
            SELECT k.*, s.nama as nama_siswa, s.kelas, s.jurusan
            FROM konseling_dhika k
            JOIN siswa_dhika s ON k.siswa_id = s.id_siswa
=======
        
        # Ambil daftar guru
        cursor.execute("SELECT id_guru, nama FROM guru")
        guru_list = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('konseling_siswa_dhika.html',
                             konseling_list=konseling_list,
                             guru_list=guru_list)
        
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('konseling_siswa_dhika.html')

@app.route('/konseling/guru')
def konseling_guru_dhika():
    """Halaman konseling untuk guru"""
    if 'logged_in' not in session or session.get('role') != 'guru':
        return redirect(url_for('login_dhika'))
    
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True)
        
        # Ambil id guru
        cursor.execute("SELECT id_guru FROM guru WHERE akun_id = %s", (session['id_akun'],))
        guru = cursor.fetchone()
        
        # Ambil daftar konseling
        cursor.execute("""
            SELECT k.*, s.nama as nama_siswa, s.kelas, s.jurusan 
            FROM konseling k
            JOIN siswa s ON k.siswa_id = s.id_siswa
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
            WHERE k.guru_id = %s
            ORDER BY k.tanggal DESC, k.jam_mulai DESC
        """, (guru['id_guru'],))
        konseling_list = cursor.fetchall()
<<<<<<< HEAD
        cursor.close()
        conn.close()
        return render_template('konseling/konseling_guru_dhika.html', konseling_list=konseling_list)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('konseling/konseling_guru_dhika.html')


@app.route('/konseling/ajukan', methods=['POST'])
def ajukan_konseling_dhika():
    if 'logged_in' not in session or session.get('role') != 'Siswa':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT id_konseling FROM konseling_dhika ORDER BY id_konseling DESC LIMIT 1")
        last = cursor.fetchone()
        if last and last[0].startswith('KS'):
            num = int(last[0][2:]) + 1
        else:
            num = 1
        id_konseling = f"KS{num:04d}"
        cursor.execute("SELECT id_siswa FROM siswa_dhika WHERE akun_id = %s", (session['id_akun'],))
        siswa = cursor.fetchone()
=======
        
        cursor.close()
        conn.close()
        
        return render_template('konseling_guru_dhika.html',
                             konseling_list=konseling_list)
        
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('konseling_guru_dhika.html')

@app.route('/konseling/ajukan', methods=['POST'])
def ajukan_konseling_dhika():
    """Ajukan konseling baru"""
    if 'logged_in' not in session or session.get('role') != 'siswa':
        return redirect(url_for('login_dhika'))
    
    try:
        # Generate ID konseling
        conn = get_db_connection_dhika()
        cursor = conn.cursor()
        cursor.execute("SELECT id_konseling FROM konseling ORDER BY id_konseling DESC LIMIT 1")
        last_id = cursor.fetchone()
        id_konseling = generate_id_dhika('KS', last_id)
        
        # Ambil id siswa
        cursor.execute("SELECT id_siswa FROM siswa WHERE akun_id = %s", (session['id_akun'],))
        siswa = cursor.fetchone()
        
        # Ambil data dari form
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
        guru_id = request.form.get('guru_id_dhika')
        jenis = request.form.get('jenis_dhika')
        tanggal = request.form.get('tanggal_dhika')
        jam_mulai = request.form.get('jam_mulai_dhika')
        jam_selesai = request.form.get('jam_selesai_dhika')
        alasan = request.form.get('alasan_dhika')
<<<<<<< HEAD
        if not all([guru_id, jenis, tanggal, jam_mulai, jam_selesai, alasan]):
            flash_dhika('Semua field harus diisi!', 'error')
            return redirect(url_for('konseling_siswa_dhika'))
        cursor.execute("""
            INSERT INTO konseling_dhika
            (id_konseling, siswa_id, guru_id, jenis, tanggal, jam_mulai, jam_selesai, alasan, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
        """, (id_konseling, siswa[0], guru_id, jenis, tanggal, jam_mulai, jam_selesai, alasan))
        conn.commit()
        try:
            conn2 = get_db_connection_dhika()
            cur2 = conn2.cursor(buffered=True)
            cur2.execute("SELECT akun_id FROM guru_dhika WHERE id_guru = %s", (guru_id,))
            guru_row = cur2.fetchone()
            if guru_row:
                pesan = f"Halo, saya telah mengajukan konseling ({jenis}) pada {tanggal} pukul {jam_mulai}-{jam_selesai}. Mohon konfirmasinya."
                cur2.execute(
                    "INSERT INTO chat_dhika (pengirim_akun_id, penerima_akun_id, pesan) VALUES (%s, %s, %s)",
                    (session['id_akun'], guru_row[0], pesan)
                )
                conn2.commit()
            cur2.close()
            conn2.close()
        except Exception:
            pass
        log_aktivitas_dhika(session['id_akun'], f'Mengajukan konseling {id_konseling}')
        cursor.close()
        conn.close()
        flash_dhika('Konseling berhasil diajukan! Chat dengan guru sudah aktif.', 'success')
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('konseling_siswa_dhika'))


@app.route('/konseling/update/<id_konseling>', methods=['POST'])
def update_konseling_dhika(id_konseling):
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        status = request.form.get('status_dhika')
        hasil = request.form.get('hasil_dhika', '')
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        cursor.execute(
            "UPDATE konseling_dhika SET status = %s, hasil = %s WHERE id_konseling = %s",
            (status, hasil, id_konseling)
        )
        conn.commit()
        log_aktivitas_dhika(session['id_akun'], f'Update konseling {id_konseling} ke {status}')
        cursor.close()
        conn.close()
        flash_dhika('Status konseling berhasil diupdate!', 'success')
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('konseling_guru_dhika'))


@app.route('/konseling/delete/<id_konseling>', methods=['POST'])
def delete_konseling_dhika(id_konseling):
    if 'logged_in' not in session:
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT siswa_id FROM konseling_dhika WHERE id_konseling = %s", (id_konseling,))
        konseling = cursor.fetchone()
        if not konseling:
            flash_dhika('Konseling tidak ditemukan!', 'error')
            return redirect(url_for('konseling_siswa_dhika'))
        cursor.execute("SELECT id_siswa FROM siswa_dhika WHERE akun_id = %s", (session['id_akun'],))
        siswa = cursor.fetchone()
        if session['role'] == 'Siswa' and siswa[0] == konseling[0]:
            cursor.execute("DELETE FROM konseling_dhika WHERE id_konseling = %s", (id_konseling,))
=======
        
        # Validasi
        if not all([guru_id, jenis, tanggal, jam_mulai, jam_selesai, alasan]):
            flash_dhika('Semua field harus diisi!', 'error')
            return redirect(url_for('konseling_siswa_dhika'))
        
        # Insert ke database
        cursor.execute("""
            INSERT INTO konseling 
            (id_konseling, siswa_id, guru_id, jenis, tanggal, jam_mulai, jam_selesai, alasan, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'pending')
        """, (id_konseling, siswa[0], guru_id, jenis, tanggal, jam_mulai, jam_selesai, alasan))
        
        conn.commit()
        
        # Log aktivitas
        log_aktivitas_dhika(session['id_akun'], f'Mengajukan konseling {id_konseling}')
        
        cursor.close()
        conn.close()
        
        flash_dhika('Konseling berhasil diajukan!', 'success')
        
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('konseling_siswa_dhika'))

@app.route('/konseling/update/<id_konseling>', methods=['POST'])
def update_konseling_dhika(id_konseling):
    """Update status konseling"""
    if 'logged_in' not in session or session.get('role') != 'guru':
        return redirect(url_for('login_dhika'))
    
    try:
        status = request.form.get('status_dhika')
        hasil = request.form.get('hasil_dhika', '')
        
        conn = get_db_connection_dhika()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE konseling 
            SET status = %s, hasil = %s 
            WHERE id_konseling = %s
        """, (status, hasil, id_konseling))
        
        conn.commit()
        
        # Log aktivitas
        log_aktivitas_dhika(session['id_akun'], f'Update konseling {id_konseling} ke status {status}')
        
        cursor.close()
        conn.close()
        
        flash_dhika(f'Status konseling berhasil diupdate!', 'success')
        
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('konseling_guru_dhika'))

# ==================== LAPORAN ====================
@app.route('/laporan')
def laporan_dhika():
    """Halaman laporan"""
    if 'logged_in' not in session:
        return redirect(url_for('login_dhika'))
    
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True)
        
        # Query berdasarkan role
        if session['role'] == 'guru':
            cursor.execute("SELECT id_guru FROM guru WHERE akun_id = %s", (session['id_akun'],))
            guru = cursor.fetchone()
            
            cursor.execute("""
                SELECT k.*, s.nama as nama_siswa, s.kelas, s.jurusan,
                       g.nama as nama_guru
                FROM konseling k
                JOIN siswa s ON k.siswa_id = s.id_siswa
                JOIN guru g ON k.guru_id = g.id_guru
                WHERE k.guru_id = %s
                ORDER BY k.tanggal DESC
            """, (guru['id_guru'],))
        else:  # admin atau semua data untuk guru tertentu
            cursor.execute("""
                SELECT k.*, s.nama as nama_siswa, s.kelas, s.jurusan,
                       g.nama as nama_guru
                FROM konseling k
                JOIN siswa s ON k.siswa_id = s.id_siswa
                JOIN guru g ON k.guru_id = g.id_guru
                ORDER BY k.tanggal DESC
            """)
        
        laporan = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('laporan_konseling_dhika.html', laporan=laporan)
        
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('laporan_konseling_dhika.html')

@app.route('/konseling/delete/<id_konseling>', methods=['POST'])
def delete_konseling_dhika(id_konseling):
    """Hapus konseling"""
    if 'logged_in' not in session:
        return redirect(url_for('login_dhika'))
    
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor()
        
        # Cek apakah user berhak menghapus
        cursor.execute("SELECT siswa_id FROM konseling WHERE id_konseling = %s", (id_konseling,))
        konseling = cursor.fetchone()
        
        if not konseling:
            flash_dhika('Konseling tidak ditemukan!', 'error')
            return redirect(url_for('konseling_siswa_dhika'))
        
        # Hanya siswa pemilik yang bisa hapus
        cursor.execute("SELECT id_siswa FROM siswa WHERE akun_id = %s", (session['id_akun'],))
        siswa = cursor.fetchone()
        
        if session['role'] == 'siswa' and siswa[0] == konseling[0]:
            cursor.execute("DELETE FROM konseling WHERE id_konseling = %s", (id_konseling,))
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
            conn.commit()
            flash_dhika('Konseling berhasil dibatalkan!', 'success')
        else:
            flash_dhika('Anda tidak berhak menghapus konseling ini!', 'error')
<<<<<<< HEAD
        cursor.close()
        conn.close()
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('konseling_siswa_dhika'))


@app.route('/laporan')
def laporan_dhika():
    if 'logged_in' not in session:
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        if session['role'] == 'Guru BK':
            cursor.execute("SELECT id_guru FROM guru_dhika WHERE akun_id = %s", (session['id_akun'],))
            guru = cursor.fetchone()
            guru_id = guru['id_guru']
            cursor.execute("""
                SELECT k.*, s.nama as nama_siswa, s.kelas, s.jurusan, g.nama as nama_guru
                FROM konseling_dhika k
                JOIN siswa_dhika s ON k.siswa_id = s.id_siswa
                JOIN guru_dhika g ON k.guru_id = g.id_guru
                WHERE k.guru_id = %s
                ORDER BY k.tanggal DESC
            """, (guru_id,))
            laporan = cursor.fetchall()
            cursor.execute("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN status='Pending' THEN 1 ELSE 0 END) as pending,
                       SUM(CASE WHEN status='Disetujui' THEN 1 ELSE 0 END) as disetujui,
                       SUM(CASE WHEN status='Selesai' THEN 1 ELSE 0 END) as selesai,
                       SUM(CASE WHEN status='Dibatalkan' THEN 1 ELSE 0 END) as dibatalkan
                FROM konseling_dhika WHERE guru_id = %s
            """, (guru_id,))
            stats = cursor.fetchone()
            cursor.execute("""
                SELECT jenis, COUNT(*) as jumlah
                FROM konseling_dhika WHERE guru_id = %s
                GROUP BY jenis ORDER BY jumlah DESC
            """, (guru_id,))
            jenis_stats = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('laporan/laporan_guru_dhika.html', laporan=laporan, stats=stats, jenis_stats=jenis_stats)
        else:
            cursor.execute("SELECT id_siswa FROM siswa_dhika WHERE akun_id = %s", (session['id_akun'],))
            siswa_row = cursor.fetchone()
            siswa_id = siswa_row['id_siswa']
            cursor.execute("""
                SELECT k.*, g.nama as nama_guru
                FROM konseling_dhika k
                JOIN guru_dhika g ON k.guru_id = g.id_guru
                WHERE k.siswa_id = %s
                ORDER BY k.tanggal DESC
            """, (siswa_id,))
            laporan = cursor.fetchall()
            cursor.execute("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN status='Pending' THEN 1 ELSE 0 END) as pending,
                       SUM(CASE WHEN status='Disetujui' THEN 1 ELSE 0 END) as disetujui,
                       SUM(CASE WHEN status='Selesai' THEN 1 ELSE 0 END) as selesai,
                       SUM(CASE WHEN status='Dibatalkan' THEN 1 ELSE 0 END) as dibatalkan
                FROM konseling_dhika WHERE siswa_id = %s
            """, (siswa_id,))
            stats = cursor.fetchone()
            cursor.execute("""
                SELECT jenis, COUNT(*) as jumlah
                FROM konseling_dhika WHERE siswa_id = %s
                GROUP BY jenis ORDER BY jumlah DESC
            """, (siswa_id,))
            jenis_stats = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('laporan/laporan_siswa_dhika.html', laporan=laporan, stats=stats, jenis_stats=jenis_stats)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        if session.get('role') == 'Guru BK':
            return render_template('laporan/laporan_guru_dhika.html', laporan=[], stats={}, jenis_stats=[])
        return render_template('laporan/laporan_siswa_dhika.html', laporan=[], stats={}, jenis_stats=[])


@app.route('/laporan/cetak')
def cetak_laporan_dhika():
    if 'logged_in' not in session:
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        cursor.execute("""
            SELECT k.id_konseling, s.nama, g.nama, k.jenis, k.tanggal, k.status
            FROM konseling_dhika k
            JOIN siswa_dhika s ON k.siswa_id = s.id_siswa
            JOIN guru_dhika g ON k.guru_id = g.id_guru
            ORDER BY k.tanggal DESC
        """)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
=======
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('konseling_siswa_dhika'))

@app.route('/laporan/cetak')
def cetak_laporan_dhika():
    """Cetak laporan PDF"""
    if 'logged_in' not in session:
        return redirect(url_for('login_dhika'))
    
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT k.id_konseling, s.nama as siswa, g.nama as guru, 
                   k.jenis, k.tanggal, k.status
            FROM konseling k
            JOIN siswa s ON k.siswa_id = s.id_siswa
            JOIN guru g ON k.guru_id = g.id_guru
            ORDER BY k.tanggal DESC
        """)
        data = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Buat PDF
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'LAPORAN KONSELING BK', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'SMK Negeri 2 Cimahi - {datetime.now().strftime("%d/%m/%Y")}', 0, 1, 'C')
        pdf.ln(10)
<<<<<<< HEAD
        pdf.set_font('Arial', 'B', 10)
        col = pdf.w / 6
        for h in ['ID', 'Siswa', 'Guru', 'Jenis', 'Tanggal', 'Status']:
            pdf.cell(col if h not in ['Siswa', 'Guru'] else col * 1.5, 10, h, 1, 0, 'C')
        pdf.ln()
        pdf.set_font('Arial', '', 9)
        for row in data:
            pdf.cell(col, 8, str(row[0]), 1, 0, 'C')
            pdf.cell(col * 1.5, 8, str(row[1])[:20], 1, 0, 'L')
            pdf.cell(col * 1.5, 8, str(row[2])[:20], 1, 0, 'L')
            pdf.cell(col, 8, str(row[3]), 1, 0, 'C')
            pdf.cell(col, 8, str(row[4]), 1, 0, 'C')
            pdf.cell(col, 8, str(row[5]), 1, 1, 'C')
        response = make_response(pdf.output(dest='S').encode('latin1'))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=laporan_konseling.pdf'
        return response
    except Exception as e:
        return f'Error: {str(e)}'


@app.route('/chat')
def chat_dhika():
    if 'logged_in' not in session:
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        if session['role'] == 'Siswa':
            cursor.execute("SELECT id_siswa FROM siswa_dhika WHERE akun_id = %s", (session['id_akun'],))
            siswa_row = cursor.fetchone()
            siswa_id = siswa_row['id_siswa'] if siswa_row else None
            cursor.execute("""
                SELECT DISTINCT g.id_guru, g.nama, a.id_akun as akun_id,
                    (SELECT pesan FROM chat_dhika
                     WHERE (pengirim_akun_id=%s AND penerima_akun_id=a.id_akun)
                        OR (pengirim_akun_id=a.id_akun AND penerima_akun_id=%s)
                     ORDER BY waktu DESC LIMIT 1) as pesan_terakhir,
                    (SELECT waktu FROM chat_dhika
                     WHERE (pengirim_akun_id=%s AND penerima_akun_id=a.id_akun)
                        OR (pengirim_akun_id=a.id_akun AND penerima_akun_id=%s)
                     ORDER BY waktu DESC LIMIT 1) as waktu_terakhir
                FROM guru_dhika g
                JOIN akun_dhika a ON g.akun_id = a.id_akun
                WHERE EXISTS (
                    SELECT 1 FROM chat_dhika
                    WHERE (pengirim_akun_id=%s AND penerima_akun_id=a.id_akun)
                       OR (pengirim_akun_id=a.id_akun AND penerima_akun_id=%s)
                ) OR g.id_guru IN (SELECT guru_id FROM konseling_dhika WHERE siswa_id=%s)
                ORDER BY waktu_terakhir DESC
            """, (session['id_akun'], session['id_akun'], session['id_akun'], session['id_akun'],
                  session['id_akun'], session['id_akun'], siswa_id))
        else:
            cursor.execute("SELECT id_guru FROM guru_dhika WHERE akun_id = %s", (session['id_akun'],))
            guru_row2 = cursor.fetchone()
            guru_id2 = guru_row2['id_guru'] if guru_row2 else None
            cursor.execute("""
                SELECT DISTINCT s.id_siswa, s.nama, a.id_akun as akun_id,
                    (SELECT pesan FROM chat_dhika
                     WHERE (pengirim_akun_id=%s AND penerima_akun_id=a.id_akun)
                        OR (pengirim_akun_id=a.id_akun AND penerima_akun_id=%s)
                     ORDER BY waktu DESC LIMIT 1) as pesan_terakhir,
                    (SELECT waktu FROM chat_dhika
                     WHERE (pengirim_akun_id=%s AND penerima_akun_id=a.id_akun)
                        OR (pengirim_akun_id=a.id_akun AND penerima_akun_id=%s)
                     ORDER BY waktu DESC LIMIT 1) as waktu_terakhir
                FROM siswa_dhika s
                JOIN akun_dhika a ON s.akun_id = a.id_akun
                WHERE EXISTS (
                    SELECT 1 FROM chat_dhika
                    WHERE (pengirim_akun_id=%s AND penerima_akun_id=a.id_akun)
                       OR (pengirim_akun_id=a.id_akun AND penerima_akun_id=%s)
                ) OR s.id_siswa IN (SELECT siswa_id FROM konseling_dhika WHERE guru_id=%s)
                ORDER BY waktu_terakhir DESC
            """, (session['id_akun'], session['id_akun'], session['id_akun'], session['id_akun'],
                  session['id_akun'], session['id_akun'], guru_id2))
        kontak_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('chat_dhika.html', kontak_list=kontak_list)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('chat_dhika.html', kontak_list=[])


@app.route('/chat/pesan/<int:lawan_akun_id>')
def chat_pesan_dhika(lawan_akun_id):
    if 'logged_in' not in session:
        return jsonify([])
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT pengirim_akun_id, pesan, DATE_FORMAT(waktu, '%H:%M') as waktu
            FROM chat_dhika
            WHERE (pengirim_akun_id=%s AND penerima_akun_id=%s)
               OR (pengirim_akun_id=%s AND penerima_akun_id=%s)
            ORDER BY waktu ASC LIMIT 100
        """, (session['id_akun'], lawan_akun_id, lawan_akun_id, session['id_akun']))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception:
        return jsonify([])


@app.route('/chat/kirim', methods=['POST'])
def chat_kirim_dhika():
    if 'logged_in' not in session:
        return jsonify({'ok': False})
    try:
        data = request.get_json()
        penerima_id = data.get('penerima_akun_id')
        pesan = data.get('pesan', '').strip()
        if not pesan or not penerima_id:
            return jsonify({'ok': False})
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        cursor.execute(
            "INSERT INTO chat_dhika (pengirim_akun_id, penerima_akun_id, pesan) VALUES (%s, %s, %s)",
            (session['id_akun'], penerima_id, pesan)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'msg': str(e)})


@app.route('/dashboard/siswa')
def dashboard_siswa_dhika():
    if 'logged_in' not in session or session.get('role') != 'Siswa':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT s.* FROM siswa_dhika s WHERE s.akun_id = %s", (session['id_akun'],))
        siswa = cursor.fetchone()
        cursor.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN status='Pending' THEN 1 ELSE 0 END) as pending,
                   SUM(CASE WHEN status='Disetujui' THEN 1 ELSE 0 END) as disetujui,
                   SUM(CASE WHEN status='Selesai' THEN 1 ELSE 0 END) as selesai
            FROM konseling_dhika WHERE siswa_id = %s
        """, (siswa['id_siswa'],))
        stats = cursor.fetchone()
        cursor.execute("""
            SELECT k.*, g.nama as nama_guru
            FROM konseling_dhika k
            JOIN guru_dhika g ON k.guru_id = g.id_guru
            WHERE k.siswa_id = %s
            ORDER BY k.tanggal DESC, k.jam_mulai DESC LIMIT 5
        """, (siswa['id_siswa'],))
        konseling_terbaru = cursor.fetchall()
        cursor.execute("""
            SELECT rp.tanggal, p.nama_pelanggaran, p.poin, p.kategori
            FROM riwayat_pelanggaran_dhika rp
            JOIN pelanggaran_dhika p ON rp.pelanggaran_id = p.id_pelanggaran
            WHERE rp.siswa_id = %s
            ORDER BY rp.tanggal DESC LIMIT 3
        """, (siswa['id_siswa'],))
        riwayat_pelanggaran = cursor.fetchall()
        cursor.close()
        conn.close()
        total_poin = siswa.get('total_poin') or 0
        status_poin = get_status_pelanggaran_dhika(total_poin)
        notif_pelanggaran = None
        if total_poin > 100:
            notif_pelanggaran = f"Anda telah mencapai {status_poin}, segera konsultasi ke BK."
        return render_template('dashboard/dashboard_siswa_dhika.html',
                               siswa=siswa, stats=stats,
                               konseling_terbaru=konseling_terbaru,
                               riwayat_pelanggaran=riwayat_pelanggaran,
                               total_poin=total_poin,
                               status_poin=status_poin,
                               notif_pelanggaran=notif_pelanggaran)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('dashboard/dashboard_siswa_dhika.html')


@app.route('/dashboard/guru')
def dashboard_guru_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT g.* FROM guru_dhika g WHERE g.akun_id = %s", (session['id_akun'],))
        guru = cursor.fetchone()
        cursor.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN status='Pending' THEN 1 ELSE 0 END) as pending,
                   SUM(CASE WHEN status='Disetujui' THEN 1 ELSE 0 END) as disetujui,
                   SUM(CASE WHEN status='Selesai' THEN 1 ELSE 0 END) as selesai
            FROM konseling_dhika WHERE guru_id = %s
        """, (guru['id_guru'],))
        stats = cursor.fetchone()
        cursor.execute("""
            SELECT jenis, COUNT(*) as jumlah
            FROM konseling_dhika WHERE guru_id = %s
            GROUP BY jenis
        """, (guru['id_guru'],))
        jenis_stats = cursor.fetchall()
        today = datetime.now().date()
        cursor.execute("""
            SELECT k.*, s.nama as nama_siswa, s.kelas
            FROM konseling_dhika k
            JOIN siswa_dhika s ON k.siswa_id = s.id_siswa
=======
        
        # Tabel
        pdf.set_font('Arial', 'B', 10)
        col_width = pdf.w / 6
        pdf.cell(col_width, 10, 'ID', 1, 0, 'C')
        pdf.cell(col_width*1.5, 10, 'Siswa', 1, 0, 'C')
        pdf.cell(col_width*1.5, 10, 'Guru', 1, 0, 'C')
        pdf.cell(col_width, 10, 'Jenis', 1, 0, 'C')
        pdf.cell(col_width, 10, 'Tanggal', 1, 0, 'C')
        pdf.cell(col_width, 10, 'Status', 1, 1, 'C')
        
        pdf.set_font('Arial', '', 9)
        for row in data:
            pdf.cell(col_width, 8, str(row[0]), 1, 0, 'C')
            pdf.cell(col_width*1.5, 8, str(row[1])[:20], 1, 0, 'L')
            pdf.cell(col_width*1.5, 8, str(row[2])[:20], 1, 0, 'L')
            pdf.cell(col_width, 8, str(row[3]), 1, 0, 'C')
            pdf.cell(col_width, 8, str(row[4]), 1, 0, 'C')
            pdf.cell(col_width, 8, str(row[5]), 1, 1, 'C')
        
        # Response
        response = make_response(pdf.output(dest='S').encode('latin1'))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=laporan_konseling.pdf'
        
        return response
        
    except Exception as e:
        return f'Error generating PDF: {str(e)}'

# ==================== FUNGSI HELPER ====================
def flash_dhika(message, category='info'):
    """Helper untuk flash message"""
    session['flash_message'] = message
    session['flash_category'] = category

def get_flash_dhika():
    """Ambil flash message dari session"""
    message = session.pop('flash_message', None)
    category = session.pop('flash_category', None)
    return message, category

# ==================== JINJA2 FILTERS ====================
@app.template_filter('format_tanggal_dhika')
def format_tanggal_dhika(value):
    """Format tanggal menjadi DD/MM/YYYY"""
    if isinstance(value, str):
        try:
            dt = datetime.strptime(value, '%Y-%m-%d')
            return dt.strftime('%d/%m/%Y')
        except:
            return value
    return value

@app.template_filter('status_badge_dhika')
def status_badge_dhika(status):
    """Return Bootstrap badge berdasarkan status"""
    badges = {
        'pending': 'warning',
        'disetujui': 'primary',
        'selesai': 'success',
        'ditolak': 'danger'
    }
    return badges.get(status, 'secondary')

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def page_not_found_dhika(e):
    return render_template('404_dhika.html'), 404

@app.errorhandler(500)
def server_error_dhika(e):
    return render_template('500_dhika.html'), 500

# ==================== CONTEXT PROCESSOR ====================
@app.context_processor
def inject_variables_dhika():
    """Inject variables ke semua template"""
    return dict(
        get_flash_dhika=get_flash_dhika,
        now=datetime.now()
    )

# ==================== ROUTE UNTUK HTML BARU ====================

@app.route('/chat')
def chat_dhika():
    """Halaman chat untuk komunikasi"""
    if 'logged_in' not in session:
        return redirect(url_for('login_dhika'))
    
    return render_template('chat_dhika.html')

@app.route('/dashboard/siswa')
def dashboard_siswa_dhika():
    """Dashboard siswa"""
    if 'logged_in' not in session or session.get('role') != 'siswa':
        return redirect(url_for('login_dhika'))
    
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True)
        
        # Ambil data siswa
        cursor.execute("""
            SELECT s.* FROM siswa s 
            WHERE s.akun_id = %s
        """, (session['id_akun'],))
        siswa = cursor.fetchone()
        
        # Hitung statistik
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'disetujui' THEN 1 ELSE 0 END) as disetujui,
                SUM(CASE WHEN status = 'selesai' THEN 1 ELSE 0 END) as selesai
            FROM konseling 
            WHERE siswa_id = %s
        """, (siswa['id_siswa'],))
        stats = cursor.fetchone()
        
        # Konseling terbaru
        cursor.execute("""
            SELECT k.*, g.nama as nama_guru 
            FROM konseling k
            JOIN guru g ON k.guru_id = g.id_guru
            WHERE k.siswa_id = %s
            ORDER BY k.tanggal DESC, k.jam_mulai DESC
            LIMIT 5
        """, (siswa['id_siswa'],))
        konseling_terbaru = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('dashboard_siswa_dhika.html',
                             siswa=siswa,
                             stats=stats,
                             konseling_terbaru=konseling_terbaru)
        
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('dashboard_siswa_dhika.html')

@app.route('/dashboard/guru')
def dashboard_guru_dhika():
    """Dashboard guru BK"""
    if 'logged_in' not in session or session.get('role') != 'guru':
        return redirect(url_for('login_dhika'))
    
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True)
        
        # Ambil data guru
        cursor.execute("""
            SELECT g.* FROM guru g 
            WHERE g.akun_id = %s
        """, (session['id_akun'],))
        guru = cursor.fetchone()
        
        # Hitung statistik
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'disetujui' THEN 1 ELSE 0 END) as disetujui,
                SUM(CASE WHEN status = 'selesai' THEN 1 ELSE 0 END) as selesai
            FROM konseling 
            WHERE guru_id = %s
        """, (guru['id_guru'],))
        stats = cursor.fetchone()
        
        # Statistik per jenis
        cursor.execute("""
            SELECT jenis, COUNT(*) as jumlah
            FROM konseling 
            WHERE guru_id = %s
            GROUP BY jenis
        """, (guru['id_guru'],))
        jenis_stats = cursor.fetchall()
        
        # Konseling hari ini
        today = datetime.now().date()
        cursor.execute("""
            SELECT k.*, s.nama as nama_siswa, s.kelas 
            FROM konseling k
            JOIN siswa s ON k.siswa_id = s.id_siswa
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
            WHERE k.guru_id = %s AND k.tanggal = %s
            ORDER BY k.jam_mulai
        """, (guru['id_guru'], today))
        konseling_hari_ini = cursor.fetchall()
<<<<<<< HEAD
        cursor.execute("""
            SELECT id_siswa, nama, kelas, jurusan, total_poin
            FROM siswa_dhika ORDER BY total_poin DESC LIMIT 5
        """)
        siswa_poin_tinggi = cursor.fetchall()
        for s in siswa_poin_tinggi:
            s['status_poin'] = get_status_pelanggaran_dhika(s['total_poin'] or 0)
        cursor.execute("""
            SELECT COUNT(*) as jml FROM pendaftaran_dhika WHERE status_daftar='Pending'
        """)
        pending_daftar = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('dashboard/dashboard_guru_dhika.html',
                               guru=guru, stats=stats,
                               jenis_stats=jenis_stats,
                               konseling_hari_ini=konseling_hari_ini,
                               today=today,
                               siswa_poin_tinggi=siswa_poin_tinggi,
                               pending_daftar=pending_daftar)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('dashboard/dashboard_guru_dhika.html')


@app.route('/data/siswa')
def data_siswa_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT s.*, a.username
            FROM siswa_dhika s
            JOIN akun_dhika a ON s.akun_id = a.id_akun
            ORDER BY s.kelas, s.nama
        """)
        siswa_list = cursor.fetchall()
        cursor.execute("""
            SELECT kelas, COUNT(*) as jumlah FROM siswa_dhika GROUP BY kelas ORDER BY kelas
        """)
        kelas_stats = cursor.fetchall()
        cursor.execute("""
            SELECT jurusan, COUNT(*) as jumlah FROM siswa_dhika GROUP BY jurusan ORDER BY jurusan
        """)
        jurusan_stats = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('data/data_siswa_dhika.html',
                               siswa_list=siswa_list,
                               kelas_stats=kelas_stats,
                               jurusan_stats=jurusan_stats)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('data/data_siswa_dhika.html')


@app.route('/data/guru')
def data_guru_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT g.*, a.username
            FROM guru_dhika g
            JOIN akun_dhika a ON g.akun_id = a.id_akun
            ORDER BY g.nama
        """)
        guru_list = cursor.fetchall()
        cursor.execute("""
            SELECT g.nama,
                   COUNT(k.id_konseling) as total_konseling,
                   SUM(CASE WHEN k.status='Pending' THEN 1 ELSE 0 END) as pending,
                   SUM(CASE WHEN k.status='Selesai' THEN 1 ELSE 0 END) as selesai
            FROM guru_dhika g
            LEFT JOIN konseling_dhika k ON g.id_guru = k.guru_id
=======
        
        cursor.close()
        conn.close()
        
        return render_template('dashboard_guru_dhika.html',
                             guru=guru,
                             stats=stats,
                             jenis_stats=jenis_stats,
                             konseling_hari_ini=konseling_hari_ini,
                             today=today)
        
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('dashboard_guru_dhika.html')

# ==================== ROUTE UNTUK DATA MASTER ====================

@app.route('/data/siswa')
def data_siswa_dhika():
    """Halaman data siswa (untuk guru)"""
    if 'logged_in' not in session or session.get('role') != 'guru':
        return redirect(url_for('login_dhika'))
    
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True)
        
        # Ambil semua data siswa
        cursor.execute("""
            SELECT s.*, a.username 
            FROM siswa s 
            JOIN akun a ON s.akun_id = a.id_akun
            ORDER BY s.kelas, s.nama
        """)
        siswa_list = cursor.fetchall()
        
        # Hitung statistik per kelas
        cursor.execute("""
            SELECT kelas, COUNT(*) as jumlah
            FROM siswa
            GROUP BY kelas
            ORDER BY kelas
        """)
        kelas_stats = cursor.fetchall()
        
        # Hitung statistik per jurusan
        cursor.execute("""
            SELECT jurusan, COUNT(*) as jumlah
            FROM siswa
            GROUP BY jurusan
            ORDER BY jurusan
        """)
        jurusan_stats = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('data_siswa_dhika.html',
                             siswa_list=siswa_list,
                             kelas_stats=kelas_stats,
                             jurusan_stats=jurusan_stats)
        
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('data_siswa_dhika.html')

@app.route('/data/guru')
def data_guru_dhika():
    """Halaman data guru BK"""
    if 'logged_in' not in session or session.get('role') != 'guru':
        return redirect(url_for('login_dhika'))
    
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True)
        
        # Ambil semua data guru
        cursor.execute("""
            SELECT g.*, a.username 
            FROM guru g 
            JOIN akun a ON g.akun_id = a.id_akun
            ORDER BY g.nama
        """)
        guru_list = cursor.fetchall()
        
        # Hitung statistik beban kerja guru
        cursor.execute("""
            SELECT g.nama, 
                   COUNT(k.id_konseling) as total_konseling,
                   SUM(CASE WHEN k.status = 'pending' THEN 1 ELSE 0 END) as pending,
                   SUM(CASE WHEN k.status = 'selesai' THEN 1 ELSE 0 END) as selesai
            FROM guru g
            LEFT JOIN konseling k ON g.id_guru = k.guru_id
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
            GROUP BY g.id_guru, g.nama
            ORDER BY total_konseling DESC
        """)
        beban_kerja = cursor.fetchall()
<<<<<<< HEAD
        cursor.close()
        conn.close()
        return render_template('data/data_guru_dhika.html', guru_list=guru_list, beban_kerja=beban_kerja)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('data/data_guru_dhika.html')


@app.route('/profile')
def profile_dhika():
    if 'logged_in' not in session:
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        if session['role'] == 'Siswa':
            cursor.execute("""
                SELECT s.*, a.username, a.created_at as tanggal_daftar
                FROM siswa_dhika s
                JOIN akun_dhika a ON s.akun_id = a.id_akun
                WHERE s.akun_id = %s
            """, (session['id_akun'],))
        else:
            cursor.execute("""
                SELECT g.*, a.username, a.created_at as tanggal_daftar
                FROM guru_dhika g
                JOIN akun_dhika a ON g.akun_id = a.id_akun
                WHERE g.akun_id = %s
            """, (session['id_akun'],))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('akun/profile_dhika.html', user=user_data)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for('dashboard_siswa_dhika' if session['role'] == 'Siswa' else 'dashboard_guru_dhika'))


@app.route('/pelanggaran')
def pelanggaran_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_siswa, nama, kelas, jurusan, total_poin FROM siswa_dhika ORDER BY total_poin DESC")
        siswa_list = cursor.fetchall()
        for s in siswa_list:
            s['status_poin'] = get_status_pelanggaran_dhika(s['total_poin'] or 0)
        cursor.execute("""
            SELECT rp.id_riwayat, s.nama as nama_siswa, s.kelas,
                   p.nama_pelanggaran, p.poin, p.kategori, rp.tanggal, rp.keterangan
            FROM riwayat_pelanggaran_dhika rp
            JOIN siswa_dhika s ON rp.siswa_id = s.id_siswa
            JOIN pelanggaran_dhika p ON rp.pelanggaran_id = p.id_pelanggaran
            ORDER BY rp.tanggal DESC LIMIT 20
        """)
        riwayat_terbaru = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('pelanggaran/pelanggaran_dhika.html', siswa_list=siswa_list, riwayat_terbaru=riwayat_terbaru)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('pelanggaran/pelanggaran_dhika.html', siswa_list=[], riwayat_terbaru=[])


@app.route('/pelanggaran/list-pelanggaran')
def pelanggaran_list_api_dhika():
    if 'logged_in' not in session:
        return jsonify([])
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_pelanggaran, nama_pelanggaran, poin, kategori FROM pelanggaran_dhika ORDER BY kategori, poin")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception:
        return jsonify([])


@app.route('/pelanggaran/input', methods=['POST'])
def pelanggaran_input_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        siswa_id = request.form.get('siswa_id_dhika')
        pelanggaran_id = request.form.get('pelanggaran_id_dhika')
        tanggal = request.form.get('tanggal_dhika')
        keterangan = request.form.get('keterangan_dhika', '')
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT poin FROM pelanggaran_dhika WHERE id_pelanggaran = %s", (pelanggaran_id,))
        pel = cursor.fetchone()
        if not pel:
            flash_dhika('Pelanggaran tidak ditemukan', 'error')
            return redirect(url_for('pelanggaran_dhika'))
        poin = pel['poin']
        cursor.execute("""
            INSERT INTO riwayat_pelanggaran_dhika (siswa_id, pelanggaran_id, tanggal, keterangan)
            VALUES (%s, %s, %s, %s)
        """, (siswa_id, pelanggaran_id, tanggal, keterangan))
        cursor.execute("UPDATE siswa_dhika SET total_poin = total_poin + %s WHERE id_siswa = %s", (poin, siswa_id))
        conn.commit()
        cursor.execute("SELECT total_poin FROM siswa_dhika WHERE id_siswa = %s", (siswa_id,))
        siswa_up = cursor.fetchone()
        total = siswa_up['total_poin'] if siswa_up else 0
        log_aktivitas_dhika(session['id_akun'], f'Input pelanggaran siswa id {siswa_id}, poin +{poin}')
        cursor.close()
        conn.close()
        if total > 100:
            flash_dhika(f'Pelanggaran dicatat. Siswa telah mencapai {get_status_pelanggaran_dhika(total)}!', 'error')
        else:
            flash_dhika('Pelanggaran berhasil dicatat.', 'success')
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('pelanggaran_dhika'))


@app.route('/pelanggaran/siswa/<int:siswa_id>')
def pelanggaran_siswa_detail_dhika(siswa_id):
    if 'logged_in' not in session:
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM siswa_dhika WHERE id_siswa = %s", (siswa_id,))
        siswa = cursor.fetchone()
        if not siswa:
            flash_dhika('Siswa tidak ditemukan', 'error')
            return redirect(url_for('pelanggaran_dhika'))
        siswa['status_poin'] = get_status_pelanggaran_dhika(siswa['total_poin'] or 0)
        cursor.execute("""
            SELECT rp.*, p.nama_pelanggaran, p.poin, p.kategori
            FROM riwayat_pelanggaran_dhika rp
            JOIN pelanggaran_dhika p ON rp.pelanggaran_id = p.id_pelanggaran
            WHERE rp.siswa_id = %s ORDER BY rp.tanggal DESC
        """, (siswa_id,))
        riwayat = cursor.fetchall()
        cursor.close()
        conn.close()
        notif = None
        if (siswa['total_poin'] or 0) > 100:
            notif = f"Siswa ini telah mencapai {get_status_pelanggaran_dhika(siswa['total_poin'])}, segera lakukan konseling."
        return render_template('pelanggaran/pelanggaran_detail_dhika.html', siswa=siswa, riwayat=riwayat, notif=notif)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for('pelanggaran_dhika'))


@app.route('/pelanggaran/reset', methods=['POST'])
def pelanggaran_reset_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    if reset_poin_semester_dhika():
        log_aktivitas_dhika(session['id_akun'], 'Reset poin pelanggaran seluruh siswa')
        flash_dhika('Poin pelanggaran seluruh siswa berhasil direset.', 'success')
    else:
        flash_dhika('Gagal reset poin.', 'error')
    return redirect(url_for('pelanggaran_dhika'))


@app.route('/pelanggaran/saya')
def pelanggaran_saya_dhika():
    if 'logged_in' not in session or session.get('role') != 'Siswa':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM siswa_dhika WHERE akun_id = %s", (session['id_akun'],))
        siswa = cursor.fetchone()
        siswa['status_poin'] = get_status_pelanggaran_dhika(siswa['total_poin'] or 0)
        cursor.execute("""
            SELECT rp.*, p.nama_pelanggaran, p.poin, p.kategori
            FROM riwayat_pelanggaran_dhika rp
            JOIN pelanggaran_dhika p ON rp.pelanggaran_id = p.id_pelanggaran
            WHERE rp.siswa_id = %s ORDER BY rp.tanggal DESC
        """, (siswa['id_siswa'],))
        riwayat = cursor.fetchall()
        cursor.close()
        conn.close()
        notif = None
        if (siswa['total_poin'] or 0) > 100:
            notif = f"Anda telah mencapai {get_status_pelanggaran_dhika(siswa['total_poin'])}, segera konsultasi ke BK."
        return render_template('pelanggaran/pelanggaran_saya_dhika.html', siswa=siswa, riwayat=riwayat, notif=notif)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('pelanggaran/pelanggaran_saya_dhika.html', siswa={}, riwayat=[], notif=None)


@app.route('/manajemen-akun')
def manajemen_akun_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT * FROM pendaftaran_dhika
            ORDER BY FIELD(status_daftar,'Pending','Disetujui','Ditolak'), tanggal_daftar DESC
        """)
        pendaftaran_list = cursor.fetchall()
        cursor.execute("""
            SELECT g.*, a.username, a.status_akun
            FROM guru_dhika g JOIN akun_dhika a ON g.akun_id = a.id_akun
            ORDER BY g.nama
        """)
        guru_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('akun/manajemen_akun_dhika.html',
                               pendaftaran_list=pendaftaran_list,
                               guru_list=guru_list)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('akun/manajemen_akun_dhika.html', pendaftaran_list=[], guru_list=[])


@app.route('/manajemen-akun/approve/<int:id_daftar>', methods=['POST'])
def approve_pendaftaran_dhika(id_daftar):
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        aksi = request.form.get('aksi_dhika')
        catatan = request.form.get('catatan_dhika', '').strip()
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM pendaftaran_dhika WHERE id_daftar = %s", (id_daftar,))
        daftar = cursor.fetchone()
        if not daftar:
            flash_dhika('Data tidak ditemukan!', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('manajemen_akun_dhika'))
        if aksi == 'setujui':
            cursor.execute(
                "INSERT INTO akun_dhika (username, password, role, status_akun) VALUES (%s, %s, 'Siswa', 'Aktif')",
                (daftar['username'], daftar['password'])
            )
            akun_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO siswa_dhika (akun_id, nis, nama, kelas, jurusan, rombel, no_ortu)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (akun_id, daftar['nis'], daftar['nama'], daftar['kelas'], daftar['jurusan'], daftar.get('rombel', 'A'), daftar.get('no_ortu')))
            cursor.execute(
                "UPDATE pendaftaran_dhika SET status_daftar='Disetujui', catatan_guru=%s, tanggal_proses=NOW() WHERE id_daftar=%s",
                (catatan or None, id_daftar)
            )
            conn.commit()
            log_aktivitas_dhika(session['id_akun'], f'Menyetujui pendaftaran {daftar["nama"]}')
            flash_dhika(f'Akun {daftar["nama"]} berhasil disetujui!', 'success')
        else:
            cursor.execute(
                "UPDATE pendaftaran_dhika SET status_daftar='Ditolak', catatan_guru=%s, tanggal_proses=NOW() WHERE id_daftar=%s",
                (catatan or None, id_daftar)
            )
            conn.commit()
            log_aktivitas_dhika(session['id_akun'], f'Menolak pendaftaran {daftar["nama"]}')
            flash_dhika(f'Pendaftaran {daftar["nama"]} ditolak.', 'error')
        cursor.close()
        conn.close()
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('manajemen_akun_dhika'))


@app.route('/manajemen-akun/tambah-guru', methods=['POST'])
def tambah_guru_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        username = request.form.get('username_guru_dhika', '').strip()
        password = request.form.get('password_guru_dhika', '').strip()
        nama = request.form.get('nama_guru_dhika', '').strip()
        nip = request.form.get('nip_guru_dhika', '').strip()
        if not all([username, password, nama, nip]):
            flash_dhika('Semua field harus diisi!', 'error')
            return redirect(url_for('manajemen_akun_dhika'))
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_akun FROM akun_dhika WHERE username = %s", (username,))
        if cursor.fetchone():
            flash_dhika('Username sudah ada!', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('manajemen_akun_dhika'))
        cursor.execute(
            "INSERT INTO akun_dhika (username, password, role, status_akun) VALUES (%s, %s, 'Guru BK', 'Aktif')",
            (username, password)
        )
        akun_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO guru_dhika (akun_id, nip, nama) VALUES (%s, %s, %s)",
            (akun_id, nip, nama)
        )
        conn.commit()
        log_aktivitas_dhika(session['id_akun'], f'Menambahkan akun guru {nama}')
        cursor.close()
        conn.close()
        flash_dhika(f'Akun Guru BK {nama} berhasil dibuat!', 'success')
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('manajemen_akun_dhika'))


@app.route('/notifikasi')
def notifikasi_dhika():
    if 'logged_in' not in session:
        return jsonify([])
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT aktivitas, waktu
            FROM log_aktivitas_dhika
            WHERE akun_id = %s
            ORDER BY waktu DESC LIMIT 10
        """, (session['id_akun'],))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        result = []
        for d in data:
            result.append({
                'aktivitas': d['aktivitas'],
                'waktu': d['waktu'].strftime('%d %b %Y %H:%M') if d['waktu'] else '-'
            })
        return jsonify(result)
    except Exception:
        return jsonify([])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
=======
        
        cursor.close()
        conn.close()
        
        return render_template('data_guru_dhika.html',
                             guru_list=guru_list,
                             beban_kerja=beban_kerja)
        
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('data_guru_dhika.html')

# ==================== ROUTE UNTUK PROFILE ====================

@app.route('/profile')
def profile_dhika():
    """Halaman profile pengguna"""
    if 'logged_in' not in session:
        return redirect(url_for('login_dhika'))
    
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True)
        
        if session['role'] == 'siswa':
            cursor.execute("""
                SELECT s.*, a.username, a.created_at as tanggal_daftar
                FROM siswa s 
                JOIN akun a ON s.akun_id = a.id_akun
                WHERE s.akun_id = %s
            """, (session['id_akun'],))
            user_data = cursor.fetchone()
        else:
            cursor.execute("""
                SELECT g.*, a.username, a.created_at as tanggal_daftar
                FROM guru g 
                JOIN akun a ON g.akun_id = a.id_akun
                WHERE g.akun_id = %s
            """, (session['id_akun'],))
            user_data = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return render_template('profile_dhika.html', user=user_data)
        
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for('dashboard_siswa_dhika' if session['role'] == 'siswa' else 'dashboard_guru_dhika'))

# ==================== RUN APP ====================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
>>>>>>> 3ecd9455e89cf6beab1f575bc1f040908db6e90a
