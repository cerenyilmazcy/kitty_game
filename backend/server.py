import os
from typing import Any, Dict

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


HF_MODEL_URL = (
    "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
)


class AnalyzePayload(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)


class SentimentCat:
    def __init__(self, token: str | None) -> None:
        self.session = requests.Session()
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    def analyze(self, text: str) -> Dict[str, Any]:
        response = self.session.post(
            HF_MODEL_URL, headers=self.headers, json={"inputs": text}, timeout=20
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            message = response.text if response is not None else str(exc)
            raise HTTPException(status_code=response.status_code, detail=message) from exc

        result = response.json()
        if not result or not result[0]:
            raise HTTPException(
                status_code=500,
                detail="HuggingFace API beklenen formatta sonuç döndürmedi.",
            )

        top = max(result[0], key=lambda item: item["score"])
        reactions = {
            "LABEL_2": {"emoji": "😺", "message": "Mırmır mutluluktan pati pati oynuyor!"},
            "LABEL_1": {"emoji": "😼", "message": "Mırmır dikkat kesildi, biraz daha anlatmanı istiyor."},
            "LABEL_0": {"emoji": "🙀", "message": "Mırmır endişelendi, sana sarılmak istiyor."},
        }

        fallback = {"emoji": "😸", "message": "Mırmır şaşkın ama seni seviyor!"}
        reaction = reactions.get(top["label"], fallback)

        return {
            "label": top["label"],
            "score": round(top["score"], 4),
            "emoji": reaction["emoji"],
            "message": reaction["message"],
        }


def create_app() -> FastAPI:
    token = os.getenv("HF_TOKEN")
    if not token:
        raise RuntimeError(
            "HF_TOKEN ortam değişkeni tanımlı değil. HuggingFace erişim token'ı gereklidir."
        )

    sentiment_cat = SentimentCat(token=token)
    app = FastAPI(title="Mırmır Sentiment API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=os.getenv("KITTY_ALLOWED_ORIGINS", "*").split(","),
        allow_credentials=False,
        allow_methods=["POST", "OPTIONS"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> Dict[str, str]:
        return {"status": "ok"}

    @app.post("/analyze")
    def analyze(payload: AnalyzePayload) -> Dict[str, Any]:
        return sentiment_cat.analyze(payload.text)

    return app


app = create_app()

