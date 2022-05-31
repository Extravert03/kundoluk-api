import uvicorn

import settings
from app import app


def main():
    uvicorn.run(
        'main:app',
        host=settings.APP_HOST,
        port=settings.APP_PORT,
    )


if __name__ == '__main__':
    main()
