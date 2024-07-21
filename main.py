def create_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
    print(f'{filename} created successfully.')

def main():
    # 1. app.py
    app_py_content = """import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Use environment variables
database_url = os.getenv('DATABASE_URL')

# Streamlit app
def main():
    st.title('My Streamlit App')
    st.write(f'Database URL: {database_url}')

if __name__ == '__main__':
    main()
"""
    create_file('app.py', app_py_content)

    # 2. create_env.py
    create_env_py_content = """def create_env_file():
    # Example data to be stored in .env
    env_variables = {
        'STREAMLIT_APP': 'app.py',
        'STREAMLIT_ENV': 'production',
        'DATABASE_URL': 'sqlite:///database.db'
    }

    # Create .env file
    with open('.env', 'w') as f:
        for key, value in env_variables.items():
            f.write(f'{key}={value}\\n')

    print('.env file created successfully.')

if __name__ == '__main__':
    create_env_file()
"""
    create_file('create_env.py', create_env_py_content)

    # 3. .env (this file will be created by create_env.py)

    # 4. requirements.txt
    requirements_txt_content = """streamlit==1.3.1
pandas==1.3.4
numpy==1.21.2
python-dotenv==0.19.2
"""
    create_file('requirements.txt', requirements_txt_content)

    # 5. Procfile
    procfile_content = """web: streamlit run app.py
"""
    create_file('Procfile', procfile_content)

    # 6. runtime.txt
    runtime_txt_content = """python-3.9.6
"""
    create_file('runtime.txt', runtime_txt_content)

    # 7. .gitignore
    gitignore_content = """.env
__pycache__/
*.pyc
"""
    create_file('.gitignore', gitignore_content)

    # 8. setup.sh (optional)
    setup_sh_content = """mkdir -p ~/.streamlit/

echo "\
[general]\\n\
email = \\"your-email@example.com\\"\\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\\n\
headless = true\\n\
enableCORS=false\\n\
port = $PORT\\n\
" > ~/.streamlit/config.toml
"""
    create_file('setup.sh', setup_sh_content)

if __name__ == '__main__':
    main()
