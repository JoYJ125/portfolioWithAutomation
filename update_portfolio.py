import argparse
import json
import os
import time
from html import escape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILES = ('assignments.json', 'ritual.json', 'projects.json')

def load_json(file_path):
    full_path = os.path.join(BASE_DIR, file_path)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def replace_section(html_content, start_tag, end_tag, replacement):
    if start_tag not in html_content or end_tag not in html_content:
        return html_content
    start_index = html_content.index(start_tag) + len(start_tag)
    end_index = html_content.index(end_tag, start_index)
    return html_content[:start_index] + "\n" + replacement + "\n" + html_content[end_index:]

RITUAL_THEMES = [
    (
        '소통과 경청',
        ('대화', '이야기', '토론', '경청', '공감', '소통', '말씀', '듣', '질문', '의견'),
        '팀 활동에서 대화를 나누고 상대의 말을 경청하며 편안한 분위기를 만드는 모습이 반복됐습니다.',
    ),
    (
        '친절과 배려',
        ('배려', '친절', '도와', '도움', '챙겨', '존중'),
        '주변의 상황을 살피고 먼저 친절하게 돕거나 배려하려는 태도가 자주 나타났습니다.',
    ),
    (
        '성장과 적응',
        ('성장', '적응', '도전', '노력', '해낼', '해냈', '자신감', '극복', '배우', '배웠'),
        '낯선 상황에도 적응하고 꾸준히 시도하며 배움을 이어가는 흐름이 드러났습니다.',
    ),
    (
        '성실과 책임',
        ('책임', '성실', '준비', '계획', '마무리', '꾸준', '기록', '실천'),
        '미리 준비하고 맡은 일을 끝까지 해내려는 책임감과 실행력이 반복해서 확인됐습니다.',
    ),
    (
        '긍정과 여유',
        ('긍정', '밝', '여유', '휴식', '편안', '조절', '침착', '페이스', '재충전'),
        '긍정적인 태도와 적절한 휴식으로 자신의 페이스를 조절하려는 모습이 나타났습니다.',
    ),
]

def summarize_ritual(ritual):
    counts = {name: 0 for name, _, _ in RITUAL_THEMES}
    entries = []
    if isinstance(ritual, dict) and isinstance(ritual.get('days'), list):
        for day in ritual['days']:
            for section_name in ('open', 'close'):
                section = day.get(section_name, [])
                if isinstance(section, list):
                    entries.extend(str(entry).split(':', 1)[-1] for entry in section)
    elif isinstance(ritual, list):
        entries.extend(str(entry).split(':', 1)[-1] for entry in ritual)

    for entry in entries:
        for name, keywords, _ in RITUAL_THEMES:
            if any(keyword in entry for keyword in keywords):
                counts[name] += 1

    ranked_themes = sorted(
        RITUAL_THEMES,
        key=lambda theme: (-counts[theme[0]], next(index for index, item in enumerate(RITUAL_THEMES) if item[0] == theme[0])),
    )
    return ''.join(
        f'<li><strong>{escape(name)}</strong> ({counts[name]}개 문장)<br>{escape(summary)}</li>\n'
        for name, _, summary in ranked_themes[:3]
        if counts[name] > 0
    )

def main():
    # 포트폴리오 데이터 JSON 로드
    assignments = load_json('assignments.json')
    ritual = load_json('ritual.json')
    projects = load_json('projects.json')

    html_path = os.path.join(BASE_DIR, 'index.html')
    if not os.path.exists(html_path):
        print("오류: index.html 파일을 찾을 수 없습니다.")
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 1. assignments.json (본편 이야기) 반영
    if isinstance(assignments, list):
        assignments_html = ""
        for item in assignments:
            ability = escape(str(item.get('ability', '')))
            task = escape(str(item.get('task', '')))
            evidence = escape(str(item.get('evidence', '')))
            assignments_html += f"""
            <div class="card">
                <h3>{ability}</h3>
                <p>{task}</p>
                <p><strong>근거:</strong> {evidence}</p>
            </div>"""
        html_content = replace_section(
            html_content,
            '<!-- @ASSIGNMENTS_START@ -->',
            '<!-- @ASSIGNMENTS_END@ -->',
            assignments_html,
        )

    # 2. ritual.json (리추얼 기록) 반영
    if ritual is not None:
        ritual_html = summarize_ritual(ritual)
        html_content = replace_section(
            html_content,
            '<!-- @RITUAL_START@ -->',
            '<!-- @RITUAL_END@ -->',
            ritual_html,
        )

    # 3. projects.json (대표작) 반영
    if isinstance(projects, list):
        projects_html = ""
        for project in projects:
            title = escape(str(project.get('title', '')))
            category = escape(str(project.get('category', '')))
            description = escape(str(project.get('description', '')))
            url = escape(str(project.get('url', '')))
            url_html = (
                f'                <a class="project-url" href="{url}" target="_blank" '
                f'rel="noopener noreferrer">{url}</a>'
                if url else ''
            )
            technologies = project.get('technologies', [])
            if not isinstance(technologies, list):
                technologies = []
            badges_html = ''.join(
                f'                    <span class="badge">{escape(str(technology))}</span>\n'
                for technology in technologies
            )
            projects_html += f"""
            <div class="card">
                <h3>{title}</h3>
                <span class="date">{category}</span>
                <p>{description}</p>
                <div class="badge-container">
{badges_html}                </div>
{url_html}
            </div>"""
        html_content = replace_section(
            html_content,
            '<!-- @PROJECTS_START@ -->',
            '<!-- @PROJECTS_END@ -->',
            projects_html,
        )

    # 결과 저장
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("과제, 리추얼, 대표작 데이터가 포트폴리오 HTML에 반영되었습니다!")

def input_signature():
    signature = []
    for file_name in INPUT_FILES:
        file_path = os.path.join(BASE_DIR, file_name)
        try:
            file_stat = os.stat(file_path)
            signature.append((file_stat.st_mtime_ns, file_stat.st_size))
        except FileNotFoundError:
            signature.append(None)
    return tuple(signature)

def watch():
    try:
        main()
    except (json.JSONDecodeError, OSError) as error:
        print(f"입력 파일을 읽지 못했습니다. 파일을 저장하면 다시 시도합니다: {error}")

    last_signature = input_signature()
    print("JSON 변경 감시 중입니다. 종료하려면 Ctrl+C를 누르세요.")
    try:
        while True:
            time.sleep(1)
            current_signature = input_signature()
            if current_signature == last_signature:
                continue

            time.sleep(0.5)
            stable_signature = input_signature()
            if stable_signature != current_signature:
                continue

            last_signature = stable_signature
            try:
                main()
            except (json.JSONDecodeError, OSError) as error:
                print(f"입력 파일을 읽지 못했습니다. 파일을 저장하면 다시 시도합니다: {error}")
    except KeyboardInterrupt:
        print("JSON 변경 감시를 종료했습니다.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--watch', action='store_true', help='JSON 파일 변경을 감시해 HTML을 자동 갱신합니다.')
    arguments = parser.parse_args()
    if arguments.watch:
        watch()
    else:
        main()