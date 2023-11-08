class CoreResultJob:
    """## CoreResultJob"""

    def __init__(
        self,
        id: int = None,
        job_id: int = None,
        worker_id: int = None,
        job_type: int = None,
        user_id: int = None,
        state: int = None,
        data: dict = None,
        msg: str = None,
        created_at: str = None,
        updated_at: str = None,
    ):
        """
        __init__

        result for the **CoreJob** object

        :param id: result id value
            and primary key
        :param job_id: parent job id
            and usually **CoreJob.id**
        :param worker_id: the llm agent
            that worked on this question
        :param job_type: the type of
            job the llm is processing
            qa vs generative
        :param user_id: user that asked
            the question
        :param state: processing state
            of the result
        :param data: dmetadata dictionary
            for the job
        :param msg: debugging message
            from the rest api
        :param created_at: utc timestamp
            creation date
        :param updated_at: utc timestamp
            last update
        """
        self.id = id
        self.job_id = job_id
        self.worker_id = worker_id
        self.job_type = job_type
        self.user_id = user_id
        self.state = state
        self.data = data
        self.msg = msg
        self.created_at = created_at
        self.updated_at = updated_at
