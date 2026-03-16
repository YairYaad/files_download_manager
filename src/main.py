from src.app.app_config import app
import uvicorn


def main():
    uvicorn.run(app, host='localhost', port=8080)


if __name__ == '__main__':
    main()
