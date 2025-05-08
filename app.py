import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# === Load Data ===
df = pd.read_excel('Form IT Helpdesk.xlsx')

# Pastikan kolom tanggal dikonversi
df["Start time"] = pd.to_datetime(df["Start time"])

# === Sidebar Filter ===
st.sidebar.title("Filter Data")
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal", 
    [df["Start time"].min().date(), df["Start time"].max().date()]
)

# === Filter Berdasarkan Rentang Tanggal ===
filtered_df = df[
    (df["Start time"].dt.date >= start_date) & 
    (df["Start time"].dt.date <= end_date)
]

# === Header ===
st.title("📊 Dashboard Keluhan Harian")
st.write(f"Data dari: {start_date.strftime('%d %B %Y')} sampai {end_date.strftime('%d %B %Y')}")
st.metric("Jumlah Keluhan", len(filtered_df))

# === Pie Chart Jenis Keluhan ===
st.subheader("Distribusi Jenis Keluhan")
jenis_counts = filtered_df["Pilih kendala dibawah Ini"].value_counts()

fig1, ax1 = plt.subplots()
ax1.pie(jenis_counts, labels=jenis_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# === Tabel Detail ===
st.subheader("📋 Tabel Keluhan")
st.dataframe(filtered_df)

# === Grafik Jumlah Harian ===
st.subheader("📈 Grafik Jumlah Keluhan per Hari")
daily_counts = df.groupby(df["Start time"].dt.date).size()
st.line_chart(daily_counts)
