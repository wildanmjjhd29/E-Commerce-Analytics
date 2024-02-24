import folium
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_folium as sf
from folium import plugins
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import streamlit_folium as sf

@st.cache_data
#Load Data CSV
def load_data(url) :
    df = pd.read_csv(url)
    return df

customer_info = load_data("https://raw.githubusercontent.com/wildanmjjhd29/E-Commerce-Analytics/main/customer_info.csv")
orders_info = load_data("https://raw.githubusercontent.com/wildanmjjhd29/E-Commerce-Analytics/main/orders_info.csv")

def brazil_map(customer_info):
        # Menghitung jumlah pelanggan untuk setiap negara bagian
    state_counts = customer_info['customer_state'].value_counts()

    # Membuat pemetaan dari singkatan ke nama lengkap negara bagian
    state_mapping = {
        'SP': 'Sao Paulo',
        'RJ': 'Rio de Janeiro',
        'MG': 'Minas Gerais',
        'RS': 'Rio Grande do Sul',
        'PR': 'Parana',
        'SC': 'Santa Catarina',
        'BA': 'Bahia',
        'ES': 'Espirito Santo',
        'GO': 'Goias',
        'MT': 'Mato Grosso',
        'PE': 'Pernambuco',
        'DF': 'Distrito Federal',
        'PA': 'Para',
        'CE': 'Ceara',
        'MS': 'Mato Grosso do Sul',
        'MA': 'Maranhao',
        'AL': 'Alagoas',
        'PB': 'Paraiba',
        'SE': 'Sergipe',
        'PI': 'Piaui',
        'RO': 'Rondonia',
        'RN': 'Rio Grande do Norte',
        'TO': 'Tocantins',
        'AC': 'Acre',
        'AM': 'Amazonas',
        'AP': 'Amapa',
        'RR': 'Roraima'
    }

    top_state = state_counts.rename(index=state_mapping).head()
     
     # Membuat peta dengan lokasi tengah Brasil
    brazil_map = folium.Map(location=[-15.7801, -47.9292], zoom_start=5, height=400)

    # Membuat instance objek MarkerCluster
    marker_cluster = plugins.MarkerCluster().add_to(brazil_map)

 
    # Menambahkan marker untuk setiap negara bagian pada peta
    for state, count in state_counts.items():
        # Menggunakan pemetaan untuk mendapatkan nama lengkap negara bagian
        state_full_name = state_mapping.get(state, state)

        # Menambahkan teks popup dengan informasi jumlah pelanggan
        popup_text = f"{state_full_name}: {count} customers"

        # Mendapatkan koordinat negara bagian (jika diketahui)
        state_location = customer_info.loc[customer_info['customer_state'] == state, ['geolocation_lat', 'geolocation_lng']]

        # Memeriksa apakah ada data lokasi untuk state tertentu
        if not state_location.empty:
            state_location = state_location.iloc[0]

            # Menambahkan marker ke dalam MarkerCluster
            folium.Marker(
                location=[state_location['geolocation_lat'], state_location['geolocation_lng']],
                icon=folium.Icon(icon="user"),
                popup=popup_text
            ).add_to(marker_cluster)

    # Menampilkan peta di Streamlit
    sf.folium_static(brazil_map)

def state_customer(customer_info):
    st.subheader("Jumlah Customer Yang Tersebar")
    # Menghitung jumlah pelanggan untuk setiap negara bagian
    state_counts = customer_info['customer_state'].value_counts()

    # Membuat pemetaan dari singkatan ke nama lengkap negara bagian
    state_mapping = {
        'SP': 'Sao Paulo',
        'RJ': 'Rio de Janeiro',
        'MG': 'Minas Gerais',
        'RS': 'Rio Grande do Sul',
        'PR': 'Parana',
        'SC': 'Santa Catarina',
        'BA': 'Bahia',
        'ES': 'Espirito Santo',
        'GO': 'Goias',
        'MT': 'Mato Grosso',
        'PE': 'Pernambuco',
        'DF': 'Distrito Federal',
        'PA': 'Para',
        'CE': 'Ceara',
        'MS': 'Mato Grosso do Sul',
        'MA': 'Maranhao',
        'AL': 'Alagoas',
        'PB': 'Paraiba',
        'SE': 'Sergipe',
        'PI': 'Piaui',
        'RO': 'Rondonia',
        'RN': 'Rio Grande do Norte',
        'TO': 'Tocantins',
        'AC': 'Acre',
        'AM': 'Amazonas',
        'AP': 'Amapa',
        'RR': 'Roraima'
    }

    top_state = state_counts.rename(index=state_mapping).head()
     
    # Membuat peta dengan lokasi tengah Brasil
    brazil_map = folium.Map(location=[-15.7801, -47.9292], zoom_start=4, height=400)

    # Membuat instance objek MarkerCluster
    marker_cluster = plugins.MarkerCluster().add_to(brazil_map)

 
    # Menambahkan marker untuk setiap negara bagian pada peta
    for state, count in state_counts.items():
        # Menggunakan pemetaan untuk mendapatkan nama lengkap negara bagian
        state_full_name = state_mapping.get(state, state)

        # Menambahkan teks popup dengan informasi jumlah pelanggan
        popup_text = f"{state_full_name}: {count} customers"

        # Mendapatkan koordinat negara bagian (jika diketahui)
        state_location = customer_info.loc[customer_info['customer_state'] == state, ['geolocation_lat', 'geolocation_lng']]

        # Memeriksa apakah ada data lokasi untuk state tertentu
        if not state_location.empty:
            state_location = state_location.iloc[0]

            # Menambahkan marker ke dalam MarkerCluster
            folium.Marker(
                location=[state_location['geolocation_lat'], state_location['geolocation_lng']],
                icon=folium.Icon(icon="user"),
                popup=popup_text
            ).add_to(marker_cluster)

    # Menampilkan peta di Streamlit
    sf.folium_static(brazil_map)
    # Membuat bar plot dengan Plotly
    top_state = top_state.sort_values(ascending=True)
    fig1 = go.Figure(data=[go.Bar(y=top_state.index, x=top_state.values, marker_color='skyblue', orientation='h')])
    fig1.update_layout(title_text='Negara Bagian Dengan Customer Terbanyak', xaxis_title="State", yaxis_title="Customer")
    st.plotly_chart(fig1)

def sales_category_analytics(orders_info):
    # Mencari trend penjualan
    transaksi_berhasil = orders_info[orders_info['order_status'].isin(['delivered', 'shipped'])].copy()

    laba_category = transaksi_berhasil.groupby('category_name')['laba'].sum()
    laba_category = laba_category.sort_values(ascending=False)

    # 5 kategori dengan hasil keuntungan paling banyak
    laba_teratas = laba_category.head()

    # 5 Kategori Yang mengalami Kerugian
    rugi_teratas = laba_category.tail()
    rugi_teratas = rugi_teratas.sort_values(ascending=True)

    st.subheader("Grafik Profit & Penjualan Per Kategori")

    #  Colom tabel
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("**5 Kategori Dengan Keuntungan Terbesar**")
        st.dataframe(laba_teratas)
    with col2:
        st.markdown("**5 kategori Dengan Kerugian Terbesar**")
        st.dataframe(rugi_teratas)
    st.empty()

    # Membuat bar plot dengan Plotly
    laba_teratas = laba_teratas.sort_values(ascending=True)
    fig1 = go.Figure(data=[go.Bar(y=laba_teratas.index, x=laba_teratas.values, marker_color='skyblue', orientation='h')])
    fig1.update_layout(title_text='Grafik 5 Kategori Penjualan & Profit Tertinggi', xaxis_title="Kategori", yaxis_title="Keuntungan")

    rugi_teratas = rugi_teratas.sort_values(ascending=False)
    fig2 = go.Figure(data=[go.Bar(y=rugi_teratas.index, x=rugi_teratas.values, marker_color='red',orientation='h')])
    fig2.update_layout(title_text='Grafik 5 Kategori Dengan Kerugian Paling Tinggi', xaxis_title="Kategori", yaxis_title="Kerugian")

    # Menampilkan plot di Streamlit
    st.plotly_chart(fig1)
    st.empty()   
    st.plotly_chart(fig2)

