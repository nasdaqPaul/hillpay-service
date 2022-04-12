from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.accounts import account_routes
from .routers.bills import bills_router
from .routers.members import member_routes
from .routers.payment_requests import payment_requests_router
from .routers.services import services_router
from .routers.session import session_routes
from .ws import ws_router

api = FastAPI(title='HillPay API', version='1.0')
# scheduler = BackgroundScheduler()
#
#
# def simple_print():
#     print('Hello')
#
#
# scheduler.add_job(simple_print, 'interval', seconds=5)
# scheduler.start()

api.include_router(member_routes)
api.include_router(session_routes)
api.include_router(account_routes)
api.include_router(services_router)
api.include_router(bills_router)
api.include_router(payment_requests_router)
api.include_router(ws_router)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True
)
