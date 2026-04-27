from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response
import mysql.connector
from fpdf import FPDF
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from html import escape
import os
import re
import uuid

app = Flask(__name__)
app.secret_key = 'andhika_bk_smk2_2026'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'pelanggaran')
PROFILE_UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'profile')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROFILE_UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

PROFILE_ROLE_CONFIG_DHIKA = {
    'Siswa': {
        'table': 'siswa_dhika',
        'dashboard': 'dashboard_siswa_dhika',
        'allow_email': True,
        'allow_no_hp': True,
        'allow_no_ortu': True,
    },
    'Guru BK': {
        'table': 'guru_dhika',
        'dashboard': 'dashboard_guru_dhika',
        'allow_email': True,
        'allow_no_hp': True,
        'allow_no_ortu': False,
    },
    'Wali Kelas': {
        'table': 'wali_kelas_dhika',
        'dashboard': 'dashboard_walikelas_dhika',
        'allow_email': True,
        'allow_no_hp': True,
        'allow_no_ortu': False,
    },
    'Kesiswaan': {
        'table': 'kesiswaan_dhika',
        'dashboard': 'dashboard_kesiswaan_dhika',
        'allow_email': True,
        'allow_no_hp': True,
        'allow_no_ortu': False,
    },
    'Admin': {
        'table': 'admin_dhika',
        'dashboard': 'dashboard_admin_dhika',
        'allow_email': True,
        'allow_no_hp': True,
        'allow_no_ortu': False,
    },
}

