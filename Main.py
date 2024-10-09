# Tool for automatically Creating create table statements in snowflake

import pandas as pd
import streamlit as st

def parse_csv(df, varchar):

    table_info = pd.DataFrame(columns = ['Column Name', 'Data Type'])

    for column in df.columns.values.tolist():
        if varchar:
            table_info.loc[len(table_info.index)] = [column, 'varchar(16777216)']
        elif (df[column].dtype.name == "int" or df[column].dtype.name == "int64"):
            table_info.loc[len(table_info.index)] = [column, 'int']
        elif df[column].dtype.name == "object":
            table_info.loc[len(table_info.index)] = [column, 'varchar(16777216)']
        elif df[column].dtype.name == "datetime64[ns]":
            table_info.loc[len(table_info.index)] = [column, 'datetime']
        elif df[column].dtype.name == "float64":
            table_info.loc[len(table_info.index)] = [column, 'float8']
        elif df[column].dtype.name == "bool":
            table_info.loc[len(table_info.index)] = [column, 'boolean']
        else:
            table_info.loc[len(table_info.index)] = [column, 'varchar(16777216)']
    
    return table_info

def create_table_statement(database,schema,table, df, uppercase):
    ## Create the table if it doesn't exist:
    create_tbl_statement = f'CREATE TABLE IF NOT EXISTS {database}.{schema}.{table} ('

    df = df.reset_index()
    for index, row in df.iterrows():
        if uppercase:
            create_tbl_statement = create_tbl_statement + '"' + row['Column Name'].upper() + '" ' + row['Data Type'] + ', '
        else:
            create_tbl_statement = create_tbl_statement + '"' + row['Column Name'] + '" ' + row['Data Type'] + ', '
    create_tbl_statement = create_tbl_statement[:-2] + ')'
        
    return create_tbl_statement



st.set_page_config(page_title='Snowflake Table Creation Query Tool', page_icon="❄️")
st.title('Snowflake Table Creation Query Tool')
st.subheader('Created by Teddy Caulton at teddycaulton.xyz')

Input_Data = st.file_uploader("Upload your input data here, make sure it's a plain csv table with comma delimination", type = 'csv')
varchar = st.checkbox("Make all data types VARCHAR")

if Input_Data:
    df = pd.read_csv(Input_Data)
    csv_info = parse_csv(df, varchar)
    st.write('here is the columns and data types we see, feel free to edit the table below if something is off')
    presented_outputs = st.data_editor(csv_info)

    database = st.text_input('Enter the database where this table will live')
    schema = st.text_input('Enter the schema where this table will live')
    table = st.text_input('Enter the name of the table that will be created')
    uppercase = st.checkbox("Uppercase all columns")

    if st.button("Generate Query"):
        query = create_table_statement(database,schema,table, presented_outputs, uppercase)
        st.code(query, language="sql")

