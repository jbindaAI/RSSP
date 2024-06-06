
from fastapi import FastAPI, Request, Query,  Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Optional, Dict
import os


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
    return sqs


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
            RNA_Fold:Optional[bool]=Form(False),
            Model_3:Optional[bool]=Form(False),
            Model_4:Optional[bool]=Form(False)
            ):

    if fasta_file.file and fasta_file.filename:
        file_content = await fasta_file.read()
        file_content = file_content.decode("utf-8")
        sqs = parse_fasta(file_content)
    else:
        sqs = parse_fasta(seq_input)
        print(sqs)

    res = {}
    if MXFold2:
        #mx_fold_res =
        #res["mx_fold"]=[mx_fold_res]
        ...
    if RNA_Fold:
        #rna_fold_res = 
        #res["rna_fold"]=rna_fold_res
        ...
    if Model_3:
        #model3_res =
        #res["model3"]=model3_res
        ...
    if Model_4:
        #model4_res =
        #res["model4"]=model4_res
        ...
    
    # visualization
    for key in res.keys():
        res[key]


    return templates.TemplateResponse(
        name="home.html", request=request)


# @app.get("/visualize_scan/{PATIENT_ID}", response_class=HTMLResponse)
# def visualize_scan(request: Request, PATIENT_ID: str, SLC: int=Query(150)):
#     scan_pt = load_dicom_into_tensor(patient_id=PATIENT_ID)
#     max_depth = scan_pt.shape[-1]
#     scan_str = plot_scan(scan_pt=scan_pt, slc=SLC)

#     return templates.TemplateResponse(
#         name="scan_slicer.html", request=request, context={"PATIENT_IDs":PATIENT_IDs,
#                                                     "PATIENT_ID":PATIENT_ID, 
#                                                     "SLC": SLC,
#                                                     "max_depth": max_depth,
#                                                     "scan_plot": scan_str})


# @app.get("/extract_nodules/{PATIENT_ID}", response_class=HTMLResponse)
# def extract_nodules(request: Request, PATIENT_ID: str):
#     scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == f"LIDC-IDRI-{PATIENT_ID}").first()
#     nodules = scan.cluster_annotations()
#     NOD_icons_lst, NOD_crops_ref = process_nodules(nodules=nodules, PATIENT_ID=PATIENT_ID)
#     NODULES=zip(NOD_icons_lst, NOD_crops_ref)
#     # caching NODULES to retrieve later:
#     with open("cache/nodules_lst.pkl", "wb") as file:
#         pickle.dump(NODULES, file)

#     return templates.TemplateResponse(
#         name="nodules_list.html", request=request, context={"PATIENT_IDs":PATIENT_IDs,
#                                                     "NODULES": NODULES
#                                                     })


# @app.get("/list_nodules/", response_class=HTMLResponse)
# def list_nodules(request: Request):
#     with open("cache/nodules_lst.pkl", "rb") as file:
#         NODULES = pickle.load(file)
#     return templates.TemplateResponse(
#         name="nodules_list.html", request=request, context={"PATIENT_IDs":PATIENT_IDs,
#                                                     "NODULES": NODULES
#                                                     })


# @app.get("/visualize_nodule/{NOD_crop}", response_class=HTMLResponse)
# def visualize_nodule(request: Request, NOD_crop: str, SLC: int=Query(17, gt=-1, le=31)):
#     # when user decide to analyze Nodule, it deletes cached tensors of patients scans other than chosen one.
#     cached_files = os.listdir("cache/")
#     for file in cached_files:
#         if file != "crops" and file != "nodules_lst.pkl":
#             os.remove("cache/"+file)
#     # loading and visualizing nodule
#     original_img = load_img(crop_path=f"cache/crops/{NOD_crop}.pt", crop_view="axial", slice_=SLC, return_both=False, device="cpu")
#     img_str = plot_nodule(original_img)

#     # Context to return to Nodule lst:
#     with open("cache/nodules_lst.pkl", "rb") as file:
#         NODULES = pickle.load(file)

#     return templates.TemplateResponse(
#         name="nodule_slicer.html", request=request, context={"NOD_crop": NOD_crop,
#                                                              "SLC":SLC,
#                                                              "NODULES": NODULES,
#                                                              "orig_plot": img_str})


# @app.get("/predict/{NODULE}/{SLICE}", response_class=HTMLResponse)
# def predict(request: Request, NODULE: str, SLICE: int, TASK: str=Query(...)):
#     original_img, attention_map, CDAM_maps, model_output = XMED.model_pipeline(NODULE=NODULE, SLICE=SLICE, TASK=TASK)

#     if TASK == "Classification":
#         PREDS = round(model_output, 2)
#         res_str = plot_res_class(maps=[attention_map, CDAM_maps])
#         res_str_att = False
#     else:
#         PREDS = model_output
#         res_str = plot_CDAM_reg(maps=[CDAM_maps], preds=PREDS)
#         res_str_att = plot_att_reg(attention_map=attention_map)

#     img_str = plot_nodule(original_img)

#     return templates.TemplateResponse(
#         name="nodule_slicer.html", request=request, context={"NOD_crop": NODULE, 
#                                                     "SLC": SLICE, 
#                                                     "TASK": TASK,
#                                                     "PREDS": PREDS,  
#                                                     "orig_plot": img_str, 
#                                                     "res_plot": res_str,
#                                                     "reg_att_plot": res_str_att
#                                                     })




