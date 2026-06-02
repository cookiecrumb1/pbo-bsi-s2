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

with open("style.css", "r", encoding="utf-8") as f:
    css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
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

# --- BAGIAN 4: FUNGSI POP-UP (DIALOG BOX) ---

@st.dialog("Konfirmasi Pesanan")
def konfirmasi_popup(nama_menu):
    harga = HARGA_MENU[nama_menu]
    jumlah = st.number_input(f"Berapa jumlah **{nama_menu}** yang ini dipesan?", min_value=1, value=1, step=1)
    subtotal = harga * jumlah
    
    st.write(f"Total untuk {jumlah} {nama_menu}: **Rp{subtotal:,}**")
    
    col_ya, col_batal = st.columns(2)
    with col_ya:
        if st.button("Ya, Tambahkan", use_container_width=True):
            if nama_menu in st.session_state.keranjang:
                st.session_state.keranjang[nama_menu] += jumlah
            else:
                st.session_state.keranjang[nama_menu] = jumlah
            st.rerun() 
            
    with col_batal:
        if st.button("Batal", use_container_width=True):
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
        st.rerun()

# --- BAGIAN 5: INISIALISASI SESSION STATE ---

if 'keranjang' not in st.session_state:
    st.session_state.keranjang = {}

# GANTI SIDEBAR → pakai session_state untuk navigasi
if 'halaman' not in st.session_state:
    st.session_state.halaman = "Pilih Menu"

menu_utama = st.session_state.halaman

# --- BAGIAN 6: TAMPILAN ANTARMUKA UTAMA (UI) ---

st.title("☕ Warkop Digital")
st.write("Kopi - Roti Bakar - Indomie - Mie Ayam & Bakso")
st.write("---")

if menu_utama == "Pilih Menu":
    st.write("### Menu")
    kategori = st.radio(" ", ["MAKANAN", "MINUMAN"], horizontal=True, label_visibility="collapsed")
    st.write("---")

    if kategori == "MAKANAN":
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/nasi_goreng.jpg", use_container_width=True)
            st.write(f"**Nasi Goreng** (Rp{HARGA_MENU['Nasi Goreng']:,})")
            if st.button("Pesan Nasi Goreng", key="ng"): konfirmasi_popup("Nasi Goreng")
        with col2:
            st.image("images/mie_goreng.jpg", use_container_width=True)
            st.write(f"**Mie Goreng** (Rp{HARGA_MENU['Mie Goreng']:,})")
            if st.button("Pesan Mie Goreng", key="mg"): konfirmasi_popup("Mie Goreng")
        
        st.write("---")
        
        col3, col4 = st.columns(2)
        with col3:
            st.image("images/roti_bakar.jpg", use_container_width=True)
            st.write(f"**Roti Bakar** (Rp{HARGA_MENU['Roti Bakar']:,})")
            if st.button("Pesan Roti Bakar", key="rb"): konfirmasi_popup("Roti Bakar")
        with col4:
            st.image("images/kentang_goreng.jpg", use_container_width=True)
            st.write(f"**Kentang Goreng** (Rp{HARGA_MENU['Kentang Goreng']:,})")
            if st.button("Pesan Kentang Goreng", key="kg"): konfirmasi_popup("Kentang Goreng")

        st.write("---")

        col5, col6 = st.columns(2)
        with col5:
            st.image("images/mie_ayam.jpg", use_container_width=True)
            st.write(f"**Mie Ayam** (Rp{HARGA_MENU['Mie Ayam']:,})")
            if st.button("Pesan Mie Ayam", key="ma"): konfirmasi_popup("Mie Ayam")
        with col6:
            st.image("images/bakso.jpg", use_container_width=True)
            st.write(f"**Bakso** (Rp{HARGA_MENU['Bakso']:,})")
            if st.button("Pesan Bakso", key="bk"): konfirmasi_popup("Bakso")

    elif kategori == "MINUMAN":
        col1, col2 = st.columns(2)
        with col1:
            st.image("images/coffee.jpg", use_container_width=True)
            st.write(f"**Coffee** (Rp{HARGA_MENU['Coffee']:,})")
            if st.button("Pesan Coffee", key="cf"): konfirmasi_popup("Coffee")
        with col2:
            st.image("images/susu.jpg", use_container_width=True)
            st.write(f"**Susu** (Rp{HARGA_MENU['Susu']:,})")
            if st.button("Pesan Susu", key="ss"): konfirmasi_popup("Susu")
        
        st.write("---")

        col3, col4 = st.columns(2)
        with col3:
            st.image("images/orange_juice.jpg", use_container_width=True)
            st.write(f"**Orange Juice** (Rp{HARGA_MENU['Orange Juice']:,})")
            if st.button("Pesan Orange Juice", key="oj"): konfirmasi_popup("Orange Juice")
        with col4:
            st.image("images/teh.jpg", use_container_width=True)
            st.write(f"**Teh** (Rp{HARGA_MENU['Teh']:,})")
            if st.button("Pesan Teh", key="th"): konfirmasi_popup("Teh")

        st.write("---")

        col5, col6 = st.columns(2)
        with col5:
            st.image("images/air_mineral.jpg", use_container_width=True)
            st.write(f"**Air Mineral** (Rp{HARGA_MENU['Air Mineral']:,})")
            if st.button("Pesan Air Mineral", key="am"): konfirmasi_popup("Air Mineral")
        with col6:
            st.image("images/soda.jpg", use_container_width=True)
            st.write(f"**Soda** (Rp{HARGA_MENU['Soda']:,})")
            if st.button("Pesan Soda", key="sd"): konfirmasi_popup("Soda")

elif menu_utama == "Lihat Keranjang":
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
                struk_popup()

# --- BAGIAN 7: BOTTOM NAVIGATION BAR ---
jumlah_item = len(st.session_state.keranjang)
badge = f" ({jumlah_item})" if jumlah_item > 0 else ""

with st.container():
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button(f"🍽️ Pilih Menu", key="nav_menu", use_container_width=True):
            st.session_state.halaman = "Pilih Menu"
            st.rerun()
    with nav2:
        if st.button(f"🛒 Keranjang{badge}", key="nav_keranjang", use_container_width=True):
            st.session_state.halaman = "Lihat Keranjang"
            st.rerun()