def allowed_file_dhika(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_optional_image_dhika(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    if not allowed_file_dhika(file_storage.filename):
        raise ValueError('Format file tidak didukung. Gunakan JPG, JPEG, PNG, atau WEBP.')
    ext = file_storage.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    file_storage.save(os.path.join(UPLOAD_FOLDER, filename))
    return filename



def paginate_dhika(data, page, per_page=20):
    total = len(data)
    total_pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    return {
        'items': data[start:end],
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages,
        'prev_page': page - 1,
        'next_page': page + 1,
        'start_idx': start + 1 if total > 0 else 0,
        'end_idx': min(end, total),
    }

def get_detail_back_context_dhika(detail_type, siswa_id=None):
    role = session.get('role')
    if role == 'Wali Kelas' and siswa_id:
        return url_for('walikelas_detail_siswa_dhika', siswa_id=siswa_id), 'Kembali ke Detail Siswa'

    mappings = {
        'konseling': {
            'Siswa': ('konseling_siswa_dhika', 'Kembali ke Konseling'),
            'Guru BK': ('konseling_guru_dhika', 'Kembali ke Kelola Konseling'),
        },
        'pengaduan': {
            'Guru BK': ('guru_lihat_pengaduan_dhika', 'Kembali ke Pengaduan'),
            'Kesiswaan': ('dashboard_kesiswaan_dhika', 'Kembali ke Dashboard'),
        },
        'pemanggilan': {
            'Guru BK': ('pemanggilan_ortu_dhika', 'Kembali ke Pemanggilan'),
            'Kesiswaan': ('dashboard_kesiswaan_dhika', 'Kembali ke Dashboard'),
        },
        'pelanggaran': {
            'Siswa': ('pelanggaran_saya_dhika', 'Kembali ke Pelanggaran Saya'),
            'Guru BK': ('pelanggaran_dhika', 'Kembali ke Pelanggaran'),
            'Kesiswaan': ('pelanggaran_dhika', 'Kembali ke Pelanggaran'),
        }
    }
    endpoint, label = mappings.get(detail_type, {}).get(role, (get_dashboard_endpoint_dhika(role), 'Kembali'))
    if detail_type == 'pelanggaran' and siswa_id and role in ['Guru BK', 'Kesiswaan']:
        return url_for('pelanggaran_siswa_detail_dhika', siswa_id=siswa_id), 'Kembali ke Detail Pelanggaran'
    return url_for(endpoint), label


def get_current_identity_dhika(cursor, role):
    if role == 'Siswa':
        cursor.execute("SELECT id_siswa FROM siswa_dhika WHERE akun_id = %s", (session['id_akun'],))
        row = cursor.fetchone()
        return row['id_siswa'] if row else None
    if role == 'Guru BK':
        cursor.execute("SELECT id_guru FROM guru_dhika WHERE akun_id = %s", (session['id_akun'],))
        row = cursor.fetchone()
        return row['id_guru'] if row else None
    if role == 'Wali Kelas':
        cursor.execute("SELECT kelas, jurusan, rombel FROM wali_kelas_dhika WHERE akun_id = %s", (session['id_akun'],))
        return cursor.fetchone()
    if role == 'Kesiswaan':
        cursor.execute("SELECT id_kesiswaan FROM kesiswaan_dhika WHERE akun_id = %s", (session['id_akun'],))
        row = cursor.fetchone()
        return row['id_kesiswaan'] if row else None
    return None


def can_access_student_record_dhika(cursor, siswa_id):
    role = session.get('role')
    if role in ['Guru BK', 'Kesiswaan', 'Admin']:
        return True
    if role == 'Siswa':
        current_siswa_id = get_current_identity_dhika(cursor, role)
        return current_siswa_id == siswa_id
    if role == 'Wali Kelas':
        walikelas = get_current_identity_dhika(cursor, role)
        if not walikelas:
            return False
        cursor.execute(
            """
            SELECT 1
            FROM siswa_dhika
            WHERE id_siswa = %s AND kelas = %s AND jurusan = %s AND rombel = %s
            """,
            (siswa_id, walikelas['kelas'], walikelas['jurusan'], walikelas['rombel'])
        )
        return cursor.fetchone() is not None
    return False




def get_db_connection_dhika():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
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
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Log error: {e}")


def get_profile_config_dhika(role):
    return PROFILE_ROLE_CONFIG_DHIKA.get(role)


def get_dashboard_endpoint_dhika(role):
    config = get_profile_config_dhika(role)
    return config['dashboard'] if config else 'login_dhika'


def normalize_nullable_value_dhika(value):
    value = (value or '').strip()
    return value or None


def valid_email_dhika(email):
    if not email:
        return True
    return re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email) is not None


def valid_phone_dhika(phone):
    if not phone:
        return True
    allowed_chars = set('0123456789+-() ')
    if any(char not in allowed_chars for char in phone):
        return False
    digit_count = sum(char.isdigit() for char in phone)
    return 8 <= digit_count <= 15


def fetch_profile_data_dhika(cursor, akun_id, role):
    config = get_profile_config_dhika(role)
    if not config:
        return None
    query = f"""
        SELECT p.*, a.username, a.role, a.created_at as tanggal_daftar
        FROM {config['table']} p
        JOIN akun_dhika a ON p.akun_id = a.id_akun
        WHERE p.akun_id = %s
    """
    cursor.execute(query, (akun_id,))
    return cursor.fetchone()


def format_export_value_dhika(value):
    if value is None or value == '':
        return '-'
    if hasattr(value, 'strftime'):
        try:
            return value.strftime('%d/%m/%Y')
        except Exception:
            return str(value)
    return str(value)


def sanitize_pdf_text_dhika(value, max_len=38):
    text = format_export_value_dhika(value).replace('\n', ' ').replace('\r', ' ')
    text = text.encode('latin-1', 'replace').decode('latin-1')
    return text if len(text) <= max_len else text[:max_len - 3] + '...'


def export_excel_response_dhika(filename, title, headers, rows):
    header_html = ''.join(
        f'<th style="background:#eef2ff;border:1px solid #cbd5e1;padding:10px;font-weight:700;">{escape(str(header))}</th>'
        for header in headers
    )
    body_html = ''
    for row in rows:
        cells = ''.join(
            f'<td style="border:1px solid #cbd5e1;padding:8px;">{escape(format_export_value_dhika(cell))}</td>'
            for cell in row
        )
        body_html += f'<tr>{cells}</tr>'

    html_doc = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>{escape(title)}</title>
    </head>
    <body>
        <h2>{escape(title)}</h2>
        <p>Diekspor pada {escape(datetime.now().strftime('%d/%m/%Y %H:%M'))}</p>
        <table cellspacing="0" cellpadding="0" style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:12px;">
            <thead><tr>{header_html}</tr></thead>
            <tbody>{body_html}</tbody>
        </table>
    </body>
    </html>
    """
    response = make_response('\ufeff' + html_doc)
    response.headers['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}.xls'
    return response


def export_pdf_response_dhika(filename, title, headers, rows, widths=None, orientation='L'):
    pdf = FPDF(orientation=orientation, unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, sanitize_pdf_text_dhika(title, 90), 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 7, sanitize_pdf_text_dhika(f'Diekspor pada {datetime.now().strftime("%d/%m/%Y %H:%M")}', 90), 0, 1, 'C')
    pdf.ln(4)

    usable_width = pdf.w - pdf.l_margin - pdf.r_margin
    if not widths or len(widths) != len(headers):
        widths = [usable_width / len(headers)] * len(headers)
    total_width = sum(widths)
    if total_width > usable_width:
        scale = usable_width / total_width
        widths = [width * scale for width in widths]

    pdf.set_font('Arial', 'B', 8)
    for idx, header in enumerate(headers):
        pdf.cell(widths[idx], 8, sanitize_pdf_text_dhika(header, 22), 1, 0, 'C')
    pdf.ln()

    pdf.set_font('Arial', '', 7)
    for row in rows:
        for idx, cell in enumerate(row):
            max_len = max(10, int(widths[idx] * 1.7))
            align = 'L'
            if idx == 0:
                align = 'C'
            pdf.cell(widths[idx], 7, sanitize_pdf_text_dhika(cell, max_len), 1, 0, align)
        pdf.ln()

    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}.pdf'
    return response



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
        try:
            conn = get_db_connection_dhika()
            if not conn:
                flash_dhika('Database connection error!', 'error')
                return render_template('auth/login_dhika.html')
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute("""
                SELECT a.*,
                       s.id_siswa, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel,
                       g.id_guru, g.nama as nama_guru,
                       wk.id_walikelas, wk.nama as nama_walikelas,
                       ks.id_kesiswaan, ks.nama as nama_kesiswaan,
                       adm.id_admin, adm.nama as nama_admin
                FROM akun_dhika a
                LEFT JOIN siswa_dhika s ON a.id_akun = s.akun_id
                LEFT JOIN guru_dhika g ON a.id_akun = g.akun_id
                LEFT JOIN wali_kelas_dhika wk ON a.id_akun = wk.akun_id
                LEFT JOIN kesiswaan_dhika ks ON a.id_akun = ks.akun_id
                LEFT JOIN admin_dhika adm ON a.id_akun = adm.akun_id
                WHERE a.username = %s
            """, (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user['password'], password):
                if user.get('status_akun') == 'Nonaktif':
                    cursor.close()
                    conn.close()
                    flash_dhika('Akun kamu telah dinonaktifkan.', 'error')
                    return render_template('auth/login_dhika.html')
                session.permanent = True
                session['logged_in'] = True
                session['id_akun'] = user['id_akun']
                session['username'] = user['username']
                session['role'] = user['role']
                role = user['role']
                nama_map = {
                    'Siswa': user.get('nama_siswa'),
                    'Guru BK': user.get('nama_guru'),
                    'Wali Kelas': user.get('nama_walikelas'),
                    'Kesiswaan': user.get('nama_kesiswaan'),
                    'Admin': user.get('nama_admin'),
                }
                session['nama'] = nama_map.get(role) or user['username']
                profile_data = fetch_profile_data_dhika(cursor, user['id_akun'], role)
                session['foto_profil'] = (profile_data or {}).get('foto_profil')
                session['profile_updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.close()
                conn.close()
                log_aktivitas_dhika(user['id_akun'], 'Login ke sistem')
                redirect_map = {
                    'Siswa': 'dashboard_siswa_dhika',
                    'Guru BK': 'dashboard_guru_dhika',
                    'Wali Kelas': 'dashboard_walikelas_dhika',
                    'Kesiswaan': 'dashboard_kesiswaan_dhika',
                    'Admin': 'dashboard_admin_dhika',
                }
                return redirect(url_for(redirect_map.get(role, 'login_dhika')))
            else:
                cursor.close()
                conn.close()
                flash_dhika('Username atau password salah!', 'error')
        except Exception as e:
            flash_dhika(f'Login error: {str(e)}', 'error')
    return render_template('auth/login_dhika.html')


@app.route('/logout')
def logout_dhika():
    if 'id_akun' in session:
        log_aktivitas_dhika(session['id_akun'], 'Logout dari sistem')
    session.clear()
    flash_dhika('Anda telah logout!', 'success')
    return redirect(url_for('login_dhika'))


@app.route('/konseling/siswa')
def konseling_siswa_dhika():
    if 'logged_in' not in session or session.get('role') != 'Siswa':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_siswa FROM siswa_dhika WHERE akun_id = %s", (session['id_akun'],))
        siswa = cursor.fetchone()
        if not siswa:
            flash_dhika('Data siswa tidak ditemukan!', 'error')
            return redirect(url_for('login_dhika'))
        cursor.execute("""
            SELECT k.*, g.nama as nama_guru
            FROM konseling_dhika k
            JOIN guru_dhika g ON k.guru_id = g.id_guru
            WHERE k.siswa_id = %s
            ORDER BY k.tanggal DESC, k.jam_mulai DESC
        """, (siswa['id_siswa'],))
        konseling_list = cursor.fetchall()
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


@app.route('/konseling/siswa/detail/<id_konseling>')
def detail_konseling_siswa_dhika(id_konseling):
    if 'logged_in' not in session or session.get('role') != 'Siswa':
        return redirect(url_for('login_dhika'))
    return redirect(url_for('detail_konseling_dhika', id_konseling=id_konseling))


@app.route('/konseling/detail/<id_konseling>')
def detail_konseling_dhika(id_konseling):
    if 'logged_in' not in session or session.get('role') not in ['Siswa', 'Guru BK', 'Wali Kelas']:
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT k.*, s.id_siswa, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel,
                   g.nama as nama_guru
            FROM konseling_dhika k
            JOIN siswa_dhika s ON k.siswa_id = s.id_siswa
            JOIN guru_dhika g ON k.guru_id = g.id_guru
            WHERE k.id_konseling = %s
        """, (id_konseling,))
        konseling = cursor.fetchone()
        if not konseling or not can_access_student_record_dhika(cursor, konseling['id_siswa']):
            cursor.close()
            conn.close()
            flash_dhika('Detail konseling tidak ditemukan atau tidak bisa diakses.', 'error')
            return redirect(url_for(get_dashboard_endpoint_dhika(session.get('role'))))
        back_url, back_label = get_detail_back_context_dhika('konseling', konseling['id_siswa'])
        cursor.close()
        conn.close()
        return render_template(
            'detail/detail_konseling_dhika.html',
            konseling=konseling,
            back_url=back_url,
            back_label=back_label
        )
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for(get_dashboard_endpoint_dhika(session.get('role'))))


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
            SELECT k.*, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel
            FROM konseling_dhika k
            JOIN siswa_dhika s ON k.siswa_id = s.id_siswa
            WHERE k.guru_id = %s
            ORDER BY k.tanggal DESC, k.jam_mulai DESC
        """, (guru['id_guru'],))
        konseling_all = cursor.fetchall()
        cursor.close()
        conn.close()
        page = request.args.get('page', 1, type=int)
        search = request.args.get('q', '').strip()
        filter_status = request.args.get('status', '').strip()
        filter_jenis = request.args.get('jenis', '').strip()
        if search:
            konseling_all = [k for k in konseling_all if search.lower() in k.get('nama_siswa','').lower()]
        if filter_status:
            konseling_all = [k for k in konseling_all if k['status'] == filter_status]
        if filter_jenis:
            konseling_all = [k for k in konseling_all if k['jenis'] == filter_jenis]
        pagination = paginate_dhika(konseling_all, page, 20)
        return render_template('konseling/konseling_guru_dhika.html',
                               konseling_list=pagination['items'],
                               pagination=pagination,
                               search=search,
                               filter_status=filter_status,
                               filter_jenis=filter_jenis)
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
        guru_id = request.form.get('guru_id_dhika')
        jenis = request.form.get('jenis_dhika')
        tanggal = request.form.get('tanggal_dhika')
        jam_mulai = request.form.get('jam_mulai_dhika')
        alasan = request.form.get('alasan_dhika')
        if not all([guru_id, jenis, tanggal, jam_mulai, alasan]):
            flash_dhika('Semua field harus diisi!', 'error')
            return redirect(url_for('konseling_siswa_dhika'))
        cursor.execute("""
            INSERT INTO konseling_dhika
            (id_konseling, siswa_id, guru_id, jenis, tanggal, jam_mulai, alasan, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pending')
        """, (id_konseling, siswa[0], guru_id, jenis, tanggal, jam_mulai, alasan))
        conn.commit()
        try:
            conn2 = get_db_connection_dhika()
            cur2 = conn2.cursor(buffered=True)
            cur2.execute("SELECT akun_id FROM guru_dhika WHERE id_guru = %s", (guru_id,))
            guru_row = cur2.fetchone()
            if guru_row:
                pesan = f"Halo, saya telah mengajukan konseling ({jenis}) pada {tanggal} pukul {jam_mulai}. Mohon konfirmasinya."
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
        hasil = request.form.get('hasil_dhika') if 'hasil_dhika' in request.form else None
        tindak_lanjut = request.form.get('tindak_lanjut_dhika') if 'tindak_lanjut_dhika' in request.form else None
        jam_selesai = request.form.get('jam_selesai_dhika') if 'jam_selesai_dhika' in request.form else None
        foto_surat = save_optional_image_dhika(request.files.get('foto_surat_dhika'))
        foto_dokumentasi = save_optional_image_dhika(request.files.get('foto_dokumentasi_dhika'))
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        updates = ["status = %s"]
        params = [status]
        if hasil is not None:
            updates.append("hasil = %s")
            params.append(normalize_nullable_value_dhika(hasil))
        if tindak_lanjut is not None:
            updates.append("tindak_lanjut = %s")
            params.append(normalize_nullable_value_dhika(tindak_lanjut))
        if jam_selesai is not None and jam_selesai.strip():
            updates.append("jam_selesai = %s")
            params.append(jam_selesai.strip())
        if foto_surat:
            updates.append("foto_surat = %s")
            params.append(foto_surat)
        if foto_dokumentasi:
            updates.append("foto_dokumentasi = %s")
            params.append(foto_dokumentasi)
        params.append(id_konseling)
        cursor.execute(f"UPDATE konseling_dhika SET {', '.join(updates)} WHERE id_konseling = %s", params)
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
            conn.commit()
            flash_dhika('Konseling berhasil dibatalkan!', 'success')
        else:
            flash_dhika('Anda tidak berhak menghapus konseling ini!', 'error')
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
                SELECT k.*, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel, g.nama as nama_guru
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
            page = request.args.get('page', 1, type=int)
            search = request.args.get('q', '').strip()
            filter_status = request.args.get('status', '').strip()
            filter_jenis = request.args.get('jenis', '').strip()
            laporan_filtered = laporan
            if search:
                laporan_filtered = [l for l in laporan_filtered if search.lower() in l.get('nama_siswa','').lower()]
            if filter_status:
                laporan_filtered = [l for l in laporan_filtered if l['status'] == filter_status]
            if filter_jenis:
                laporan_filtered = [l for l in laporan_filtered if l['jenis'] == filter_jenis]
            pagination = paginate_dhika(laporan_filtered, page, 20)
            return render_template('laporan/laporan_guru_dhika.html',
                                   laporan=pagination['items'],
                                   pagination=pagination,
                                   stats=stats,
                                   jenis_stats=jenis_stats,
                                   search=search,
                                   filter_status=filter_status,
                                   filter_jenis=filter_jenis)
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
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'LAPORAN KONSELING BK', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'SMK Negeri 2 Cimahi - {datetime.now().strftime("%d/%m/%Y")}', 0, 1, 'C')
        pdf.ln(10)
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


@app.route('/laporan/guru/export/<string:filetype>')
def export_laporan_guru_dhika(filetype):
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    if filetype not in ['pdf', 'excel']:
        return redirect(url_for('laporan_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_guru, nama FROM guru_dhika WHERE akun_id = %s", (session['id_akun'],))
        guru = cursor.fetchone()
        if not guru:
            cursor.close()
            conn.close()
            flash_dhika('Data guru tidak ditemukan.', 'error')
            return redirect(url_for('laporan_dhika'))

        cursor.execute("""
            SELECT k.id_konseling, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel,
                   k.jenis, k.tanggal, k.jam_mulai, k.jam_selesai, k.status, k.hasil
            FROM konseling_dhika k
            JOIN siswa_dhika s ON k.siswa_id = s.id_siswa
            WHERE k.guru_id = %s
            ORDER BY k.tanggal DESC, k.jam_mulai DESC
        """, (guru['id_guru'],))
        laporan = cursor.fetchall()
        cursor.close()
        conn.close()

        headers = ['ID', 'Siswa', 'Kelas', 'Jenis', 'Tanggal', 'Waktu', 'Status', 'Hasil']
        rows = [[
            row['id_konseling'],
            row['nama_siswa'],
            f"{row['kelas']} - {row['jurusan']} - {row['rombel']}",
            row['jenis'],
            format_export_value_dhika(row['tanggal']),
            f"{row['jam_mulai']} - {row['jam_selesai']}",
            row['status'],
            row['hasil'] or '-'
        ] for row in laporan]
        filename = f"laporan_konseling_guru_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        title = f"Laporan Konseling Guru BK - {guru['nama']}"

        if filetype == 'excel':
            return export_excel_response_dhika(filename, title, headers, rows)
        return export_pdf_response_dhika(filename, title, headers, rows, [14, 42, 36, 22, 22, 28, 23, 75], 'L')
    except Exception as e:
        flash_dhika(f'Error export laporan guru: {str(e)}', 'error')
        return redirect(url_for('laporan_dhika'))


@app.route('/laporan/pengaduan/export/<string:filetype>')
def export_laporan_pengaduan_dhika(filetype):
    if 'logged_in' not in session or session.get('role') != 'Kesiswaan':
        return redirect(url_for('login_dhika'))
    if filetype not in ['pdf', 'excel']:
        return redirect(url_for('laporan_pengaduan_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT pg.judul, pg.deskripsi, pg.status, pg.tanggal,
                   s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel,
                   ks.nama as nama_kesiswaan
            FROM pengaduan_dhika pg
            JOIN siswa_dhika s ON pg.siswa_id = s.id_siswa
            JOIN kesiswaan_dhika ks ON pg.kesiswaan_id = ks.id_kesiswaan
            ORDER BY pg.tanggal DESC
        """)
        pengaduan_list = cursor.fetchall()
        cursor.close()
        conn.close()

        headers = ['Siswa', 'Kelas', 'Judul', 'Deskripsi', 'Status', 'Tanggal', 'Petugas']
        rows = [[
            row['nama_siswa'],
            f"{row['kelas']} - {row['jurusan']} - {row['rombel']}",
            row['judul'],
            row['deskripsi'] or '-',
            row['status'],
            format_export_value_dhika(row['tanggal']),
            row['nama_kesiswaan']
        ] for row in pengaduan_list]
        filename = f"laporan_pengaduan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        title = 'Laporan Pengaduan Kesiswaan'

        if filetype == 'excel':
            return export_excel_response_dhika(filename, title, headers, rows)
        return export_pdf_response_dhika(filename, title, headers, rows, [30, 34, 34, 68, 23, 24, 42], 'L')
    except Exception as e:
        flash_dhika(f'Error export pengaduan: {str(e)}', 'error')
        return redirect(url_for('laporan_pengaduan_dhika'))


