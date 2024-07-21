def create_env_file():
    # Example data to be stored in .env
    env_variables = {
        'STREAMLIT_APP': 'app.py',
        'STREAMLIT_ENV': 'production',
        'DATABASE_URL': 'sqlite:///database.db'
    }

    # Create .env file
    with open('.env', 'w') as f:
        for key, value in env_variables.items():
            f.write(f'{key}={value}\n')

    print('.env file created successfully.')

if __name__ == '__main__':
    create_env_file()
