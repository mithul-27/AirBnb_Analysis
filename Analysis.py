import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import folium
from streamlit_folium import st_folium

Hotel_df = pd.read_csv('Hotels_data.csv')


icon='https://avatars.githubusercontent.com/u/698437?s=280&v=4'
st.set_page_config(page_title='AIRBNB ',page_icon=icon,initial_sidebar_state='expanded',
                        layout='wide')

title_text = '''<h1 style='font-size: 36px;color:#ff5a5f;text-align: center;'>AIRBNB</h1><h2 style='font-size: 24px;color:#008891;text-align: center;'>Explore Your Dream Stays</h2>'''
st.markdown(title_text, unsafe_allow_html=True)

#set up home page and optionmenu 
selected = option_menu("MainMenu",
                        options=["OVERVIEW","HOME","DISCOVER","INSIGHTS","POWERBI"],
                        icons=["list icon","house", "globe","lightbulb","kanban"],
                        default_index=1,
                        orientation="horizontal",
                        styles={"container": {"width": "100%","border": "1px ridge  ","background-color": "#002b36","primaryColor": "#FF69B4"},
                                "icon": {"color": "#F8CD47", "font-size": "20px"}})

#set up the details for option 'overview'
if selected == "OVERVIEW":
    col1,col2=st.columns([2,1])

    with col1:
        st.subheader(':red[Project Title :]')
        st.markdown('<h5> Airbnb Analysis',unsafe_allow_html=True)

        st.subheader(':red[Domain :]')
        st.markdown('<h5> Travel Industry, Property Management and Tourism',unsafe_allow_html=True)

        st.subheader(':red[Technologies :]')
        st.markdown('<h5> Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.',unsafe_allow_html=True)

        st.subheader(':red[Overview :]')
        bullet_points = [
        " Accessed and processed a JSON dataset containing Airbnb data from 2019",
        "Utilized Python for data transformation, ensuring it fit into a structured DataFrame",
        "Applied data preprocessing techniques, including cleaning and organizing, to enhance data quality and usability",
        "Developed an interactive dashboard using Streamlit, providing users with a platform to explore insights from the dataset",
        "Incorporated dynamic visualizations with Plotly to enrich the dashboard's analytical capabilities"
        ]
    with col2:
        st.image("Airbnb-Symbol.jpg")


    for point in bullet_points:
        st.markdown(f"**- {point}**")

#=======================================================================================================================================================#   

if selected == "HOME":
    st.subheader("Unlocking Insights with Data Visualization")

    st.markdown("---")  

    st.markdown(
        """Airbnb, a revolutionary platform, has transformed the way we travel. Connecting people with unique accommodations worldwide, it has redefined the concept of hospitality.    
    This interactive dashboard empowers you to delve into the fascinating world of Airbnb data. Our mission is to unlock valuable insights hidden within this data, providing you with a deeper understanding of the global landscape of Airbnb listings."""
    )

    st.divider() 


    st.subheader("Embark on a Journey of Discovery")
    st.markdown("""
    - :red[**Global Distribution:**] Explore a captivating world map showcasing the distribution of Airbnb listings across different regions.
                            This interactive visualization allows you to pinpoint areas with high listing density and uncover potential travel hotspots.
    - :red[**Data-Driven Exploration:**] We'll equip you with the tools to filter and analyze listings based on a variety of criteria. 
                               This empowers you to tailor your exploration to your specific interests, whether you're curious about trends in specific locations, price ranges, or reviews given.
    - :red[**Interactive Insights (Optional):**] Depending on the scope of your project, you might encounter sections dedicated to uncovering deeper insights through interactive visualizations.
                                       These visualizations could reveal trends in pricing, popularity, or other relevant factors.
    - :red[**Predictions (Optional):**] If your project incorporates historical data analysis, you might encounter a section exploring potential future trends and pricing predictions for Airbnb listings."""
    )



    st.markdown("---") 


    st.markdown("Through this Streamlit application, you'll gain a comprehensive understanding of Airbnb's global presence, identify valuable patterns within the data, and potentially predict future trends in this dynamic market.  Let's dive in and unlock the hidden stories within the world of Airbnb!")

#===================================================================================================================================================================#

