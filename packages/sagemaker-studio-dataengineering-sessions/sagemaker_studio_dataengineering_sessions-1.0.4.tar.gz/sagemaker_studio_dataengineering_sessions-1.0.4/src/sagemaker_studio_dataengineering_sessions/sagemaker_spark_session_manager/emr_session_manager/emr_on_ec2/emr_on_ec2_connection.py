import enum


class EmrOnEc2Connection(object):
    def __init__(self,
                 connection_name: str,
                 connection_id: str,
                 cluster_id: str,
                 runtime_role_arn: str,
                 trusted_certificates_s3_uri: str,
                 url: str,
                 governance_type: enum):
        self.connection_name = connection_name
        self.connection_id = connection_id
        self.cluster_id = cluster_id
        self.runtime_role_arn = runtime_role_arn
        self.trusted_certificates_s3_uri = trusted_certificates_s3_uri
        self.url = url
        self.governance_type = governance_type
