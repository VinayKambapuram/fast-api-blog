from fastapi import APIRouter, status, HTTPException, Response, Depends
from .. import schemas, models, oauth2
from ..database import SessionDep


router = APIRouter(prefix='/blog',
    tags=['blogs'])


@router.get('/', response_model=list[schemas.ShowBlog])
def get_all(db:SessionDep, current_user:schemas.User=Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db:SessionDep, current_user:schemas.User=Depends(oauth2.get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def get_blog(id, db:SessionDep, current_user:schemas.User=Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
                            detail=f'Blog with {id} is not available'
                            )
    return blog


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db:SessionDep, current_user:schemas.User=Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with {id} is not available')
    
    blog.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Blog, db:SessionDep, current_user:schemas.User=Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with {id} is not available')
    
    blog.update(request.model_dump())
    db.commit()
    return 'Updated'