if selected == 'DISCOVER':
    tab1, tab2 = st.tabs(["**PRICE ANALYSIS**","**GEOSPATIAL VISUALIZATION**"])
    
    with tab1:
        st.subheader("PRICE ANALYSIS W.R.T. COUNTRIES & ROOM TYPE")

        countries = st.multiselect("Select the Countries", Hotel_df['country'].unique())

        df_country = Hotel_df[Hotel_df['country'].isin(countries)]
        df_country.reset_index(inplace = True)

        rt = st.multiselect("Select the Room Type", df_country['room_type'].unique())
        df_rt = df_country[df_country['room_type'].isin(rt)]
        df_rt.reset_index(inplace= True)

        col1, col2= st.columns(2)

        with col1:
            df1 = pd.DataFrame(df_rt.groupby("property_type")[["price","no_of_reviews"]].sum())
            df1.reset_index(inplace=True)
            fig = px.bar(df1, x='property_type', y="price", title="TOTAL PRICE FOR PROPERTY TYPES",
                        hover_data=["no_of_reviews"],
                        color_discrete_sequence=px.colors.sequential.Sunsetdark,
                        width=700, height=600)
            st.plotly_chart(fig)

        with col2:
            total_price_selected_countries = Hotel_df[Hotel_df['country'].isin(countries)]['price'].sum()
            st.metric(label="**:red[TOTAL PRICE FOR SELECTED COUNTRIES]**", value=total_price_selected_countries, delta=None)

            min_price_country = Hotel_df[Hotel_df['country'].isin(countries)]['price'].min()
            # Display metric showing min price for selected countries
            st.metric(label="**:red[MINIMUM PRICE FOR SELECTED COUNTRIES]**", value=min_price_country, delta=None)

            max_price_country = Hotel_df[Hotel_df['country'].isin(countries)]['price'].max()
            st.metric(label="**:red[MAXIMUM PRICE FOR SELECTED COUNTRIES]**", value=max_price_country, delta=None)

            Avg_bedroom = Hotel_df[Hotel_df['country'].isin(countries)]['total_bedrooms'].mean()
            rounded_avg_bedrooms = round(Avg_bedroom, 2)
            st.metric(label="**:red[AVERAGE BEDROOMS FOR SELECTED COUNTRIES]**", value=rounded_avg_bedrooms , delta=None)

            avg_review_score = Hotel_df[Hotel_df['country'].isin(countries)]['review_score'].mean()
            rounded_avg_review_score =  round(avg_review_score,0)
            st.metric(label="**:red[AVERAGE REVIEW SCORE FOR SELECTED COUNTRIES]**", value=rounded_avg_review_score, delta=None)

        col3, col4 = st.columns(2)

        with col3:
            avg_price_country = df_country.groupby('country')['price'].mean().reset_index()
            avg_price_country = avg_price_country.sort_values(by='price', ascending=False)

            fig = px.bar(avg_price_country,x='price',y='country',orientation='h',title="AVERAGE PRICE OF AIRBNB LISTINGS BY COUNTRY",
                    labels={'price': 'Average Price', 'country': 'Country'},width=550, height=450)

            fig.update_layout(
                    margin=dict(l=100, r=20, t=70, b=70), 
                )

            for i, row in avg_price_country.iterrows(): #iterate through avg price of country 
                    fig.add_annotation(
                        x=row['price'],
                        y=row['country'],
                        text=f"{row['price']:.0f}", 
                        showarrow=False,
                        xanchor='left',
                        yanchor='middle'
                    )

            st.plotly_chart(fig)
            

        with col4:
           total_listings_by_country_roomtype = df_rt.groupby(['country', 'room_type'])['Host_total_listings'].sum().reset_index()

           total_listings_all_countries_roomtype = total_listings_by_country_roomtype['Host_total_listings'].sum()


           total_listings_by_country_roomtype['percentage'] = (total_listings_by_country_roomtype['Host_total_listings'] / total_listings_all_countries_roomtype) * 100

           fig_pie_roomtype = px.pie(total_listings_by_country_roomtype, 
                                        values='percentage', 
                                        names='country', 
                                        title='PERCENTAGE OF TOTAL LISTINGS  BY COUNTRY AND ROOM TYPE',
                                        labels={'percentage': 'Percentage', 'country': 'Country'},
                                        color_discrete_sequence=px.colors.qualitative.Vivid)

           st.plotly_chart(fig_pie_roomtype)

    
    with tab2:
        st.subheader("GEO-SPATIAL VISUALISATION")

        city_counts = Hotel_df.groupby('street')['id'].count().reset_index()
        city_counts.rename(columns={'id': 'count'}, inplace=True)

        df_city = pd.merge(Hotel_df, city_counts, on='street', how='left')
        df_city['price']=df_city['price'].astype(dtype='str')
        df_city['hover_info'] = df_city['name'] + ', ' + df_city['country']+', '+ 'Price=$'+df_city['price']


        fig = px.scatter_mapbox(
            df_city,
            lat = "Latitude",
            lon = "Longitude",
            color = "count",
            size = "count", 
            mapbox_style = "open-street-map",
            zoom = 1,
            hover_name = 'hover_info', 
            labels = {"count": "Airbnb Listings"},
            title = "AIRBNB LISTINGS BY COUNTRY",
            template = 'plotly_dark',
            width=1200, height=700,
            color_continuous_scale='bluered'
        )

        fig.update_layout(
            geo=dict(showcoastlines=False, projection=dict(type='mercator')),
            coloraxis_colorbar=dict(title="Listing Count"),
            margin=dict(l=50, r=0, t=50, b=0)
        )

        st.plotly_chart(fig)

