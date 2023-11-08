#!/usr/bin/env python3

import client_aic.ask as ask


# if your user does not exist it will be created
username = "publicdemos100"
email = "publicdemos100@redten.io"
password = "789987"
collection_id = "embed-security"
question = 'using std::namespace; int main() { std::cout << "hello" << std::endl; return 256;}'
wait_for_result = False
# ask the llm the question and let the
# llm use the collection_id embeddings to perform rag
# before responding
print("asking question")
(user, res_job, res_ai) = ask.ask(
    question=question,
    collection_id=collection_id,
    username=username,
    email=email,
    password=password,
    wait_for_result=wait_for_result,
)
if not user:
    print(f"failed to find user with email={email}")
elif not res_job:
    print("failed to find job result")
elif wait_for_result:
    if res_ai:
        print(
            f"{email} - job_id={res_job.job_id} "
            "result:\n"
            f"question: {question}\n"
            f"answer: {res_ai.answer}\n"
            f"score: {res_ai.score}"
        )
    else:
        print(
            "failed to get ai result for "
            f"job_id={res_job.job_id}"
        )
else:
    print(
        "did not wait for "
        f"user_id={user.id} "
        f"job={res_job.job_id} "
        "ai result "
        "please use:\n\n"
        f"get-ai-result.py -i {res_job.job_id}"
        "\n"
    )
