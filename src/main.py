import streamlit as st
import pandas as pd
import sqlalchemy 

st.title("Product Development: Project")


engine = sqlalchemy.create_engine("mysql://test:test123@db/covid",
                            encoding='latin1', echo=True)

confirmed = pd.read_sql_table('confirmed',engine)

confirmed