@app.route('/walikelas/export/<string:dataset>/<string:filetype>')
def export_walikelas_dhika(dataset, filetype):
    if 'logged_in' not in session or session.get('role') != 'Wali Kelas':
        return redirect(url_for('login_dhika'))
    if filetype not in ['pdf', 'excel'] or dataset not in ['siswa', 'panggilan-ortu']:
        return redirect(url_for('dashboard_walikelas_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM wali_kelas_dhika WHERE akun_id = %s", (session['id_akun'],))
        walikelas = cursor.fetchone()
        if not walikelas:
            cursor.close()
            conn.close()
            flash_dhika('Data wali kelas tidak ditemukan.', 'error')
            return redirect(url_for('dashboard_walikelas_dhika'))

        kelas_label = f"{walikelas['kelas']} - {walikelas['jurusan']} - {walikelas['rombel']}"

        if dataset == 'siswa':
            cursor.execute("""
                SELECT id_siswa, nis, nama, kelas, jurusan, rombel, email, no_ortu
                FROM siswa_dhika
                WHERE kelas = %s AND jurusan = %s AND rombel = %s
                ORDER BY nama
            """, (walikelas['kelas'], walikelas['jurusan'], walikelas['rombel']))
            siswa_list = cursor.fetchall()
            rows = []
            for siswa in siswa_list:
                cursor.execute("SELECT COUNT(*) as total FROM konseling_dhika WHERE siswa_id = %s", (siswa['id_siswa'],))
                total_konseling = cursor.fetchone()['total']
                cursor.execute("SELECT COUNT(*) as total FROM riwayat_pelanggaran_dhika WHERE siswa_id = %s", (siswa['id_siswa'],))
                total_pelanggaran = cursor.fetchone()['total']
                rows.append([
                    siswa['nis'],
                    siswa['nama'],
                    f"{siswa['kelas']} - {siswa['jurusan']} - {siswa['rombel']}",
                    siswa.get('email') or '-',
                    siswa.get('no_ortu') or '-',
                    total_konseling,
                    total_pelanggaran
                ])
            headers = ['NIS', 'Nama', 'Kelas', 'Email', 'No. Ortu', 'Total Konseling', 'Total Pelanggaran']
            title = f'Data Siswa Wali Kelas - {kelas_label}'
            filename = f"walikelas_siswa_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            response = export_excel_response_dhika(filename, title, headers, rows) if filetype == 'excel' else export_pdf_response_dhika(filename, title, headers, rows, [22, 48, 34, 46, 28, 22, 24], 'L')
        else:
            cursor.execute("""
                SELECT pm.tujuan, pm.tanggal, pm.status, pm.catatan,
                       s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel,
                       g.nama as nama_guru_bk
                FROM pemanggilan_ortu_dhika pm
                JOIN siswa_dhika s ON pm.siswa_id = s.id_siswa
                JOIN guru_dhika g ON pm.guru_id = g.id_guru
                WHERE s.kelas = %s AND s.jurusan = %s AND s.rombel = %s
                ORDER BY pm.tanggal DESC
            """, (walikelas['kelas'], walikelas['jurusan'], walikelas['rombel']))
            panggilan_list = cursor.fetchall()
            headers = ['Siswa', 'Kelas', 'Guru BK', 'Tanggal', 'Status', 'Tujuan', 'Catatan']
            rows = [[
                row['nama_siswa'],
                f"{row['kelas']} - {row['jurusan']} - {row['rombel']}",
                row['nama_guru_bk'],
                format_export_value_dhika(row['tanggal']),
                row['status'] or 'Dijadwalkan',
                row['tujuan'],
                row['catatan'] or '-'
            ] for row in panggilan_list]
            title = f'Riwayat Panggilan Ortu - {kelas_label}'
            filename = f"walikelas_panggilan_ortu_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            response = export_excel_response_dhika(filename, title, headers, rows) if filetype == 'excel' else export_pdf_response_dhika(filename, title, headers, rows, [32, 34, 35, 24, 24, 58, 58], 'L')

        cursor.close()
        conn.close()
        return response
    except Exception as e:
        flash_dhika(f'Error export wali kelas: {str(e)}', 'error')
        return redirect(url_for('dashboard_walikelas_dhika'))


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
            
            # Query gabungan untuk guru BK, wali kelas, dan kesiswaan
            akun = session['id_akun']
            cursor.execute("""
                SELECT a.id_akun as akun_id, 
                    COALESCE(g.nama, wk.nama, ks.nama, ad.nama) as nama,
                    a.role,
                    (SELECT pesan FROM chat_dhika
                     WHERE (pengirim_akun_id=%s AND penerima_akun_id=a.id_akun)
                        OR (pengirim_akun_id=a.id_akun AND penerima_akun_id=%s)
                     ORDER BY waktu DESC LIMIT 1) as pesan_terakhir,
                    (SELECT waktu FROM chat_dhika
                     WHERE (pengirim_akun_id=%s AND penerima_akun_id=a.id_akun)
                        OR (pengirim_akun_id=a.id_akun AND penerima_akun_id=%s)
                     ORDER BY waktu DESC LIMIT 1) as waktu_terakhir,
                    (SELECT COUNT(*) FROM chat_dhika
                     WHERE pengirim_akun_id=a.id_akun AND penerima_akun_id=%s AND dibaca=0) as unread_count
                FROM akun_dhika a
                LEFT JOIN guru_dhika g ON a.id_akun = g.akun_id
                LEFT JOIN wali_kelas_dhika wk ON a.id_akun = wk.akun_id
                LEFT JOIN kesiswaan_dhika ks ON a.id_akun = ks.akun_id
                LEFT JOIN admin_dhika ad ON a.id_akun = ad.akun_id
                WHERE a.role IN ('Guru BK', 'Wali Kelas', 'Kesiswaan', 'Admin')
                AND EXISTS (
                    SELECT 1 FROM chat_dhika
                    WHERE (pengirim_akun_id=%s AND penerima_akun_id=a.id_akun)
                       OR (pengirim_akun_id=a.id_akun AND penerima_akun_id=%s)
                )
                ORDER BY waktu_terakhir DESC
            """, (akun, akun, akun, akun, akun, akun, akun))
            kontak_list = cursor.fetchall()
        else:
            cursor.execute("SELECT id_guru FROM guru_dhika WHERE akun_id = %s", (session['id_akun'],))
            guru_row2 = cursor.fetchone()
            guru_id2 = guru_row2['id_guru'] if guru_row2 else None
            cursor.execute("""
                SELECT s.id_siswa, s.nama, a.id_akun as akun_id,
                    (SELECT pesan FROM chat_dhika
                     WHERE (pengirim_akun_id=%s AND penerima_akun_id=a.id_akun)
                        OR (pengirim_akun_id=a.id_akun AND penerima_akun_id=%s)
                     ORDER BY waktu DESC LIMIT 1) as pesan_terakhir,
                    (SELECT waktu FROM chat_dhika
                     WHERE (pengirim_akun_id=%s AND penerima_akun_id=a.id_akun)
                        OR (pengirim_akun_id=a.id_akun AND penerima_akun_id=%s)
                     ORDER BY waktu DESC LIMIT 1) as waktu_terakhir,
                    (SELECT COUNT(*) FROM chat_dhika
                     WHERE pengirim_akun_id=a.id_akun AND penerima_akun_id=%s AND dibaca=0) as unread_count
                FROM siswa_dhika s
                JOIN akun_dhika a ON s.akun_id = a.id_akun
                WHERE EXISTS (
                    SELECT 1 FROM chat_dhika
                    WHERE (pengirim_akun_id=%s AND penerima_akun_id=a.id_akun)
                       OR (pengirim_akun_id=a.id_akun AND penerima_akun_id=%s)
                ) OR s.id_siswa IN (SELECT siswa_id FROM konseling_dhika WHERE guru_id=%s)
                ORDER BY waktu_terakhir DESC
            """, (session['id_akun'], session['id_akun'], session['id_akun'], session['id_akun'],
                  session['id_akun'], session['id_akun'], session['id_akun'], guru_id2))
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
            SELECT pengirim_akun_id, pesan,
                   DATE_FORMAT(waktu, '%d/%m/%Y %H:%i') as waktu,
                   waktu as waktu_sort
            FROM chat_dhika
            WHERE (pengirim_akun_id=%s AND penerima_akun_id=%s)
               OR (pengirim_akun_id=%s AND penerima_akun_id=%s)
            ORDER BY waktu_sort ASC LIMIT 100
        """, (session['id_akun'], lawan_akun_id, lawan_akun_id, session['id_akun']))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        data = [{'pengirim_akun_id': r['pengirim_akun_id'], 'pesan': r['pesan'], 'waktu': r['waktu']} for r in rows]
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


        if not siswa:
          flash_dhika('Data siswa tidak ditemukan!', 'error')
          return redirect(url_for('login_dhika'))
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
            SELECT rp.tanggal, p.nama_pelanggaran, p.kategori
            FROM riwayat_pelanggaran_dhika rp
            JOIN pelanggaran_dhika p ON rp.pelanggaran_id = p.id_pelanggaran
            WHERE rp.siswa_id = %s
            ORDER BY rp.tanggal DESC LIMIT 3
        """, (siswa['id_siswa'],))
        riwayat_pelanggaran = cursor.fetchall()
        cursor.execute("""
            SELECT k.id_konseling, k.jenis, k.tanggal, k.jam_mulai, g.nama as nama_guru
            FROM konseling_dhika k
            JOIN guru_dhika g ON k.guru_id = g.id_guru
            WHERE k.siswa_id = %s AND k.status = 'Disetujui'
            AND k.tanggal >= CURDATE()
            ORDER BY k.tanggal ASC, k.jam_mulai ASC LIMIT 3
        """, (siswa['id_siswa'],))
        panggilan_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('dashboard/dashboard_siswa_dhika.html',
                               siswa=siswa, stats=stats,
                               konseling_terbaru=konseling_terbaru,
                               riwayat_pelanggaran=riwayat_pelanggaran,
                               panggilan_list=panggilan_list)
    except Exception as e:
        import traceback
        traceback.print_exc()   # 🔥 WAJIB

        flash_dhika(f'Error: {e}', 'error')  # biar keliatan di web
        return redirect(url_for('login_dhika'))


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
        
        # Query untuk statistik pengaduan
        cursor.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN status='Baru' THEN 1 ELSE 0 END) as baru,
                   SUM(CASE WHEN status='Diproses' THEN 1 ELSE 0 END) as diproses,
                   SUM(CASE WHEN status='Selesai' THEN 1 ELSE 0 END) as selesai
            FROM pengaduan_dhika
        """)
        pengaduan_stats = cursor.fetchone()
        
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
            WHERE k.guru_id = %s AND k.tanggal = %s
            ORDER BY k.jam_mulai
        """, (guru['id_guru'], today))
        konseling_hari_ini = cursor.fetchall()
        cursor.execute("""
            SELECT id_siswa, nama, kelas, jurusan, rombel
            FROM siswa_dhika ORDER BY nama ASC LIMIT 5
        """)
        siswa_list_preview = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('dashboard/dashboard_guru_dhika.html',
                               guru=guru, stats=stats, pengaduan_stats=pengaduan_stats,
                               jenis_stats=jenis_stats,
                               konseling_hari_ini=konseling_hari_ini,
                               today=today,
                               siswa_list_preview=siswa_list_preview)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('dashboard/dashboard_guru_dhika.html')


