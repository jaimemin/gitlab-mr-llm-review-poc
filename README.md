# GitLab MR LLM PoC
---
<h4>본 프로젝트는 GitLab Merge Request(병합 요청)를 분석하고, OpenAI를 활용하여 시니어 개발자 수준의 리뷰 코멘트를 생성한 뒤, 그 결과를 GitLab MR Discussion에 업로드합니다.</h4>

## 설치 방법

필수 패키지 설치:
```bash
pip install -r requirements.txt
```
---
## 시퀀스 다이어그램

<img width="703" alt="image" src="https://github.com/user-attachments/assets/1b9215b3-5664-4454-b691-7734bd318a0c" />

---
## Koyeb 배포 및 환경변수 설정 안내

PoC 검증을 위해 [Koyeb](https://www.koyeb.com/)에 무료 인스턴스로 배포하여 검증했습니다.
배포 시 **아래와 같은 환경변수(Environment Variables) 세팅이 필수**입니다.

```python
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
PROJECTS = [{
    "id": os.environ.get("GITLAB_PROJECT_ID", ""),
    "name": "Mr Review Bot Poc"
}]
```

app.py 내 환경변수를 확인할 수 있습니다.
* GITLAB_TOKEN: GitLab Personal Access Token (READ API 권한 포함)
* OPENAI_API_KEY: OpenAI API 사용을 위한 키
* GITLAB_PROJECT_ID: 리뷰를 적용할 GitLab 프로젝트의 numeric ID

Koyeb 대시보드에서
**App > Settings > Environment Variables**
항목에 위 3개의 환경변수를 등록해야 애플리케이션이 정상 동작합니다.
