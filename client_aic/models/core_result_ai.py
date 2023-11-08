import logging
import client_aic.ppj as ppj


log = logging.getLogger(__name__)


class CoreResultAI:
    """## CoreResultAI"""

    def __init__(
        self,
        id: int = None,
        user_id: int = None,
        job_id: int = None,
        worker_id: int = None,
        state: int = None,
        question: str = None,
        answer: str = None,
        model_name: str = None,
        score: float = None,
        question_score: str = None,
        answer_score: str = None,
        match_source: str = None,
        match_page: int = None,
        match_content: str = None,
        summarized_question: str = None,
        summarized_answer: str = None,
        summarized_score: float = None,
        reviewed_answer: str = None,
        reviewed_score: float = None,
        reviewed_computed_score: float = None,
        reviewed_notes: str = None,
        collection: str = None,
        collection_notes: str = None,
        session_id: str = None,
        derived_session_id: str = None,
        embed_model_name: str = None,
        category: str = None,
        tags: str = None,
        latency: float = None,
        data: dict = None,
        created_at: str = None,
        updated_at: str = None,
    ):
        """
        CoreResultAI

        ai results schema that supports,
        rag with RLHF (reinforcement learning
        with human feedback), summarization review,
        reviewing rag source confidence,
        historical context using session_ids

        the rest api processes
        ai jobs and an llm agent stores the results
        an CoreResultAI record.

        this class represents the
        underlying, public api model.

        :param id: db ai_result.id primary key
        :param user_id: user id
        :param job_id: job id
        :param worker_id: llm agent worker id
        :param state: result record state
        :param question: question for the llm
        :param answer: llm's answer to the
            questions
            :param model_name: model name (usually
            one from hugging face that is
            locally-stored like **falcon-170b** vs
            **mistral-7B**)
        :param score: llm's confidence in the
            answer with values between
            **0.00** <-> **1.00**
        :param question_score: similarity
            matching score for the llm's answer
            which shows how confident the
            llm is in the question from the rag
            data sources
        :param answer_score: similarity
            matching score for the llm's answer
            which shows how confident the
            llm is in the answer from the rag
            data sources
        :param match_source: best matching
            source/file on disk
            from the most confident rag data source
        :param match_page: best matching
            page extracted
            from the most confident rag data source
        :param match_content: best matching
            content extracted
            from the most confident rag data source
        :param summarized_question: after
            running the question, the autograder
            can provide a summarized question for
            reviewing historical trends and finding
            unique write-through cache keys
            within your llm ai results
        :param summarized_answer: after
            running the question, the autograder
            can provide a summarized answer for
            reviewing historical trends and finding
            unique write-through cache keys within
            your llm ai results
        :param summarized_score: after
            running the autograder
            summarizes the question and answer
            and provides a summarization score
            based off the rag data sources. this
            is helpful for tracking how many
            unique question/answer pairs
            does this llm need to support over time.
        :param reviewed_answer: subject matter
            expert's answer for this question
        :param reviewed_score: subject matter
            expert's confidence score for their
            **reviewed_answer** (score is on
            a similarity confidence scale with values
            betweeen
            **0.00** -> **1.00**)
        :param reviewed_computed_score: after
            grading the score, the auto-grader will
            recompute the score based off the current
            rag-sources in the pgvector embeddings
            and provided the best score from those
            data sources. if there is a low score, then
            the subject matter answer in the
            **reviewed_answer** field should be
            the preferred answer over the rag source(s).
            if this score is higher then there could
            be an issue with your lora/qlora peft
            configuration that is creating an output
            issue
        :param reviewed_notes: notes added during
            the human feedback update flow
        :param collection: name of the collection
            in an embedding pgvector database
            :param collection_notes: notes for this
        collection (e.g. useful for tracking collection id
            multi-tenant rag backend source matches with a
            data source location
            **s3_loc=s3://source_bucket**)
        :param session_id: custom session id
            for tracking the conversation history
            usually a **uuid** or
            **f'{user_id}.{job_type}.{uuid}'**
        :param derived_session_id: optional child
            session from the parent **session_id**
        :param embed_model_name: embedding model name
        :param category: custom label for
            this result
        :param tags: comma-delimited list of tags
        :param latency: latency for processing the
            job
        :param data: metadata dictionary
        :param created_at: utc timestamp creation date
        :param updated_at: utc timestamp last update
        """
        self.id = id
        self.user_id = user_id
        self.job_id = job_id
        self.worker_id = worker_id
        self.state = state
        self.question = question
        self.answer = answer
        self.model_name = model_name
        self.score = score
        self.question_score = question_score
        self.answer_score = answer_score
        self.match_source = match_source
        self.match_page = match_page
        self.match_content = match_content
        self.summarized_question = summarized_question
        self.summarized_answer = summarized_answer
        self.summarized_score = summarized_score
        self.reviewed_answer = reviewed_answer
        self.reviewed_score = reviewed_score
        self.reviewed_computed_score = (
            reviewed_computed_score
        )
        self.reviewed_notes = reviewed_notes
        self.collection = collection
        self.collection_notes = collection_notes
        self.session_id = session_id
        self.derived_session_id = derived_session_id
        self.embed_model_name = embed_model_name
        self.category = category
        self.tags = tags
        self.latency = latency
        self.data = data
        self.created_at = created_at
        self.updated_at = updated_at

    def load_response_dict(
        self,
        rec_dict,
    ):
        self.sql_query = rec_dict.get("sql_query", None)
        self.msg = rec_dict.get("msg", None)
        self.recs = []
        for rec in rec_dict.get("recs", []):
            self.add_rec(rec)
        self.id = rec_dict.get("id", None)
        self.user_id = rec_dict.get("user_id", None)
        self.job_id = rec_dict.get("job_id", None)
        self.worker_id = rec_dict.get("worker_id", None)
        self.state = rec_dict.get("state", None)
        self.question = rec_dict.get("question", None)
        self.answer = rec_dict.get("answer", None)
        self.model_name = rec_dict.get("model_name", None)
        self.score = rec_dict.get("score", None)
        self.question_score = rec_dict.get(
            "question_score", None
        )
        self.answer_score = rec_dict.get(
            "answer_score", None
        )
        self.match_source = rec_dict.get(
            "match_source", None
        )
        self.match_page = rec_dict.get("match_page", None)
        self.match_content = rec_dict.get(
            "match_content", None
        )
        self.summarized_question = rec_dict.get(
            "summarized_question", None
        )
        self.summarized_answer = rec_dict.get(
            "summarized_answer", None
        )
        self.summarized_score = rec_dict.get(
            "summarized_score", None
        )
        self.reviewed_answer = rec_dict.get(
            "reviewed_answer", None
        )
        self.reviewed_score = rec_dict.get(
            "reviewed_score", None
        )
        self.reviewed_computed_score = rec_dict.get(
            "reviewed_computed_score", None
        )
        self.reviewed_notes = rec_dict.get(
            "reviewed_notes", None
        )
        self.collection = rec_dict.get("collection", None)
        self.collection_notes = rec_dict.get(
            "collection_notes", None
        )
        self.session_id = rec_dict.get("session_id", None)
        self.derived_session_id = rec_dict.get(
            "derived_session_id", None
        )
        self.embed_model_name = rec_dict.get(
            "embed_model_name", None
        )
        self.category = rec_dict.get("category", None)
        self.tags = rec_dict.get("tags", None)
        self.latency = rec_dict.get("latency", None)
        self.data = rec_dict.get("data", None)
        self.created_at = rec_dict.get("created_at", None)
        self.updated_at = rec_dict.get("updated_at", None)

    def get_dict(self):
        """
        get_dict

        build a dictionary for the object and return
        the dictionary

        :returns: dictionary
        :rtype: dict
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "job_id": self.job_id,
            "worker_id": self.worker_id,
            "state": self.state,
            "question": self.question,
            "answer": self.answer,
            "model_name": self.model_name,
            "score": self.score,
            "question_score": self.question_score,
            "answer_score": self.answer_score,
            "match_source": self.match_source,
            "match_page": self.match_page,
            "match_content": self.match_content,
            "summarized_question": self.summarized_question,
            "summarized_answer": self.summarized_answer,
            "summarized_score": self.summarized_score,
            "reviewed_answer": self.reviewed_answer,
            "reviewed_score": self.reviewed_score,
            "reviewed_computed_score": self.reviewed_computed_score,
            "reviewed_notes": self.reviewed_notes,
            "collection": self.collection,
            "collection_notes": self.collection_notes,
            "session_id": self.session_id,
            "derived_session_id": self.derived_session_id,
            "embed_model_name": self.embed_model_name,
            "category": self.category,
            "latency": self.latency,
            "tags": self.tags,
            "data": self.data,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def show(self):
        """
        show

        pretty-print as a
        dictionary to the log
        """
        log.info(
            f"CoreResultAI.id={self.id} values:\n"
            f"{ppj.ppj(self.get_dict())}"
        )
