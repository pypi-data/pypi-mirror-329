### imports
import os.path
import os
import pandas as pd
from ast import literal_eval
#from typing import Optional, List, Dict, Any

### template info. for user input
infoDict_template={'project':None, 'componentType':None, 'testType':None, 'stage':None, 'parameter':None}
## copy function - for use in functions
def copyTemplate():
    return infoDict_template.copy()

### process user information
'''
def GetSpecInfo(**kwargs):
    print("Get spec info")
    infoDict=copyTemplate()
    ## pick up arguments
    print("get inputs")
    for k in infoDict.keys():
        try:
            infoDict[k]=kwargs[ [x for x in kwargs.keys() if k in x.lower()][0] ]
            print(f" - found {k}")
        except IndexError:
            pass
    ## check necessaries
    print("check inputs")
    stuffCheck=True
    for k,v in infoDict.items():
        if v==None:
            print(f" - missing {k} information")
            stuffCheck=False
    if stuffCheck==False:
        print("returning nothing :(")
        return None
    ## return info
    return infoDict
'''

### Function for returning a single spec from a unique parameter
def getSpec(**kwargs):
    inCheck = True
    core_keys = ['project', 'componentType', 'testType', 'stage', 'parameter']

    # Check for missing core labels
    if any(kwargs.get(label) is None for label in core_keys):
        print(" there's a core label missing. Please check inputs.")
        inCheck = False

    # Determine the file name
    fileName = "_".join([kwargs['project'], kwargs['componentType']]) + ".csv"

    # Check if the file exists
    if fileName is not None:
        # Get root directory
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the spec_files directory
        spec_files_directory = os.path.join(current_directory, "spec_files")
        print(f"  csv files directory: {spec_files_directory}")

        # Construct the full path to the file
        file_path = os.path.join(spec_files_directory, fileName)
        try:
            os.path.isfile(file_path)
            print(f"  file path: {file_path}\n")
        except FileNotFoundError:
            print("Error: This specification file does not exist yet or inputs are incorrect.")
            inCheck = False

    if not inCheck:
        print("returning nothing :(")
        return pd.DataFrame()

    # Open the file and get spec data
    print("# getting spec from csv #\n")
    df_csv = pd.read_csv(file_path, converters={"spec": literal_eval})

    queryStr=f'project==\"{kwargs["project"]}\" & componentType==\"{kwargs["componentType"]}\" & parameter==\"{kwargs["parameter"]}\"'
    print(f"query spec using: \n{queryStr}\n")

    df_spec=df_csv.query(queryStr)

    if df_spec.empty:
        print(" - empty spec csv :(.")
        return pd.DataFrame()
    else:
        spec_dict = df_spec.to_dict()
        out_dict = {
            'parameter': spec_dict['parameter'][0],
            'spec': spec_dict['spec'][0]
        }
        print(df_spec.to_markdown())
    return out_dict

### Function for returning multiple specs from various parameters
def getSpecList(**kwargs):
    inCheck = True
    core_keys = ['project', 'componentType', 'testType', 'stage']

    # Check for missing core labels
    if any(kwargs.get(label) is None for label in core_keys):
        print(" there's a core label missing. Please check inputs.")
        inCheck = False

    # Determine the file name
    fileName = "_".join([kwargs['project'], kwargs['componentType']]) + ".csv"

    # Check if the file exists
    if fileName is not None:
        # Get the main directory
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the spec_files directory
        spec_files_directory = os.path.join(current_directory, "spec_files")
        print(f"  csv files directory: {spec_files_directory}")

        # Construct the full path to the file
        file_path = os.path.join(spec_files_directory, fileName)
        try:
            os.path.isfile(file_path)
            print(f"  file path: {file_path}")
        except FileNotFoundError:
            print("Error: This specification file does not exist yet or inputs are incorrect.")
            inCheck = False

    if not inCheck:
        print("returning nothing :(")
        return pd.DataFrame()

    # Open the file and get spec data
    print("# getting spec from csv #\n")
    df_csv = pd.read_csv(file_path, converters={"spec": literal_eval})

    queryStr=f'project==\"{kwargs["project"]}\" & componentType==\"{kwargs["componentType"]}\"'
    print(f"query spec using: \n{queryStr}\n")
    
    df_spec=df_csv.query(queryStr)

    if df_spec.empty:
        print(" - empty spec csv :(.")
        return pd.DataFrame()
    else:
        spec_dict = df_spec.to_dict()
        out_dict = {
            'parameter': list(spec_dict['parameter'].values()),
            'spec': list(spec_dict['spec'].values())
        }
        print(df_spec.to_markdown())
        print(out_dict)
    return out_dict