#==========================================================================================================================================================#

if selected == 'INSIGHTS':
    question = st.selectbox("Select a question:", [
    "What are the counts of different room types in the listings?",
    "Which are the top 15 hosts with the most number of listings?",
    "What is the average number of listings per host?",
    "What is the average price per night for each cancellation policy?",
    "What is the Range of the number of guests included?",
    "What is the relationship between review scores and price?",
    "What is the most common property type?",
    "What is the average price per night for each bed type?",
    "What is the average price per night for Top 10 hosts?",
    "What is the distribution of listings across different countries?"
])
        # Visualizations based on the selected question

    if question == "What are the counts of different room types in the listings?":
        fig = px.histogram(Hotel_df, x='room_type', title="Different Room Types in the Listings",
                   labels={'room_type': 'Room Type', 'count': 'Count'},
                   color='room_type')
        fig.update_layout(barmode='group', xaxis_tickangle=-45, height=700, width=1000)

    elif question == "Which are the top 15 hosts with the most number of listings?":
        top_hosts = Hotel_df['host_name'].value_counts().sort_values(ascending = False).index[:15]
        df_top_hosts = Hotel_df[Hotel_df['host_name'].isin(top_hosts)]
        fig = px.histogram(df_top_hosts, x='host_name', title="Top 15 Hosts with Most Number of Listings",
                        labels={'host_name': 'Host Name', 'count': 'Count'})
        fig.update_layout(barmode='group', xaxis_tickangle=-45)
        
    elif question == "What is the average number of listings per host?":
        average_listings_per_host = Hotel_df.groupby('host_name')['Host_total_listings'].mean().reset_index().sort_values(by='Host_total_listings', ascending=False)[:10]
        fig = px.bar(average_listings_per_host, x='host_name', y='Host_total_listings', color='Host_total_listings')
        fig.update_layout(title="Average Number of Listings per Host", xaxis_title="Host Name", yaxis_title="Average Number of Listings", height=700, width=1000)

    elif question == "What is the average price per night for each cancellation policy?":
        avg_price_by_cancel_policy = Hotel_df.groupby('cancellation_policy')['price'].mean().reset_index()
        fig = px.bar(avg_price_by_cancel_policy, x='cancellation_policy', y='price', color='price')
        fig.update_layout(title="Average Price per Night for Each Cancellation Policy", xaxis_title="Cancellation Policy", yaxis_title="Average Price", height=700, width=1000)

    elif question == "What is the Range of the number of guests included?":
        x = Hotel_df['guests_included'].value_counts().sort_index().reset_index()
        fig = px.bar(x, x = x.index, y=x.values, color=x.values)
        fig.update_layout(title="Distribution of the Number of Guests Included", xaxis_title="No. of Guests", yaxis_title="Count", height=700, width=1000)

    elif question == "What is the relationship between review scores and price?":
        fig = px.scatter(Hotel_df, x='review_score', y='price')
        fig.update_layout(title="Relationship between Review Scores and Price", xaxis_title="Review Score", yaxis_title="Price", height=700, width=1000)

    elif question == "What is the most common property type?":
        property_type_counts = Hotel_df['property_type'].value_counts().reset_index()
        fig = px.bar(property_type_counts, x=property_type_counts.index, y=property_type_counts.values, color=property_type_counts.values)
        fig.update_layout(title="Most Common Property Type", xaxis_title="Property Type", yaxis_title="Frequency", height=700, width=1000)

    elif question == "What is the average price per night for each bed type?":
        avg_price_by_bed_type = Hotel_df.groupby('bed_type')['price'].mean().reset_index()
        fig = px.bar(avg_price_by_bed_type, x='bed_type', y='price')
        fig.update_layout(title="Average Price per Night for Each Bed Type", xaxis_title="Bed Type", yaxis_title="Average Price", height=700, width=1000)

    elif question == "What is the average price per night for Top 10 hosts?":
        avg_price_by_host = Hotel_df.groupby('host_name')['price'].mean().sort_values(ascending=False)[:15].reset_index()
        fig = px.bar(avg_price_by_host, x='host_name', y='price', color='price')
        fig.update_layout(title="Average Price per Night for Each Host", xaxis_title="Host Name", yaxis_title="Average Price", height=700, width=1000)

    elif question == "What is the distribution of listings across different countries?":
        country_counts = Hotel_df['country'].value_counts().reset_index()
        fig = px.bar(country_counts, x=country_counts.index, y=country_counts.values, color=country_counts.values)
        fig.update_layout(title="Distribution of Listings Across Different Countries", xaxis_title="Country", yaxis_title="Frequency", height=700, width=1000)

    st.plotly_chart(fig)

#======================================================================================================================================================#

if selected =='POWERBI':

    st.image('PowerBiAirbnb.png', caption='PowerBI DashBoard Screenshot', width=1200)

        
