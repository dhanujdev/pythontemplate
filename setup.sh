#!/bin/bash

# Make setup.sh executable
chmod +x setup.sh

# Install Python dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py 