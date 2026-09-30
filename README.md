# Portfolio Automation Device README

리추얼 기록, 과제 목록, 대표작 데이터를 반영하여 포트폴리오 내용을 자동으로 갱신하는 장치입니다.

## 🚀 돌리는 방법 (3단계)

1. **1단계 (파일 준비):** 
    동일한 폴더에 아래 파일을 둡니다.
   - `update_portfolio.py` (스크립트 파일)
    - `index.html` (포트폴리오 HTML)
  - `ritual.json` (리추얼 기록 파일)
   - `assignments.json` (과제 목록 파일)
    - `projects.json` (대표작 목록 파일)

2. **2단계 (자동 갱신 실행):** 
    터미널(Terminal 또는 CMD)을 열고 해당 폴더로 이동한 뒤 아래 명령어를 실행합니다. 실행해 두면 JSON 파일을 저장할 때마다 `index.html`이 자동으로 갱신됩니다.
   ```bash
    python update_portfolio.py --watch
  ```
    감시를 종료하려면 터미널에서 `Ctrl+C`를 누릅니다. 한 번만 갱신하려면 `python update_portfolio.py`를 실행합니다.

### 3. 짧은 확인 방법 (BRA-C11 충족 가이드)

* **사이트 주소:** `https://[배포된-내-포트폴리오-주소].app` (계정 생성·로그인·인증·CAPTCHA 없이 새 시크릿 창에서 즉시 열림)
* **이야기·숫자·대표작의 위치:**
  * **이야기 본편:** 사이트 메인 페이지 하단 「1. 본편 이야기」 섹션 (날짜 없이 세 능력 표기)
  * **리추얼 요약:** 사이트 메인 페이지 「2. 13주 리추얼 기록」 섹션 (반복 주제 상위 3개)
  * **대표작 위치:** 사이트 메인 페이지 「4. 대표작」 섹션 (`projects.json` 내용 자동 표시)
* **문서와 장치 ZIP 안 어디에 무엇이 있는지:**
  * 제출용 ZIP 파일(`portfolio_package.zip`) 내부 구조:
    * `documents/`: `resume.pdf`, `cover_letter.pdf`, `career_description.pdf` (비밀번호 없이 즉시 열림)
    * `device/`: `update_portfolio.py`, `README.md`, `ritual.json`, `assignments.json`, `projects.json` (장치 스크립트 및 입력 파일 세트)
* **보안 검증 (BRA-C10 준수):** 제출물 및 코드, URL 어디에도 본인 이름(조유정) 외의 타인 실명·연락처, 비밀번호, 토큰, API 키가 일체 포함되어 있지 않음.