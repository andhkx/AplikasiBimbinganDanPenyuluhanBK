import sys
import os

# Tambah path parent biar bisa import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import dari file appBK_dhika.py
from appBK_dhika import app as application

# Vercel butuh variable 'app'
app = application
