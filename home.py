import streamlit as st
import pandas as pd
import numpy as np
import time
def app():
    st.markdown("#首頁")
    st.write("""# My first app Hello *world!*""")
    df = pd.DataFrame(
        {
        'first column':[1,2,3,4],
        'second column':[10,20,30,40]
        })
    st.write(df) # interactive table
    st.table(df) # static table
    dataframe = pd.DataFrame(
        np.random.randn(10,20),
        columns=('col %d' % i for i in range(20))
        )
    st.dataframe(dataframe.style.highlight_max(axis=0))

    # Draw a line chart
    chart_data = pd.DataFrame(
        np.random.randn(20,3),
        columns=['a','b','c']
    )
    st.line_chart(chart_data)

    # Plot a map
    map_data = pd.DataFrame(
        np.random.randn(1000,2)/[50,50] + [37.76,-122.4],
        columns=['lat','lon']
    )
    st.map(map_data)

    # Widgets (slider)
    x = st.slider('x')
    st.write(x,'squared is', x*x)

    # Widgets (text_input)
    st.text_input("Your name",key="name")
    st.session_state.name

    # Use checkboxes to show/hide data
    if st.checkbox('Show dataframe'):
        chart_data

    # Use a selectbox for options
    option = st.selectbox(
        'Which number do you like best?',
        df['first column'] 
    )
    'You selected: ', option

    # layout
    add_selectbox = st.sidebar.selectbox(
        'How would you like to be contacted?',
        ('Email','Home phone','Mobile phone')
    )

    add_slider = st.sidebar.slider(
        'Select a range of values',
        0.0, 100.0, (25.0,75.0)
    )

    left_column, right_column = st.columns(2)
    left_column.button('Press me!')

    with right_column:
        chosen = st.radio(
            'sorting hat',
            ("gryffindor","Ravenclaw","Hufflepuff","SLytherin"),
        )
        st.write(f"You are in {chosen} house!")

    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(10):
        latest_iteration.text(f'Iteration{i+1}')
        bar.progress(i+1)
        time.sleep(0.1)
    'and now we\'re done!'

    #st.cache_data 儲存 str, int, float, Dataframe, dict, list
    #st.cache_source 儲存 ML_models, database connections

    @st.cache_data
    def long_running_function(param1,param2):
        return ...

    if "counter" not in st.session_state:
        st.session_state.counter = 0 
    st.session_state.counter +=1
    st.header(f"This page has run {st.session_state.counter} times")
    st.button("Run it again")

    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(
            np.random.randn(20,2),columns=["x","y"]
        )
    st.header("Choose a datapoint color")
    color = st.color_picker("Color","#FF0000")
    st.divider()
    st.scatter_chart(st.session_state.df,x="x",y="y",color=color)