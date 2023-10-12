#!/usr/bin/env python
# coding: utf-8

# In[10]:


import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import locale

# Lees het CSV-bestand in als een DataFrame
Laadpalen_1 = pd.read_csv('Laadpalen.csv')

# Lees het CSV-bestand in als een DataFrame
df_cleaned = pd.read_csv('df_cleaned.csv')
result_df= pd.read_csv('result_df.csv')
#df4 = pd.read_csv('Autos_jaar_brndstof.csv')

df9 = pd.read_csv('prijs_voorspellen.csv')
df10 = pd.read_csv('prijs_voorspellen.csv')
#df8 = pd.read_csv('Autos_merk_jaar_prijs.csv')
#df6 = pd.read_csv('Autos_merk_brandstof.csv')
df11 = pd.read_csv('df11.csv')
df12 = pd.read_csv("df12.csv")
df6 = pd.read_csv("df6.csv")


# In[12]:


df_cleaned['Started'] = pd.to_datetime(df_cleaned['Started'], format= '%Y-%m-%d %H:%M:%S')
df_cleaned['Ended'] = pd.to_datetime(df_cleaned['Ended'], format='%Y-%m-%d %H:%M:%S')


# In[13]:


# Functie om de inleidingspagina weer te geven
def inleiding_pagina():
    st.title("Inleiding")
    st.write("Welkom op dit Streamlit-dashboard met informatie over elektrische auto's, laadpalen en laadpaalgebruik in Nederland.")

    st.write("In dit dashboard kun je informatie vinden over:")
    st.markdown("- **Elektrische Auto's:** Verken gegevens en statistieken met betrekking tot elektrische auto's in Nederland.")
    st.markdown("- **Laadpalen:** Ontdek waar laadpalen zich bevinden en hoeveel er zijn in Nederland.")
    st.markdown("- **Laadpaalgebruik:** Bekijk gegevens over het gebruik van laadpalen voor elektrische voertuigen.")

   # Instructies voor gebruik
    st.write("### Instructies voor gebruik:")
    st.write(
        "1. Gebruik de inhoudsopgave en tabladen om de gewenste visualisatieopties te bekijken."
    )
    st.write(
        "2. Bekijk de grafieken en visualisaties om patronen en trends te ontdekken. Veeg met uw muis over de visualisaties heen om de gewenste data in te zien."
    )
    st.write(
        "3. Gebruik de slidebars, selectieboxen en drop-down menu's om het gewenste jaartal en bereik toe te passen."
        
        
    )
    # Voetnoot en contactinformatie
    st.write(
        "Dit dashboard is gemaakt door Eric de Jong en Elayza Lo-Ning-Hing en is bedoeld voor informatieve doeleinden."
    )

