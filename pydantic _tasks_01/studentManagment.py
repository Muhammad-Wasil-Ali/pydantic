from pydantic import BaseModel,Field,EmailStr
from enum import Enum
from typing import List

class Grade(str,Enum):
    
    A="A"
    B="B"
    C="C"
    D="D"
    

class Student(BaseModel):
    id:str=Field(strict=True)
    name:str=Field(min_length=5,max_length=50)
    age:int=Field(ge=1,le=80)
    email:EmailStr
    grade:Grade
    isactive:bool=Field(default=True,strict=True)
    
    
class Course(BaseModel):
    course_id:int
    course_name:str
    credits:int=Field(ge=1,le=6)
    


class Enrollment(BaseModel):
    student:Student
    courses:List[Course]
    enrollment_date:str
    
    
    
print("="*20)
print("Creating 2 students")

std1=Student(name="alpha",email="alpha@gmail.com",age=22,grade="B",isactive=True,id="123132")

std2=Student(name="bravo",email="bravo@gmail.com",age=23,grade="A",isactive=False,id="1283945")

print("="*20)
print("Creating 3 courses")

course1=Course(course_id="123132",course_name="i repeat",credits=3)

course2=Course(course_id="920342",course_name="target_Locked",credits=4)


enrollment1 = Enrollment(
    student=std1,
    courses=[course1, course2],
    enrollment_date="2024-01-15"
)

enrollment2 = Enrollment(
    student=std2,
    courses=[course1,course2],
    enrollment_date="2024-01-16"
)

print(enrollment1)