from fastapi import FastAPI, HTTPException, Request
from gitlab_client import GitlabClient
from ai_analyzer import AIAnalyzer
import os

app = FastAPI(title="GitLab MR Review API")

GITLAB_URL = "https://gitlab.com/api/v4"
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
PROJECTS = [{"id": os.environ.get("GITLAB_PROJECT_ID", ""), "name": "Mr Review Bot Poc"}]

gitlab_client = GitlabClient(GITLAB_URL, GITLAB_TOKEN)
ai_analyzer = AIAnalyzer(OPENAI_API_KEY)


def analyze_all_projects():
    for project in PROJECTS:
        project_id = project["id"]
        mrs = gitlab_client.get_open_mrs(project_id)
        for mr in mrs:
            mr_iid = mr["iid"]
            # MR 세부 정보 및 Diff 가져오기
            mr_data, mr_diff = gitlab_client.get_mr_details(project_id, mr_iid)
            # AI 분석 수행
            analysis = ai_analyzer.analyze_mr(mr_data, mr_diff)
            # GitLab Discussion(코멘트) 남기기
            gitlab_client.post_mr_note(project_id, mr_iid, analysis)


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/webhook")
async def gitlab_webhook(request: Request):
    event = await request.json()
    if event.get("object_kind") == "merge_request":
        attr = event["object_attributes"]
        if attr.get("state") == "opened":  # 필요시 'reopened', 'update' 등도 추가
            project_id = event["project"]["id"]
            mr_iid = attr["iid"]
            # 여기서 직접 분석 및 리뷰 코멘트 등록 로직 호출
            mr_data, mr_diff = gitlab_client.get_mr_details(project_id, mr_iid)
            analysis = ai_analyzer.analyze_mr(mr_data, mr_diff)
            comment_body = analysis  # 마크다운 전체
            gitlab_client.post_mr_note(project_id, mr_iid, comment_body)
    return {"result": "ok"}


if __name__ == "__main__":
    analyze_all_projects()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
