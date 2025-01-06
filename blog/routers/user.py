from fastapi import APIRouter, status, HTTPException, Depends
from .. import schemas, models, oauth2
from ..database import SessionDep
from ..hashing import Hash


router = APIRouter(prefix='/user',
    tags=['user'])


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: SessionDep, current_user:schemas.User=Depends(oauth2.get_current_user)):
    new_user = models.User(name = request.name, email = request.email, 
                           password = Hash.encrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id : int, db:SessionDep, current_user:schemas.User=Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with {id} is not available')
    
    return user