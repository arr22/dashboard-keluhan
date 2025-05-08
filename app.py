import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# === Load Data ===
df = pd.read_excel('Form IT Helpdesk.xlsx')
df["Start time"] = pd.to_datetime(df["Start time"])

# === Sidebar ===
st.sidebar.markdown("## 🔧 Filter Data")
start_date, end_date = st.sidebar.date_input(
    "🗓️ Pilih Rentang Tanggal", 
    [df["Start time"].min().date(), df["Start time"].max().date()]
)

filtered_df = df[
    (df["Start time"].dt.date >= start_date) & 
    (df["Start time"].dt.date <= end_date)
]

# === Header ===
st.markdown("<h1 style='text-align: center;'>📊 Dashboard IT Helpdesk</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>Data dari <b>{start_date.strftime('%d %B %Y')}</b> sampai <b>{end_date.strftime('%d %B %Y')}</b></p>", unsafe_allow_html=True)

# === Metric Box ===
col1, col2 = st.columns([1, 3])
col1.metric("📝 Jumlah Keluhan", len(filtered_df))
col2.write("")

# === Pie Chart ===
st.markdown("### 🧾 Distribusi Jenis Keluhan")
jenis_counts = filtered_df["Pilih kendala dibawah Ini"].value_counts()

fig1, ax1 = plt.subplots()
ax1.pie(jenis_counts, labels=jenis_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# === Tabel ===
st.markdown("### 📋 Detail Keluhan")
st.dataframe(filtered_df.style.set_properties(**{'background-color': 'lavender', 'color': 'black'}))

# === Grafik Harian ===
st.markdown("### 📈 Grafik Jumlah Keluhan per Hari")
daily_counts = filtered_df.groupby(filtered_df["Start time"].dt.date).size()
st.line_chart(daily_counts)
