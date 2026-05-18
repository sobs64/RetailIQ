@echo off

:: Activate the virtual environment
call "d:\Projects\RetailIQ\.venv\Scripts\activate.bat"

:: Run the Streamlit app
streamlit run app\streamlit_app.py %*

:: Deactivate after exit
deactivate
