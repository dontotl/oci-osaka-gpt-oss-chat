# OCI Osaka `gpt-oss` LangChain 챗앱

이 예제는 OCI Osaka 리전의 `openai.gpt-oss-20b` 또는 `openai.gpt-oss-120b`를 호출해서 LangChain 기반의 간단한 챗앱을 실행하는 최소 예제입니다.

구성:

- UI: `Streamlit`
- LLM 래퍼: `langchain-openai`
- OCI 인증/전송: `oci-openai`
- 모델: `openai.gpt-oss-20b` 기본값

## 1. 전제 조건

- Python `3.10+`
- `~/.oci/config` 가 API Key 방식으로 정상 설정되어 있어야 함
- 대상 컴파트먼트에서 OCI Generative AI 호출 권한이 있어야 함
- Osaka 리전(`ap-osaka-1`)에서 해당 모델 사용 가능해야 함

현재 서버의 Python이 `3.6.8`이면 이 예제는 그대로 실행되지 않습니다.  
새 VM 또는 별도 가상환경에서 Python `3.10+`를 준비한 뒤 실행하세요.

## 2. 설치

```bash
cd /home/opc/oci-osaka-gpt-oss-chat
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## 3. 환경 변수

`.env.example` 내용을 참고해서 환경변수를 설정합니다.

예시:

```bash
export OCI_PROFILE=DEFAULT
export OCI_COMPARTMENT_ID=<your_compartment_ocid>
export OCI_GENAI_REGION=ap-osaka-1
export OCI_GENAI_MODEL=openai.gpt-oss-20b
```

## 4. 실행

```bash
cd /home/opc/oci-osaka-gpt-oss-chat
source .venv/bin/activate
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

브라우저 접속:

```text
http://<VM_PUBLIC_IP>:8501
```

## 5. 코드 설명

핵심 포인트:

- `base_url`

```text
https://inference.generativeai.ap-osaka-1.oci.oraclecloud.com/20231130/actions/v1
```

- 인증은 `OciUserPrincipalAuth(profile_name="DEFAULT")` 를 사용
- `CompartmentId` 헤더를 반드시 전달
- LangChain에서는 `ChatOpenAI`를 사용
- 모델 이름은 `openai.gpt-oss-20b` 또는 `openai.gpt-oss-120b`

## 6. 자주 나는 오류

### 1) 인증 오류

증상:

```text
NotAuthorizedOrNotFound
```

점검:

- `~/.oci/config` 확인
- `OCI_CLI_AUTH=instance_principal` 같은 강제 환경변수 제거
- 해당 사용자/API Key에 Generative AI 호출 권한이 있는지 확인

### 2) 컴파트먼트 헤더 누락

증상:

- 요청이 실패하거나 권한 오류 발생

점검:

- `headers={"CompartmentId": compartment_id}` 가 포함되어야 함

### 3) Python 버전 문제

증상:

- 설치 실패
- `langchain-openai` import 실패

점검:

- Python `3.10+` 사용

