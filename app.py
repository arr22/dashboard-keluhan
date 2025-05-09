import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO

# === Load Data ===
df = pd.read_excel('Form IT Helpdesk.xlsx')

# Ubah kolom waktu jadi datetime
if 'Start time' in df.columns:
    df['Start time'] = pd.to_datetime(df['Start time'])

# === Sidebar ===
st.sidebar.title("🎛️ Filter")

# Filter tanggal
start_date, end_date = st.sidebar.date_input(
    "📅 Pilih Rentang Tanggal",
    [df['Start time'].min().date(), df['Start time'].max().date()]
)

filtered_df = df[
    (df['Start time'].dt.date >= start_date) &
    (df['Start time'].dt.date <= end_date)
]

# Filter PIC
pic_list = df['PIC'].dropna().unique().tolist()
selected_pic = st.sidebar.selectbox("👤 Pilih PIC", ["Semua"] + pic_list)

if selected_pic != "Semua":
    filtered_df = filtered_df[filtered_df['PIC'] == selected_pic]

# === Header ===
st.title("📊 Dashboard Keluhan Helpdesk")
st.write(f"Periode: {start_date.strftime('%d %B %Y')} - {end_date.strftime('%d %B %Y')}")

# === Statistik ===
st.metric("📝 Total Keluhan", len(filtered_df))
daily_counts = filtered_df.groupby(filtered_df["Start time"].dt.date).size()
avg_per_day = daily_counts.mean() if not daily_counts.empty else 0
st.metric("📉 Rata-rata Keluhan per Hari", f"{avg_per_day:.1f}")

# === Pie Chart Jenis Keluhan ===
st.subheader("📌 Distribusi Jenis Keluhan")
if 'Pilih kendala dibawah Ini' in filtered_df.columns:
    jenis_counts = filtered_df['Pilih kendala dibawah Ini'].value_counts()
    if not jenis_counts.empty:
        fig1, ax1 = plt.subplots()
        ax1.pie(jenis_counts, labels=jenis_counts.index, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)
    else:
        st.info("Tidak ada data untuk ditampilkan.")

# === Line Chart ===
st.subheader("📈 Jumlah Keluhan per Hari")
if not daily_counts.empty:
    st.line_chart(daily_counts)
else:
    st.info("Data keluhan harian tidak tersedia.")

# === Tabel ===
st.subheader("📋 Detail Keluhan")
st.dataframe(filtered_df)

# === Export Excel ===
def to_excel(dataframe):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    dataframe.to_excel(writer, index=False, sheet_name='Keluhan')
    writer.close()
    return output.getvalue()

excel_data = to_excel(filtered_df)
st.download_button(
    label="📥 Download Data Excel",
    data=excel_data,
    file_name="keluhan_filtered.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
) 
