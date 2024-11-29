import streamlit as st
st.sidebar.markdown(
    """
    <style>
    .sidebar-title {
        font-size: 80px;
        font-weight: bold;
        color: #4CAF50; /* Green color */
        text-align: center;
    }

     div.stButton > button{
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px;
        border: none;
        border-radius: 5px;
        width: 100%;
        text-align: center;
        cursor: pointer;
    }
    .sidebar-button:hover {
        background-color: #FF0000;
    }

    </style>
    """, unsafe_allow_html=True
)