@app.route('/data/siswa')
def data_siswa_dhika():
    if 'logged_in' not in session or session.get('role') not in ['Guru BK', 'Kesiswaan', 'Wali Kelas']:
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
        siswa_all = cursor.fetchall()
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
        page = request.args.get('page', 1, type=int)
        search = request.args.get('q', '').strip()
        filter_kelas = request.args.get('kelas', '').strip()
        filter_jurusan = request.args.get('jurusan', '').strip()
        if search:
            siswa_all = [s for s in siswa_all if search.lower() in s['nama'].lower() or search.lower() in s['nis'].lower()]
        if filter_kelas:
            siswa_all = [s for s in siswa_all if s['kelas'] == filter_kelas]
        if filter_jurusan:
            siswa_all = [s for s in siswa_all if s['jurusan'] == filter_jurusan]
        pagination = paginate_dhika(siswa_all, page, 20)
        return render_template('data/data_siswa_dhika.html',
                               siswa_list=pagination['items'],
                               pagination=pagination,
                               kelas_stats=kelas_stats,
                               jurusan_stats=jurusan_stats,
                               search=search,
                               filter_kelas=filter_kelas,
                               filter_jurusan=filter_jurusan)
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
        guru_all = cursor.fetchall()
        cursor.execute("""
            SELECT g.nama,
                   COUNT(k.id_konseling) as total_konseling,
                   SUM(CASE WHEN k.status='Pending' THEN 1 ELSE 0 END) as pending,
                   SUM(CASE WHEN k.status='Selesai' THEN 1 ELSE 0 END) as selesai
            FROM guru_dhika g
            LEFT JOIN konseling_dhika k ON g.id_guru = k.guru_id
            GROUP BY g.id_guru, g.nama
            ORDER BY total_konseling DESC
        """)
        beban_kerja = cursor.fetchall()
        cursor.close()
        conn.close()
        page = request.args.get('page', 1, type=int)
        search = request.args.get('q', '').strip()
        if search:
            guru_all = [g for g in guru_all if search.lower() in g['nama'].lower() or search.lower() in g.get('nip','').lower()]
        pagination = paginate_dhika(guru_all, page, 20)
        return render_template('data/data_guru_dhika.html',
                               guru_list=pagination['items'],
                               pagination=pagination,
                               beban_kerja=beban_kerja,
                               search=search)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('data/data_guru_dhika.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile_dhika():
    if 'logged_in' not in session:
        return redirect(url_for('login_dhika'))
    role = session.get('role')
    config = get_profile_config_dhika(role)
    if not config:
        flash_dhika('Role tidak dikenali untuk halaman profil.', 'error')
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        user_data = fetch_profile_data_dhika(cursor, session['id_akun'], role)
        if not user_data:
            cursor.close()
            conn.close()
            flash_dhika('Data profil tidak ditemukan.', 'error')
            return redirect(url_for(get_dashboard_endpoint_dhika(role)))

        if request.method == 'POST':
            update_fields = []
            update_values = []

            if config['allow_email']:
                email = normalize_nullable_value_dhika(request.form.get('email_dhika'))
                if not valid_email_dhika(email):
                    cursor.close()
                    conn.close()
                    flash_dhika('Format email tidak valid.', 'error')
                    return redirect(url_for('profile_dhika'))
                update_fields.append("email = %s")
                update_values.append(email)

            if config['allow_no_hp']:
                no_hp = normalize_nullable_value_dhika(request.form.get('no_hp_dhika'))
                if not valid_phone_dhika(no_hp):
                    cursor.close()
                    conn.close()
                    flash_dhika('Format no. HP tidak valid.', 'error')
                    return redirect(url_for('profile_dhika'))
                update_fields.append("no_hp = %s")
                update_values.append(no_hp)

            if config['allow_no_ortu']:
                no_ortu = normalize_nullable_value_dhika(request.form.get('no_ortu_dhika'))
                if not valid_phone_dhika(no_ortu):
                    cursor.close()
                    conn.close()
                    flash_dhika('Format no. HP ortu tidak valid.', 'error')
                    return redirect(url_for('profile_dhika'))
                update_fields.append("no_ortu = %s")
                update_values.append(no_ortu)

            foto_baru = None
            if 'foto_profil_dhika' in request.files:
                foto = request.files['foto_profil_dhika']
                if foto and foto.filename:
                    if not allowed_file_dhika(foto.filename):
                        cursor.close()
                        conn.close()
                        flash_dhika('Format foto profil harus jpg, jpeg, png, atau webp.', 'error')
                        return redirect(url_for('profile_dhika'))
                    ext = foto.filename.rsplit('.', 1)[1].lower()
                    foto_baru = f"{uuid.uuid4().hex}.{ext}"
                    foto.save(os.path.join(PROFILE_UPLOAD_FOLDER, foto_baru))
                    update_fields.append("foto_profil = %s")
                    update_values.append(foto_baru)

                    foto_lama = user_data.get('foto_profil')
                    if foto_lama:
                        foto_lama_path = os.path.join(PROFILE_UPLOAD_FOLDER, foto_lama)
                        if os.path.exists(foto_lama_path):
                            try:
                                os.remove(foto_lama_path)
                            except OSError:
                                pass

            if update_fields:
                update_values.append(session['id_akun'])
                cursor.execute(
                    f"UPDATE {config['table']} SET {', '.join(update_fields)} WHERE akun_id = %s",
                    tuple(update_values)
                )
                conn.commit()

            user_data = fetch_profile_data_dhika(cursor, session['id_akun'], role)
            session['foto_profil'] = (user_data or {}).get('foto_profil')
            session['profile_updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_aktivitas_dhika(session['id_akun'], 'Memperbarui profil akun')
            flash_dhika('Profil berhasil diperbarui.', 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('profile_dhika'))

        cursor.close()
        conn.close()
        return render_template('akun/profile_dhika.html', user=user_data, profile_config=config)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for(get_dashboard_endpoint_dhika(role)))


@app.route('/pelanggaran')
def pelanggaran_dhika():
    if 'logged_in' not in session or session.get('role') not in ['Guru BK', 'Kesiswaan']:
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_siswa, nama, kelas, jurusan, rombel FROM siswa_dhika ORDER BY kelas, jurusan, rombel, nama")
        siswa_list = cursor.fetchall()
        cursor.execute("""
            SELECT rp.id_riwayat, s.nama as nama_siswa, s.kelas, s.rombel,
                   p.nama_pelanggaran, p.kategori, rp.tanggal, rp.keterangan
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
        cursor.execute("SELECT id_pelanggaran, nama_pelanggaran, kategori FROM pelanggaran_dhika ORDER BY kategori, nama_pelanggaran")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception:
        return jsonify([])


@app.route('/pelanggaran/input', methods=['POST'])
def pelanggaran_input_dhika():
    if 'logged_in' not in session or session.get('role') not in ['Guru BK', 'Kesiswaan']:
        return redirect(url_for('login_dhika'))
    try:
        siswa_id = request.form.get('siswa_id_dhika')
        pelanggaran_id = request.form.get('pelanggaran_id_dhika')
        tanggal = request.form.get('tanggal_dhika')
        keterangan = request.form.get('keterangan_dhika', '')
        tindakan_guru = request.form.get('tindakan_guru_dhika', '')
        tindak_lanjut = request.form.get('tindak_lanjut_dhika', '')
        foto_path = save_optional_image_dhika(request.files.get('foto_dhika'))
        foto_surat = save_optional_image_dhika(request.files.get('foto_surat_dhika'))
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_pelanggaran FROM pelanggaran_dhika WHERE id_pelanggaran = %s", (pelanggaran_id,))
        pel = cursor.fetchone()
        if not pel:
            flash_dhika('Jenis pelanggaran tidak ditemukan', 'error')
            return redirect(url_for('pelanggaran_dhika'))
        cursor.execute("""
            INSERT INTO riwayat_pelanggaran_dhika
            (siswa_id, pelanggaran_id, tanggal, keterangan, tindakan_guru, tindak_lanjut, foto_surat, foto_dokumentasi)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (siswa_id, pelanggaran_id, tanggal, keterangan,
              tindakan_guru or None, tindak_lanjut or None, foto_surat, foto_path))
        conn.commit()
        log_aktivitas_dhika(session['id_akun'], f'Input pelanggaran siswa id {siswa_id}')
        cursor.close()
        conn.close()
        flash_dhika('Pelanggaran berhasil dicatat.', 'success')
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('pelanggaran_dhika'))


