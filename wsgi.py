from app import app

if __name__ == "__main__":
    print("Running Flask App through gunicorn")
    app.run()