'''
def GetParam(**kwargs):
    print("Get spec data")
    infoKeys = copyTemplate().keys()
    print("check inputs")
    inCheck = True

    # Check if all required keys are present
    if set(infoKeys).issubset(kwargs.keys()):
        # Check if any value is None
        if None in kwargs.values():
            print(" - something is None. Please check inputs.")
            inCheck = False
        else:
            print(" - got all info.")
    else:
        print(" - something is missing. Please check inputs.")
        inCheck = False

    # Determine the file name
    fileName = None
    try:
        fileName = kwargs[[x for x in kwargs.keys() if "file" in x.lower()][0]]
        print(f" - found file path: {fileName}")
    except IndexError:
        print(" - file is missing. Will construct from info.")
        fileName = "_".join([kwargs['project'], kwargs['componentType']]) + ".csv"

    # Check if the file exists
    if fileName is not None:
        # Get the main directory
        current_directory = 'c:\itk\itk-pdb-specifica'
        # Construct the full path to the spec_files directory
        spec_files_directory = os.path.join(current_directory, "spec_files")
        print(f" - spec_files directory: {spec_files_directory}")
        # Construct the full path to the file
        file_path = os.path.join(spec_files_directory, fileName)
        print(f" - file path: {file_path}")
        
        if os.path.isfile(file_path):
            print(" - file exists")
        else:
            print(" - file does not exist. Please check inputs.")
            inCheck = False

    if inCheck == False:
        print("returning nothing :(")
        return pd.DataFrame()

    # Open the file and get spec data
    print("get spec data from file")
    df_csv = pd.read_csv(file_path, converters={"spec": literal_eval})
    # print(df_csv.to_markdown())
    queryStr=f'project==\"{kwargs["project"]}\" & componentType==\"{kwargs["componentType"]}\"'
    print(f"query spec using: \n\t{queryStr}")
    df_para=df_csv.query(queryStr)
    if df_para.empty:
        print(" - empty spec data :(.")
        return pd.DataFrame()
    else:
        df_para=df_para.explode('spec')
        df_para=pd.json_normalize(df_para['spec'])
        print(df_para.to_markdown())
    return df_para
'''

def listSpecFiles():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    spec_files_directory = os.path.join(current_directory, "spec_files")
    
    ## get list of (csv) files in directory
    csv_list=os.listdir(spec_files_directory)
    ## filter csv files
    csv_list=[x for x in csv_list if ".csv" in x]
    
    print(f"csv files in directory: {csv_list}")
    return csv_list
'''
#def ListSpecData(**kwargs):

    dir_name='spec_files'
    # Print all keyword arguments
    df_files = listSpecFiles(dir_name)
    
    # Create a list of values that are not None
    non_none_values = [value for value in kwargs.values() if value is not None]
    print(f"Number of keyword arguments: {len(non_none_values)}")
    
    list_pos=[]

    for file in df_files:
        print(file)
        content = pd.read_csv(dir_name+'/'+file)
        print(content)
        # Check if all non-None values are present in the DataFrame
        if all(value in content.values for value in non_none_values):
            print("found:")
            print(content)
            list_pos.append([file,content])
            
    if len(list_pos)==0:
        print("No matching content found.")
    elif len(list_pos)==1:
        print("One matching content found.")
    elif len(list_pos)>1:
        print(f"{len(list_pos)} matching contents found.")

    for i in range(len(list_pos)):
        print(f"Content {i+1}:")
        print(list_pos[i][0])
        print(list_pos[i][1])
    return list_pos
'''

#getSpec(project='P', componentType='PCB', testType='METROLOGY', stage='PCB_RECEPTION', parameter='BOW1')