@app.route('/pelanggaran/siswa/<int:siswa_id>')
def pelanggaran_siswa_detail_dhika(siswa_id):
    if 'logged_in' not in session or session.get('role') not in ['Guru BK', 'Kesiswaan']:
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM siswa_dhika WHERE id_siswa = %s", (siswa_id,))
        siswa = cursor.fetchone()
        if not siswa:
            flash_dhika('Siswa tidak ditemukan', 'error')
            return redirect(url_for('pelanggaran_dhika'))
        cursor.execute("""
            SELECT rp.*, p.nama_pelanggaran, p.kategori
            FROM riwayat_pelanggaran_dhika rp
            JOIN pelanggaran_dhika p ON rp.pelanggaran_id = p.id_pelanggaran
            WHERE rp.siswa_id = %s ORDER BY rp.tanggal DESC
        """, (siswa_id,))
        riwayat = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('pelanggaran/pelanggaran_detail_dhika.html', siswa=siswa, riwayat=riwayat)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for('pelanggaran_dhika'))


@app.route('/pelanggaran/riwayat/<int:id_riwayat>')
def detail_pelanggaran_riwayat_dhika(id_riwayat):
    if 'logged_in' not in session or session.get('role') not in ['Siswa', 'Guru BK', 'Kesiswaan', 'Wali Kelas']:
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT rp.*, p.nama_pelanggaran, p.kategori,
                   s.id_siswa, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel
            FROM riwayat_pelanggaran_dhika rp
            JOIN pelanggaran_dhika p ON rp.pelanggaran_id = p.id_pelanggaran
            JOIN siswa_dhika s ON rp.siswa_id = s.id_siswa
            WHERE rp.id_riwayat = %s
        """, (id_riwayat,))
        riwayat = cursor.fetchone()
        if not riwayat or not can_access_student_record_dhika(cursor, riwayat['id_siswa']):
            cursor.close()
            conn.close()
            flash_dhika('Detail pelanggaran tidak ditemukan atau tidak bisa diakses.', 'error')
            return redirect(url_for(get_dashboard_endpoint_dhika(session.get('role'))))
        back_url, back_label = get_detail_back_context_dhika('pelanggaran', riwayat['id_siswa'])
        cursor.close()
        conn.close()
        return render_template(
            'detail/detail_pelanggaran_dhika.html',
            riwayat=riwayat,
            back_url=back_url,
            back_label=back_label
        )
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for(get_dashboard_endpoint_dhika(session.get('role'))))





@app.route('/pelanggaran/saya')
def pelanggaran_saya_dhika():
    if 'logged_in' not in session or session.get('role') != 'Siswa':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM siswa_dhika WHERE akun_id = %s", (session['id_akun'],))
        siswa = cursor.fetchone()
        cursor.execute("""
            SELECT rp.*, p.nama_pelanggaran, p.kategori
            FROM riwayat_pelanggaran_dhika rp
            JOIN pelanggaran_dhika p ON rp.pelanggaran_id = p.id_pelanggaran
            WHERE rp.siswa_id = %s ORDER BY rp.tanggal DESC
        """, (siswa['id_siswa'],))
        riwayat = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('pelanggaran/pelanggaran_saya_dhika.html', siswa=siswa, riwayat=riwayat)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('pelanggaran/pelanggaran_saya_dhika.html', siswa={}, riwayat=[], notif=None)


@app.route('/dashboard/walikelas')
def dashboard_walikelas_dhika():
    if 'logged_in' not in session or session.get('role') != 'Wali Kelas':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM wali_kelas_dhika WHERE akun_id = %s", (session['id_akun'],))
        walikelas = cursor.fetchone()
        cursor.execute("""
            SELECT s.*
            FROM siswa_dhika s
            WHERE s.kelas = %s AND s.jurusan = %s AND s.rombel = %s
            ORDER BY s.nama
        """, (walikelas['kelas'], walikelas['jurusan'], walikelas['rombel']))
        siswa_list = cursor.fetchall()
        for s in siswa_list:
            cursor.execute("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN status='Pending' THEN 1 ELSE 0 END) as pending,
                       SUM(CASE WHEN status='Selesai' THEN 1 ELSE 0 END) as selesai
                FROM konseling_dhika WHERE siswa_id = %s
            """, (s['id_siswa'],))
            s['stats_konseling'] = cursor.fetchone()
            cursor.execute("""
                SELECT COUNT(*) as total FROM riwayat_pelanggaran_dhika WHERE siswa_id = %s
            """, (s['id_siswa'],))
            s['total_pelanggaran'] = cursor.fetchone()['total']
        cursor.execute("""
            SELECT pm.*, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel, g.nama as nama_guru_bk
            FROM pemanggilan_ortu_dhika pm
            JOIN siswa_dhika s ON pm.siswa_id = s.id_siswa
            JOIN guru_dhika g ON pm.guru_id = g.id_guru
            WHERE s.kelas = %s AND s.jurusan = %s AND s.rombel = %s
            ORDER BY pm.tanggal DESC
        """, (walikelas['kelas'], walikelas['jurusan'], walikelas['rombel']))
        panggilan_ortu_terbaru = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('dashboard/dashboard_walikelas_dhika.html',
                               walikelas=walikelas, siswa_list=siswa_list,
                               panggilan_ortu_terbaru=panggilan_ortu_terbaru)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('dashboard/dashboard_walikelas_dhika.html', walikelas={}, siswa_list=[], panggilan_ortu_terbaru=[])


