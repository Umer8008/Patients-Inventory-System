from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional

class patient(BaseModel):
    id:Annotated[str,Field(...,max_length=10,description='Enter ID',examples=['P001'])]
    name:Annotated[str,Field(...,max_length=120,description='Enter patient name',examples=['Faraz'])]
    city:Annotated[str,Field(...,description='City where patient is living')]
    age:Annotated[int,Field(...,gt=0,lt=120,description='Age of the patient')]
    gender:Annotated[Literal['male','female','others'],Field(...,description='Enter gender')]
    height:Annotated[float,Field(...,gt=0,description='Height of patient in meters')]
    weight:Annotated[float,Field(...,gt=0,description='Weight of the patient in kgs')]
    
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi<18.5:
            return 'Under weight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'normal'
        else:
            return 'Obese'

class update_patient(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    gender:Annotated[Optional[Literal['male','female','others']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]
    
    
    


    
    
def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
        
    return data    

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)


app=FastAPI()
@app.get("/")
def hello():
    return{'message':'Patient management system!!!'}


@app.get('/about')
def about():
    return{'message':'A fully functional API to manage your patient records '} 

@app.get('/view')
def view():
    data=load_data()
    
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description='Put ID of the patient in the DB',examples='P004')):
    data=load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient Not Found!!')

@app.get('/sort')
def sort_patient(sort_by:str =Query(...,description="Sort on the Basis of height,weight or bmi"), 
order:str=Query('asc',description='sort in asc or desc order')):
    valid_fields=['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid Field Selection !! select from{valid_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order selection')
    data=load_data()
    sort_order=True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    
    return sorted_data

@app.post('/create')
def create_patient(patient: patient):
    #load existing data
    data=load_data()
    #check if same patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists with this id')
    
    #new patient added to the database
    data[patient.id]=patient.model_dump(exclude=['id'])
    
    #save into json file
    save_data(data)
    
    return JSONResponse(status_code=201,content={'message':'Patient added successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: update_patient):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail='Patient not found'
        )

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(
        exclude_unset=True
    )

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id

    # Validate updated data
    patient_pydantic_object = patient(**existing_patient_info)

    # Pydantic object → dictionary
    existing_patient_info = patient_pydantic_object.model_dump(
        exclude={'id'}
    )

    # Update data dictionary
    data[patient_id] = existing_patient_info

    # Save to JSON file
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={'message': 'Patient Updated'}
    )

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(
            status_code=404,
            detail='Patient not found'
        )

    del data[patient_id]

    save_data(data)

    return {
        'message': 'Patient deleted successfully'
    }