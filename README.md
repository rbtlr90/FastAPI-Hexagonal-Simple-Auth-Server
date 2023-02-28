<p align="center">
    <image height="150" src="./static/image/fastapi.png">
</p>

# FastAPI-Hexagonal-Simple-Auth-Server

FastAPI를 기반으로 Hexagonal architecture 연습용으로 만든 간단한 account/auth api 서버입니다.<br />
Python3.10에서 테스트됐으며,<br />
Python 3.9, 3.11과 일부 library와 version conflict 발생을 확인했습니다.

</br>

## Usage
Docker:
```
docker-compose up
```

Local:<br />

```
install Postgres, Redis in local 
install python dependency
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## License
- MIT License
