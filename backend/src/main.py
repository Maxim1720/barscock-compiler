from fastapi import FastAPI, Response
from fastapi import Request
from starlette.responses import JSONResponse

from .analyzer.syntax.syntax_analyzer import SyntaxAnalyzer
from .analyzer.syntax.tools import lex_table_from_file
from .analyzer.lexical.lexical_analyzer import Analyzer
from .conf import get_global_config
from .files import read_out, flush_out
from .schema import CodeRequestSchema, AnalyzeResponseSchema

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.exception_handler(TypeError)
async def type_error_handler(request: Request, exc: TypeError):
    return (JSONResponse(
        status_code=400,
        content={
            "error": "type",
            "message": str(exc)
        }
    ))


@app.exception_handler(SyntaxError)
async def value_error_handler(request: Request, exc: SyntaxError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "syntax",
            "message": str(exc)
        }
    )


config = get_global_config()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или можно указать конкретный домен, например "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/lexical", response_model=AnalyzeResponseSchema, status_code=200)
async def lexical(code: CodeRequestSchema) -> AnalyzeResponseSchema:
    flush_out()
    state = Analyzer(code.data).analyze()
    tw = read_out("tw")
    tl = read_out("tl")
    tn = read_out("tn")
    ti = read_out("ti")
    print(state)
    return AnalyzeResponseSchema(tw=tw, tl=tl, tn=tn, ti=ti, state=state.name)


@app.post("/syntax", status_code=200)
async def syntax():
    SyntaxAnalyzer(lex_table_from_file()).analyze()
    return JSONResponse(status_code=200, content={
        "message": "Syntax analyzer successfully finished"
    })
