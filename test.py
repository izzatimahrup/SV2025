import streamlit as st 

st.set_page_config(
    page_title="Student Survey"
)

visualise = st.Page('studentSurvey.py', title='Pencapaian Akademik Pelajar', icon=':material/school:')

home = st.page('home.py', title='HomePage', default=True, icon=':material/school:')



pg = st.navigation (
    {
        "Menu" : [home, visualise]
    }
)

pg.run()
