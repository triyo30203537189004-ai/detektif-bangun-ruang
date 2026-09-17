import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

# ==============================================================================
# CONFIG & STYLING (Tema: Petualangan Detektif Bangun Ruang)
# Palet Warna: Sky Blue (#E3F2FD), Lemon Yellow (#FFFDE7), Mint Green (#E8F5E9), Navy (#1A237E)
# ==============================================================================
st.set_page_config(
    page_title="Petualangan Detektif Bangun Ruang - MIN 5 Palangka Raya",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan ceria, ramah anak, dan bertema detektif
st.markdown("""
    <style>
    /* Background & Main Layout */
    .stApp {
        background-color: #F4F9FF;
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Fredoka', sans-serif;
    }
    
    /* Header Styling */
    .header-box {
        background: linear-gradient(135deg, #81D4FA 0%, #B2EBF2 100%);
        border: 4px solid #0288D1;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .header-title {
        color: #01579B;
        font-size: 32px;
        font-weight: bold;
        margin: 0;
        text-shadow: 1px 1px 2px white;
    }
    .header-subtitle {
        color: #0277BD;
        font-size: 18px;
        margin-top: 5px;
    }
    
    /* Detective Card */
    .detective-card {
        background-color: #FFFDE7;
        border: 3px dashed #FBC02D;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Mint Box */
    .mint-card {
        background-color: #E8F5E9;
        border: 3px solid #81C784;
        border-radius: 15px;
        padding: 18px;
        margin-bottom: 15px;
    }
    
    /* Badge & Accent */
    .badge-tag {
        background-color: #FFB74D;
        color: #E65100;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 12px;
        display: inline-block;
        font-size: 14px;
    }
    
    /* Button Customization */
    .stButton>button {
        background-color: #FFF176;
        color: #333333;
        font-weight: bold;
        border: 2px solid #FBC02D;
        border-radius: 12px;
        padding: 10px 24px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FFEE58;
        transform: scale(1.03);
        box-shadow: 0 4px 12px rgba(251, 192, 45, 0.4);
    }
    
    /* Math Step Box */
    .step-box {
        background-color: #FFFFFF;
        border-left: 6px solid #29B6F6;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# HELPER FUNCTIONS FOR 3D PLOTTING & JARING-JARING
# ==============================================================================

def plot_3d_shape(shape_name):
    """Membuat visualisasi 3D menggunakan Matplotlib dengan warna pastel yang menarik."""
    fig = plt.figure(figsize=(5, 4), facecolor='none')
    ax = fig.add_subplot(111, projection='3d', facecolor='none')
    ax.set_axis_off()

    if shape_name == "Kubus":
        # Sisi kubus
        r = [0, 1]
        X, Y = np.meshgrid(r, r)
        # Bawah & Atas
        ax.plot_surface(X, Y, np.atleast_2d(0), color='#81D4FA', alpha=0.7, edgecolor='#01579B')
        ax.plot_surface(X, Y, np.atleast_2d(1), color='#81D4FA', alpha=0.7, edgecolor='#01579B')
        # Samping
        ax.plot_surface(X, np.atleast_2d(0), Y, color='#A7FFEB', alpha=0.7, edgecolor='#01579B')
        ax.plot_surface(X, np.atleast_2d(1), Y, color='#A7FFEB', alpha=0.7, edgecolor='#01579B')
        ax.plot_surface(np.atleast_2d(0), X, Y, color='#FFF59D', alpha=0.7, edgecolor='#01579B')
        ax.plot_surface(np.atleast_2d(1), X, Y, color='#FFF59D', alpha=0.7, edgecolor='#01579B')
        ax.set_title("Visual 3D Kubus", fontsize=12, fontweight='bold', color='#01579B')

    elif shape_name == "Balok":
        # Balok p=1.5, l=1, t=0.8
        x = np.array([0, 1.5])
        y = np.array([0, 1])
        z = np.array([0, 0.8])
        X, Y = np.meshgrid(x, y)
        ax.plot_surface(X, Y, np.atleast_2d(0), color='#FFE082', alpha=0.7, edgecolor='#E65100')
        ax.plot_surface(X, Y, np.atleast_2d(0.8), color='#FFE082', alpha=0.7, edgecolor='#E65100')
        
        X2, Z2 = np.meshgrid(x, z)
        ax.plot_surface(X2, np.atleast_2d(0), Z2, color='#80CBC4', alpha=0.7, edgecolor='#E65100')
        ax.plot_surface(X2, np.atleast_2d(1), Z2, color='#80CBC4', alpha=0.7, edgecolor='#E65100')
        ax.set_title("Visual 3D Balok", fontsize=12, fontweight='bold', color='#E65100')

    elif shape_name == "Tabung":
        z = np.linspace(0, 1.5, 30)
        theta = np.linspace(0, 2*np.pi, 30)
        theta_grid, z_grid = np.meshgrid(theta, z)
        r = 0.8
        x_grid = r * np.cos(theta_grid)
        y_grid = r * np.sin(theta_grid)
        ax.plot_surface(x_grid, y_grid, z_grid, color='#81D4FA', alpha=0.7, edgecolor='#0277BD')
        
        # Tutup & Alas
        r_grid, th_grid = np.meshgrid(np.linspace(0, r, 10), theta)
        ax.plot_surface(r_grid*np.cos(th_grid), r_grid*np.sin(th_grid), np.atleast_2d(0), color='#B2EBF2', alpha=0.8)
        ax.plot_surface(r_grid*np.cos(th_grid), r_grid*np.sin(th_grid), np.atleast_2d(1.5), color='#B2EBF2', alpha=0.8)
        ax.set_title("Visual 3D Tabung", fontsize=12, fontweight='bold', color='#0277BD')

    elif shape_name == "Prisma Segitiga":
        # Alas segitiga
        x = np.array([0, 1, 0.5, 0])
        y = np.array([0, 0, 0.866, 0])
        z1 = np.zeros(4)
        z2 = np.ones(4) * 1.2
        ax.plot(x, y, z1, color='#00695C', lw=2)
        ax.plot(x, y, z2, color='#00695C', lw=2)
        for i in range(3):
            ax.plot([x[i], x[i]], [y[i], y[i]], [0, 1.2], color='#26A69A', lw=2)
        ax.set_title("Visual 3D Prisma Segitiga", fontsize=12, fontweight='bold', color='#00695C')

    elif shape_name == "Limas Segiempat":
        # Alas segiempat + titik puncak
        x = [0, 1, 1, 0, 0]
        y = [0, 0, 1, 1, 0]
        z = [0, 0, 0, 0, 0]
        ax.plot(x, y, z, color='#D81B60', lw=2)
        apex = [0.5, 0.5, 1.2]
        for i in range(4):
            ax.plot([x[i], apex[0]], [y[i], apex[1]], [z[i], apex[2]], color='#FF4081', lw=2)
        ax.set_title("Visual 3D Limas Segiempat", fontsize=12, fontweight='bold', color='#D81B60')

    elif shape_name == "Kerucut":
        z = np.linspace(0, 1.5, 30)
        theta = np.linspace(0, 2*np.pi, 30)
        theta_grid, z_grid = np.meshgrid(theta, z)
        r = 0.8 * (1 - z_grid/1.5)
        x_grid = r * np.cos(theta_grid)
        y_grid = r * np.sin(theta_grid)
        ax.plot_surface(x_grid, y_grid, z_grid, color='#FFCC80', alpha=0.8, edgecolor='#EF6C00')
        ax.set_title("Visual 3D Kerucut", fontsize=12, fontweight='bold', color='#EF6C00')

    elif shape_name == "Bola":
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 30)
        x = 1 * np.outer(np.cos(u), np.sin(v))
        y = 1 * np.outer(np.sin(u), np.sin(v))
        z = 1 * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z, color='#CE93D8', alpha=0.8, edgecolor='#6A1B9A')
        ax.set_title("Visual 3D Bola", fontsize=12, fontweight='bold', color='#6A1B9A')

    plt.tight_layout()
    return fig


def plot_net_diagram(shape_name):
    """Menggambar diagram 2D jaring-jaring bangun ruang."""
    fig, ax = plt.subplots(figsize=(5, 4), facecolor='none')
    ax.set_facecolor('white')
    ax.axis('off')

    if shape_name == "Kubus":
        # Jaring-jaring bentuk T (6 persegi)
        squares = [
            (1, 2), (0, 1), (1, 1), (2, 1), (1, 0), (3, 1)
        ]
        for (x, y) in squares:
            rect = plt.Rectangle((x, y), 0.95, 0.95, facecolor='#B2EBF2', edgecolor='#00838F', lw=2)
            ax.add_patch(rect)
            ax.text(x+0.475, y+0.475, "Sisi", ha='center', va='center', fontsize=9, color='#006064', fontweight='bold')
        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-0.5, 3.5)
        ax.set_title("Jaring-jaring Kubus (Pola T)", fontsize=11, fontweight='bold', color='#00838F')

    elif shape_name == "Balok":
        # Jaring-jaring balok
        rects = [
            (0, 1, 1, 0.6, 'Alas'), (1, 1, 1.5, 0.6, 'Samping'),
            (2.5, 1, 1, 0.6, 'Atas'), (3.5, 1, 1.5, 0.6, 'Samping'),
            (1, 1.6, 1.5, 0.8, 'Depan'), (1, 0.2, 1.5, 0.8, 'Belakang')
        ]
        for (x, y, w, h, label) in rects:
            r = plt.Rectangle((x, y), w, h, facecolor='#FFF59D', edgecolor='#F57F17', lw=2)
            ax.add_patch(r)
            ax.text(x+w/2, y+h/2, label, ha='center', va='center', fontsize=8, color='#F57F17', fontweight='bold')
        ax.set_xlim(-0.5, 5.5)
        ax.set_ylim(-0.2, 2.6)
        ax.set_title("Jaring-jaring Balok", fontsize=11, fontweight='bold', color='#F57F17')

    elif shape_name == "Tabung":
        # 1 persegi panjang + 2 lingkaran
        rect = plt.Rectangle((0.5, 1), 3, 1.2, facecolor='#E1BEE7', edgecolor='#7B1FA2', lw=2)
        ax.add_patch(rect)
        circle1 = plt.Circle((2, 2.6), 0.4, facecolor='#80DEEA', edgecolor='#00838F', lw=2)
        circle2 = plt.Circle((2, 0.4), 0.4, facecolor='#80DEEA', edgecolor='#00838F', lw=2)
        ax.add_patch(circle1)
        ax.add_patch(circle2)
        ax.text(2, 1.6, "Selimut Tabung\n(Persegi Panjang)", ha='center', va='center', fontsize=9, color='#4A148C', fontweight='bold')
        ax.text(2, 2.6, "Tutup", ha='center', va='center', fontsize=8, color='#006064')
        ax.text(2, 0.4, "Alas", ha='center', va='center', fontsize=8, color='#006064')
        ax.set_xlim(-0.2, 4.2)
        ax.set_ylim(-0.2, 3.2)
        ax.set_title("Jaring-jaring Tabung", fontsize=11, fontweight='bold', color='#7B1FA2')

    elif shape_name == "Prisma Segitiga":
        # 3 persegi panjang + 2 segitiga
        rect1 = plt.Rectangle((0, 1), 1, 1.2, facecolor='#C8E6C9', edgecolor='#2E7D32', lw=2)
        rect2 = plt.Rectangle((1, 1), 1, 1.2, facecolor='#A5D6A7', edgecolor='#2E7D32', lw=2)
        rect3 = plt.Rectangle((2, 1), 1, 1.2, facecolor='#C8E6C9', edgecolor='#2E7D32', lw=2)
        ax.add_patch(rect1); ax.add_patch(rect2); ax.add_patch(rect3)
        
        tri1 = plt.Polygon([[1, 2.2], [2, 2.2], [1.5, 2.9]], facecolor='#FFD54F', edgecolor='#F57F17', lw=2)
        tri2 = plt.Polygon([[1, 1], [2, 1], [1.5, 0.3]], facecolor='#FFD54F', edgecolor='#F57F17', lw=2)
        ax.add_patch(tri1); ax.add_patch(tri2)
        ax.set_xlim(-0.3, 3.3)
        ax.set_ylim(-0.1, 3.2)
        ax.set_title("Jaring-jaring Prisma Segitiga", fontsize=11, fontweight='bold', color='#2E7D32')

    elif shape_name == "Limas Segiempat":
        # 1 Persegi + 4 Segitiga
        sq = plt.Rectangle((1, 1), 1, 1, facecolor='#FFCDD2', edgecolor='#C62828', lw=2)
        ax.add_patch(sq)
        t_top = plt.Polygon([[1, 2], [2, 2], [1.5, 2.8]], facecolor='#FFE082', edgecolor='#E65100', lw=2)
        t_bot = plt.Polygon([[1, 1], [2, 1], [1.5, 0.2]], facecolor='#FFE082', edgecolor='#E65100', lw=2)
        t_left = plt.Polygon([[1, 1], [1, 2], [0.2, 1.5]], facecolor='#FFE082', edgecolor='#E65100', lw=2)
        t_right = plt.Polygon([[2, 1], [2, 2], [2.8, 1.5]], facecolor='#FFE082', edgecolor='#E65100', lw=2)
        for t in [t_top, t_bot, t_left, t_right]: ax.add_patch(t)
        ax.set_xlim(-0.2, 3.2)
        ax.set_ylim(-0.1, 3.1)
        ax.set_title("Jaring-jaring Limas Segiempat", fontsize=11, fontweight='bold', color='#C62828')

    else:
        ax.text(2, 1.5, f"Jaring-jaring {shape_name}\ndapat diamati dalam wujud selimut lengkungnya", ha='center', va='center', fontsize=10, color='#333')
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 3)

    plt.tight_layout()
    return fig


# ==============================================================================
# HEADER & NAVIGATION
# ==============================================================================

st.markdown("""
    <div class="header-box">
        <div class="header-title">🕵️‍♂️ PETUALANGAN DETEKTIF BANGUN RUANG</div>
        <div class="header-subtitle">Modul Digital Interaktif Matematika SD/MI • MIN 5 Kota Palangka Raya</div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1995/1995539.png", width=100)
st.sidebar.title("🔍 Papan Navigasi Detektif")
st.sidebar.markdown("**Halo Detektif Cilik!** Pilih markas yang ingin kamu jelajahi:")

menu = st.sidebar.radio(
    "Pilihan Misi:",
    [
        "🏠 Markas Utama & Pengenalan",
        "📦 Laboratorium Benda Nyata",
        "📐 Studio Jaring-Jaring Visual",
        "🧮 Kalkulator Pintar (Langkah Rumus)",
        "🏆 Kuis Misi Kasus Detektif"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("🏫 **MIN 5 Kota Palangka Raya**\n\n*Dikembangkan oleh:* Senior EdTech Developer & Ahli Kurikulum Matematika Anak")


# ==============================================================================
# MODULE 1: MARKAS UTAMA & PENGENALAN
# ==============================================================================
if menu == "🏠 Markas Utama & Pengenalan":
    st.markdown("""
        <div class="detective-card">
            <h2>🔎 Selamat Datang, Detektif Cilik MIN 5 Palangka Raya!</h2>
            <p style="font-size: 16px;">
                Kota Palangka Raya membutuhkan bantuanmu! Banyak benda di sekitar kita — seperti kotak kado,
                kaleng minuman, tumpeng, hingga bangunan khas — yang memiliki bentuk <b>Bangun Ruang</b>.
            </p>
            <p style="font-size: 16px;">
                Di aplikasi interaktif ini, kamu tidak hanya sekadar menghitung angka, tetapi akan belajar 
                <b>memahami proses rahasia di balik setiap rumus</b>!
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="mint-card">
                <h3>📦 1. Benda Nyata</h3>
                <p>Amati wujud 3D dan temukan contoh benda nyata di sekitarmu!</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="mint-card">
                <h3>📐 2. Jaring-Jaring</h3>
                <p>Buka bangun ruang menjadi bidang datar untuk memahami selimutnya.</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="mint-card">
                <h3>🧮 3. Kalkulator Pintar</h3>
                <p>Pahami langkah penyelesaian rumus Volume & Luas Permukaan secara runtut.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🌟 Target Capaian Pembelajaran:")
    st.checkbox("Memahami sifat-sifat dasar 7 jenis Bangun Ruang.", value=True, disabled=True)
    st.checkbox("Mengenali jaring-jaring pembentuk Bangun Ruang.", value=True, disabled=True)
    st.checkbox("Mampu menguraikan langkah perhitungan Volume dan Luas Permukaan.", value=True, disabled=True)


# ==============================================================================
# MODULE 2: LABORATORIUM BENDA NYATA
# ==============================================================================
elif menu == "📦 Laboratorium Benda Nyata":
    st.subheader("📦 Laboratorium Benda Nyata & Sifat Geometri")
    st.write("Pilih salah satu Bangun Ruang di bawah ini untuk menyelidiki bentuk 3D dan benda nyata di sekitar kita!")

    bangun_selected = st.selectbox(
        "Pilih Bangun Ruang:",
        ["Kubus", "Balok", "Tabung", "Prisma Segitiga", "Limas Segiempat", "Kerucut", "Bola"]
    )

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown(f"#### 🎨 Visualisasi 3D Interaktif: **{bangun_selected}**")
        fig_3d = plot_3d_shape(bangun_selected)
        st.pyplot(fig_3d)

    with col_right:
        st.markdown(f"#### 🔍 Sifat & Contoh Benda Nyata: **{bangun_selected}**")
        
        if bangun_selected == "Kubus":
            st.write("""
            - 🟦 **Sifat Unik:** Memiliki **6 sisi** berbentuk persegi yang sama luas, **12 rusuk** sama panjang, dan **8 titik sudut**.
            - 🏠 **Benda Nyata di Sekitar:** Dadu permainan, Rubik, kotak kado persegi, es batu kubus.
            """)
        elif bangun_selected == "Balok":
            st.write("""
            - 🟨 **Sifat Unik:** Memiliki **6 sisi** (sisi berhadapan sama luas), **12 rusuk**, dan **8 titik sudut**.
            - 🏠 **Benda Nyata di Sekitar:** Kotak pensil, lemari pakaian, kotak susu kemasan, penghapus papan tulis.
            """)
        elif bangun_selected == "Tabung":
            st.write("""
            - 🥤 **Sifat Unik:** Memiliki **alas dan tutup** lingkaran yang sejajar & identik, serta **1 sisi selimut lengkung**.
            - 🏠 **Benda Nyata di Sekitar:** Kaleng biskuit, drum air, pipa PVC, kaleng minuman soda.
            """)
        elif bangun_selected == "Prisma Segitiga":
            st.write("""
            - 🔺 **Sifat Unik:** Memiliki **2 sisi alas/tutup segitiga**, **3 sisi tegak**, **9 rusuk**, dan **6 titik sudut**.
            - 🏠 **Benda Nyata di Sekitar:** Atap rumah lipat, tenda pramuka, kemasan cokelat Toblerone.
            """)
        elif bangun_selected == "Limas Segiempat":
            st.write("""
            - 🎪 **Sifat Unik:** Memiliki **1 alas segi empat**, **4 sisi tegak segitiga** yang bertemu di titik puncak.
            - 🏠 **Benda Nyata di Sekitar:** Piramida Mesir, atap gazebos/pendopo, puncak tumpeng persegi.
            """)
        elif bangun_selected == "Kerucut":
            st.write("""
            - 🍦 **Sifat Unik:** Memiliki **1 alas lingkaran**, **1 selimut lengkung**, dan **1 titik puncak**.
            - 🏠 **Benda Nyata di Sekitar:** Topi ulang tahun, tumpeng nasi, cone es krim, kerucut lalu lintas (*traffic cone*).
            """)
        elif bangun_selected == "Bola":
            st.write("""
            - ⚽ **Sifat Unik:** Memiliki **1 sisi lengkung**, tanpa rusuk dan tanpa titik sudut!
            - 🏠 **Benda Nyata di Sekitar:** Bola basket, kelereng, globe bumi, buah semangka utuh.
            """)

        st.markdown("""
            <div class="detective-card" style="padding:10px; margin-top:10px;">
                💡 <b>Petunjuk Detektif:</b> Amati benda-benda di ruang kelas MIN 5 Kota Palangka Raya, benda mana sajakah yang mirip dengan bangun ini?
            </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# MODULE 3: STUDIO JARING-JARING VISUAL
# ==============================================================================
elif menu == "📐 Studio Jaring-Jaring Visual":
    st.subheader("📐 Studio Jaring-Jaring Visual")
    st.write("Jaring-jaring adalah gabungan bidang datar pembentuk bangun ruang jika dibuka/dibentangkan.")

    bangun_net = st.selectbox(
        "Pilih Jaring-Jaring yang Ingin Dibuka:",
        ["Kubus", "Balok", "Tabung", "Prisma Segitiga", "Limas Segiempat"]
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"#### 🗺️ Diagram Jaring-Jaring: **{bangun_net}**")
        fig_net = plot_net_diagram(bangun_net)
        st.pyplot(fig_net)

    with col2:
        st.markdown("#### 🕵️‍♂️ Analisis Pembentukan Sisi:")
        if bangun_net == "Kubus":
            st.success("Kubus terdiri dari **6 persegi identik**. Jika dilipat mengikuti garis rusuk, seluruh sisi akan saling menutupi membentuk kubus utuh!")
        elif bangun_net == "Balok":
            st.success("Balok terdiri dari **3 pasang persegi panjang** yang sejajar dan sama luas (Alas-Atas, Depan-Belakang, Kiri-Kanan).")
        elif bangun_net == "Tabung":
            st.success("Tabung jika dibuka terdiri dari **2 lingkaran** (alas & tutup) serta **1 persegi panjang** sebagai selimut tabung!")
        elif bangun_net == "Prisma Segitiga":
            st.success("Prisma Segitiga terdiri dari **2 segitiga** (alas & atas) dan **3 persegi/persegi panjang** sebagai sisi tegaknya.")
        elif bangun_net == "Limas Segiempat":
            st.success("Limas Segiempat terdiri dari **1 alas segiempat** dan **4 segitiga tegak** yang akan bertemu pada 1 titik puncak saat dilipat.")


# ==============================================================================
# MODULE 4: KALKULATOR PINTAR (DETAILED STEP SOLVER)
# ==============================================================================
elif menu == "🧮 Kalkulator Pintar (Langkah Rumus)":
    st.subheader("🧮 Kalkulator Pintar Detektif (Langkah demi Langkah)")
    st.markdown("""
        *Kalkulator ini dirancang khusus agar kamu memahami **proses matematika**, bukan sekadar hasil akhir instan!*
    """, unsafe_allow_html=True)

    shape_calc = st.selectbox(
        "Pilih Bangun Ruang yang Ingin Dihitung:",
        ["Kubus", "Balok", "Tabung", "Prisma Segitiga", "Kerucut", "Bola"]
    )

    calc_type = st.radio("Pilih Jenis Perhitungan:", ["Volume (Isi)", "Luas Permukaan (Selimut & Alas)"])

    st.markdown("---")
    st.markdown("### 📝 Masukkan Dimensi / Ukuran Benda:")

    if shape_calc == "Kubus":
        s = st.number_input("Panjang Rusuk / Sisi (s) dalam cm:", min_value=1.0, value=5.0, step=1.0)
        
        if st.button("🔎 Analisis Langkah Hitung"):
            st.markdown("### 🕵️‍♂️ Laporan Analisis Kasus Perhitungan:")
            if calc_type == "Volume (Isi)":
                st.markdown("""
                <div class="step-box">
                    <b>Langkah 1: Identifikasi Rumus Volume Kubus</b><br>
                    Volume Kubus dihitung dengan mengalikan sisi sebanyak tiga kali (panjang × lebar × tinggi yang ukurannya sama).<br>
                    <code>Rumus: Volume = s × s × s = s³</code>
                </div>
                <div class="step-box">
                    <b>Langkah 2: Substitusi Angka ke Rumus</b><br>
                    Masukkan nilai s = {} cm:<br>
                    <code>Volume = {} × {} × {}</code>
                </div>
                <div class="step-box">
                    <b>Langkah 3: Proses Penghitungan Bertahap</b><br>
                    • Hitung {} × {} = {}<br>
                    • Lalu hasil tersebut dikalikan {} lagi = {}
                </div>
                """.format(s, s, s, s, s, s, s**2, s, s**3), unsafe_allow_html=True)
                st.success(f"🏆 **KESIMPULAN AKHIR DETEKTIF:** Volume Kubus adalah **{s**3:.2f} cm³**")

            else: # Luas Permukaan
                st.markdown("""
                <div class="step-box">
                    <b>Langkah 1: Identifikasi Rumus Luas Permukaan Kubus</b><br>
                    Kubus memiliki 6 sisi persegi identik. Maka luas total adalah 6 kali luas satu persegi.<br>
                    <code>Rumus: Luas Permukaan = 6 × (s × s) = 6 × s²</code>
                </div>
                <div class="step-box">
                    <b>Langkah 2: Substitusi Angka ke Rumus</b><br>
                    Masukkan nilai s = {} cm:<br>
                    <code>Luas Permukaan = 6 × ({} × {})</code>
                </div>
                <div class="step-box">
                    <b>Langkah 3: Proses Penghitungan Bertahap</b><br>
                    • Luas 1 sisi persegi = {} × {} = {} cm²<br>
                    • Luas 6 sisi = 6 × {} = {} cm²
                </div>
                """.format(s, s, s, s, s, s**2, s**2, 6*(s**2)), unsafe_allow_html=True)
                st.success(f"🏆 **KESIMPULAN AKHIR DETEKTIF:** Luas Permukaan Kubus adalah **{6*(s**2):.2f} cm²**")

    elif shape_calc == "Balok":
        p = st.number_input("Panjang (p) dalam cm:", min_value=1.0, value=6.0)
        l = st.number_input("Lebar (l) dalam cm:", min_value=1.0, value=4.0)
        t = st.number_input("Tinggi (t) dalam cm:", min_value=1.0, value=3.0)

        if st.button("🔎 Analisis Langkah Hitung"):
            st.markdown("### 🕵️‍♂️ Laporan Analisis Kasus Perhitungan:")
            if calc_type == "Volume (Isi)":
                vol = p * l * t
                st.markdown(f"""
                <div class="step-box">
                    <b>Langkah 1: Identifikasi Rumus Volume Balok</b><br>
                    <code>Rumus: Volume = p × l × t</code>
                </div>
                <div class="step-box">
                    <b>Langkah 2: Substitusi Angka</b><br>
                    <code>Volume = {p} × {l} × {t}</code>
                </div>
                <div class="step-box">
                    <b>Langkah 3: Penghitungan Bertahap</b><br>
                    • Hitung p × l = {p} × {l} = {p*l}<br>
                    • Kalikan dengan tinggi = {p*l} × {t} = {vol}
                </div>
                """, unsafe_allow_html=True)
                st.success(f"🏆 **KESIMPULAN AKHIR DETEKTIF:** Volume Balok adalah **{vol:.2f} cm³**")
            else:
                pl = p * l
                pt = p * t
                lt = l * t
                lp = 2 * (pl + pt + lt)
                st.markdown(f"""
                <div class="step-box">
                    <b>Langkah 1: Identifikasi Rumus Luas Permukaan Balok</b><br>
                    <code>Rumus: Luas Permukaan = 2 × ((p × l) + (p × t) + (l × t))</code>
                </div>
                <div class="step-box">
                    <b>Langkah 2: Hitung Masing-Masing Pasangan Sisi</b><br>
                    • Sisi Alas & Atas (p × l) = {p} × {l} = {pl} cm²<br>
                    • Sisi Depan & Belakang (p × t) = {p} × {t} = {pt} cm²<br>
                    • Sisi Kiri & Kanan (l × t) = {l} × {t} = {lt} cm²
                </div>
                <div class="step-box">
                    <b>Langkah 3: Jumlahkan & Kalikan 2</b><br>
                    • Jumlah pasangan = {pl} + {pt} + {lt} = {pl+pt+lt} cm²<br>
                    • Luas Total = 2 × {pl+pt+lt} = {lp} cm²
                </div>
                """, unsafe_allow_html=True)
                st.success(f"🏆 **KESIMPULAN AKHIR DETEKTIF:** Luas Permukaan Balok adalah **{lp:.2f} cm²**")

    elif shape_calc == "Tabung":
        r = st.number_input("Jari-jari alas (r) dalam cm:", min_value=1.0, value=7.0)
        t_tabung = st.number_input("Tinggi tabung (t) dalam cm:", min_value=1.0, value=10.0)

        pi_val = 22/7 if r % 7 == 0 else 3.14

        if st.button("🔎 Analisis Langkah Hitung"):
            if calc_type == "Volume (Isi)":
                vol = pi_val * (r**2) * t_tabung
                st.markdown(f"""
                <div class="step-box">
                    <b>Langkah 1: Identifikasi Rumus Volume Tabung</b><br>
                    Volume Tabung = Luas Alas (Lingkaran) × Tinggi Tabung<br>
                    <code>Rumus: V = π × r² × t</code> (Nilai π = {pi_val})
                </div>
                <div class="step-box">
                    <b>Langkah 2: Hitung Luas Alas Lingkaran</b><br>
                    • Luas Alas = π × r × r = {pi_val} × {r} × {r} = {pi_val*(r**2):.2f} cm²
                </div>
                <div class="step-box">
                    <b>Langkah 3: Kalikan dengan Tinggi Tabung</b><br>
                    • Volume = {pi_val*(r**2):.2f} × {t_tabung} = {vol:.2f} cm³
                </div>
                """, unsafe_allow_html=True)
                st.success(f"🏆 **KESIMPULAN AKHIR DETEKTIF:** Volume Tabung adalah **{vol:.2f} cm³**")
            else:
                lp = 2 * pi_val * r * (r + t_tabung)
                st.markdown(f"""
                <div class="step-box">
                    <b>Langkah 1: Identifikasi Rumus Luas Permukaan Tabung</b><br>
                    <code>Rumus: LP = 2 × π × r × (r + t)</code>
                </div>
                <div class="step-box">
                    <b>Langkah 2: Hitung komponen (r + t)</b><br>
                    • r + t = {r} + {t_tabung} = {r + t_tabung} cm
                </div>
                <div class="step-box">
                    <b>Langkah 3: Kalikan seluruh variabel</b><br>
                    • LP = 2 × {pi_val} × {r} × {r + t_tabung} = {lp:.2f} cm²
                </div>
                """, unsafe_allow_html=True)
                st.success(f"🏆 **KESIMPULAN AKHIR DETEKTIF:** Luas Permukaan Tabung adalah **{lp:.2f} cm²**")

    else:
        st.info("Pilih ukuran dimensi di atas lalu klik tombol 'Analisis Langkah Hitung' untuk melihat penguraian lengkapnya.")


# ==============================================================================
# MODULE 5: KUIS MISI KASUS DETEKTIF
# ==============================================================================
elif menu == "🏆 Kuis Misi Kasus Detektif":
    st.subheader("🏆 Misi Detektif: Kasus Bangun Ruang MIN 5 Palangka Raya")
    st.write("Selesaikan kasus-kasus di bawah ini untuk mendapatkan Lencana Detektif Utama!")

    score = 0

    # Kasus 1
    st.markdown("#### 🔍 Kasus #1: Kotak Kado Berbentuk Kubus")
    q1 = st.radio(
        "Ahmad membeli kotak kado berbentuk kubus dengan panjang rusuk 10 cm. Berapakah volume kotak kado tersebut?",
        ["100 cm³", "600 cm³", "1.000 cm³", "10.000 cm³"]
    )
    if q1 == "1.000 cm³":
        st.caption("✅ **Tepat sekali!** Volume = 10 × 10 × 10 = 1.000 cm³.")
        score += 1

    st.markdown("---")

    # Kasus 2
    st.markdown("#### 🔍 Kasus #2: Kaleng Minuman")
    q2 = st.radio(
        "Jika sebuah kaleng minuman berbentuk tabung dibuka, jaring-jaring selimutnya berbentuk bangun datar apa?",
        ["Segitiga", "Persegi Panjang", "Lingkaran", "Janjang Genjang"]
    )
    if q2 == "Persegi Panjang":
        st.caption("✅ **Hebat!** Selimut tabung jika dibentangkan berbentuk persegi panjang.")
        score += 1

    st.markdown("---")

    # Kasus 3
    st.markdown("#### 🔍 Kasus #3: Sifat Bangun Ruang")
    q3 = st.radio(
        "Bangun ruang manakah yang memilki 1 alas lingkaran, 1 selimut lengkung, dan 1 titik puncak?",
        ["Tabung", "Kerucut", "Bola", "Limas Segiempat"]
    )
    if q3 == "Kerucut":
        st.caption("✅ **Jawaban Benar!** Kerucut memiliki alas lingkaran dan titik puncak.")
        score += 1

    st.markdown("---")

    if st.button("🎯 Serahkan Laporan Kuis Misi"):
        if score == 3:
            st.balloons()
            st.success("🎉 **LUAR BIASA! Skor Sempurna 3/3.**\n\nSelamat, kamu resmi mendapatkan **Lencana Detektif Ahli Bangun Ruang MIN 5 Kota Palangka Raya**! 🥇🕵️‍♂️")
        else:
            st.warning(f"Skor kamu: {score}/3. Ayo periksa kembali laboratorium materi dan coba lagi, Detektif!")