@app.route('/walikelas/siswa/<int:siswa_id>')
def walikelas_detail_siswa_dhika(siswa_id):
    if 'logged_in' not in session or session.get('role') != 'Wali Kelas':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM wali_kelas_dhika WHERE akun_id = %s", (session['id_akun'],))
        walikelas = cursor.fetchone()
        cursor.execute("SELECT * FROM siswa_dhika WHERE id_siswa = %s AND kelas = %s AND jurusan = %s AND rombel = %s",
                       (siswa_id, walikelas['kelas'], walikelas['jurusan'], walikelas['rombel']))
        siswa = cursor.fetchone()
        if not siswa:
            flash_dhika('Siswa tidak ditemukan atau bukan wali kelas siswa ini.', 'error')
            return redirect(url_for('dashboard_walikelas_dhika'))
        cursor.execute("""
            SELECT k.*, g.nama as nama_guru
            FROM konseling_dhika k
            JOIN guru_dhika g ON k.guru_id = g.id_guru
            WHERE k.siswa_id = %s ORDER BY k.tanggal DESC
        """, (siswa_id,))
        riwayat_konseling = cursor.fetchall()
        cursor.execute("""
            SELECT rp.*, p.nama_pelanggaran, p.kategori
            FROM riwayat_pelanggaran_dhika rp
            JOIN pelanggaran_dhika p ON rp.pelanggaran_id = p.id_pelanggaran
            WHERE rp.siswa_id = %s ORDER BY rp.tanggal DESC
        """, (siswa_id,))
        riwayat_pelanggaran = cursor.fetchall()
        cursor.execute("""
            SELECT pg.*, ks.nama as nama_kesiswaan
            FROM pengaduan_dhika pg
            JOIN kesiswaan_dhika ks ON pg.kesiswaan_id = ks.id_kesiswaan
            WHERE pg.siswa_id = %s ORDER BY pg.tanggal DESC
        """, (siswa_id,))
        riwayat_pengaduan = cursor.fetchall()
        cursor.execute("""
            SELECT pm.*, g.nama as nama_guru_bk
            FROM pemanggilan_ortu_dhika pm
            JOIN guru_dhika g ON pm.guru_id = g.id_guru
            WHERE pm.siswa_id = %s ORDER BY pm.tanggal DESC
        """, (siswa_id,))
        riwayat_pemanggilan_ortu = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('guru/walikelas_detail_siswa_dhika.html',
                               siswa=siswa, riwayat_konseling=riwayat_konseling,
                               riwayat_pengaduan=riwayat_pengaduan,
                               riwayat_pelanggaran=riwayat_pelanggaran,
                               riwayat_pemanggilan_ortu=riwayat_pemanggilan_ortu)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for('dashboard_walikelas_dhika'))


@app.route('/dashboard/kesiswaan')
def dashboard_kesiswaan_dhika():
    if 'logged_in' not in session or session.get('role') != 'Kesiswaan':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM kesiswaan_dhika WHERE akun_id = %s", (session['id_akun'],))
        kesiswaan = cursor.fetchone()
        cursor.execute("""
            SELECT pg.*, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel
            FROM pengaduan_dhika pg
            JOIN siswa_dhika s ON pg.siswa_id = s.id_siswa
            ORDER BY pg.tanggal DESC
        """)
        pengaduan_list = cursor.fetchall()
        cursor.execute("""
            SELECT pm.*, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel, g.nama as nama_guru_bk
            FROM pemanggilan_ortu_dhika pm
            JOIN siswa_dhika s ON pm.siswa_id = s.id_siswa
            JOIN guru_dhika g ON pm.guru_id = g.id_guru
            ORDER BY pm.tanggal DESC
        """)
        panggilan_ortu_list = cursor.fetchall()
        cursor.execute("""
            SELECT rp.*, p.nama_pelanggaran, p.kategori,
                   s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel
            FROM riwayat_pelanggaran_dhika rp
            JOIN pelanggaran_dhika p ON rp.pelanggaran_id = p.id_pelanggaran
            JOIN siswa_dhika s ON rp.siswa_id = s.id_siswa
            ORDER BY rp.tanggal DESC
            LIMIT 8
        """)
        riwayat_pelanggaran_terbaru = cursor.fetchall()
        cursor.execute("SELECT id_siswa, nama, kelas, jurusan, rombel FROM siswa_dhika ORDER BY kelas, jurusan, rombel, nama")
        siswa_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('dashboard/dashboard_kesiswaan_dhika.html',
                               kesiswaan=kesiswaan, pengaduan_list=pengaduan_list,
                               siswa_list=siswa_list, panggilan_ortu_list=panggilan_ortu_list,
                               riwayat_pelanggaran_terbaru=riwayat_pelanggaran_terbaru)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('dashboard/dashboard_kesiswaan_dhika.html', kesiswaan={}, pengaduan_list=[], panggilan_ortu_list=[], riwayat_pelanggaran_terbaru=[])





@app.route('/pengaduan/buat', methods=['POST'])
def buat_pengaduan_dhika():
    if 'logged_in' not in session or session.get('role') != 'Kesiswaan':
        return redirect(url_for('login_dhika'))
    try:
        siswa_id = request.form.get('siswa_id_dhika')
        judul = request.form.get('judul_dhika', '').strip()
        deskripsi = request.form.get('deskripsi_dhika', '').strip()
        if not all([siswa_id, judul, deskripsi]):
            flash_dhika('Semua field harus diisi!', 'error')
            return redirect(url_for('dashboard_kesiswaan_dhika'))
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_kesiswaan FROM kesiswaan_dhika WHERE akun_id = %s", (session['id_akun'],))
        ks = cursor.fetchone()
        cursor.execute(
            "INSERT INTO pengaduan_dhika (kesiswaan_id, siswa_id, judul, deskripsi) VALUES (%s, %s, %s, %s)",
            (ks['id_kesiswaan'], siswa_id, judul, deskripsi)
        )
        conn.commit()
        cursor.close()
        conn.close()
        log_aktivitas_dhika(session['id_akun'], f'Membuat pengaduan untuk siswa id {siswa_id}')
        flash_dhika('Pengaduan berhasil dibuat.', 'success')
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('dashboard_kesiswaan_dhika'))


@app.route('/pengaduan/update/<int:id_pengaduan>', methods=['POST'])
def update_pengaduan_dhika(id_pengaduan):
    if 'logged_in' not in session or session.get('role') not in ['Kesiswaan', 'Guru BK']:
        return redirect(url_for('login_dhika'))
    try:
        status = request.form.get('status_dhika')
        catatan = request.form.get('catatan_dhika', '').strip()
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        cursor.execute(
            "UPDATE pengaduan_dhika SET status = %s, catatan = %s WHERE id_pengaduan = %s",
            (status, catatan, id_pengaduan)
        )
        conn.commit()
        cursor.close()
        conn.close()
        log_aktivitas_dhika(session['id_akun'], f'Update pengaduan #{id_pengaduan} ke {status}')
        flash_dhika('Pengaduan berhasil diupdate.', 'success')
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    role = session.get('role')
    if role == 'Guru BK':
        return redirect(url_for('guru_lihat_pengaduan_dhika'))
    return redirect(url_for('dashboard_kesiswaan_dhika'))


