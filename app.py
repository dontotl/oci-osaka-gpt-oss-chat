import os
from typing import List, Tuple

import httpx
import streamlit as st
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from oci_openai import OciUserPrincipalAuth
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


DEFAULT_REGION = os.getenv("OCI_GENAI_REGION", "ap-osaka-1")
DEFAULT_MODEL = os.getenv("OCI_GENAI_MODEL", "openai.gpt-oss-20b")
DEFAULT_PROFILE = os.getenv("OCI_PROFILE", "DEFAULT")
DEFAULT_COMPARTMENT_ID = os.getenv("OCI_COMPARTMENT_ID", "")


def build_base_url(region: str) -> str:
    return f"https://inference.generativeai.{region}.oci.oraclecloud.com/20231130/actions/v1"


def make_llm(profile: str, compartment_id: str, region: str, model: str, temperature: float) -> ChatOpenAI:
    if not compartment_id:
        raise ValueError("OCI_COMPARTMENT_ID is required.")

    return ChatOpenAI(
        model=model,
        api_key="OCI",
        base_url=build_base_url(region),
        temperature=temperature,
        http_client=httpx.Client(
            auth=OciUserPrincipalAuth(profile_name=profile),
            headers={"CompartmentId": compartment_id},
            timeout=60.0,
        ),
    )


def to_langchain_messages(history: List[Tuple[str, str]]) -> List[BaseMessage]:
    converted: List[BaseMessage] = [
        SystemMessage(content="당신은 OCI Osaka의 OpenAI gpt-oss 모델과 연결된 도움이 되는 한국어 챗봇입니다.")
    ]
    for role, content in history:
        if role == "user":
            converted.append(HumanMessage(content=content))
        else:
            converted.append(AIMessage(content=content))
    return converted


st.set_page_config(page_title="OCI Osaka GPT-OSS Chat", page_icon=":speech_balloon:", layout="centered")
st.title("OCI Osaka GPT-OSS Chat")
st.caption("LangChain + OCI OpenAI 호환 API + OpenAI gpt-oss")

with st.sidebar:
    st.subheader("설정")
    profile = st.text_input("OCI Profile", value=DEFAULT_PROFILE)
    compartment_id = st.text_input("Compartment OCID", value=DEFAULT_COMPARTMENT_ID)
    region = st.text_input("Region", value=DEFAULT_REGION)
    model = st.selectbox(
        "Model",
        options=["openai.gpt-oss-20b", "openai.gpt-oss-120b"],
        index=0 if DEFAULT_MODEL == "openai.gpt-oss-20b" else 1,
    )
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    st.markdown(
        "\n".join(
            [
                "`OCI Profile`은 `~/.oci/config`의 프로파일 이름입니다.",
                "`Compartment OCID`는 Generative AI 호출 권한이 있는 컴파트먼트여야 합니다.",
                "`Region`은 Osaka 기준 `ap-osaka-1`입니다.",
            ]
        )
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, content in st.session_state.chat_history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(content)

prompt = st.chat_input("메시지를 입력하세요")

if prompt:
    st.session_state.chat_history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        llm = make_llm(
            profile=profile,
            compartment_id=compartment_id,
            region=region,
            model=model,
            temperature=temperature,
        )
        response = llm.invoke(to_langchain_messages(st.session_state.chat_history))
        answer = response.content if isinstance(response.content, str) else str(response.content)
    except Exception as exc:
        answer = f"호출 실패: {exc}"

    st.session_state.chat_history.append(("assistant", answer))
    with st.chat_message("assistant"):
        st.markdown(answer)
