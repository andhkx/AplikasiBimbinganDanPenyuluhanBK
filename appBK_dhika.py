from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
import mysql.connector
from fpdf import FPDF
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
app.secret_key = 'andhika_bk_smk2_2026'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

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
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
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
        
        try:
            conn = get_db_connection_dhika()
            if not conn:
                flash_dhika('Database connection error!', 'error')
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
                session.permanent = True
                session['logged_in'] = True
                session['id_akun'] = user['id_akun']
                session['username'] = user['username']
                session['role'] = user['role']
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
    if 'id_akun' in session:
        log_aktivitas_dhika(session['id_akun'], 'Logout dari sistem')
    session.clear()
    flash_dhika('Anda telah logout!', 'success')
    return redirect(url_for('login_dhika'))

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
            WHERE k.siswa_id = %s
            ORDER BY k.tanggal DESC, k.jam_mulai DESC
        """, (siswa['id_siswa'],))
        konseling_list = cursor.fetchall()
        
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
            WHERE k.guru_id = %s
            ORDER BY k.tanggal DESC, k.jam_mulai DESC
        """, (guru['id_guru'],))
        konseling_list = cursor.fetchall()
        
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
        guru_id = request.form.get('guru_id_dhika')
        jenis = request.form.get('jenis_dhika')
        tanggal = request.form.get('tanggal_dhika')
        jam_mulai = request.form.get('jam_mulai_dhika')
        jam_selesai = request.form.get('jam_selesai_dhika')
        alasan = request.form.get('alasan_dhika')
        
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
            conn.commit()
            flash_dhika('Konseling berhasil dibatalkan!', 'success')
        else:
            flash_dhika('Anda tidak berhak menghapus konseling ini!', 'error')
        
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
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'LAPORAN KONSELING BK', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'SMK Negeri 2 Cimahi - {datetime.now().strftime("%d/%m/%Y")}', 0, 1, 'C')
        pdf.ln(10)
        
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
            WHERE k.guru_id = %s AND k.tanggal = %s
            ORDER BY k.jam_mulai
        """, (guru['id_guru'], today))
        konseling_hari_ini = cursor.fetchall()
        
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
            GROUP BY g.id_guru, g.nama
            ORDER BY total_konseling DESC
        """)
        beban_kerja = cursor.fetchall()
        
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