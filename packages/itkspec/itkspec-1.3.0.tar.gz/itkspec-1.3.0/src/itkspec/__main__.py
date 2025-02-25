import os
import itkdb
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from .ReadSpec import getSpec, getSpecList

app = FastAPI()

# Model for the input of parameters
class SpecDataInput(BaseModel):
    accessCode1: str = Field(default=None,examples=["my_access_code1"])
    accessCode2: str = Field(default=None,examples=["my_access_code2"])
    project: str = Field(default=None,examples=["P"])
    componentType: str = Field(default=None,examples=["PCB"])
    testType: str = Field(default=None,examples=["METROLOGY"])
    stage: str = Field(default=None,examples=["PCB_RECEPTION"])
    parameter: Optional[str] = Field(default=None,examples=["BOW1"])

# Model for the output of parameters
class SpecDataOutput(BaseModel):
    project: Optional[str] = None
    componentType: Optional[str] = None
    testType: Optional[str] = None
    stage: Optional[str] = None
    parameter: List[str] = None
    specList: Dict[str, Dict[str, Any]] = None
    

#################
### ENDPOINTS ###
#################

### Redirect to swagger
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

### Single specification retrieval
@app.post("/spec")
async def specRetrieval(kwargs: SpecDataInput):
    kwargs_dict=kwargs.model_dump()

    # auth
    user = itkdb.core.User(access_code1=kwargs_dict["accessCode1"], access_code2=kwargs_dict["accessCode2"])
    try:
        user.authenticate()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    # function
    query = getSpec(**kwargs_dict)

    # output structure
    output = SpecDataOutput(
        project=kwargs_dict["project"],
        componentType=kwargs_dict["componentType"],
        testType=kwargs_dict["testType"],
        stage=kwargs_dict["stage"],
        parameter=[query["parameter"]],
        specList={query["parameter"]:query["spec"]}
    )

    return output


### Multiple specifications retrieval
@app.post("/speclist")
async def specListRetrieval(kwargs: SpecDataInput):
    kwargs_dict=kwargs.model_dump()

    # auth
    user = itkdb.core.User(access_code1=kwargs_dict["accessCode1"], access_code2=kwargs_dict["accessCode2"])
    try:
        user.authenticate()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    # function
    query = getSpecList(**kwargs_dict)

    # output structure
    output = SpecDataOutput(
        project=kwargs_dict["project"],
        componentType=kwargs_dict["componentType"],
        testType=kwargs_dict["testType"],
        stage=kwargs_dict["stage"],
        parameter=query["parameter"],
        specList={x : y | {"associatedParam": []} for x, y in zip(query["parameter"], query["spec"])}
    )
    return output


# Example endpoint to read modules
@app.get("/modules")
def read_modules():
    csv_folder_path = "/spec_files"

    if not os.path.exists(csv_folder_path):
        raise HTTPException(status_code=404, detail="CSV files not found")
    try:
        df = pd.read_csv(csv_folder_path)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example endpoint to read a specific module by ID
@app.get("/modules/{module_id}")
def read_module(module_id: int):
    # treating the module id input
    if module_id[-4:] != ".csv":
        module_id = module_id + ".csv"

    # csv file path if the working directory is the root of the project
    csv_file_path = f"/spec_files/{module_id}"

    if not os.path.exists(csv_file_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    try:
        df = pd.read_csv(csv_file_path)
        if module_id >= len(df) or module_id < 0:
            raise HTTPException(status_code=404, detail="Module ID not found")
        return df.iloc[module_id].to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/help")
def help():
    return {
        "message": "Welcome to itk-spec",
        "endpoints": {
            "/spec": {
                "method": "GET",
                "description": "Get specification for a single parameter",
                "parameters": {
                    "project": "Project name",
                    "componentType": "Component type",
                    "testType": "Test type",
                    "stage": "Stage",
                    "parameter": "Parameter"
                }
            },
            "/speclist": {
                "method": "GET",
                "description": "Get specifications for multiple parameters",
                "parameters": {
                    "project": "Project name",
                    "componentType": "Component type",
                    "testType": "Test type",
                    "stage": "Stage",
                }
            },
            "/modules": {
                "method": "GET",
                "description": "Get all modules"
            },
            "/modules/{module_id}": {
                "method": "GET",
                "description": "Get a specific module by ID"
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")