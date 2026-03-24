#server_project
#handle: _MUMINUL__ISLAM___


#code
from redis import Redis
import json
from database import info
from fastapi import HTTPException

redis_conection=Redis(host='10.185.100.136',port=6379,db=0,decode_responses=True,socket_keepalive=True, retry_on_timeout=True)
redis_connection=Redis(host='10.185.100.136',port=6379,db=1,decode_responses=True,socket_keepalive=True, retry_on_timeout=True)


def GetCache(customerID,db):
    cached= redis_conection.get(customerID)
    if cached:
        print("from redis")
        return json.loads(cached) # type: ignore
    else:
        print("from database")
        row=db.query(info).filter(customerID==customerID).first()
        if row:
            customer_row={
                    "customerID":row.customerID,
                    "orderID":row.orderID,
                    "orderPrice":row.orderPrice
            }
            redis_conection.set(customerID,json.dumps(customer_row),ex=60)
            return customer_row
        return None
    
    
def rateLimit(cusotmerID):

    LIMIT=2
    WINDOW=30

    print("from limit")

    current_rate= int(redis_connection.incr(cusotmerID)) # type: ignore
    if current_rate==1:
        print("1st time in limit")
        redis_connection.expire(cusotmerID,WINDOW)

    elif current_rate>=LIMIT:
        print("limit crossed")
        raise HTTPException(400,"Limit Crossed")
    
    return True