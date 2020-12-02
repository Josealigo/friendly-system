import altair as alt
import streamlit as st
from vega_datasets import data
import sqlalchemy 

st.title("Product Development: Project")


engine = create_engine("mysql://test:test123@db/covid",
                            encoding='latin1', echo=True)

confirmed = pd.read_sql_table('confirmed',engine)

confirmed