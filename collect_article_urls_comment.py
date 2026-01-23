'''
각 언론사 별 네이버 뉴스 홈페이지
랭킹 - 댓글 많은 순 - 날짜 - 상위 N개 기사 댓글 크롤링
'''

import time
import re
import json
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from utils import extract_oid_aid, press_dict

reverse_press_dict = {v: k for k, v in press_dict.items()}

def get_comments(oid, aid, extra_info):
    comments_list = []
    url = f"https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&pool=cbox5&lang=ko&country=KR&objectId=news{oid}%2C{aid}&pageSize=100"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://n.news.naver.com/article/{oid}/{aid}"
    }

    try:
        response = requests.get(url, headers=headers)
        json_data = re.search(r'\((\{.*\})\)', response.text).group(1)
        data = json.loads(json_data)

        if data['success']:
            comments = data['result']['commentList']
            for c in comments:
                # 코드를 이름으로 변환 (딕셔너리에 없으면 코드 그대로 표시)
                press_name = reverse_press_dict.get(extra_info['press_code'], extra_info['press_code'])
                
                comment_row = {
                    "언론사": press_name,
                    "검색기준날짜": extra_info['target_date'],
                    "기사순위": extra_info['rank'],
                    "기사제목": extra_info['title'],
                    "댓글내용": c['contents'].replace('\n', ' '),
                    "좋아요수": c['sympathyCount'],
                    "싫어요수": c['antipathyCount'],
                    "답글수": c['replyCount'],
                    "댓글작성일": c['modTime'][:10],
                    "댓글작성자": c['maskedUserId'],
                    "기사링크": extra_info['url']
                }
                comments_list.append(comment_row)
        return comments_list
    except Exception as e:
        print(f"      [오류] 댓글 파싱 실패: {e}")
        return []

def run_integrated_crawler(press_names, date_list, top_n=10):
    # 1. 언론사 이름을 코드로 변환
    press_codes = []
    for name in press_names:
        if name in press_dict:
            press_codes.append(press_dict[name])
        else:
            print(f"[경고] '{name}'은 press_dict에 없는 언론사입니다. 제외합니다.")

    options = Options()
    # options.add_argument("--headless") # 필요 시 활성화
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    all_final_data = []

    try:
        for press_code in press_codes:
            current_press_name = reverse_press_dict.get(press_code, press_code)
            for target_date in date_list:
                ranking_url = f"https://media.naver.com/press/{press_code}/ranking?type=comment&date={target_date}"
                print(f"\n[{current_press_name} | {target_date}] 랭킹 접속 중...")
                
                driver.get(ranking_url)
                time.sleep(2)

                # 1. 기사 아이템들을 더 넓은 범위로 탐색
                items = driver.find_elements(By.CSS_SELECTOR, "li") 
                
                count = 0
                for item in items:
                    if count >= top_n: break
                    
                    try:
                        # 2. 제목이 들어있는 요소를 찾음 (보내주신 구조 반영)
                        title_el = item.find_element(By.CSS_SELECTOR, ".list_title, .as_thumb_title, .as_text_title")
                        title = title_el.text
                        
                        # 3. 그 제목을 감싸고 있거나 같은 레벨에 있는 링크(a) 태그 찾기
                        # 보통 제목(strong)의 부모가 a 태그이거나, 같은 li 안에 a 태그가 있습니다.
                        link_el = item.find_element(By.TAG_NAME, "a")
                        url = link_el.get_attribute("href")
                        
                        # 네이버 기사 주소가 맞는지 검증 (oid, aid가 있어야 함)
                        oid, aid = extract_oid_aid(url)
                        
                        if oid and aid:
                            count += 1
                            print(f"   ({count}/{top_n}) 수집 중: {title[:20]}...")
                            
                            extra_info = {
                                'rank': count,
                                'press_code': press_code,
                                'target_date': target_date,
                                'title': title,
                                'url': url
                            }
                            
                            article_comments = get_comments(oid, aid, extra_info)
                            all_final_data.extend(article_comments)
                            time.sleep(0.3)
                    except:
                        # 해당 li 안에 기사 정보가 없는 경우(광고 등)는 그냥 넘어감
                        continue
    finally:
        driver.quit()

    return all_final_data