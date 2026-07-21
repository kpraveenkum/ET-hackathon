from fastapi import APIRouter, UploadFile, File, HTTPException

from rag.ingestion import process_uploaded_file


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_document(
    file: UploadFile = File(...)
):

    try:

        result = process_uploaded_file(file)

        return result


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )