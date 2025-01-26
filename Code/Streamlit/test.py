import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import requests
from io import BytesIO

@st.cache_data
def load_svg(): 
        return requests.get('https://raw.githubusercontent.com/Toqa-Yasser/SHEIN_Data_Analyses/refs/heads/main/Code/Streamlit/window-shopping-animate.svg').content.decode('utf-8')
svg_content = load_svg()
st.markdown(f"<div style='width: 300px; height: 300px; align: center'>{svg_content}</div>", unsafe_allow_html=True)

def display_all_products(dff):
    cols_per_row = 2  # Number of columns per row
    images_per_col = 2  # Number of images to display per product (including the main image)
    
    try:
        for index, row in dff.iterrows():
            first_image_url = row['Picture Of Product'].split(', ')[0]
            all_image_urls = row['Picture Of Product'].split(', ')
            
            # Create columns for image and details
            col1, col2 = st.columns([1, 2])
            
            # Display the first image in a smaller size
            with col1:
                st.image(first_image_url, width=200)
            
            # Display product details next to the image
            with col2:
                st.write(f"**Store Name:** {row['Store Name']}")
                st.write(f"**Price:** ${row['Price($)']}")
                st.write(f"**Discount:** {row['Discount(%)']}%")
                st.write(f"**Rate:** {row['Rate']}")

            with st.expander("View More details"):
                st.write(f"**Product Name:** {row['Product']}")
                st.write(f"**Color:** {row['Color']}")
                st.write(f"**Size:** {row['Size']}")
                st.write(f"**Sku:** {row['Sku']}")
                
        
            # Create an expander for more images
            with st.expander("View More Images"):
                # Arrange images in columns and rows
                for i in range(0, len(all_image_urls), images_per_col):
                    cols = st.columns(images_per_col)
                    for col, image_url in zip(cols, all_image_urls[i:i+images_per_col]):
                        col.image(image_url, use_column_width=True)
            
                
            
    except:
        pass
        
@st.cache_data        
def load_csv:
        return pd.read_csv(BytesIO(requests.get('https://raw.githubusercontent.com/Toqa-Yasser/SHEIN_Data_Analyses/refs/heads/main/Code/Streamlit/Shein_clean.csv').content))

df=load_csv()

st.title('SHEIN Product Analysis ')
st.sidebar.title('Category')

selected_category = st.sidebar.selectbox('', options=['Overview'] + df['Category'].unique().tolist())

