# OCI Osaka `gpt-oss` LangChain 챗앱

OCI Osaka 리전의 `openai.gpt-oss-20b` 또는 `openai.gpt-oss-120b`를 LangChain으로 호출하는 간단한 Streamlit 챗앱입니다.

기본 구성:

- UI: `Streamlit`
- LLM 래퍼: `langchain-openai`
- OCI 인증/전송: `oci-openai`
- 기본 모델: `openai.gpt-oss-20b`
- 기본 리전: `ap-osaka-1`

## 빠른 시작

### 1. 전제 조건

- Python `3.10+`
- `~/.oci/config` 가 API Key 방식으로 정상 설정되어 있어야 함
- 대상 컴파트먼트에 OCI Generative AI 호출 권한이 있어야 함
- Osaka 리전(`ap-osaka-1`)에서 해당 모델 사용 가능해야 함

### 2. 설치

```bash
cd /home/opc/oci-osaka-gpt-oss-chat
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

### 3. 설정

`.env.example`을 참고해서 `.env` 파일을 만듭니다.

예시:

```bash
cp .env.example .env
vi .env
```

`.env` 예시:

```bash
OCI_PROFILE=DEFAULT
OCI_COMPARTMENT_ID=<your_compartment_ocid>
OCI_GENAI_REGION=ap-osaka-1
OCI_GENAI_MODEL=openai.gpt-oss-20b
```

### 4. 실행

포그라운드 실행:

```bash
cd /home/opc/oci-osaka-gpt-oss-chat
source .venv/bin/activate
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

백그라운드 실행:

```bash
cd /home/opc/oci-osaka-gpt-oss-chat
./run.sh
```

접속:

```text
http://<VM_PUBLIC_IP>:8501
```

## 실행 스크립트

### `run.sh`

- `.env`와 `.venv` 존재 여부 확인
- 이미 실행 중인지 확인
- `streamlit.log`에 로그 저장
- `streamlit.pid`에 PID 저장
- `0.0.0.0:8501`으로 백그라운드 실행

실행:

```bash
./run.sh
```

### `stop.sh`

- `streamlit.pid`에 저장된 PID를 읽어서 종료

실행:

```bash
./stop.sh
```

## 파일 구성

- `app.py`: Streamlit 앱 본체
- `requirements.txt`: Python 패키지 목록
- `.env.example`: 환경 변수 템플릿
- `run.sh`: 백그라운드 실행 스크립트
- `stop.sh`: 종료 스크립트

## 동작 방식

핵심 포인트:

- OCI OpenAI 호환 엔드포인트 사용

```text
https://inference.generativeai.ap-osaka-1.oci.oraclecloud.com/20231130/actions/v1
```

- 인증은 `OciUserPrincipalAuth(profile_name="DEFAULT")` 사용
- `CompartmentId` 헤더 전달
- LangChain에서는 `ChatOpenAI` 사용
- 모델 이름은 `openai.gpt-oss-20b` 또는 `openai.gpt-oss-120b`

## 자주 나는 오류

### 1. 인증 오류

증상:

```text
NotAuthorizedOrNotFound
```

점검:

- `~/.oci/config` 확인
- `OCI_CLI_AUTH=instance_principal` 같은 강제 환경변수 제거
- 해당 사용자/API Key에 Generative AI 호출 권한이 있는지 확인

### 2. 컴파트먼트 헤더 누락

증상:

- 요청 실패
- 권한 오류

점검:

- `CompartmentId` 헤더가 포함되어야 함

### 3. Python 버전 문제

증상:

- 설치 실패
- `langchain-openai` import 실패

점검:

- Python `3.10+` 사용

### 4. 포트 접속 불가

점검:

- OS 방화벽에서 `8501/tcp` 허용 여부 확인
- OCI 시큐리티리스트 또는 NSG에서 `8501/tcp` 허용 여부 확인
- 앱이 실제로 실행 중인지 확인

```bash
cat streamlit.pid
tail -f streamlit.log
```
