from fastapi import FastAPI, Response
from starlette.requests import Request

from .analyzer.lexical.lexical_analyzer import Analyzer
from .conf import get_global_config
from .files import read_out
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



@app.post("/analyze", response_model=AnalyzeResponseSchema, status_code=200)
async def root(code: CodeRequestSchema) -> AnalyzeResponseSchema:
    # LexicalAnalyzer(code.data).analyze()
    state = Analyzer(code.data).analyze()
    tw = read_out("tw")
    tl = read_out("tl")
    tn = read_out("tn")
    ti = read_out("ti")
    print(state.value)
    return AnalyzeResponseSchema(tw=tw, tl=tl, tn=tn, ti=ti, state=state.name)





