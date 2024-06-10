
from fastapi import FastAPI, Request,  Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional, Dict
from models.mx_fold2 import run_mxfold2
from models.knot_fold import run_knotfold
from pathlib import Path
import pickle
import uuid
import os

from models.rnastructure_fold import run_rnastructure_fold

# Creating cache folder:
Path("file_cache/").mkdir(parents=True, exist_ok=True)
# Creating results folder:
Path("results/").mkdir(parents=True, exist_ok=True)


def parse_fasta(fasta_block:str)->Dict[str, str]:
    sqs = {}
    seq_input = fasta_block.split(">")[1:]
    for elt in seq_input:
        fasta=elt.strip().split("\n")
        if len(fasta)>2:
            temp = ""
            for i in range(1, len(fasta)):
                temp+=fasta[i].strip()
        else:
            temp=fasta[1].strip()
        sqs[fasta[0].strip()]=temp
    # Cache clean fasta file, for models:
    with open("file_cache/cache.fasta", "w") as f:
        for key in sqs.keys():
            f.write(">"+key+"\n") # Header
            f.write(sqs[key]+"\n") # Sequence
    return sqs


def generate_unique_id():
    unique_id = uuid.uuid4()
    return f"{unique_id}"


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        name="home.html", request=request)


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request,
                  seq_input:Optional[str]=Form(None),
                  fasta_file:Optional[UploadFile]=File(...),
                  MXFold2:Optional[bool]=Form(False),
                  KnotFold:Optional[bool]=Form(False),
                  RNAstructure:Optional[bool]=Form(False),
                  Model_4:Optional[bool]=Form(False)
                  ):

    if fasta_file.file and fasta_file.filename:
        file_content = await fasta_file.read()
        file_content = file_content.decode("utf-8")
        parse_fasta(file_content)
    else:
        parse_fasta(seq_input)
    

    res = {}
    if MXFold2:
        mx_fold_res = run_mxfold2("file_cache/cache.fasta")
        # Parsing results:
        mx_fold_res = mx_fold_res.stdout.split(">")[1:]
        temp_dict={}
        for elt in mx_fold_res:
            content = elt.split("\n")
            temp_dict[content[0]] = (content[1].strip(), content[2].split()[0].strip())
        res["MXFold2"] = temp_dict

    if KnotFold:
        knot_fold_res = run_knotfold("file_cache/cache.fasta")
        res["KnotFold"]=knot_fold_res

    if RNAstructure:
        rnastructure_res = run_rnastructure_fold("file_cache/cache.fasta")
        res["RNAstructure"]=rnastructure_res

    if Model_4:
        #model4_res =
        #res["model4"]=model4_res
        ...
    
    # There should be dropped results id to make unique res files.
    ID = generate_unique_id()
    # Saving user results:
    with open(f"results/{ID}.pkl", "wb") as file:
        pickle.dump(res, file)
    
    # After predictions are done, delete cached fasta files:
    os.remove("file_cache/cache.fasta")
    
    #Initial header to plot results:
    headers = list(res[list(res.keys())[0]].keys())
    header = headers[0]
    return RedirectResponse(url=f'/results/{ID}/{header}', status_code=303)


@app.get("/results/{ID}/{header}", response_class=HTMLResponse)
def results(request: Request, ID: str, header: str):
    with open(f"results/{ID}.pkl", "rb") as file:
        res = pickle.load(file)
        headers = list(res[list(res.keys())[0]].keys())
    to_send={}
    for method in res.keys():
        to_send[method]=res[method][header]
    return templates.TemplateResponse(
        name="results.html", request=request, context={"res_dict":to_send, "ID":ID, "header":header, "headers":headers})

