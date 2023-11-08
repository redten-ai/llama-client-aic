class CoreJob:
    """## CoreJob"""

    def __init__(
        self,
        id: int,
        user_id: int,
        worker_id: int,
        state: int,
        status: int,
        job_type: int,
        data: dict,
        msg: str,
        created_at: str,
        updated_at: str,
    ):
        """
        __init__

        the rest api processes generalized jobs
        and this class represents the
        underlying, public api model

        all generic jobs representation
        and the **CoreJob.id** value
        is for tracking job progress and
        looking up the ai result

        :param id: job id
        :param user_id: user id
        :param worker_id: llm agent worker id
        :param state: state of the job
        :param status: job processing status
        :param job_type: type of the job
        :param data:  metadata dictionary
        :param msg: rest api debugging message
        :param created_at: utc timestamp creation date
        :param updated_at: utc timestamp last update
        """
        self.id = id
        self.user_id = user_id
        self.worker_id = worker_id
        self.state = state
        self.status = status
        self.job_type = job_type
        self.data = data
        self.msg = msg
        self.created_at = created_at
        self.updated_at = updated_at