def laadpalen_pagina():
    # Aangepaste kleurtoewijzing voor laadpaaltypes
    color_mapping = {
        'AC (Three-Phase)': 'green',
        'DC': 'red',
        'AC (Single-Phase)': 'blue',
        'Onbekend': 'gray'
    }
    
    province_names = ["Zuid-Holland", "Drenthe", "Flevoland", "Friesland", "Gelderland", "Groningen", "Limburg", "Noord-Brabant", "Noord-Holland", "Overijssel", "Utrecht", "Zeeland", "Alle provincies"]
    
    province_coords = {
        "Alle provincies": [52.1326, 5.2913],
        "Drenthe": [52.816951, 6.918983],
        "Flevoland": [52.550000, 5.750000],
        "Friesland": [53.164722, 5.781111],
        "Gelderland": [52.083333, 5.916667],
        "Groningen": [53.219383, 6.566502],
        "Limburg": [51.209722, 5.927778],
        "Noord-Brabant": [51.441641, 5.469722],
        "Noord-Holland": [52.366667, 4.900000],
        "Overijssel": [52.514444, 6.095556],
        "Utrecht": [52.090833, 5.121389],
        "Zeeland": [51.514722, 3.849722],
        "Zuid-Holland": [51.922500, 4.479167]
    }

    # Streamlit App
    st.title("Laadpalen")
    st.write("Dit is de pagina over laadpalen. Hier kun je informatie vinden over laadpalen voor elektrische auto's.")
    selected_province = st.selectbox("Selecteer een provincie:", province_names)
    m = folium.Map(location=[52.3784, 4.9005], zoom_start=7)
    province_map = folium.Map(location=province_coords[selected_province], zoom_start=9)
    
    # Voeg de code toe voor de interactieve kaart met provincie selectie en marker cluster checkbox
    show_marker_cluster = st.checkbox("Toon marker cluster", value=True)
    
    if selected_province != "Alle provincies":
        Laadpalen = Laadpalen_1[Laadpalen_1['Provincie'] == selected_province]
    else: 
        Laadpalen = Laadpalen_1

    if show_marker_cluster:
        marker_cluster = MarkerCluster().add_to(m)
        marker_cluster1 = MarkerCluster().add_to(province_map)

        for map_obj in [m, province_map]:
            for index, row in Laadpalen.iterrows():
                latitude = row['AddressInfo.Latitude']
                longitude = row['AddressInfo.Longitude']
                title = row['AddressInfo.Title']
                current_type = row['CurrentType.Title']
                color = color_mapping.get(current_type, 'gray')
                
                folium.Circle(
                    location=[latitude, longitude],
                    radius=100,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.3,
                    popup=title
                ).add_to(marker_cluster if map_obj is m else marker_cluster1)
    else:
        st.write("Marker cluster is uitgeschakeld.")
        
        for map_obj in [m, province_map]:
            for index, row in Laadpalen.iterrows():
                latitude = row['AddressInfo.Latitude']
                longitude = row['AddressInfo.Longitude']
                title = row['AddressInfo.Title']
                current_type = row['CurrentType.Title']
                color = color_mapping.get(current_type, 'gray')
                
                folium.Circle(
                    location=[latitude, longitude],
                    radius=100,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.3,
                    popup=title
                ).add_to(map_obj)

    col1, col2 = st.columns([3, 1])

    with col1:
        if selected_province != "Alle provincies":
            folium_static(province_map, width=500)
        else:
            folium_static(m, width=500)

    # Voeg de code voor de legenda toe
    col2.markdown(
        '<div style="border: 1px solid black; padding: 10px; border-radius: 5px;">'
        '<div style="background-color: white; padding: 5px;">'
        '<div style="display: flex; flex-direction: column;">'
        '<div style="text-align: center; margin-bottom: 10px;">'
        '<span style="margin-left: 5px; margin-right: 10px; font-weight: bold;">Soorten laadpalen</span>'
        '</div>'
        '<div style="margin-bottom: 5px;">'
        '<i style="background:blue; width: 15px; height: 15px; display:inline-block;"></i>'
        '<span style="margin-left: 5px; margin-right: 10px;">Wisselstroom (Driefasen)</span>'
        '</div>'
        '<div style="margin-bottom: 5px;">'
        '<i style="background:red; width: 15px; height: 15px; display:inline-block;"></i>'
        '<span style="margin-left: 5px; margin-right: 10px;">Gelijkstroom</span>'
        '</div>'
        '<div style="margin-bottom: 5px;">'
        '<i style="background:green; width: 15px; height: 15px; display:inline-block;"></i>'
        '<span style="margin-left: 5px; margin-right: 10px;">Wisselstroom (Eénfase)</span>'
        '</div>'
        '<div style="margin-bottom: 5px;">'
        '<i style="background:gray; width: 15px; height: 15px; display:inline-block;"></i>'
        '<span style="margin-left: 5px;">Onbekend</span>'
        '</div>'
        '</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


        
def laadpaaldata_pagina():
    st.title("Laadpaaldata")
    st.write("Dit is de pagina over laadpaaldata. Hier kun je informatie vinden over gegevens met betrekking tot laadpalen voor elektrische auto's.")

    # Maak de tabs voor de grafieken
    tabs = st.tabs(["Aantal connecties", "Laadprofiel", "Laadtijd"])

    # Inhoud van de tabs
    with tabs[0]:
        st.header("Het laadpaalprofiel van de laadpaaldata")
        
        
        df_cleaned['Hour'] = df_cleaned['Started'].dt.hour
        connections_per_hour = df_cleaned.groupby('Hour').size().reset_index(name='Number of Connections')
        fig2 = px.bar(connections_per_hour, x='Hour', y='Number of Connections', 
                      labels={'Number of Connections': 'Aantal verbindingen', 'Hour': 'Uur van de Dag'},
                      title='Aantal Connecties per Uur van de Dag')

        
        # Toon het staafdiagram
        st.plotly_chart(fig2)
        

        # Voeg een kolom 'Hour' toe om het uur van de dag te extraheren uit 'ChargeTime'
        df_cleaned['ChargeHour'] = df_cleaned['Oplaadtijd'].astype(int)

        # Groepeer de gegevens op 'ChargeTime' en tel het aantal verbindingen
        grouped_data = df_cleaned.groupby('ChargeHour')['Connectietijd'].count().reset_index()

        # Maak het staafdiagram met Plotly Express
        fig10 = px.bar(grouped_data, x='ChargeHour', y='Connectietijd',
                     labels={'Connectietijd': 'Aantal verbindingen', 'ChargeHour': 'Oplaadtijd (uren)'},
                     title='Aantal verbindingen per Oplaadtijd')
        fig10.update_xaxes(type='category', tickmode='array', tickvals=grouped_data['ChargeHour'], ticktext=grouped_data['ChargeHour'],
                           rangeslider_visible=True, rangeselector=dict(buttons=list([
                           dict(count=1, label='1d', step='day', stepmode='backward'),
                           dict(count=7, label='1w', step='day', stepmode='backward'),
                           dict(count=1, label='1m', step='month', stepmode='backward'),
                           dict(count=1, label='1y', step='year', stepmode='backward'),
                           dict(step='all')
                           ])))

        # Toon het staafdiagram
        st.plotly_chart(fig10)

        
        

    with tabs[1]:         
        st.header("Het Gemiddelde Laadprofiel per Uur van de Dag ")
        df_cleaned1 = df_cleaned.copy()
        df_cleaned1 = df_cleaned1.loc[df_cleaned1['Oplaadtijd'] > 0]
        df_cleaned1['Hour'] = df_cleaned1['Started'].dt.hour
        df_cleaned1['Power'] = df_cleaned1['TotalEnergy'] / (df_cleaned1['Oplaadtijd'] * 1000)
        average_power_per_hour = df_cleaned1.groupby('Hour')['Power'].mean().reset_index(name='Average Power (kW)')
        fig = px.line(average_power_per_hour, x='Hour', y='Average Power (kW)', 
                      labels={'Average Power (kW)': 'Gemiddeld Vermogen (kW)', 'Hour': 'Uur van de Dag'},
                      title='Gemiddeld Laadprofiel per Uur van de Dag')
        average_power = average_power_per_hour['Average Power (kW)'].mean()
        fig.add_shape(type='line', x0=0, x1=23, y0=average_power, y1=average_power, 
                      line=dict(color='red', width=2, dash='dash'))
        st.plotly_chart(fig)


    with tabs[2]:
        st.header("Het oplaadtijd profiel")

        # Inlezen van gegevens en filteren op de geselecteerde Charge Time Range
        df_cleaned['ChargeHour'] = df_cleaned['Oplaadtijd'].astype(int)
        min_charge_time = df_cleaned['Oplaadtijd'].min()
        max_charge_time = df_cleaned['Oplaadtijd'].max()
        # Laat de gebruiker de Charge Time Range instellen met een tweezijdige slider

        # Filter de gegevens op basis van de geselecteerde Charge Time Range
        filtered_df = df_cleaned[(df_cleaned['Oplaadtijd'] >= min_charge_time) & (df_cleaned['Oplaadtijd'] <= max_charge_time)]

        # Creëer een histogram van de laadtijd
        fig = go.Figure()
        
        num_bins = int(max_charge_time)

        hist_values, hist_labels = np.histogram(filtered_df['ChargeHour'], bins=num_bins)

        # Voeg histogramgegevens toe
        fig.add_trace(go.Bar(x=hist_labels[:-1], y=hist_values, width=1, name='Histogram'))

        # Voeg annotatie van het gemiddelde toe
        gemiddelde = np.mean(filtered_df['ChargeHour'])
        fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=gemiddelde,
                x1=gemiddelde,
                y0=0,
                y1=max(hist_values),
                line=dict(color="red", width=2, dash="dash"),
            )
        )
        fig.add_annotation(
            go.layout.Annotation(
                x=gemiddelde,
                y=max(hist_values),
                text=f"Gemiddelde: {gemiddelde:.2f}",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-50,
            )
        )

        # Voeg annotatie van de mediaan toe
        mediaan = np.median(filtered_df['ChargeHour'])
        fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=mediaan,
                x1=mediaan,
                y0=0,
                y1=max(hist_values),
                line=dict(color="green", width=2, dash="dash"),
            )
        )
        fig.add_annotation(
            go.layout.Annotation(
                x=mediaan,
                y=max(hist_values),
                text=f"Mediaan: {mediaan:.2f}",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40,
            )
        )

        # Bereken benadering van de kansdichtheidsfunctie
        kde = gaussian_kde(filtered_df['ChargeHour'], bw_method=0.2)
        x_vals = np.linspace(min(filtered_df['ChargeHour']), max(filtered_df['ChargeHour']), 100)
        y_vals = kde(x_vals) * len(filtered_df) * (hist_labels[1] - hist_labels[0])  # Schaal de KDE naar het aantal gegevenspunten

        # Voeg KDE toe als een lijnplot
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Kansdichtheidsfunctie'))

        # Voeg labels en titel toe
        fig.update_layout(
            xaxis_title='Oplaadtijd (uren)',
            yaxis_title='Frequentie',
            title='Histogram van Laadtijd met Gemiddelde, Mediaan en Kansdichtheidsfunctie',
            bargap=0.05,  # Aanpassen van de ruimte tussen de histogramstaven
        )
        
        fig.update_xaxes(rangeslider_visible = True)
        # Toon het figuur
        st.plotly_chart(fig)
        

