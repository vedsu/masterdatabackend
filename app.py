# run.py
from app import app

# Run the application
if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")