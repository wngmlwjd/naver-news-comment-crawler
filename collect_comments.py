import requests
import pandas as pd
import time
import re

def get_comments(oid, aid):
    """
    네이버 뉴스 API를 호출하여 댓글 정보를 가져옵니다.
    """
    comments_list = []
    # 네이버 댓글 API URL (JSON 형식으로 데이터를 가져옵니다)
    # page_size를 100으로 설정하여 한 번에 많은 댓글 수집
    url = f"https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&pool=cbox5&lang=ko&country=KR&objectId=news{oid}%2C{aid}&pageSize=100"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://n.news.naver.com/article/{oid}/{aid}"
    }

    try:
        response = requests.get(url, headers=headers)
        # JSONP 형식을 JSON으로 파싱하기 위한 처리
        json_data = re.search(r'\((\{.*\})\)', response.text).group(1)
        import json
        data = json.loads(json_data)

        if data['success']:
            comments = data['result']['commentList']
            for c in comments:
                comments_list.append({
                    "작성일": c['modTime'][:10], # YYYY-MM-DD
                    "작성자": c['maskedUserId'],
                    "댓글내용": c['contents'].replace('\n', ' '), # 줄바꿈 제거
                    "공감수": c['sympathyCount'],
                    "비공감수": c['antipathyCount'],
                    "답글수": c['replyCount']
                })
        return comments_list
    except Exception as e:
        print(f"      [오류] 댓글 파싱 실패 ({oid}-{aid}): {e}")
        return []

def collect_all_comments(input_file):
    """
    txt 파일을 읽어서 모든 기사의 댓글을 수집합니다.
    """
    all_data = []
    
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 데이터 시작 부분 찾기 (헤더 제외)
    start_processing = False
    for line in lines:
        if line.startswith("-" * 10): # 구분선 다음부터 데이터
            start_processing = True
            continue
        if not start_processing or "\t" not in line:
            continue

        parts = line.strip().split("\t")
        if len(parts) < 3: continue
        
        oid, aid, url = parts[0], parts[1], parts[2]
        print(f"-> 기사 분석 중: {oid}-{aid}")
        
        comments = get_comments(oid, aid)
        for c in comments:
            c['기사URL'] = url # URL 정보 추가
            all_data.append(c)
        
        time.sleep(0.5) # 서버 부하 방지용 짧은 대기

    return all_data