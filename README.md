# GitLab MR LLM PoC

이 프로젝트는 GitLab Merge Request(병합 요청)를 분석하고, OpenAI를 활용하여 시니어 개발자 수준의 리뷰 코멘트를 생성한 뒤, 그 결과를 Gitlab MR Discussion에 업로드합니다. REST API를 통해 프로젝트, MR, 분석 결과를 조회할 수 있습니다.


설치 방법
필수 패키지 설치:
```
pip install -r requirements.txt
```

* 참고: https://github.com/sercancelenk/ai-mr-review
