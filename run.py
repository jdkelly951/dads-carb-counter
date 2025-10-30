from dotenv import load_dotenv
load_dotenv()  # reads .env into environment variables

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
