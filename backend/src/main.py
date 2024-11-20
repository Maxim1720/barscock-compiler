from fastapi import FastAPI, Response
from starlette.requests import Request

from .analyzer.lexical.lexical_analyzer import analyze
from .conf import get_global_config
from .schema import CodeRequestSchema, AnalyzeResponseSchema

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

config = get_global_config()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или можно указать конкретный домен, например "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def read_out(type: str):
    items = []
    f = open(f"{config.OUT_DIR}/lex/{type}.txt", "r", encoding='utf-8')
    for line in f:
        line = line.strip()
        items.append(line)
    return items


@app.post("/analyze", response_model=AnalyzeResponseSchema, status_code=200)
def root(code: CodeRequestSchema) -> AnalyzeResponseSchema:
    # LexicalAnalyzer(code.data).analyze()
    state = analyze(code.data)
    tw = read_out("tw")
    tl = read_out("tl")
    tn = read_out("tn")
    ti = read_out("ti")
    return AnalyzeResponseSchema(tw=tw, tl=tl, tn=tn, ti=ti, state=state.value)


