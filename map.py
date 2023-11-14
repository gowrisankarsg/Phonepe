import pandas as pd
import os
import json
import mysql.connector
import streamlit as st
import plotly.express as px






def maptrans():
    conn = mysql.connector.connect(
        host = 'localhost',
        port =  '3306',
        user = 'root',
        password = '1414',
        database = 'phonepe_pulse'
    )
    cursor = conn.cursor()
    # Transaction
    maptranspath = "phonepe_pulse/data/map/transaction/hover/country/india/state/"
    maptransdata = {
        "state" : [],
        'year' : [],
        'quarter' : [],
        'district' : [],
        'count' : [],
        'amount' : []
    }
    for i in os.listdir(maptranspath):
        transtate = maptranspath+i+'/'
        for j in os.listdir(transtate):
            transyear = transtate+j+'/'
            for k in os.listdir(transyear):
                transfile = json.load(open(transyear+k))
                for m in transfile['data']['hoverDataList']:
                    district = m['name']
                    count = m['metric'][0]['count']
                    amount = m['metric'][0]['amount']
                    maptransdata['state'].append(i)
                    maptransdata['year'].append(int(j))
                    maptransdata['quarter'].append(int(k.strip('.json')))
                    maptransdata['district'].append(district.strip(' district'))
                    maptransdata['count'].append(int(count))
                    maptransdata['amount'].append(int(amount))

    maptransdata_df = pd.DataFrame(maptransdata)
    maptxn_df = pd.read_sql_query("select * from map_transaction",conn)
    
    if maptxn_df.empty:
        st.sidebar.write("maptxn_df dataframe is empty")
        for row in maptransdata_df.itertuples():            
            cursor.execute(f"insert into map_transaction values ('{row[1]}',{row[2]},{row[3]},'{row[4]}',{row[5]},{row[6]})")
        st.sidebar.success("successfully inserted")
    else:
        st.sidebar.error("maptxn_df informartion already existed")

    # User
    mapuserpath = "phonepe_pulse/data/map/user/hover/country/india/state/"
    mapuserdata = {
        "state" : [],
        'year' : [],
        'quarter' : [],
        'district' : [],
        'registeredUsers' : [],
        'appOpens' : []
    }
    for i in os.listdir(mapuserpath):
        userstate = mapuserpath+i+'/'
        for j in os.listdir(userstate):
            useryear = userstate+j+'/'
            for k in os.listdir(useryear):
                userfile = json.load(open(useryear+k))
                for m in userfile['data']['hoverData']:
                    registeredUsers = userfile['data']['hoverData'][m]['registeredUsers']
                    appOpens = userfile['data']['hoverData'][m]['appOpens']
                    mapuserdata['state'].append(i)
                    mapuserdata['year'].append(int(j))
                    mapuserdata['quarter'].append(int(k.strip('.json')))
                    mapuserdata['district'].append(m.strip(' district'))
                    mapuserdata['registeredUsers'].append(registeredUsers)
                    mapuserdata['appOpens'].append(appOpens)

    mapuserdata_df = pd.DataFrame(mapuserdata)
    mapuser_df = pd.read_sql_query("select * from map_user",conn)
    
    if mapuser_df.empty:
        st.sidebar.write("mapuser_df dataframe is empty")
        for row in mapuserdata_df.itertuples():            
            cursor.execute(f"insert into map_user values ('{row[1]}',{row[2]},{row[3]},'{row[4]}',{row[5]},{row[6]})")
        st.sidebar.success("successfully inserted")
    else:
        st.sidebar.error("mapuser_df informartion already existed")

    
    states = {
        'himachal-pradesh' : 'Himachal Pradesh',
        'puducherry' : 'Puducherry',
        'punjab' : 'Punjab',
        'tripura' : 'Tripura',
        'odisha' : 'Odisha',
        'jammu-&-kashmir' : 'Jammu & Kashmir',
        'mizoram' : 'Mizoram',
        'west-bengal' : 'West Bengal',
        'ladakh' : 'Ladakh',
        'uttarakhand' : 'Uttarakhand',
        'maharashtra' : 'Maharashtra',
        'jharkhand' : 'Jharkhand',
        'uttar-pradesh' : 'Uttar Pradesh',
        'haryana' : 'Haryana',
        'manipur' : 'Manipur',
        'kerala' : 'Kerala',
        'andaman-&-nicobar-islands' : 'Andaman & Nicobar',
        'assam' : 'Assam',
        'tamil-nadu' : 'Tamil Nadu',
        'nagaland' : 'Nagaland',
        'meghalaya' : 'Meghalaya',
        'dadra-&-nagar-haveli-&-daman-&-diu' : 'Dadra and Nagar Haveli and Daman and Diu',
        'chhattisgarh' : 'Chhattisgarh',
        'goa' : 'Goa',
        'lakshadweep' : 'Lakshadweep',
        'karnataka' : 'Karnataka',
        'telangana' : 'Telangana',
        'andhra-pradesh' : 'Andhra Pradesh',
        'delhi' : 'Delhi',
        'rajasthan' : 'Rajasthan',
        'chandigarh' : 'Chandigarh',
        'arunachal-pradesh' : 'Arunachal Pradesh',
        'madhya-pradesh' : 'Madhya Pradesh',
        'gujarat' : 'Gujarat',
        'sikkim' : 'Sikkim',
        'bihar' : 'Bihar',

    }


    types = st.selectbox("Types",("Transaction","User"),index=None,placeholder="Select the types")
    col1,col2 = st.columns(2)
    with col1:
        Year = st.slider("Year",2018,2023)

    with col2:
        Quarter = st.slider("Quarter",1,4)

    if types == 'Transaction':
        maptxn_df['State'] = maptxn_df['State'].map(states)
        ind = maptxn_df.query("Trans_year == @Year and Trans_quarter == @Quarter",engine='python')
        st.subheader('Transaction Amount')
        fig = px.choropleth(
            ind,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Trans_amount',
            hover_name= 'State',
            color_continuous_scale='Reds'
        )

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        st.subheader('Transaction Count')
        tcm = px.choropleth(
            ind,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Trans_count',
            hover_name= 'State',
            color_continuous_scale='Reds'
        )

        tcm.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(tcm)

    if types == 'User':
        mapuser_df['State'] = mapuser_df['State'].map(states)
        ind = mapuser_df.query("User_year == @Year and User_quarter == @Quarter",engine='python')
        st.subheader('Registered Users count')
        fig = px.choropleth(
            ind,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='RegisteredUsers_count',
            hover_name= 'State',
            color_continuous_scale='Reds'
        )

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig)
        st.subheader('App Opens')
        uac = px.choropleth(
            ind,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='AppOpens',
            hover_name= 'State',
            color_continuous_scale='Reds'
        )

        uac.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(uac)

    conn.commit()
    cursor.close()
    conn.close()

    