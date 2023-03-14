from setuptools import find_packages,setup
from typing import List

HYPEN_e_dot = "-e ."

def get_requirements(file_path:str)->List[str]:
    
    '''
    From here we get the list of requirements
    '''

    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
        
        if HYPEN_e_dot in requirements:
            requirements.remove(HYPEN_e_dot)
    return requirements
    
setup(
    
    name='ProjectMl',
    version='0.0.1',
    author='Abhishek',
    author_email='chauhanabhi280@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
    )