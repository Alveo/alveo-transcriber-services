from application.auth.required import auth_required
from application.misc.event_router import EventRouter

class UserstoreListAPI(EventRouter):
    def get(self):
        return self.event("userstore_list").handle()

userstore_list_api = auth_required(UserstoreListAPI.as_view('userstore_list_api'))