def elektrische_autos_pagina():
    st.title("Elektrische Auto's")
    st.write("Dit is de pagina over elektrische auto's. Hier kun je informatie vinden over elektrische auto's.")

        

    st.subheader("Verkoopinformatie Auto's")
    
    merk_keuze = st.selectbox('Selecteer een merk', df6['Merk'].unique(), key='front')

    jaar_keuze = st.slider('Selecteer een jaar', min_value=int(df10['Jaar'].min()), max_value=int(df10['Jaar'].max()), key='jaar_slider')


    filtered_df = df10[(df10['Merk'] == merk_keuze) & (df10['Jaar'] == jaar_keuze)]

    col1, col2 = st.columns([1, 1])

    # Set de locale naar Nederlands


    # Formatteer de gemiddelde catalogusprijs met een punt als duizendtalscheider en een komma als decimaalscheider



    with col1:
        if not filtered_df.empty:
            st.write('**Aantal verkochte auto\'s in {}**: {}'.format(jaar_keuze, filtered_df["Aantal verkochte auto's"].values[0]))
            st.write('**Totaal verkochte autos**: {}'.format(filtered_df["Totaal verkochte auto's"].values[0]))

        else:
            st.write('Er is geen informatie beschikbaar voor het geselecteerde merk en jaar.')

    with col2:
        if not filtered_df.empty:
            locale.setlocale(locale.LC_NUMERIC, 'nl_NL')
            gemiddelde_catalogusprijs = locale.format_string("%.2f", filtered_df["Gemiddelde Catalogusprijs"].values[0], grouping=True)
            st.write(f'**Gemiddelde Catalogusprijs**: €{gemiddelde_catalogusprijs}')
            st.write('**Ranking in {}**: {}'.format(jaar_keuze, filtered_df["Ranking"].values[0]))
        else:
            st.write(' ')
    #col2.plotly_chart(fig1, use_container_width=True, height=50)  # Pas de hoogte aan zoals gewenst


    # Plaats de voorspelde data in de tweede kolom

    
    cumulatieve_checkbox = st.checkbox("Toon cumulatieve grafiek", value=False, key = 'k')

    col3, col4 = st.columns([1, 1])


    filtered_df = df6[df6['Merk'] == merk_keuze]

    #brandstof_verdeling = filtered_df['Brandstof omschrijving'].value_counts()

    fig1 = px.pie(filtered_df, values='brandstof verdeling', names='Brandstof omschrijving',
                  title=f'Brandstofverdeling voor {merk_keuze}', hole=0.5)


    col3.plotly_chart(fig1, use_container_width=True, height=300)  # Pas de hoogte aan zoals gewenst


    # Voeg een indexkolom toe aan beide datasets


    #df4['Index'] = range(len(df4))
    #df8['Index'] = range(len(df8))
    #df8.drop('Jaar', axis=1, inplace=True)

    # Samenvoeging op basis van de indexkolom
    #df12 = pd.merge(df4, df8, on='Index')

    grouped_df = df12[df12['Merk'] == merk_keuze]

    #grouped_df = filtered_df3.groupby(['Jaar', 'Brandstof omschrijving']).size().reset_index(name='Aantal')


    if cumulatieve_checkbox:
        grouped_df['Cumulatief'] = grouped_df.groupby('Brandstof omschrijving')['Aantal'].cumsum()
        fig2 = px.line(grouped_df, x='Jaar', y='Cumulatief', color='Brandstof omschrijving',
                       labels={'Cumulatief': "Cumulatief aantal auto's", 'Jaar': 'Jaar', 'Brandstof omschrijving': 'Brandstoftype'},
                       title="Cumulatief aantal auto's per jaar en brandstoftype", markers=True)
    else:
        fig2 = px.line(grouped_df, x='Jaar', y='Aantal', color='Brandstof omschrijving',
                       labels={'Aantal': "Aantal auto's", 'Jaar': 'Jaar', 'Brandstof omschrijving': 'Brandstoftype'},
                       title="Aantal auto's per jaar en brandstoftype", markers=True)

    col4.plotly_chart(fig2, use_container_width=True, height=300)



    
    col5, col6 = st.columns([1, 1])


    filtered_df2 = df11[df11['Merk'] == merk_keuze]

    #gemiddelde_catalogusprijs = filtered_df2.groupby('Jaar')['Catalogusprijs'].mean()

    fig3 = px.line(filtered_df2, x='Jaar', y='gemiddelde prijs',
                  labels={'x': 'Jaar', 'y': 'Gemiddelde Catalogusprijs (in Euro)'},
                  title=f'Gemiddelde Catalogusprijs voor {merk_keuze}')




    filtered_df1 = df9[df9['Merk'] == merk_keuze]
    model = LinearRegression()
    X = filtered_df1[['Jaar']]
    y = filtered_df1['Gemiddelde Catalogusprijs']
    model.fit(X, y)

    komende_jaren = 5
    toekomstige_jaren = filtered_df1['Jaar'].max() + 1 + np.arange(komende_jaren).reshape(-1, 1)
    voorspellingen = model.predict(toekomstige_jaren)

    voorspelde_data = pd.DataFrame({'Jaar': toekomstige_jaren.flatten(), 'Voorspelde Catalogusprijs': voorspellingen})

    fig4 = px.line(voorspelde_data, x='Jaar', y='Voorspelde Catalogusprijs', title='Voorspelde Gemiddelde Catalogusprijs')


    col5.plotly_chart(fig3, use_container_width=True, height=300)
    col6.plotly_chart(fig4, use_container_width=True, height=300)

    

        
# Hoofdprogramma
st.sidebar.title("Inhoudsopgave")

# Voeg deze regels toe om de inleidingspagina en datasets weer te geven
pagina_keuze = st.sidebar.radio("Kies een pagina", ("Inleiding", "Datasets"))

if pagina_keuze == "Inleiding":
    inleiding_pagina()

elif pagina_keuze == "Datasets":
    st.sidebar.markdown("### Datasets")
    dataset_keuze = st.sidebar.radio("Kies een dataset", ("Laadpalen","Laadpaaldata","Elektrische Auto's"))
    if dataset_keuze == "Laadpalen":
        laadpalen_pagina()
    elif dataset_keuze == "Laadpaaldata":
        laadpaaldata_pagina()
    elif dataset_keuze == "Elektrische Auto's":
        elektrische_autos_pagina()





# In[ ]:




