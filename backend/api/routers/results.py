from fastapi import APIRouter
import redis
import json

r = redis.Redis(host="redis", port=6379, db=0)

router = APIRouter()


@router.get("/results/{request_id}")
async def get_result(request_id: str):
    val = r.get(request_id)
    if val:
        try:
            return {"result": json.loads(val)}
        except Exception:
            return {"result": None, "status": "decode_error"}
    return {"result": None, "status": "processing"}
