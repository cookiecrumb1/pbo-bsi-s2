# Mengimpor library Streamlit untuk membuat antarmuka web
import streamlit as st
import base64
import requests  # Menggunakan requests untuk menembak API Google secara langsung
from datetime import datetime

URL_API_GOOGLE_SHEETS = "https://script.google.com/macros/s/AKfycbxtUq-WBLDv0FFLbocCBT5E-atVU7edSNLYh-JpX4_SVkpDENwcWNwz8N5GrBYsvpKA4w/exec"


# --- BAGIAN 1: FUNGSI UNTUK BACKGROUND (BASE64) ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg(img_file):
    try:
        bin_str = get_base64(img_file)
        # Kita hanya menyisipkan gambar base64-nya ke dalam properti background-image
        page_bg = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
        }}
        </style>
        '''
        st.markdown(page_bg, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Gagal memuat background: {e}")

# ------------------------------------------

st.set_page_config(page_title="Digital Warkop", page_icon="☕", layout="centered")

try:
    set_bg('images/warkop_bg.jpg')
except:
    pass 

try:
    with open("style.css", "r", encoding="utf-8") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except:
    pass
    
# --- BAGIAN 2: DATA MASTER ---
HARGA_MENU = {
    "Nasi Goreng": 15000,
    "Roti Bakar": 10000,
    "French Fries": 10000,
    "Mie Goreng": 12000,
    "Mie Ayam": 13000,
    "Bakso": 15000,
    "Coffee": 7000,
    "Susu": 6000,
    "Orange Juice": 10000,
    "Air Mineral": 4000,
    "Teh": 5000,
    "Soda": 8000
}

# Kelompok Menu untuk Otomatisasi UI Loop
MENU_KATEGORI = {
    "MAKANAN": ["Nasi Goreng", "Mie Goreng", "Roti Bakar", "French Fries", "Mie Ayam", "Bakso"],
    "MINUMAN": ["Coffee", "Susu", "Orange Juice", "Teh", "Air Mineral", "Soda"]
}

# --- BAGIAN 3: FUNGSI POP-UP (DIALOG BOX) ---

@st.dialog("Konfirmasi Pesanan")
def konfirmasi_popup(nama_menu):
    harga = HARGA_MENU[nama_menu]
    jumlah = st.number_input(f"Berapa jumlah **{nama_menu}** yang ingin dipesan?", min_value=1, value=1, step=1)
    subtotal = harga * jumlah
    
    st.write(f"Total untuk {jumlah} {nama_menu}: **Rp{subtotal:,}**")
    
    col_ya, col_batal = st.columns(2)
    with col_ya:
        if st.button("Ya, Tambahkan", use_container_width=True):
            if nama_menu in st.session_state.keranjang:
                st.session_state.keranjang[nama_menu] += jumlah
            else:
                st.session_state.keranjang[nama_menu] = jumlah
            
            st.session_state.selected_menu = None
            st.rerun() 
            
    with col_batal:
        if st.button("Batal", use_container_width=True):
            st.session_state.selected_menu = None
            st.rerun() 

@st.dialog("🧾 Struk Pembayaran")
def struk_popup():
    # --- TAHAP 1: RINCIAN STRUK ---
    if st.session_state.step_struk == "struk":
        st.write("### Rincian Pesanan:")
        total_bayar = 0
        
        i = 1
        for item, jumlah in st.session_state.keranjang.items():
            harga_satuan = HARGA_MENU.get(item, 0)
            subtotal_item = harga_satuan * jumlah
            total_bayar += subtotal_item
            st.write(f"{i}. {item} (x{jumlah}) — Rp{subtotal_item:,}")
            i += 1
            
        st.write("---")
        st.subheader(f"Total Pembayaran: Rp{total_bayar:,}")
        st.info("👨‍🍳 Silakan tunjukkan layar ini ke kasir.")
        
        if st.button("Selesai & Bayar", type="primary", use_container_width=True):
            st.session_state.step_struk = "saran"
            st.rerun()

    # --- TAHAP 2: POP-UP FORMULIR SARAN (Direct Web API) ---
    elif st.session_state.step_struk == "saran":
        st.write("### 💬 Saran")
        st.write("Terima kasih sudah berkunjung! Masukan Anda sangat berarti bagi perkembangan bisnis kami.")
        
        saran_input = st.text_area("Tulis kritik atau saran Anda di sini:", placeholder="Contoh: Rasa kopi mantap, kalau bisa tambah menu baru...")
        
        if st.button("Kirim Saran & Selesai", type="primary", use_container_width=True):
            if saran_input.strip():
                try:
                    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Membuat payload paket data JSON
                    payload = {
                        "tanggal": waktu_sekarang,
                        "saran": saran_input.strip()
                    }
                    
                    # Menembak data langsung ke Google API Endpoint
                    respons = requests.post(URL_API_GOOGLE_SHEETS, json=payload)
                    
                    if respons.status_code == 200:
                        st.toast("Terima kasih atas saran Anda! Data langsung masuk cloud. 🙏")
                    else:
                        st.toast("Saran terkirim (Status bypass). Terima kasih! 👍")
                except Exception as e:
                    st.toast("Saran dicatat! Terima kasih. 😊")
            else:
                st.toast("Pesanan selesai! Terima kasih. 😊")
                
            # Paksa tutup popup dan kosongkan keranjang sebelum rerun
            st.session_state.keranjang = {}
            st.session_state.show_struk = False
            st.session_state.step_struk = "struk"
            st.rerun()

# --- BAGIAN 4: INISIALISASI SESSION STATE ---

if 'keranjang' not in st.session_state:
    st.session_state.keranjang = {}

# Langsung diarahkan ke halaman Pilih Menu
if 'halaman' not in st.session_state:
    st.session_state.halaman = "Pilih Menu"

if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = None

if 'show_struk' not in st.session_state:
    st.session_state.show_struk = False

# State tambahan untuk melacak tahapan alur di dalam pop-up pembayaran
if 'step_struk' not in st.session_state:
    st.session_state.step_struk = "struk"

menu_utama = st.session_state.halaman

# 🛡️ SYSTEM PROTEKSI RESET STATE (Mencegah Loop Pop-up saat Refresh / Tab Berpindah)
if menu_utama == "Pilih Menu" and st.session_state.step_struk == "saran":
    st.session_state.show_struk = False
    st.session_state.step_struk = "struk"

# --- BAGIAN 5: TAMPILAN ANTARMUKA UTAMA (UI) ---

# 1. TAMPILAN: PILIH MENU
if menu_utama == "Pilih Menu":
    st.title("☕ Warkop Digital")
    st.write("Kopi - Roti Bakar - Indomie - Mie Ayam & Bakso")
    st.write("---")
    st.write("### Menu")
    
    # Menambahkan fungsi callback (on_change) saat mengganti kategori
    def reset_popups_on_change():
        st.session_state.show_struk = False
        st.session_state.step_struk = "struk"

    kategori = st.radio(" ", ["MAKANAN", "MINUMAN"], horizontal=True, label_visibility="collapsed", on_change=reset_popups_on_change)
    st.write("---")

    daftar_item = MENU_KATEGORI[kategori]
    
    for idx in range(0, len(daftar_item), 2):
        col1, col2 = st.columns(2)
        
        # --- KOLOM 1 (KIRI) ---
        with col1:
            item = daftar_item[idx]
            img_path = f"images/{item.lower().replace(' ', '_')}.jpg"
            
            sub_kiri1, sub_tengah1, sub_kanan1 = st.columns([3, 7, 3])
            with sub_tengah1:
                st.image(img_path, use_container_width=True)
                st.markdown(f"<div style='text-align: center; margin-bottom: 8px;'><strong>{item}</strong> (Rp{HARGA_MENU[item]:,})</div>", unsafe_allow_html=True)
                
                if st.button(f"Pesan", key=f"btn_{idx}", use_container_width=True):
                    st.session_state.selected_menu = item
                    st.rerun()
                
        # --- KOLOM 2 (KANAN) ---
        if idx + 1 < len(daftar_item):
            with col2:
                item = daftar_item[idx+1]
                img_path = f"images/{item.lower().replace(' ', '_')}.jpg"
                
                sub_kiri2, sub_tengah2, sub_kanan2 = st.columns([3, 7, 3])
                with sub_tengah2:
                    st.image(img_path, use_container_width=True)
                    st.markdown(f"<div style='text-align: center; margin-bottom: 8px;'><strong>{item}</strong> (Rp{HARGA_MENU[item]:,})</div>", unsafe_allow_html=True)
                    
                    if st.button(f"Pesan", key=f"btn_{idx+1}", use_container_width=True):
                        st.session_state.selected_menu = item
                        st.rerun()
        st.write("---")

# 2. TAMPILAN: LIHAT KERANJANG
elif menu_utama == "Lihat Keranjang":
    st.title("☕ Warkop Digital")
    st.header("🛒 Keranjang Anda")
    
    if not st.session_state.keranjang:
        st.warning("Keranjang anda kosong, Silahkan pesan dahulu.")
    else:
        total_sementara = 0
        i = 1
        
        for item, jumlah in st.session_state.keranjang.items():
            harga_satuan = HARGA_MENU.get(item, 0)
            subtotal_item = harga_satuan * jumlah
            total_sementara += subtotal_item
            st.write(f"{i}. {item} (x{jumlah}) — Rp{subtotal_item:,}")
            i += 1
        
        st.write("---")
        st.subheader(f"Total: Rp{total_sementara:,}")
        
        c_hapus, c_bayar = st.columns(2)
        with c_hapus:
            if st.button("Kosongkan Keranjang", use_container_width=True):
                st.session_state.get('keranjang').clear()
                st.rerun()
        with c_bayar:
            if st.button("Bayar di Kasir", type="primary", use_container_width=True):
                st.session_state.show_struk = True
                st.rerun()

# --- BAGIAN 6: BOTTOM NAVIGATION BAR ---
jumlah_item = sum(st.session_state.keranjang.values())
badge = f" ({jumlah_item})" if jumlah_item > 0 else ""

with st.bottom:
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button(f"🍽️ Pilih Menu", key="nav_menu", use_container_width=True):
            st.session_state.halaman = "Pilih Menu"
            st.session_state.show_struk = False
            st.session_state.step_struk = "struk"
            st.rerun()
    with nav2:
        if st.button(f"🛒 Keranjang{badge}", key="nav_keranjang", use_container_width=True):
            st.session_state.halaman = "Lihat Keranjang"
            st.session_state.show_struk = False
            st.session_state.step_struk = "struk"
            st.rerun()

# --- BAGIAN 7: TRIGGER DIALOG BOX ---
if st.session_state.selected_menu:
    konfirmasi_popup(st.session_state.selected_menu)

if st.session_state.show_struk:
    struk_popup()