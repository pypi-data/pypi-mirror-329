
from atlaz.codeGen.backend.flask_server import app
    
def main():
    app.run(debug=True, port=5050)

if __name__ == "__main__":
    main()