@app.route('/pengaduan/detail/<int:id_pengaduan>')
def detail_pengaduan_dhika(id_pengaduan):
    if 'logged_in' not in session or session.get('role') not in ['Guru BK', 'Kesiswaan', 'Wali Kelas']:
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT pg.*, s.id_siswa, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel,
                   ks.nama as nama_kesiswaan
            FROM pengaduan_dhika pg
            JOIN siswa_dhika s ON pg.siswa_id = s.id_siswa
            JOIN kesiswaan_dhika ks ON pg.kesiswaan_id = ks.id_kesiswaan
            WHERE pg.id_pengaduan = %s
        """, (id_pengaduan,))
        pengaduan = cursor.fetchone()
        if not pengaduan or not can_access_student_record_dhika(cursor, pengaduan['id_siswa']):
            cursor.close()
            conn.close()
            flash_dhika('Detail pengaduan tidak ditemukan atau tidak bisa diakses.', 'error')
            return redirect(url_for(get_dashboard_endpoint_dhika(session.get('role'))))
        back_url, back_label = get_detail_back_context_dhika('pengaduan', pengaduan['id_siswa'])
        cursor.close()
        conn.close()
        return render_template(
            'detail/detail_pengaduan_dhika.html',
            pengaduan=pengaduan,
            back_url=back_url,
            back_label=back_label
        )
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for(get_dashboard_endpoint_dhika(session.get('role'))))


@app.route('/dashboard/admin')
def dashboard_admin_dhika():
    if 'logged_in' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT COUNT(*) as total FROM akun_dhika")
        total_akun = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM siswa_dhika")
        total_siswa = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM guru_dhika")
        total_guru = cursor.fetchone()['total']
        cursor.execute("SELECT COUNT(*) as total FROM konseling_dhika")
        total_konseling = cursor.fetchone()['total']
        cursor.execute("""
            SELECT a.id_akun, a.username, a.role, a.status_akun, a.created_at
            FROM akun_dhika a ORDER BY a.created_at DESC
        """)
        semua_akun = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('dashboard/dashboard_admin_dhika.html',
                               total_akun=total_akun, total_siswa=total_siswa,
                               total_guru=total_guru, total_konseling=total_konseling,
                               semua_akun=semua_akun)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return render_template('dashboard/dashboard_admin_dhika.html')


@app.route('/admin/toggle-akun/<int:id_akun>', methods=['POST'])
def admin_toggle_akun_dhika(id_akun):
    if 'logged_in' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login_dhika'))
    try:
        status_baru = request.form.get('status_dhika')
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        cursor.execute("UPDATE akun_dhika SET status_akun = %s WHERE id_akun = %s", (status_baru, id_akun))
        conn.commit()
        cursor.close()
        conn.close()
        log_aktivitas_dhika(session['id_akun'], f'Update status akun #{id_akun} ke {status_baru}')
        flash_dhika('Status akun berhasil diubah.', 'success')
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('dashboard_admin_dhika'))


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
        return jsonify([{
            'aktivitas': d['aktivitas'],
            'waktu': d['waktu'].strftime('%d %b %Y %H:%M') if d['waktu'] else '-'
        } for d in data])
    except Exception:
        return jsonify([])


@app.route('/chat/unread')
def chat_unread_dhika():
    if 'logged_in' not in session:
        return jsonify({'count': 0})
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        cursor.execute(
            "SELECT COUNT(*) FROM chat_dhika WHERE penerima_akun_id = %s AND dibaca = 0",
            (session['id_akun'],)
        )
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({'count': count})
    except Exception:
        return jsonify({'count': 0})


@app.route('/chat/tandai-baca/<int:lawan_akun_id>', methods=['POST'])
def chat_tandai_baca_dhika(lawan_akun_id):
    if 'logged_in' not in session:
        return jsonify({'ok': False})
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        cursor.execute(
            "UPDATE chat_dhika SET dibaca = 1 WHERE pengirim_akun_id = %s AND penerima_akun_id = %s AND dibaca = 0",
            (lawan_akun_id, session['id_akun'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'ok': True})
    except Exception:
        return jsonify({'ok': False})


@app.route('/chat/kontak')
def chat_kontak_dhika():
    if 'logged_in' not in session:
        return jsonify([])
    role = session.get('role')
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        kontak = []
        if role == 'Wali Kelas':
            cursor.execute("SELECT kelas, jurusan, rombel FROM wali_kelas_dhika WHERE akun_id = %s", (session['id_akun'],))
            wk = cursor.fetchone()
            cursor.execute("""
                SELECT a.id_akun, g.nama, 'Guru BK' as role
                FROM guru_dhika g JOIN akun_dhika a ON g.akun_id = a.id_akun
                WHERE a.status_akun = 'Aktif'
            """)
            kontak += cursor.fetchall()
            if wk:
                cursor.execute("""
                    SELECT a.id_akun, s.nama, 'Siswa' as role
                    FROM siswa_dhika s JOIN akun_dhika a ON s.akun_id = a.id_akun
                    WHERE s.kelas = %s AND s.jurusan = %s AND s.rombel = %s
                    AND a.status_akun = 'Aktif'
                """, (wk['kelas'], wk['jurusan'], wk['rombel']))
                kontak += cursor.fetchall()
        elif role == 'Kesiswaan':
            cursor.execute("""
                SELECT a.id_akun, g.nama, 'Guru BK' as role
                FROM guru_dhika g JOIN akun_dhika a ON g.akun_id = a.id_akun
                WHERE a.status_akun = 'Aktif'
            """)
            kontak += cursor.fetchall()
            cursor.execute("""
                SELECT a.id_akun, wk.nama, 'Wali Kelas' as role
                FROM wali_kelas_dhika wk JOIN akun_dhika a ON wk.akun_id = a.id_akun
                WHERE a.status_akun = 'Aktif'
            """)
            kontak += cursor.fetchall()
            cursor.execute("""
                SELECT DISTINCT a.id_akun, s.nama, 'Siswa' as role
                FROM pengaduan_dhika pg
                JOIN siswa_dhika s ON pg.siswa_id = s.id_siswa
                JOIN akun_dhika a ON s.akun_id = a.id_akun
                JOIN kesiswaan_dhika ks ON pg.kesiswaan_id = ks.id_kesiswaan
                WHERE ks.akun_id = %s AND a.status_akun = 'Aktif'
            """, (session['id_akun'],))
            kontak += cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(kontak)
    except Exception as e:
        return jsonify([])



@app.route('/admin/tambah-akun', methods=['POST'])
def admin_tambah_akun_dhika():
    if 'logged_in' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login_dhika'))
    try:
        role = request.form.get('role_dhika')
        nama = request.form.get('nama_dhika', '').strip()
        username = request.form.get('username_dhika', '').strip()
        password = request.form.get('password_dhika', '').strip()
        nis = request.form.get('nis_dhika', '').strip()
        nip = request.form.get('nip_dhika', '').strip()
        kelas = request.form.get('kelas_dhika', '').strip()
        jurusan = request.form.get('jurusan_dhika', '').strip()
        rombel = request.form.get('rombel_dhika', '').strip()
        if not all([role, nama, username, password]):
            flash_dhika('Field wajib belum lengkap!', 'error')
            return redirect(url_for('dashboard_admin_dhika'))
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_akun FROM akun_dhika WHERE username = %s", (username,))
        if cursor.fetchone():
            flash_dhika('Username sudah dipakai!', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('dashboard_admin_dhika'))
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO akun_dhika (username, password, role, status_akun) VALUES (%s, %s, %s, 'Aktif')",
            (username, hashed_password, role)
        )
        akun_id = cursor.lastrowid
        if role == 'Siswa':
            cursor.execute(
                "INSERT INTO siswa_dhika (akun_id, nis, nama, kelas, jurusan, rombel) VALUES (%s, %s, %s, %s, %s, %s)",
                (akun_id, nis, nama, kelas, jurusan, rombel)
            )
        elif role == 'Guru BK':
            cursor.execute(
                "INSERT INTO guru_dhika (akun_id, nip, nama) VALUES (%s, %s, %s)",
                (akun_id, nip, nama)
            )
        elif role == 'Wali Kelas':
            cursor.execute(
                "INSERT INTO wali_kelas_dhika (akun_id, nama, nip, kelas, jurusan, rombel) VALUES (%s, %s, %s, %s, %s, %s)",
                (akun_id, nama, nip, kelas, jurusan, rombel)
            )
        elif role == 'Kesiswaan':
            cursor.execute(
                "INSERT INTO kesiswaan_dhika (akun_id, nama, nip) VALUES (%s, %s, %s)",
                (akun_id, nama, nip)
            )
        elif role == 'Admin':
            cursor.execute(
                "INSERT INTO admin_dhika (akun_id, nama) VALUES (%s, %s)",
                (akun_id, nama)
            )
        conn.commit()
        log_aktivitas_dhika(session['id_akun'], f'Membuat akun {role}: {username}')
        cursor.close()
        conn.close()
        flash_dhika(f'Akun {role} "{nama}" berhasil dibuat!', 'success')
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('dashboard_admin_dhika'))


@app.route('/laporan/pengaduan')
def laporan_pengaduan_dhika():
    if 'logged_in' not in session or session.get('role') != 'Kesiswaan':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT pg.*, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel,
                   ks.nama as nama_kesiswaan
            FROM pengaduan_dhika pg
            JOIN siswa_dhika s ON pg.siswa_id = s.id_siswa
            JOIN kesiswaan_dhika ks ON pg.kesiswaan_id = ks.id_kesiswaan
            ORDER BY pg.tanggal DESC
        """)
        pengaduan_list = cursor.fetchall()
        cursor.execute("""
            SELECT COUNT(*) as total,
                SUM(CASE WHEN status='Baru' THEN 1 ELSE 0 END) as baru,
                SUM(CASE WHEN status='Diproses' THEN 1 ELSE 0 END) as diproses,
                SUM(CASE WHEN status='Selesai' THEN 1 ELSE 0 END) as selesai
            FROM pengaduan_dhika
        """)
        stats = cursor.fetchone()
        cursor.close()
        conn.close()
        page = request.args.get('page', 1, type=int)
        search = request.args.get('q', '').strip()
        if search:
            pengaduan_list = [p for p in pengaduan_list if search.lower() in p.get('nama_siswa','').lower()]
        pagination = paginate_dhika(pengaduan_list, page, 20)
        return render_template('laporan/laporan_pengaduan_dhika.html',
                               pengaduan_list=pagination['items'],
                               pagination=pagination,
                               stats=stats,
                               search=search)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for('dashboard_kesiswaan_dhika'))


@app.route('/admin/manajemen-kelas')
def admin_manajemen_kelas_dhika():
    if 'logged_in' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT kelas, jurusan, rombel, COUNT(*) as jumlah
            FROM siswa_dhika
            GROUP BY kelas, jurusan, rombel
            ORDER BY kelas, jurusan, rombel
        """)
        kelas_data = cursor.fetchall()
        cursor.execute("""
            SELECT wk.*, a.username
            FROM wali_kelas_dhika wk
            JOIN akun_dhika a ON wk.akun_id = a.id_akun
        """)
        walikelas_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('dashboard/admin_kelas_dhika.html',
                               kelas_data=kelas_data, walikelas_list=walikelas_list)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for('dashboard_admin_dhika'))


@app.route('/admin/log-aktivitas')
def admin_log_aktivitas_dhika():
    if 'logged_in' not in session or session.get('role') != 'Admin':
        return redirect(url_for('login_dhika'))
    try:
        search = request.args.get('q', '').strip()
        role_filter = request.args.get('role', '').strip()
        start_date = request.args.get('start_date', '').strip()
        end_date = request.args.get('end_date', '').strip()

        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        query = """
            SELECT l.*, a.username, a.role
            FROM log_aktivitas_dhika l
            JOIN akun_dhika a ON l.akun_id = a.id_akun
        """
        conditions = []
        params = []

        if search:
            conditions.append("(a.username LIKE %s OR l.aktivitas LIKE %s)")
            keyword = f"%{search}%"
            params.extend([keyword, keyword])

        if role_filter:
            conditions.append("a.role = %s")
            params.append(role_filter)

        if start_date:
            conditions.append("DATE(l.waktu) >= %s")
            params.append(start_date)

        if end_date:
            conditions.append("DATE(l.waktu) <= %s")
            params.append(end_date)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY l.waktu DESC LIMIT 300"
        cursor.execute(query, tuple(params))
        log_list = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template(
            'dashboard/admin_log_dhika.html',
            log_list=log_list,
            filters={
                'q': search,
                'role': role_filter,
                'start_date': start_date,
                'end_date': end_date,
            }
        )
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for('dashboard_admin_dhika'))


@app.route('/api/siswa-by-kelas')
def api_siswa_by_kelas_dhika():
    if 'logged_in' not in session:
        return jsonify([])
    kelas = request.args.get('kelas', '')
    jurusan = request.args.get('jurusan', '')
    rombel = request.args.get('rombel', '')
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        conditions = []
        params = []
        if kelas:
            conditions.append("kelas = %s")
            params.append(kelas)
        if jurusan:
            conditions.append("jurusan = %s")
            params.append(jurusan)
        if rombel:
            conditions.append("rombel = %s")
            params.append(rombel)
        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        cursor.execute(
            "SELECT id_siswa, nama, kelas, jurusan, rombel FROM siswa_dhika " + where + " ORDER BY nama",
            params
        )
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify([])


@app.route('/guru/pengaduan')
def guru_lihat_pengaduan_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT pg.*, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel, s.id_siswa,
                   ks.nama as nama_kesiswaan
            FROM pengaduan_dhika pg
            JOIN siswa_dhika s ON pg.siswa_id = s.id_siswa
            JOIN kesiswaan_dhika ks ON pg.kesiswaan_id = ks.id_kesiswaan
            ORDER BY pg.tanggal DESC
        """)
        pengaduan_list = cursor.fetchall()
        cursor.execute("SELECT id_guru FROM guru_dhika WHERE akun_id = %s", (session['id_akun'],))
        guru = cursor.fetchone()
        cursor.execute("""
            SELECT k.*, s.nama as nama_siswa FROM konseling_dhika k
            JOIN siswa_dhika s ON k.siswa_id = s.id_siswa
            WHERE k.guru_id = %s AND k.status IN ('Pending','Disetujui')
            ORDER BY k.tanggal DESC
        """, (guru['id_guru'],))
        konseling_aktif = cursor.fetchall()
        cursor.close()
        conn.close()
        page = request.args.get('page', 1, type=int)
        search = request.args.get('q', '').strip()
        filter_status = request.args.get('status', '').strip()
        if search:
            pengaduan_list = [p for p in pengaduan_list if search.lower() in p.get('nama_siswa','').lower()]
        if filter_status:
            pengaduan_list = [p for p in pengaduan_list if p['status'] == filter_status]
        pagination = paginate_dhika(pengaduan_list, page, 15)
        return render_template('konseling/guru_pengaduan_dhika.html',
                               pengaduan_list=pagination['items'],
                               pagination=pagination,
                               konseling_aktif=konseling_aktif,
                               search=search,
                               filter_status=filter_status)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for('dashboard_guru_dhika'))


