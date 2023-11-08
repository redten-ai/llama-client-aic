import client_aic.models.core_result_ai as core_result_ai


class CoreSearchResultAI:
    """## CoreSearchResultAI"""

    def __init__(
        self,
        query: str = None,
        sql_query: str = None,
        recs: list = None,
        msg: str = None,
    ):
        """
        __init__

        search api object
        that contains all matching
        **CoreResultAI** records in the
        **self.recs** member variable

        :param query: logical name of the
            type of query to run (not
            a sql query from the frontend)
            :param sql_query: str: debugging
            value for tracking the sql
            statement(s) that were used
            to find these matching record(s)
        :param recs:
            of matching records for
            the rest api search
        :param msg: debugging message
            from the rest api
        """
        self.query = query
        self.sql_query = sql_query
        self.recs = recs
        self.msg = msg

    def load_response_dict(
        self,
        rec_dict,
    ):
        """
        load_response_dict

        load a rest api response
        into a **CoreSearchResultAI** object

        :param rec_dict dict: response
            dictionary from the rest api
        """
        self.sql_query = rec_dict.get("sql_query", None)
        self.msg = rec_dict.get("msg", None)
        self.recs = []
        for rec in rec_dict.get("recs", []):
            self.add_rec(rec)

    def add_rec(
        self,
        rec_dict,
    ):
        """
        add_rec

        helper for creating **CoreResultAI** records
        from the rest api dictionary

        :param rec_dict dict: values for this
            matching **CoreResultAI** record
            from the ai reinforcement learning
            database
        """
        cur_o = core_result_ai.CoreResultAI(
            id=rec_dict.get("id", None),
            user_id=rec_dict.get("user_id", None),
            job_id=rec_dict.get("job_id", None),
            worker_id=rec_dict.get("worker_id", None),
            state=rec_dict.get("state", None),
            question=rec_dict.get("question", None),
            answer=rec_dict.get("answer", None),
            model_name=rec_dict.get("model_name", None),
            score=rec_dict.get("score", None),
            question_score=rec_dict.get(
                "question_score", None
            ),
            answer_score=rec_dict.get("answer_score", None),
            match_source=rec_dict.get("match_source", None),
            match_page=rec_dict.get("match_page", None),
            match_content=rec_dict.get(
                "match_content", None
            ),
            summarized_question=rec_dict.get(
                "summarized_question", None
            ),
            summarized_answer=rec_dict.get(
                "summarized_answer", None
            ),
            summarized_score=rec_dict.get(
                "summarized_score", None
            ),
            reviewed_answer=rec_dict.get(
                "reviewed_answer", None
            ),
            reviewed_score=rec_dict.get(
                "reviewed_score", None
            ),
            reviewed_computed_score=rec_dict.get(
                "reviewed_computed_score", None
            ),
            reviewed_notes=rec_dict.get(
                "reviewed_notes", None
            ),
            collection=rec_dict.get("collection", None),
            collection_notes=rec_dict.get(
                "collection_notes", None
            ),
            session_id=rec_dict.get("session_id", None),
            derived_session_id=rec_dict.get(
                "derived_session_id", None
            ),
            category=rec_dict.get("category", None),
            tags=rec_dict.get("tags", None),
            latency=rec_dict.get("latency", None),
            data=rec_dict.get("data", None),
            created_at=rec_dict.get("created_at", None),
            updated_at=rec_dict.get("updated_at", None),
        )
        if not self.recs:
            self.recs = [cur_o]
        else:
            self.recs.append(cur_o)

    def get_dict(self):
        """
        get_dict

        return a dictionary for this object

        :returns: dictionary
        :rtype: dict
        """
        res = {
            "query": self.query,
            "sql_query": self.sql_query,
            "msg": self.msg,
            "recs": self.recs,
        }
        return res
