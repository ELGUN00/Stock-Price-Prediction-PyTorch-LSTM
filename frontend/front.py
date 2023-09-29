import streamlit as st
import requests
import altair as alt
import pandas as pd
import datetime


st.set_page_config(
    page_title="STOCK PRICS PREDICITON",page_icon=':person:',initial_sidebar_state="expanded"
)

with st.container():
    st.write("""# Stock price prediction""")
    st.write('---')

  

with open('./frontend/style.css') as f:
    st.markdown(f'<style>{f.read()}/<style>', unsafe_allow_html=True)

c1 = st.container()
c2 = st.container()

today = datetime.datetime.now() + datetime.timedelta(days=1)
businessDays = pd.date_range(end=today, periods=14, freq='D')
df = pd.DataFrame({'Date' : businessDays[-11:]})
st.days_list = df.Date.dt.strftime('%d-%m-%Y').to_list()

def predict(ticket):
    if ticket:
        try:
            with st.spinner('Wait for it...'):
                # r = requests.post(f'http://localhost:8080/predict',json={"ticket":ticket})
                r = requests.post(f'http://api:8080/predict',json={"ticket":ticket})
            data = r.json()
            status = data.get('status')
            if status=='OK':
                print(r.json().get('status'))
                st.value = data.get('prediction')
                st.prices = data.get('lookback_days')
                st.delta = st.prices[-1]
                st.prices.append(st.value)
            else:
                st.error(status, icon="🚨")
        except Exception as e:
            st.error(e, icon="🚨")
    else:
        st.error('Please type ticket name', icon="🚨")

with c1:
    with st.form(key='Predict stock price for tomorrow'):
        st.write('Stock price ticket')
        st.ticket = st.text_input(label="Ticket")
        submit_form = st.form_submit_button(label="Predict stock price for tomorrow", help="Click to predict stock price!", on_click=predict(st.ticket))


col1, col2 = st.columns(2)
st.write('---')

if submit_form:
  
    with col1:
        st.metric(label="Today date", value=f"{datetime.datetime.now().strftime('%d-%m-%Y')}")

    chart_data = pd.DataFrame({
       "Date": st.days_list,
       "Price": st.prices
    })
        
    with col2:
        st.metric(label=f"{st.ticket} price for tomorrow", value=f"{st.value:.2f} $", delta=f"Previous: {st.delta:.2f} $")

    main = (
       alt.Chart(chart_data)
       .mark_area(point=True)
       .encode(x=alt.X("Date"), y=alt.Y("Price",scale=alt.Scale(domain=[round(min(st.prices))-2,round(max(st.prices))+2])))
    )
    
   
    line = alt.Chart(chart_data[-2:-1]).mark_rule(size=0.5).encode(x=alt.X("Date"))

    st.altair_chart((main + line).interactive(), use_container_width=True)