def sales_trend(orders_info):
    
    # Convert 'order_purchase_timestamp' to datetime if not already
    orders_info['order_purchase_timestamp'] = pd.to_datetime(orders_info['order_purchase_timestamp'])

    # Filter successful transactions
    transaksi_berhasil = orders_info[orders_info['order_status'].isin(['delivered', 'shipped'])].copy()

    # Create a column to store month and year information as a string
    transaksi_berhasil['bulan_tahun'] = transaksi_berhasil['order_purchase_timestamp'].dt.to_period('M').astype(str)

    # Mencari trend penjualan
    trend_penjualan = transaksi_berhasil.groupby('bulan_tahun')['total_harga'].sum()

    # Trend total laba
    trend_laba = transaksi_berhasil.groupby('bulan_tahun')['laba'].sum()

    # Mencari trend total pendapatan
    trend_total_pendapatan = transaksi_berhasil.groupby('bulan_tahun')['total_pendapatan'].sum()


    df = transaksi_berhasil.groupby('bulan_tahun')[['total_pendapatan', 'total_harga', 'laba']].sum()
    
    # Mengubah 'bulan_tahun' menjadi datetime
    df.index = pd.to_datetime(df.index)

    # Menambahkan slider untuk memilih tahun
    tahun = st.slider('Pilih Tahun', min_value=df.index.year.min(), max_value=df.index.year.max())

    # Filter DataFrame berdasarkan tahun yang dipilih
    df_tahun = df[df.index.year == tahun]

    # Membuat line plot dengan Plotly
    fig = go.Figure()

    # Menambahkan line untuk total pendapatan
    fig.add_trace(go.Scatter(x=df_tahun.index, y=df_tahun['total_pendapatan'], mode='lines+markers', name='Profit'))

    # Menambahkan line untuk total harga
    fig.add_trace(go.Scatter(x=df_tahun.index, y=df_tahun['total_harga'], mode='lines+markers', name='Penjualan'))

    # Menambahkan judul dan label sumbu
    fig.update_layout(title=f'Trend Profit dan Penjualan Tahun {tahun}',
                xaxis_title='Bulan',
                yaxis_title='Jumlah',
                legend_title='Variabel')

    # Menambahkan total laba di sisi kanan atas
    fig.add_annotation(x=df_tahun.index[-1], y=df_tahun['laba'].iloc[-1],
                text=f"Total Profit: {df_tahun['laba'].sum()}",
                showarrow=False,
                xanchor='right', yanchor='top',
                xshift=10, yshift=10)

    # Menampilkan plot di Streamlit
    st.plotly_chart(fig)

def all_sales_trend(orders_info):
    # Convert 'order_purchase_timestamp' to datetime if not already
    orders_info['order_purchase_timestamp'] = pd.to_datetime(orders_info['order_purchase_timestamp'])

    # Filter successful transactions
    transaksi_berhasil = orders_info[orders_info['order_status'].isin(['delivered', 'shipped'])].copy()

    # Create a column to store month and year information as a string
    transaksi_berhasil['bulan_tahun'] = transaksi_berhasil['order_purchase_timestamp'].dt.to_period('M').astype(str)

    # Mencari trend penjualan
    trend_penjualan = transaksi_berhasil.groupby('bulan_tahun')['total_harga'].sum()

    # Trend total laba
    trend_laba = transaksi_berhasil.groupby('bulan_tahun')['laba'].sum()

    # Mencari trend total pendapatan
    trend_total_pendapatan = transaksi_berhasil.groupby('bulan_tahun')['total_pendapatan'].sum()

    # Membuat DataFrame baru dengan 'bulan_tahun' sebagai index dan 'total_pendapatan', 'total_harga', dan 'laba' sebagai kolom
    df = transaksi_berhasil.groupby('bulan_tahun')[['total_pendapatan', 'total_harga', 'laba']].sum()

    # Membuat line plot dengan Plotly
    fig = go.Figure()

    # Menambahkan line untuk total pendapatan
    fig.add_trace(go.Scatter(x=df.index, y=df['total_pendapatan'], mode='lines+markers', name='Total Pendapatan'))

    # Menambahkan line untuk total harga
    fig.add_trace(go.Scatter(x=df.index, y=df['total_harga'], mode='lines+markers', name='Total Harga'))

    # Menambahkan judul dan label sumbu
    fig.update_layout(title='Trend Total Pendapatan dan Penjualan',
                    xaxis_title='Bulan',
                    yaxis_title='Jumlah',
                    legend_title='Variabel')

    # Menambahkan total laba di sisi kanan atas
    fig.add_annotation(x=df.index[-1], y=df['laba'].iloc[-1],
                    text=f"Total Laba: {df['laba'].sum()}",
                    showarrow=False,
                    xanchor='right', yanchor='top',
                    xshift=10, yshift=10)

    # Menampilkan plot di Streamlit
    st.plotly_chart(fig)

