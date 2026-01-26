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
    press_codes = [press_dict[name] for name in press_names if name in press_dict]
    if not press_codes:
        return []

    options = Options()
    options.add_argument("--headless") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    all_final_data = []

    try:
        for press_code in press_codes:
            current_press_name = reverse_press_dict.get(press_code, press_code)
            for target_date in date_list:
                ranking_url = f"https://media.naver.com/press/{press_code}/ranking?type=comment&date={target_date}"
                print(f"   > [{current_press_name} | {target_date}] 접속 중...")
                
                driver.get(ranking_url)
                time.sleep(1.5) # 페이지 로딩 대기

                items = driver.find_elements(By.CSS_SELECTOR, "li") 
                
                count = 0
                for item in items:
                    if count >= top_n: break
                    
                    try:
                        title_el = item.find_element(By.CSS_SELECTOR, ".list_title, .as_thumb_title, .as_text_title")
                        title = title_el.text
                        url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                        oid, aid = extract_oid_aid(url)
                        
                        if oid and aid:
                            count += 1
                            # print(f"      ({count}/{top_n}) 수집 중: {title[:15]}...")
                            extra_info = {
                                'rank': count,
                                'press_code': press_code,
                                'target_date': target_date,
                                'title': title,
                                'url': url
                            }
                            article_comments = get_comments(oid, aid, extra_info)
                            all_final_data.extend(article_comments)
                            time.sleep(0.3) # API 부하 방지
                    except:
                        continue
    finally:
        driver.quit()

    return all_final_data