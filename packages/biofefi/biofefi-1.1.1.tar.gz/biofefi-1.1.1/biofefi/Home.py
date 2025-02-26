import streamlit as st

from biofefi.components.images.logos import header_logo, sidebar_logo

st.set_page_config(
    page_title="BioFEFI",
    page_icon=sidebar_logo(),
)
header_logo()
sidebar_logo()

st.write("# Welcome")
st.write(
    """
    **BioFEFI** stands for biological data feature importance fusion framework.

    Using BioFEFI, you can **rapidly** develop machine learning models of many kinds, and evaluate their performance
    down to a **feature-by-feature** level.

    You can create models to solve either **classification** problems (e.g. is this image a cat 🐱 or a dog 🐶?)
    or **regression** problems (e.g. what will be the price of gold 🏅 tomorrow 📈?).

    Your models can then be evaluated by general measures, such as **accuracy**, and by individual feature metrics,
    such as **SHAP**.

    ### Using BioFEFI

    To create a **new experiment** ⚗️, go to the sidebar on the **left** and click **"New Experiment"**.

    To view your previous experiments 📈, go to the sidebar on the **left** and click **"View Experiments"**.

    To train new machine learning models 🏋️, go to the sidebar on the **left** and click **"Train Models"**.

    To run a feature importance analysis 📊, go to the sidebar on the **left** and click **"Feature Importance"**.
    """
)
