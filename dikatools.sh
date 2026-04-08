#!/data/data/com.termux/files/usr/bin/bash

# Warna keren
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Folder proyek
PROJECT_DIR="/storage/emulated/0/Download/Coding/AplikasiBimbinganDanPenyuluhanBK-main"
cd "$PROJECT_DIR" || { echo -e "${RED}❌ Folder tidak ditemukan!${NC}"; exit 1; }

# HEADER
echo -e "${CYAN}╔════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         🛠️  DIKA TOOLS v3.0                 ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}[?] Silahkan pilih menu:${NC}"
echo -e "${GREEN}[1]${NC} Commit & Push (Manual pesan)"
echo -e "${GREEN}[2]${NC} Pull update dari GitHub"
echo -e "${GREEN}[3]${NC} Lihat status file"
echo -e "${GREEN}[4]${NC} Lihat history commit (5 terakhir)"
echo -e "${GREEN}[5]${NC} Cek conflict sebelum commit"
echo -e "${GREEN}[6]${NC} Backup semua file"
echo -e "${RED}[7]${NC} Keluar & hapus session"
echo ""
read -p "Pilihan (1-7): " pilihan

case $pilihan in
    1)
        echo -e "${BLUE}────────────────────────────────────────${NC}"
        
        # Cek conflict dulu
        echo -e "${YELLOW}🔍 Cek conflict marker...${NC}"
        if grep -r "<<<<" . --include="*.html" --include="*.py" --include="*.txt" 2>/dev/null; then
            echo -e "${RED}❌ Masih ada conflict marker! Selesaikan dulu.${NC}"
            exit 1
        fi
        echo -e "${GREEN}✅ Tidak ada conflict.${NC}"
        
        # Pull update dari GitHub (biar aman)
        echo -e "${YELLOW}⬇️  Cek update dari GitHub...${NC}"
        git pull origin main --no-edit
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Gagal pull. Cek koneksi atau selesaikan conflict.${NC}"
            exit 1
        fi
        
        # Cek perubahan
        echo -e "${YELLOW}🔍 Mengecek perubahan lokal...${NC}"
        
        if [[ -z $(git status -s) ]]; then
            echo -e "${RED}✨ Tidak ada perubahan untuk di-commit.${NC}"
            exit 0
        fi
        
        echo -e "${BLUE}📁 File yang akan di-commit:${NC}"
        git status -s | while read line; do
            echo -e "   ${GREEN}➜${NC} $line"
        done
        
        echo -e "${YELLOW}➕ Menambahkan semua perubahan...${NC}"
        git add .
        
        # Manual commit message
        echo ""
        echo -e "${PURPLE}📝 Tulis pesan commit (WAJIB diisi):${NC}"
        echo -e "${CYAN}   Contoh: fix bug login, add fitur dashboard, update UI${NC}"
        read -p "> " user_msg
        
        while [[ -z "$user_msg" ]]; do
            echo -e "${RED}❌ Pesan commit tidak boleh kosong!${NC}"
            read -p "> " user_msg
        done
        
        COMMIT_MSG="$user_msg (📅 $(date +'%d/%m/%Y %H:%M:%S'))"
        echo -e "${PURPLE}📝 Commit message: ${WHITE}$COMMIT_MSG${NC}"
        
        git commit -m "$COMMIT_MSG"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Commit berhasil!${NC}"
        else
            echo -e "${RED}❌ Commit gagal!${NC}"
            exit 1
        fi
        
        echo -e "${YELLOW}☁️  Mengirim ke GitHub...${NC}"
        git push origin main
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
            echo -e "${GREEN}║   🎉 SUCCESS! Terkirim ke GitHub!     ║${NC}"
            echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
        else
            echo -e "${RED}❌ Push gagal! Cek koneksi atau token GitHub.${NC}"
        fi
        ;;
    
    2)
        echo -e "${BLUE}────────────────────────────────────────${NC}"
        echo -e "${YELLOW}⬇️  Menarik update dari GitHub...${NC}"
        git pull origin main
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Update berhasil ditarik!${NC}"
        else
            echo -e "${RED}❌ Gagal menarik update. Cek konflik atau koneksi.${NC}"
        fi
        ;;
    
    3)
        echo -e "${BLUE}────────────────────────────────────────${NC}"
        echo -e "${YELLOW}📊 Status file yang berubah:${NC}"
        git status -s
        if [[ -z $(git status -s) ]]; then
            echo -e "${GREEN}✅ Tidak ada perubahan, semua file sudah sync.${NC}"
        fi
        ;;
    
    4)
        echo -e "${BLUE}────────────────────────────────────────${NC}"
        echo -e "${YELLOW}📜 History 5 commit terakhir:${NC}"
        git log --oneline -5 --color=always
        ;;
    
    5)
        echo -e "${BLUE}────────────────────────────────────────${NC}"
        echo -e "${YELLOW}🔍 Mencari conflict marker di semua file...${NC}"
        CONFLICT_FOUND=$(grep -r "<<<<" . --include="*.html" --include="*.py" --include="*.txt" 2>/dev/null)
        if [[ -n "$CONFLICT_FOUND" ]]; then
            echo -e "${RED}⚠️ Conflict ditemukan di file:${NC}"
            echo "$CONFLICT_FOUND"
        else
            echo -e "${GREEN}✅ Tidak ada conflict marker. Aman!${NC}"
        fi
        ;;
    
    6)
        echo -e "${BLUE}────────────────────────────────────────${NC}"
        echo -e "${YELLOW}💾 Membuat backup...${NC}"
        BACKUP_DIR="../Backup_$(date +'%Y%m%d_%H%M%S')"
        mkdir -p "$BACKUP_DIR"
        cp -r ./* "$BACKUP_DIR/" 2>/dev/null
        echo -e "${GREEN}✅ Backup berhasil disimpan di:${NC}"
        echo -e "   ${CYAN}$BACKUP_DIR${NC}"
        ;;
    
    7)
        echo -e "${RED}🗑️  Menghapus session dan keluar...${NC}"
        git config --global --unset credential.helper
        echo -e "${GREEN}✅ Session terhapus! Sampai jumpa.${NC}"
        exit 0
        ;;
    
    *)
        echo -e "${RED}❌ Pilihan salah! Masukkan angka 1-7.${NC}"
        exit 1
        ;;
esac