import streamlit as st
import matplotlib.pyplot as plt

from visuals import create_visuals2

st.title('FPL Draft League - There Can Be Only One')
st.text('This competitive Fantasy Premier League pits managers against each other as they draft their teams and battle it out all season long.')
st.text('Now in its third thrilling edition, the big question remains: will the reigning two-time champion, Los Porro Hermanos, finally be dethroned?')
st.text('League data is updated every Monday—or sooner upon request.')
figure = create_visuals2
fig, ax = plt.subplots(figure)
st.pyplot(fig)