@app.route('/guru/panggil-siswa', methods=['POST'])
def guru_panggil_siswa_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        siswa_id = request.form.get('siswa_id_dhika')
        tanggal = request.form.get('tanggal_dhika')
        jam_mulai = request.form.get('jam_mulai_dhika')
        alasan = request.form.get('alasan_dhika', '').strip()
        pengaduan_id = request.form.get('pengaduan_id_dhika')
        if not all([siswa_id, tanggal, jam_mulai]):
            flash_dhika('Tanggal dan jam harus diisi!', 'error')
            return redirect(url_for('guru_lihat_pengaduan_dhika'))
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT id_konseling FROM konseling_dhika ORDER BY id_konseling DESC LIMIT 1")
        last = cursor.fetchone()
        if last and last[0].startswith('KS'):
            num = int(last[0][2:]) + 1
        else:
            num = 1
        id_konseling = f"KS{num:04d}"
        cursor.execute("SELECT id_guru FROM guru_dhika WHERE akun_id = %s", (session['id_akun'],))
        guru = cursor.fetchone()
        cursor.execute("""
            INSERT INTO konseling_dhika
            (id_konseling, siswa_id, guru_id, jenis, tanggal, jam_mulai, alasan, status)
            VALUES (%s, %s, %s, 'Pribadi', %s, %s, %s, 'Disetujui')
        """, (id_konseling, siswa_id, guru[0], tanggal, jam_mulai,
              alasan or 'Panggilan dari Guru BK'))
        if pengaduan_id:
            cursor.execute(
                "UPDATE pengaduan_dhika SET status = 'Diproses' WHERE id_pengaduan = %s",
                (pengaduan_id,)
            )
        conn.commit()
        log_aktivitas_dhika(session['id_akun'], f'Memanggil siswa id {siswa_id} untuk konseling {id_konseling}')
        cursor.close()
        conn.close()
        flash_dhika('Siswa berhasil dipanggil! Jadwal konseling sudah dibuat.', 'success')
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('guru_lihat_pengaduan_dhika'))


@app.route('/guru/pemanggilan-ortu')
def pemanggilan_ortu_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_guru FROM guru_dhika WHERE akun_id = %s", (session['id_akun'],))
        guru = cursor.fetchone()
        cursor.execute("""
            SELECT pm.*, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel, s.no_ortu
            FROM pemanggilan_ortu_dhika pm
            JOIN siswa_dhika s ON pm.siswa_id = s.id_siswa
            WHERE pm.guru_id = %s
            ORDER BY pm.tanggal DESC
        """, (guru['id_guru'],))
        pemanggilan_list = cursor.fetchall()
        cursor.close()
        conn.close()
        page = request.args.get('page', 1, type=int)
        search = request.args.get('q', '').strip()
        if search:
            pemanggilan_list = [p for p in pemanggilan_list if search.lower() in p.get('nama_siswa','').lower()]
        pagination = paginate_dhika(pemanggilan_list, page, 15)
        return render_template('guru/pemanggilan_ortu_dhika.html',
                               pemanggilan_list=pagination['items'],
                               pagination=pagination,
                               search=search)
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for('dashboard_guru_dhika'))


@app.route('/guru/pemanggilan-ortu/buat', methods=['POST'])
def buat_pemanggilan_ortu_dhika():
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        siswa_id = request.form.get('siswa_id_dhika')
        tujuan = request.form.get('tujuan_dhika', '').strip()
        tanggal = request.form.get('tanggal_dhika')
        if not all([siswa_id, tujuan, tanggal]):
            flash_dhika('Semua field wajib diisi!', 'error')
            return redirect(url_for('pemanggilan_ortu_dhika'))
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT id_guru FROM guru_dhika WHERE akun_id = %s", (session['id_akun'],))
        guru = cursor.fetchone()
        cursor.execute("""
            INSERT INTO pemanggilan_ortu_dhika (siswa_id, guru_id, tujuan, tanggal)
            VALUES (%s, %s, %s, %s)
        """, (siswa_id, guru['id_guru'], tujuan, tanggal))
        conn.commit()
        log_aktivitas_dhika(session['id_akun'], f'Membuat pemanggilan orang tua siswa id {siswa_id}')
        cursor.close()
        conn.close()
        flash_dhika('Pemanggilan orang tua berhasil dijadwalkan!', 'success')
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('pemanggilan_ortu_dhika'))


@app.route('/guru/pemanggilan-ortu/update/<int:id_pemanggilan>', methods=['POST'])
def update_pemanggilan_ortu_dhika(id_pemanggilan):
    if 'logged_in' not in session or session.get('role') != 'Guru BK':
        return redirect(url_for('login_dhika'))
    try:
        status = request.form.get('status_dhika')
        catatan = request.form.get('catatan_dhika', '')
        foto_surat = save_optional_image_dhika(request.files.get('foto_surat_dhika'))
        foto_dokumentasi = save_optional_image_dhika(request.files.get('foto_dokumentasi_dhika'))
        conn = get_db_connection_dhika()
        cursor = conn.cursor(buffered=True)
        updates = ["status = %s", "catatan = %s"]
        params = [status, normalize_nullable_value_dhika(catatan)]
        if foto_surat:
            updates.append("foto_surat = %s")
            params.append(foto_surat)
        if foto_dokumentasi:
            updates.append("foto_dokumentasi = %s")
            params.append(foto_dokumentasi)
        params.append(id_pemanggilan)
        cursor.execute(
            f"UPDATE pemanggilan_ortu_dhika SET {', '.join(updates)} WHERE id_pemanggilan = %s",
            params
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash_dhika('Status pemanggilan berhasil diupdate.', 'success')
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
    return redirect(url_for('pemanggilan_ortu_dhika'))


@app.route('/pemanggilan-ortu/detail/<int:id_pemanggilan>')
def detail_pemanggilan_ortu_dhika(id_pemanggilan):
    if 'logged_in' not in session or session.get('role') not in ['Guru BK', 'Kesiswaan', 'Wali Kelas']:
        return redirect(url_for('login_dhika'))
    try:
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT pm.*, s.id_siswa, s.nama as nama_siswa, s.kelas, s.jurusan, s.rombel, s.no_ortu,
                   g.nama as nama_guru_bk
            FROM pemanggilan_ortu_dhika pm
            JOIN siswa_dhika s ON pm.siswa_id = s.id_siswa
            JOIN guru_dhika g ON pm.guru_id = g.id_guru
            WHERE pm.id_pemanggilan = %s
        """, (id_pemanggilan,))
        pemanggilan = cursor.fetchone()
        if not pemanggilan or not can_access_student_record_dhika(cursor, pemanggilan['id_siswa']):
            cursor.close()
            conn.close()
            flash_dhika('Detail pemanggilan tidak ditemukan atau tidak bisa diakses.', 'error')
            return redirect(url_for(get_dashboard_endpoint_dhika(session.get('role'))))
        back_url, back_label = get_detail_back_context_dhika('pemanggilan', pemanggilan['id_siswa'])
        cursor.close()
        conn.close()
        return render_template(
            'detail/detail_pemanggilan_ortu_dhika.html',
            pemanggilan=pemanggilan,
            back_url=back_url,
            back_label=back_label
        )
    except Exception as e:
        flash_dhika(f'Error: {str(e)}', 'error')
        return redirect(url_for(get_dashboard_endpoint_dhika(session.get('role'))))


@app.route('/chat/polling/<int:lawan_akun_id>')
def chat_polling_dhika(lawan_akun_id):
    if 'logged_in' not in session:
        return jsonify([])
    try:
        since = request.args.get('since', '')
        conn = get_db_connection_dhika()
        cursor = conn.cursor(dictionary=True, buffered=True)
        if since:
            cursor.execute("""
                SELECT pengirim_akun_id, pesan,
                       DATE_FORMAT(waktu, '%d/%m/%Y %H:%i') as waktu,
                       waktu as waktu_sort
                FROM chat_dhika
                WHERE ((pengirim_akun_id=%s AND penerima_akun_id=%s)
                    OR (pengirim_akun_id=%s AND penerima_akun_id=%s))
                AND waktu > %s
                ORDER BY waktu_sort ASC
            """, (session['id_akun'], lawan_akun_id, lawan_akun_id, session['id_akun'], since))
        else:
            cursor.execute("""
                SELECT pengirim_akun_id, pesan,
                       DATE_FORMAT(waktu, '%d/%m/%Y %H:%i') as waktu,
                       waktu as waktu_sort
                FROM chat_dhika
                WHERE (pengirim_akun_id=%s AND penerima_akun_id=%s)
                   OR (pengirim_akun_id=%s AND penerima_akun_id=%s)
                ORDER BY waktu_sort ASC LIMIT 100
            """, (session['id_akun'], lawan_akun_id, lawan_akun_id, session['id_akun']))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        data = [{'pengirim_akun_id': r['pengirim_akun_id'], 'pesan': r['pesan'], 'waktu': r['waktu'],
                 'waktu_sort': str(r['waktu_sort'])} for r in rows]
        return jsonify(data)
    except Exception:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
