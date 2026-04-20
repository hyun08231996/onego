# -*- coding: utf-8 -*-
import json
import os
import re

import requests


GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


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


def _extract_candidates(candidates):
    results = []
    for candidate in candidates:
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        if not parts:
            continue
        generated = parts[0].get("text", "").strip()
        chunks = re.split(r"[\n\r]+", generated)
        for chunk in chunks:
            cleaned = re.sub(r"^\s*\d+[.)-]?\s*", "", chunk).strip()
            if not cleaned:
                continue

            sentence_parts = re.findall(r"[^.?!\n\r]+[.?!]?", cleaned)
            accepted = False
            for sentence_part in sentence_parts:
                finalized = _finalize_sentence(sentence_part.strip())
                if finalized:
                    results.append(finalized)
                    accepted = True

            if not accepted:
                salvaged = _salvage_sentence(cleaned)
                if salvaged:
                    results.append(salvaged)

    deduped = []
    for result in results:
        if result and result not in deduped:
            deduped.append(result)
    return deduped[:5]

def sentence_complete(text):
    if not GEMINI_API_KEY:
        return ["GEMINI_API_KEY가 설정되지 않아 자동완성을 사용할 수 없습니다."]

    prompt = (
        "다음 한국어 문장을 자연스럽게 이어서 쓸 수 있는 짧은 후속 문장 5개를 작성해 주세요. "
        "반드시 각 항목을 완결된 한 문장으로만 쓰고, 문장 끝을 마침표나 물음표로 끝내세요. "
        "문장이 중간에 끊기면 안 됩니다. 각 문장은 한 줄씩만 출력하고, 번호만 붙여 주세요. 설명은 쓰지 마세요.\n\n"
        f"입력 문장: {text}"
    )

    response = requests.post(
        url=(
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{GEMINI_MODEL}:generateContent"
        ),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "x-goog-api-key": GEMINI_API_KEY,
        },
        data=json.dumps(
            {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 256,
                    "candidateCount": 2,
                },
            }
        ),
        timeout=20,
    )

    response.raise_for_status()
    payload = response.json()
    candidates = payload.get("candidates", [])
    results = _extract_candidates(candidates)

    if not results:
        return ["자동완성 결과를 만들지 못했습니다. 입력 문장을 조금 더 구체적으로 적어 주세요."]

    return results
