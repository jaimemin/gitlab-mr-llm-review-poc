import json

from openai import OpenAI

class AIAnalyzer:
    def __init__(self, api_key: str):
        print("OPEN AI : ", api_key)
        self.client = OpenAI(api_key=api_key)

    def analyze_mr(self, mr_data, mr_diff):
        diff_text = "\n".join([diff["diff"] for diff in mr_diff])
        prompt = (
            f"시니어 소프트웨어 개발자로서 아래의 GitLab Merge Request를 리뷰해 주세요:\n"
            f"MR 제목: {mr_data['title']}\n"
            f"설명: {mr_data['description']}\n"
            f"코드 변경사항:\n```diff\n{diff_text}\n```\n"
            f"성능, 가독성, 오류 가능성, 설계 측면에서 상세히 평가해 주세요.\n"
            f"출력은 아래의 마크다운 형식을 그대로 따라주세요:\n"
            "## :clipboard: 코드 리뷰 결과\n\n"
            "### :bookmark_tabs: 요약\n"
            "- (전체 리뷰 요약)\n\n"
            "---\n\n"
            "### :sparkles: 잘된 점\n"
            "- (좋은 점 1)\n"
            "- (좋은 점 2)\n\n"
            "---\n\n"
            "### :bulb: 개선이 필요한 점\n"
            "- (개선 제안 1)\n"
            "- (개선 제안 2)\n\n"
            "---\n\n"
            "### :mag: 세부 평가\n"
            "- **성능:**  (성능 관련 평가)\n"
            "- **가독성:**  (가독성 관련 평가)\n"
            "- **오류 가능성:**  (오류 가능성 평가)\n"
            "- **설계:**  (설계 관련 평가)\n"
        )

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 코드 분석을 전문으로 하는 시니어 소프트웨어 개발자입니다.",
                },
                {"role": "user", "content": prompt},
            ],
        )

        analysis_markdown = response.choices[0].message.content.strip()
        return analysis_markdown
