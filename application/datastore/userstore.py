from application.auth.required import auth_required
from application.misc.event_router import EventRouter

class UserstoreAPI(EventRouter):
    def get(self):
        return self.event("userstore_archive").handle()

userstore_api = auth_required(UserstoreAPI.as_view('userstore_api'))
