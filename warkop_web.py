# Mengimpor library Streamlit untuk membuat antarmuka web
import streamlit as st
import base64

# --- BAGIAN 1: FUNGSI UNTUK BACKGROUND (BASE64) ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg(img_file):
    try:
        bin_str = get_base64(img_file)
        page_bg = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
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
    
# --- BAGIAN 3: DATA MASTER ---
HARGA_MENU = {
    "Nasi Goreng": 15000,
    "Roti Bakar": 10000,
    "Kentang Goreng": 10000,
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
    "MAKANAN": ["Nasi Goreng", "Mie Goreng", "Roti Bakar", "Kentang Goreng", "Mie Ayam", "Bakso"],
    "MINUMAN": ["Coffee", "Susu", "Orange Juice", "Teh", "Air Mineral", "Soda"]
}

# --- BAGIAN 4: FUNGSI POP-UP (DIALOG BOX) ---

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
        st.session_state.keranjang = {}
        st.session_state.show_struk = False
        st.rerun()

# --- BAGIAN 5: INISIALISASI SESSION STATE ---

if 'keranjang' not in st.session_state:
    st.session_state.keranjang = {}

if 'halaman' not in st.session_state:
    st.session_state.halaman = "Landing Page"

if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = None

if 'show_struk' not in st.session_state:
    st.session_state.show_struk = False

menu_utama = st.session_state.halaman

# --- BAGIAN 6: TAMPILAN ANTARMUKA UTAMA (UI) ---

# 1. TAMPILAN: LANDING PAGE
if menu_utama == "Landing Page":
    st.markdown('''
        <style>
        /* 1. Atur halaman utama agar flexbox-nya siap menengahkan konten secara global */
        section.main {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
        }

        /* 2. Atur wrapper utama box hitam transparan di tengah layar browser */
        .main .block-container {
            background-color: rgba(0, 0, 0, 0.6) !important;
            box-shadow: none !important;
            border: none !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
            max-width: 600px !important;
            min-height: 70vh !important;
            margin: auto !important;
            padding: 2rem !important;
        }

        /* 3. Paksa blok vertikal Streamlit untuk menyusun teks & tombol di satu garis tengah vertikal */
        .main [data-testid="stVerticalBlock"] {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
        }

        /* 4. SOLUSI UTAMA: Meremukkan stButton bawaan agar membungkus tombol di tengah secara absolut */
        .main div.stButton {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
        }

        /* Sembunyikan bottom bar bawaan di landing page */
        [data-testid="stBottom"] {
            display: none !important;
        }

        /* 5. Kustomisasi Tombol "PESAN" Kotak Kuning */
        .stButton > button {
            background-color: #FFCC00 !important; 
            color: #000000 !important;            
            border: 4px solid #000000 !important; 
            border-radius: 0px !important;        
            font-size: 24px !important;
            font-weight: bold !important;
            letter-spacing: 2px !important;
            height: 65px !important;
            width: 280px !important;
            max-width: 280px !important;
            box-shadow: 0px 6px 15px rgba(0,0,0,0.5) !important;
            transition: 0.2s ease-in-out !important;
            margin: 0 auto !important;
        }
        .stButton > button:hover {
            background-color: #FFE066 !important;
            transform: scale(1.05) !important;
        }
        </style>
    ''', unsafe_allow_html=True)
    
    # Judul Menu Utama (Text-align center sudah terkunci)
    st.markdown("<h1 style='color: #FFFFFF; font-family: sans-serif; font-size: 52px; font-weight: bold; letter-spacing: 4px; margin-bottom: 40px; text-shadow: 3px 3px 10px rgba(0,0,0,0.95); text-align: center;'>MENU DIGITAL</h1>", unsafe_allow_html=True)
    
    # Tombol PESAN
    if st.button("PESAN", key="btn_landing_pesan"):
        st.session_state.halaman = "Pilih Menu"
        st.rerun()

# 2. TAMPILAN: PILIH MENU
elif menu_utama == "Pilih Menu":
    st.title("☕ Warkop Digital")
    st.write("Kopi - Roti Bakar - Indomie - Mie Ayam & Bakso")
    st.write("---")
    st.write("### Menu")
    kategori = st.radio(" ", ["MAKANAN", "MINUMAN"], horizontal=True, label_visibility="collapsed")
    st.write("---")

    daftar_item = MENU_KATEGORI[kategori]
    
    for idx in range(0, len(daftar_item), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            item = daftar_item[idx]
            img_path = f"images/{item.lower().replace(' ', '_')}.jpg"
            st.image(img_path, use_container_width=True)
            st.write(f"**{item}** (Rp{HARGA_MENU[item]:,})")
            if st.button(f"Pesan {item}", key=f"btn_{idx}", use_container_width=True):
                st.session_state.selected_menu = item
                st.rerun()
                
        if idx + 1 < len(daftar_item):
            with col2:
                item = daftar_item[idx+1]
                img_path = f"images/{item.lower().replace(' ', '_')}.jpg"
                st.image(img_path, use_container_width=True)
                st.write(f"**{item}** (Rp{HARGA_MENU[item]:,})")
                if st.button(f"Pesan {item}", key=f"btn_{idx+1}", use_container_width=True):
                    st.session_state.selected_menu = item
                    st.rerun()
        st.write("---")

# 3. TAMPILAN: LIHAT KERANJANG
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
                st.session_state.keranjang = {}
                st.rerun()
        with c_bayar:
            if st.button("Bayar di Kasir", type="primary", use_container_width=True):
                st.session_state.show_struk = True
                st.rerun()

# --- BAGIAN 7: BOTTOM NAVIGATION BAR ---
if menu_utama != "Landing Page":
    jumlah_item = sum(st.session_state.keranjang.values())
    badge = f" ({jumlah_item})" if jumlah_item > 0 else ""

    with st.bottom:
        nav1, nav2 = st.columns(2)
        with nav1:
            if st.button(f"🍽️ Pilih Menu", key="nav_menu", use_container_width=True):
                st.session_state.halaman = "Pilih Menu"
                st.rerun()
        with nav2:
            if st.button(f"🛒 Keranjang{badge}", key="nav_keranjang", use_container_width=True):
                st.session_state.halaman = "Lihat Keranjang"
                st.rerun()

# --- BAGIAN 8: TRIGGER DIALOG BOX ---
if st.session_state.selected_menu:
    konfirmasi_popup(st.session_state.selected_menu)

if st.session_state.show_struk:
    struk_popup()