def review_analitics(orders_info):
    # Mencari trend penjualan
    transaksi_berhasil = orders_info[orders_info['order_status'].isin(['delivered', 'shipped'])].copy()

    rating = transaksi_berhasil['review_score'].value_counts()
    rating = rating[[5,4,3,2,1]]

    rating_kategori = transaksi_berhasil.groupby('category_name')['review_score'].value_counts()
    rating_kategori = rating_kategori.unstack(level='review_score')

    # Mencari kategori produk yang paling banyak mendapat ulasan baik
    rating_lima = rating_kategori.sort_values(by=5, ascending=False).head()

    rating_lima  = rating_lima[5]

    # Membuat pie chart dengan Plotly
    fig1 = go.Figure(data=[go.Pie(labels=rating.index, values=rating.values, hole=.3)])
    fig1.update_layout(title_text='Ulasan Produk')

    # Kategori Dengan Ulasan Baik Terbanyak
    rating_lima = rating_lima.sort_values(ascending=True)

    # Membuat bar chart dengan Plotly
    fig2 = go.Figure(data=[go.Bar(x=rating_lima.values, y=rating_lima.index, orientation='h')])
    fig2.update_layout(title_text='Kategori Produk Dengan Rating Baik Terbanyak', xaxis_title="Jumlah", yaxis_title="Kategori")

    # Menampilkan plot di Streamlit
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)


with st.sidebar :
    selected = option_menu('Keras',['Dashboard','Sales Analytics','Category Analitics','Customer Analytics'],
    icons =["easel2", "graph-up","graph-up"],
    menu_icon="cast",
    default_index=0)

if (selected=='Dashboard'):
    st.title("ANALISIS E-COMMERCE")
    st.subheader("Dashboard E-Commerce Analytics")
    brazil_map(customer_info)
    st.markdown('---')
    st.caption('Wildan Mujjahid Robbani')
     
elif (selected == 'Sales Analytics') :
    st.header(f"Sales & Profit Analytics")
    tab1,tab2 = st.tabs(["Trend Profit & Penjualan",'Analisis Trend Profit & Penjualan'])
    with tab1:
        st.subheader("Trend Profit dan Penjualan 2016-2017")
        all_sales_trend(orders_info)
        with st.expander("Penjelasan Mengenai Visualisasi"):
            st.write('Visualisasi Di atas menampilkan bagaimana trend Profit & Penjualan sepanjang waktu')
    
    with tab2:
        st.subheader("Analisis Trend Penjualan Dari Tahun Ke Tahun")
        sales_trend(orders_info)
        with st.expander("Penjelasan Mengenai Visualisasi"):
            st.write('Di sini saya menampilkan trend profit & Penjualan dari tahun ke tahun (Tahun bisa di pilih menggunakan slider)')

elif (selected == 'Category Analitics'):
    st.header(f"Product Category Analitics")
    tab1,tab2 = st.tabs(["Profit Kategori","Review Category"])
    with tab1:
        sales_category_analytics(orders_info)
        with st.expander("Penjelasan Mengenai Visualisasi"):
            st.write('Visualisasi dia atas menampilkan 5 kategori produk dengan profit terbesar dan juga menampilkan 5 kategori dengan kerugian paling besar juga')

    with tab2:
        st.subheader("Category Review Analitics")
        review_analitics(orders_info)
        with st.expander("Penjelasan Mengenai Visualisasi"):
            st.write('Visualisasi di atas menampilkan Perbandingan Rating dari 1-5 menggunkan pie chart dapat di lihat bahwa Rate 5 paling mendominasi, selain itu juga saya menampilkan untuk 5 kategori Produk dengan rate 5 paling banyak')

elif (selected == 'Customer Analytics') :
    st.header(f"Analsis Penyebaran Customer")
    tab1 = st.tabs(["Persebaran Customer"])
    with tab1[0]:
        state_customer(customer_info)
    with st.expander("Penjelasan Mengenai Visualisasi"):
        st.write('Visualisasi Di atas menampilkan Peta persebaran jumlah Customer E-Commerce Di Brazil, Selain itu di tampilkan juga untuk 5 State yang memiliki Customer paling banyak')

