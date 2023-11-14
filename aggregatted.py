import pandas as pd
import os
import json
import mysql.connector
import streamlit as st
import plotly.express as px




def aggtrans():
    conn = mysql.connector.connect(
        host = 'localhost',
        port =  '3306',
        user = 'root',
        password = '1414',
        database = 'phonepe_pulse'
    )
    cursor = conn.cursor()

    # Transaction
    aggtranspath = "phonepe_pulse/data/aggregated/transaction/country/india/state/"
    aggtransdata ={
        'state' : [],
        'year' : [],
        'quarter' : [],
        'transaction_type' : [],
        'transaction_count' : [],
        'transaction_amount' : []
    }
    for i in os.listdir(aggtranspath):
        transtate = aggtranspath+i+'/'
        for j in os.listdir(transtate):
            transyear = transtate+j+'/'
            for k in os.listdir(transyear):
                transfile = json.load(open(transyear+k,'r'))
                for m in transfile['data']['transactionData']:
                    type = m['name']
                    count = m['paymentInstruments'][0]['count']
                    amount = m['paymentInstruments'][0]['amount']
                    aggtransdata['transaction_type'].append(type)
                    aggtransdata['transaction_count'].append(count)
                    aggtransdata['transaction_amount'].append(amount)
                    aggtransdata['state'].append(i)
                    aggtransdata['year'].append(int(j))
                    aggtransdata['quarter'].append(int(k.strip('.json')))

    aggtransdata_df = pd.DataFrame(aggtransdata)
    aggtxn_df = pd.read_sql_query("select * from aggregate_transaction",conn)
    if aggtxn_df.empty:
        st.sidebar.write("aggtxn_df dataframe is empty")
        for row in aggtransdata_df.itertuples():            
            cursor.execute(f"insert into aggregate_transaction values ('{row[1]}',{row[2]},{row[3]},'{row[4]}',{row[5]},{row[6]})")
        st.sidebar.success("successfully inserted")
    else:
        st.sidebar.error("aggtxn_df informartion already existed")

    # User
    agguserpath = "phonepe_pulse/data/aggregated/user/country/india/state/"
    aggUserData = {
        "state" : [],
        'year' : [],
        'quarter' : [],
        'devive_brand' : [],
        'count' : [],
        'percentage' : []
    }
    for i in os.listdir(agguserpath):
        aggUserState = agguserpath+i+'/'
        for j in os.listdir(aggUserState):
            aggUseryear = aggUserState+j+'/'
            for k in os.listdir(aggUseryear):
                aggUserFile = aggUseryear+k
                auf = open(aggUserFile)
                aufd = json.load(auf)
                if aufd['data']['usersByDevice'] is not None:
                    for m in aufd['data']['usersByDevice']:
                        brand = m['brand']
                        count = m['count']
                        percentage = m['percentage']
                        aggUserData['state'].append(i)
                        aggUserData['year'].append(int(j))
                        aggUserData['quarter'].append(int(k.strip('.json')))
                        aggUserData['devive_brand'].append(brand)
                        aggUserData['count'].append(count)
                        aggUserData['percentage'].append(percentage)

    aggUserData_df = pd.DataFrame(aggUserData)
    agguser_df = pd.read_sql_query("select * from aggregate_user",conn)
    if agguser_df.empty:
        st.sidebar.write("agguser_df dataframe is empty")
        for row in aggUserData_df.itertuples():            
            cursor.execute(f"insert into aggregate_user values ('{row[1]}',{row[2]},{row[3]},'{row[4]}',{row[5]},{row[6]})")
        st.sidebar.success("successfully inserted")
    else:
        st.sidebar.error("agguser_df informartion already existed")

    types = st.selectbox("Types",("Transaction","User"),index=None,placeholder="Select the types")
    col1,col2 = st.columns(2)
    with col1:
        Year = st.slider("Year",2018,2023)

    with col2:
        Quarter = st.slider("Quarter",1,4)

    if types == 'Transaction':
        st.subheader("Year and Quarter wise bar chart")
        yq = aggtxn_df.query("Trans_year == @Year and Trans_quarter == @Quarter",engine='python')
        yqb = px.bar(yq,x='State',y='Trans_amount',color='State')
        st.plotly_chart(yqb)
        st.subheader("Group Bar Chart")
        gbc = px.bar(aggtxn_df,x="State",y = "Trans_amount",color = "Trans_year",barmode='group')
        st.plotly_chart(gbc)
        st.subheader("Stack Bar Chart")
        sbc = px.bar(aggtxn_df,x="State",y = "Trans_amount",color = "Trans_year",barmode='stack')
        st.plotly_chart(sbc)
        st.subheader("Area Chart")
        ac = px.area(aggtxn_df,x="State",y = "Trans_amount",color = "Trans_year")
        st.plotly_chart(ac)
        st.subheader("Sunburst Chart")
        sb = aggtxn_df.groupby(['State','Trans_year'])['Trans_amount'].sum().reset_index()
        sunburstchart = px.sunburst(sb,path=['State','Trans_year'],values='Trans_amount')
        st.plotly_chart(sunburstchart)

    if types == 'User':
        st.subheader("Year and Quarter wise Bar Chart")
        ywb = agguser_df.query("User_year == @Year and User_quarter == @Quarter",engine='python')
        ywbc = px.bar(ywb,x='State',y='User_count',color='State')
        st.plotly_chart(ywbc)
        st.subheader('Pie Chart')
        dp = agguser_df.groupby(['Devive_brand'])['Percentage'].sum().reset_index()
        dpc = px.pie(dp,values='Percentage',names='Devive_brand')
        st.plotly_chart(dpc)
        st.subheader('Area Chart')
        ac = px.area(agguser_df,x="State",y = "Percentage",color = "User_year")
        st.plotly_chart(ac)
        st.subheader('Sunburst Chart')
        usb = agguser_df.groupby(['State','User_year'])['Devive_brand'].count().reset_index()
        usbc = px.sunburst(usb,path=['State','User_year'],values='Devive_brand')
        st.plotly_chart(usbc)
        


    
    conn.commit()
    cursor.close()
    conn.close()




