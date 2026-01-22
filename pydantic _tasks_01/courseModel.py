from pydantic import BaseModel,Field

class Course(BaseModel):
    course_id:int
    course_name:str
    credits:int=Field(ge=1,le=6)
    
    
try:
    course=Course(credits=4,course_name="Human Psychology",course_id=1233)
    print(course)
except Exception as e:
    print(f"Error while creating course : {e}")
