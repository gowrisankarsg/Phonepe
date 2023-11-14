import pandas as pd
import os
import json
import mysql.connector
import streamlit as st
import plotly.express as px


def toptrans():
    conn = mysql.connector.connect(
        host = 'localhost',
        port =  '3306',
        user = 'root',
        password = '1414',
        database = 'phonepe_pulse'
    )
    cursor = conn.cursor()

    # Transaction
    toptranspath = "phonepe_pulse/data/top/transaction/country/india/state/"
    toptransdata = {
        "state" : [],
        'year' : [],
        'quarter' : [],
        'district' : [],
        'count' : [],
        'amount' : []
    }
    for i in os.listdir(toptranspath):
        toptranstate = toptranspath+i+'/'
        for j in os.listdir(toptranstate):
            toptransyear = toptranstate+j+'/'
            for k in os.listdir(toptransyear):
                toptransfile = json.load(open(toptransyear+k))
                for m in toptransfile['data']['districts']:
                    district = m['entityName']
                    count = m['metric']['count']
                    amount = m['metric']['amount']
                    toptransdata['state'].append(i)
                    toptransdata['year'].append(int(j))
                    toptransdata['quarter'].append(int(k.strip('.json')))
                    toptransdata['district'].append(district)
                    toptransdata['count'].append(int(count))
                    toptransdata['amount'].append(amount)
    
    toptransdata_df = pd.DataFrame(toptransdata)
    toptxn_df = pd.read_sql_query("select * from top_transaction",conn)
    if toptxn_df.empty:
        st.sidebar.write("toptxn_df dataframe is empty")
        for row in toptransdata_df.itertuples():            
            cursor.execute(f"insert into top_transaction values ('{row[1]}',{row[2]},{row[3]},'{row[4]}',{row[5]},{row[6]})")
        st.sidebar.success("successfully inserted")
    else:
        st.sidebar.error("toptxn_df informartion already existed")

    # User
    topuserpath = "phonepe_pulse/data/top/user/country/india/state/"
    topuserdata = {
        "state" : [],
        'year' : [],
        'quarter' : [],
        'district' : [],
        'registeredUsers' : []
    }
    for i in os.listdir(topuserpath):
        userstate = topuserpath+i+'/'
        for j in os.listdir(userstate):
            useryear = userstate+j+'/'
            for k in os.listdir(useryear):
                userfile = json.load(open(useryear+k))
                for m in userfile['data']['districts']:
                    district = m['name']
                    registeredUsers = m['registeredUsers']
                    topuserdata['state'].append(i)
                    topuserdata['year'].append(int(j))
                    topuserdata['quarter'].append(int(k.strip('.json')))
                    topuserdata['district'].append(district)
                    topuserdata['registeredUsers'].append(int(registeredUsers))

    topuserdata_df = pd.DataFrame(topuserdata)
    topuser_df = pd.read_sql_query("select * from top_user",conn)
    if topuser_df.empty:
        st.sidebar.write("aggtxn_df dataframe is empty")
        for row in topuserdata_df.itertuples():            
            cursor.execute(f"insert into top_user values ('{row[1]}',{row[2]},{row[3]},'{row[4]}',{row[5]})")
        st.sidebar.success("successfully inserted")
    else:
        st.sidebar.error("topuser_df informartion already existed")

    types = st.selectbox("Types",("Transaction","User"),index=None,placeholder="Select the types")
    State = list(toptxn_df['State'].unique())
    state = st.selectbox('State',State,index=None,placeholder="Select the state")
    col1,col2 = st.columns(2)
    with col1:
        Year = st.slider("Year",2018,2023)

    with col2:
        Quarter = st.slider("Quarter",1,4)

    if types == 'Transaction':
        st.subheader(state)
        sb = toptxn_df.query("State == @state and Trans_year == @Year and Trans_quarter == @Quarter")
        sbc = px.bar(sb,x='District',y='Trans_amount',color='District')
        st.plotly_chart(sbc)

    if types == 'User':
        st.subheader(state)
        usb = topuser_df.query("State == @state and User_year == @Year and User_quarter == @Quarter")
        usbc = px.bar(usb,x='District',y='User_count',color='District')
        st.plotly_chart(usbc)

    conn.commit()
    cursor.close()
    conn.close()