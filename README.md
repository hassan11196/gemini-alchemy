# gemini-alchemy

Mind mapping is an enduringly popular method for recording, organizing, and presenting information. With Gemini and other models we are able to quickly visualize concepts but mindmapping is the area which still needs some work. We realized that it's super hard to create beautifully appealing mindmaps on complex concepts and data. Therefore, we came up with **Gemini-Alchemy**, which is a tool to convert abstract ideas into a visually appealing mindmap format.

## Guide to locally run the code

- Create and activate venv
- install requirements by 'pip install -r requirements.txt'
- first run the backend
  - Uvicorn app:app
- then run the streamlit app:
  - Streamlit run streamlit_app.py
- you should also have a .env file with all necessary variables in it such as API_URL, and GEMINI_API_KEY
