# Newsbite Backend

Python ingestion and API service for automated AI news summaries.

---

## Quickstart

### 1) 사전 준비
- `.env.example`를 복사해 `.env` 생성 후 값 채우기
- 반드시 이 디렉터리(`newsbite-backend`)에서 명령 실행

### 2) Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

백그라운드(독립 프로세스) 실행/중지:
```powershell
$p = Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m","uvicorn","app.main:app","--reload","--port","8000" -PassThru
Start-Sleep -Seconds 2
iwr http://localhost:8000/health -UseBasicParsing | Select-Object -Expand Content
# 중지
Stop-Process -Id $p.Id
```

### 3) macOS/Linux (zsh/bash)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

백그라운드 실행/중지:
```bash
nohup python -m uvicorn app.main:app --reload --port 8000 > uvicorn.out 2>&1 &
echo $! > uvicorn.pid
# 중지
kill "$(cat uvicorn.pid)"
```

### 4) 확인
```powershell
iwr http://localhost:8000/health -UseBasicParsing | Select-Object -Expand Content
```
```bash
curl -s http://localhost:8000/health
```

문제 해결:
- `requirements.txt`를 못 찾는 경우: 현재 위치가 `newsbite-backend`인지 확인
- `uvicorn`을 찾지 못하는 경우: 가상환경 활성화 후 설치 여부 확인

---

## Database & Alembic

### 설정
- `.env`의 `DATABASE_URL` 값을 사용합니다. (기본: `sqlite:///./newsbite.db`)

### 마이그레이션 워크플로
```powershell
# 1) 모델 변경 후 리비전 생성
.\.venv\Scripts\python.exe -m alembic revision --autogenerate -m "change"

# 2) 업그레이드 적용
.\.venv\Scripts\python.exe -m alembic upgrade head

# 3) 다운그레이드(필요 시)
.\.venv\Scripts\python.exe -m alembic downgrade -1
```

```bash
# 1) 모델 변경 후 리비전 생성
python -m alembic revision --autogenerate -m "change"

# 2) 업그레이드 적용
python -m alembic upgrade head

# 3) 다운그레이드(필요 시)
python -m alembic downgrade -1
```

### 트러블슈팅
- Windows 인코딩 오류 발생 시: `alembic.ini`에 비ASCII 주석을 피하세요.
- `ImportError` 발생 시: `app/` 하위 모듈에 `__init__.py`가 있는지 확인.