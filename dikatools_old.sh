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

# HEADER ala BAHAN MUDS
echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║          🛠️  DIKA TOOLS v1.0           ║${NC}"
echo -e "${CYAN}║       GitHub Auto Commit Hacker        ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}[?] silahkan pilih menu banned numbernya${NC}"
echo -e "${GREEN}[1]${NC} Masuk ke menu (Commit & Push)"
echo -e "${RED}[2]${NC} Keluar menu dan hapus session"
echo ""
read -p "Pilihan (1/2): " pilihan

case $pilihan in
    1)
        echo -e "${BLUE}────────────────────────────────────────${NC}"
        echo -e "${YELLOW}🔍 Mengecek perubahan...${NC}"
        
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
        
        COMMIT_MSG="🚀 Auto-commit: $(date +'%d/%m/%Y %H:%M:%S') | 📦 Update proyek BK"
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
        echo -e "${RED}🗑️  Menghapus session dan keluar...${NC}"
        git config --global --unset credential.helper
        echo -e "${GREEN}✅ Session terhapus! Sampai jumpa.${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Pilihan salah!${NC}"
        exit 1
        ;;
esac