if selected_category == 'Overview':
    st.markdown('<h3>Overview about SHEIN site : </h3>',unsafe_allow_html=True)
    maxcategory=df['Category'].value_counts().idxmax()
    st.markdown(f'<h6> - The most Products in Category in SHEIN is in {maxcategory}</h6>',unsafe_allow_html=True)
    st.plotly_chart(px.pie(data_frame=df,names='Category',height=600,width=800))

    avg=df['Price($)'].mean()
    maxx=df['Price($)'].max()
    minn=df['Price($)'].min()
    st.markdown(f'<h6> - The average prices in SHEIN site is ${avg}  and the lowest Price in the SHEIN site is ${minn} and highest Price is {maxx}$</h6>',unsafe_allow_html=True)
    st.plotly_chart(px.histogram(data_frame=df,x='Price($)',height=600,width=800))

    maxcategory=df['Category'].loc[df['Price($)'].idxmax()]
    mincategory=df['Category'].loc[df['Price($)'].idxmin()]
    st.markdown(f'<h6> - The most expensive price in SHEIN is in {maxcategory} Category and the chepest product in SHEIN is in {mincategory} Category</h6>',unsafe_allow_html=True)
    max_prices = df.groupby('Category')['Price($)'].max().reset_index()
    st.plotly_chart(px.histogram(data_frame=max_prices, x='Category', y='Price($)', text_auto=True,height=600,width=800,color='Category',color_discrete_sequence=px.colors.sequential.Plotly3))
    min_prices = df.groupby('Category')['Price($)'].min().reset_index()
    st.plotly_chart(px.histogram(data_frame=min_prices, x='Category', y='Price($)', text_auto=True,height=600,color='Category',color_discrete_sequence=px.colors.sequential.amp,width=800))

    maxrate=df['Rate'].max()
    st.markdown(f'<h6> - The most Products in SHEIN is token rate {maxrate} Star and that mean the products of shien is perfect</h6>',unsafe_allow_html=True)
    st.plotly_chart(px.histogram(data_frame=df,x='Rate',height=600,color_discrete_sequence=px.colors.sequential.thermal,color='Category',width=800))

    st.markdown('<h6> - The Average rate of each Cateogory is nearly equal</h6>',unsafe_allow_html=True)
    st.plotly_chart(px.histogram(data_frame=df,x='Category',y='Rate',histfunc='avg',text_auto=True,height=600,color_discrete_sequence=px.colors.sequential.deep,color='Category',width=800))

    minrate=df['Rate'].min()
    st.markdown(f'<h6> - The Highest rate in SHEIN is {maxrate} and lowest rate is {minrate} that mean the products of SHEIN is perfect. ',unsafe_allow_html=True)
    max_Rate= df.groupby('Category')['Rate'].max().reset_index()
    st.plotly_chart(px.histogram(data_frame=max_Rate, x='Category', y='Rate', text_auto=True,height=600,color_discrete_sequence=px.colors.sequential.speed,color='Category',width=800))
    min_Rate= df.groupby('Category')['Rate'].min().reset_index()
    st.plotly_chart(px.histogram(data_frame=min_Rate, x='Category', y='Rate',color_discrete_sequence=px.colors.sequential.haline ,color='Category',text_auto=True,height=600,width=800))

    avgstorerate=df['Store Rate'].mean()
    st.markdown(f'<h6> - The Average Store rate in SHEIN is {avgstorerate}and that mean the Stores of shien is very trusted.</h6>',unsafe_allow_html=True)
    st.plotly_chart(px.histogram(data_frame=df,x='Rate',height=600,color_discrete_sequence=[px.colors.sequential.Brwnyl[4]],width=800))

    maxstore=df['Store Name'].value_counts().idxmax()
    st.markdown(f'<h6> - The most Store that buy sells in SHEIN is {maxstore}</h6>',unsafe_allow_html=True)
    st.plotly_chart(px.histogram(data_frame=df,x=df['Store Name'],height=600,width=800))

    avgmaxprice=df.groupby(['Category'])['Price($)'].mean().idxmax()
    avgminprice=df.groupby(['Category'])['Price($)'].mean().idxmin()
    st.markdown(f'<h6> - The {avgmaxprice} category has the most expensive average prices, while {avgminprice} has the cheapest average products on SHEIN.</h6>',unsafe_allow_html=True)
    st.plotly_chart(px.histogram(data_frame=df,x='Category',y='Price($)',color_discrete_sequence=[px.colors.sequential.matter],histfunc='avg',text_auto=True,height=600,width=800))

    maxdiscount=df['Discount(%)'].max()
    maxdiscountcategory=df['Category'].loc[df['Discount(%)'].idxmax()]
    st.markdown(f'<h6> - The Highest Discount in SHEIN site is {maxdiscount}% in {maxdiscountcategory} Cateogry</h6>',unsafe_allow_html=True)
    max_discounts = df.groupby('Category')['Discount(%)'].max().reset_index()
    st.plotly_chart(px.histogram(data_frame=max_discounts, x='Category', y='Discount(%)', color_discrete_sequence=[px.colors.sequential.tempo] ,text_auto=True,height=600,width=800))

    maxavgdiscount=df.groupby(['Category'])['Discount(%)'].mean().idxmax()
    st.markdown(f'<h6> - The Highest avergae Discount in SHEIN is in {maxavgdiscount} Cateogry</h6>',unsafe_allow_html=True)
    st.plotly_chart(px.histogram(data_frame=df,x='Category',y='Discount(%)',histfunc='avg',text_auto=True,color_discrete_sequence=[px.colors.sequential.Turbo],height=600,width=800))

    df_non_zero_discount = df[df['Discount(%)'] != 0]
    discount_counts = df_non_zero_discount.groupby('Category').size().reset_index(name='Discount Count')
    discount_total = df.groupby('Category')['Discount(%)'].count().reset_index(name='Discount_total')
    discount=pd.merge(left=discount_counts,right=discount_total,on='Category',how='inner')
    discount['Rate Of Discount %']=(discount['Discount Count']/discount['Discount_total'])*100
    maxratediscount=discount['Category'].loc[discount['Rate Of Discount %'].idxmax()]
    st.markdown(f'<h6> - The Cateogray that have most of its products discountetd is {maxratediscount}</h6>',unsafe_allow_html=True)
    df_non_zero_discount = df[df['Discount(%)'] != 0]
    discount_counts = df_non_zero_discount.groupby('Category').size().reset_index(name='Discount Count')
    discount_total = df.groupby('Category')['Discount(%)'].count().reset_index(name='Discount_total')
    discount=pd.merge(left=discount_counts,right=discount_total,on='Category',how='inner')
    discount['Rate Of Discount %']=(discount['Discount Count']/discount['Discount_total'])*100
    st.plotly_chart(px.bar(data_frame=discount,x='Category',y='Rate Of Discount %',text_auto=True,color_discrete_sequence=[px.colors.sequential.ice],height=600,width=800))

    st.markdown('<h6> - The average rate of most 12 stores sells products in SHEIN.</h6>',unsafe_allow_html=True)
    top_stores = df['Store Name'].value_counts().nlargest(12).index
    filtered_df = df[df['Store Name'].isin(top_stores)]
    st.plotly_chart(px.histogram(
        data_frame=filtered_df,
        x='Store Name',
        y='Store Rate',
        color='Category',
        histfunc='avg',
        text_auto=True,
        height=500,
        width=1150
    ))

    
    ##not dynamic
    st.markdown('<h6> - The average prices of most 12 stores sells product in SHEIN. Store Augensten and pate leathr have highest avg Price in Dress shoes and Men shoes</h6>',unsafe_allow_html=True)
    top_stores = df['Store Name'].value_counts().nlargest(12).index
    filtered_df = df[df['Store Name'].isin(top_stores)]
    st.plotly_chart(px.histogram(
        data_frame=filtered_df,
        x='Store Name',
        y='Price($)',
        color='Category',
        histfunc='avg',
        text_auto=True,
        height=600,width=800,
    ))

    st.markdown('<h6> - The average discount of most 12 stores sells products in SHEIN. </h6>',unsafe_allow_html=True)
    st.plotly_chart(px.histogram(
    data_frame=filtered_df,
    x='Store Name',
    y='Discount(%)',
    color='Category',
    histfunc='avg',
    text_auto=True,
    height=600,width=800
    ))


