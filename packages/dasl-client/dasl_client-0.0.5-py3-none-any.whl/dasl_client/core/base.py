from dasl_client.auth.auth import Authorization


class BaseMixin:
    def __init__(self, auth: Authorization, **kwargs):
        try:
            super().__init__(auth=auth, **kwargs)
        except TypeError:
            super().__init__()  # If this is last mixin, super() will be object()
        self.auth = auth
