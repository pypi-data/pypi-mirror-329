class AthenaConnection(object):
    def __init__(self, connection_name: str, connection_id: str, work_group: str, region: str):
        self.connection_name = connection_name
        self.connection_id = connection_id
        self.work_group = work_group
        self.region = region