else:
    filtered_data = df[df['Category'] == selected_category]
    st.markdown(f'<h3>{selected_category}</h3>',unsafe_allow_html=True)
    tab1, tab2 = st.tabs(['Analysis','Products'])
    with tab1:
        st.markdown(f'<h3>Overview about SHEIN {selected_category} : </h3>',unsafe_allow_html=True)
        meanprice=filtered_data['Price($)'].mean()
        st.markdown(f'<h6> - The Price distrbution of Cateogory {selected_category} and the average price is {meanprice}$ </h6>',unsafe_allow_html=True)
        st.plotly_chart(px.histogram(filtered_data, x='Price($)', nbins=20,height=600,width=800))

        meanrate=filtered_data['Rate'].mean()
        st.markdown(f'<h6> - The Rate distrbution of Cateogory {selected_category} and the average Rate is {meanrate}$ </h6>',unsafe_allow_html=True)
        st.plotly_chart(px.histogram(filtered_data, x='Rate', nbins=20, color_discrete_sequence=['pink'],height=600,width=800))

        meandiscount=filtered_data['Discount(%)'].mean()
        st.markdown(f'<h6> - The Discount distrbution of Cateogory {selected_category} and the average Discount is {meandiscount}$ </h6>',unsafe_allow_html=True)
        st.plotly_chart(px.histogram(filtered_data, x='Discount(%)', nbins=20, color_discrete_sequence=['White'],height=600,width=800))

        avg_price_by_store = filtered_data.groupby('Store Name')['Price($)'].mean().reset_index()
        storenamemaxavg=avg_price_by_store.loc[avg_price_by_store['Price($)'].idxmax()]['Store Name']
        storenameminavg=avg_price_by_store.loc[avg_price_by_store['Price($)'].idxmin()]['Store Name']
        st.markdown(f'<h6> - The Average prices of each store in Cateogory {selected_category} and the highest average prices in Store {storenamemaxavg} and the lowest average prices in Store {storenameminavg} </h6>',unsafe_allow_html=True)
        st.plotly_chart(px.histogram(avg_price_by_store, y='Price($)', x='Store Name',text_auto=True,height=600,width=800,color='Store Name'))

        avg_store_rate = filtered_data.groupby('Store Name')['Store Rate'].mean().reset_index()
        st.markdown(f'<h6> - The Average Rate of each store in Cateogory {selected_category} and all of them is around 4.9 and that is great. </h6>',unsafe_allow_html=True)
        st.plotly_chart(px.histogram(avg_store_rate, y='Store Rate', x='Store Name', text_auto=True,height=600,width=800,color='Store Name'))

    with tab2:
        st.markdown(f'<h3>The products of {selected_category} : </h3>',unsafe_allow_html=True)
        st.sidebar.title('Products sort by : ')
        selected_option = st.sidebar.selectbox('', options=['Most popular', 'Price low to high', 'Price high to low'])


        if selected_option == 'Most popular':
            display_all_products(filtered_data)
        elif selected_option == 'Price low to high':
            dff=filtered_data.sort_values(by= ['Price($)'], ascending= True)
            display_all_products(dff)
        else :
            dff=filtered_data.sort_values(by= ['Price($)'], ascending= False)
            display_all_products(dff)

            
