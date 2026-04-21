# -*- coding: utf-8 -*-
import json
import os
import re

import requests


HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "Qwen/Qwen2.5-7B-Instruct")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")


def _clean_sentence(text):
    hanguel = re.compile("[^ ㄱ-ㅣ가-힣.,?!\\d+]")
    text = hanguel.sub("", text)
    return re.sub(r"[-=+#/:^$@*\"※~&%ㆍ_!』\\‘|\(\)\[\]\<\>`'…》]", "", text).strip()


def _finalize_sentence(text):
    text = _clean_sentence(text)
    if not text:
        return ""

    match = re.search(r"^.*?[.?!](?=\s|$)", text)
    if match:
        text = match.group(0).strip()

    if text[-1] not in ".?!":
        if re.search(r"(다|요|죠|네|까|니다|했다|였다|된다|했다가|한다)$", text):
            text = f"{text}."
        else:
            return ""

    return text


def _salvage_sentence(text):
    text = _clean_sentence(text)
    if not text:
        return ""
    text = re.sub(r"^\s*\d+[.)-]?\s*", "", text).strip()
    if not text:
        return ""
    if text[-1] not in ".?!":
        text = f"{text}."
    return text


def _looks_like_chat_response(text):
    lowered = text.strip()
    blocked_patterns = [
        r"설명해\s*주실\s*수\s*있",
        r"말씀해\s*주실\s*수\s*있",
        r"알려\s*주실\s*수\s*있",
        r"도와드릴까요",
        r"더\s+자세히\s+설명",
        r"까요\?$",
        r"인가요\?$",
    ]
    return any(re.search(pattern, lowered) for pattern in blocked_patterns)


def _extract_texts_from_payload(payload):
    texts = []

    if isinstance(payload, str):
        stripped = payload.strip()
        if stripped:
            texts.append(stripped)
        return texts

    if isinstance(payload, list):
        for item in payload:
            texts.extend(_extract_texts_from_payload(item))
        return texts

    if not isinstance(payload, dict):
        return texts

    for key in ("generated_text", "summary_text", "text", "content", "response"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            texts.append(value.strip())
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and isinstance(item.get("text"), str) and item.get("text").strip():
                    texts.append(item.get("text").strip())

    choices = payload.get("choices", [])
    for choice in choices:
        if isinstance(choice, dict):
            message = choice.get("message", {})
            if isinstance(message, dict):
                content = message.get("content")
                if isinstance(content, str) and content.strip():
                    texts.append(content.strip())
                elif isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and isinstance(item.get("text"), str) and item.get("text").strip():
                            texts.append(item.get("text").strip())
            delta = choice.get("delta", {})
            if isinstance(delta, dict) and isinstance(delta.get("content"), str) and delta.get("content").strip():
                texts.append(delta.get("content").strip())

    if isinstance(payload.get("message"), dict):
        message = payload["message"]
        if isinstance(message.get("content"), str) and message.get("content").strip():
            texts.append(message.get("content").strip())

    generated = payload.get("generated_text")
    if isinstance(generated, list):
        texts.extend(_extract_texts_from_payload(generated))

    return texts


def _collect_sentence_candidates(raw_texts):
    results = []
    for generated in raw_texts:
        chunks = re.split(r"[\n\r]+", generated)
        for chunk in chunks:
            cleaned = re.sub(r"^\s*\d+[.)-]?\s*", "", chunk).strip()
            if not cleaned:
                continue

            sentence_parts = re.findall(r"[^.?!\n\r]+[.?!]?", cleaned)
            accepted = False
            for sentence_part in sentence_parts:
                finalized = _finalize_sentence(sentence_part.strip())
                if finalized and not _looks_like_chat_response(finalized):
                    results.append(finalized)
                    accepted = True

            if not accepted:
                salvaged = _salvage_sentence(cleaned)
                if salvaged and not _looks_like_chat_response(salvaged):
                    results.append(salvaged)

    deduped = []
    for result in results:
        if result and result not in deduped:
            deduped.append(result)
    return deduped[:5]


def _extract_huggingface_candidates(payload):
    raw_texts = _extract_texts_from_payload(payload)
    results = _collect_sentence_candidates(raw_texts)
    if results:
        return results

    relaxed = []
    for generated in raw_texts:
        chunks = re.split(r"[\n\r]+", generated)
        for chunk in chunks:
            cleaned = re.sub(r"^\s*\d+[.)-]?\s*", "", chunk).strip()
            if not cleaned:
                continue
            salvaged = _salvage_sentence(cleaned)
            if salvaged:
                relaxed.append(salvaged)

    deduped_relaxed = []
    for result in relaxed:
        if result and result not in deduped_relaxed:
            deduped_relaxed.append(result)
    return deduped_relaxed[:5]

def sentence_complete(text):
    if not HUGGINGFACE_API_KEY:
        return ["HUGGINGFACE_API_KEY가 설정되지 않아 자동완성을 사용할 수 없습니다."]

    prompt = (
        "당신은 블로그 글 초안을 이어 쓰는 한국어 문장 완성기입니다. "
        "입력된 내용의 문맥과 어조를 유지한 채, 작성자가 바로 이어 붙일 수 있는 자연스러운 후속 문장만 작성하세요. "
        "질문을 던지거나, 독자에게 되묻거나, 설명을 요청하거나, AI 비서처럼 반응하면 안 됩니다. "
        "\"좀 더 자세히 설명해 주실 수 있나요?\", \"어떤 프로젝트인지 궁금하네요\" 같은 대화형 문장은 절대 쓰지 마세요. "
        "완성 결과는 블로그 본문에 그대로 들어가도 어색하지 않은 서술형 문장이어야 합니다. "
        "각 항목은 서로 조금씩 다르게 쓰되, 모두 입력 내용의 흐름을 자연스럽게 이어야 합니다. "
        "반드시 각 항목을 완결된 한 문장으로만 쓰고, 문장 끝은 마침표로 끝내세요. "
        "문장이 중간에 끊기면 안 됩니다. 각 문장은 한 줄씩만 출력하세요. "
        "번호, 불릿, 따옴표, 설명 문구는 절대 쓰지 마세요. 문장 5개만 줄바꿈으로 출력하세요.\n\n"
        f"입력 문맥:\n{text}"
    )

    response = requests.post(
        url="https://router.huggingface.co/v1/chat/completions",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        },
        data=json.dumps(
            {
                "model": HUGGINGFACE_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "temperature": 0.45,
                "max_tokens": 256,
            }
        ),
        timeout=20,
    )

    response.raise_for_status()
    payload = response.json()
    results = _extract_huggingface_candidates(payload)

    if not results:
        return ["자동완성 결과를 만들지 못했습니다. 입력 문장을 조금 더 구체적으로 적어 주세요."]

    return results
