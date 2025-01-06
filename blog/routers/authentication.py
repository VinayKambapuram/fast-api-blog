from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, models
from ..database import SessionDep
from ..hashing import Hash
from ..auth_token import create_access_token

router = APIRouter(tags=['authentication'])


@router.post('/login')
def login(db : SessionDep, request:OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                            detail=f'Invalid Credentilas'
                            )
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                            detail=f'Incorrect Password'
                            )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token":access_token, "token_type":"bearer"}