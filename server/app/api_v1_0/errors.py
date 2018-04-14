class Error:
    @property
    def page_not_found(self):
        return {'error': 'page not found'}

    @property
    def internal_server_error(Self):
        return {'error': 'internal server error'}