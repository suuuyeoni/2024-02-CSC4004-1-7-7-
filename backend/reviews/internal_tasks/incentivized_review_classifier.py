import json
import os
from typing import List

import django
from colorama import Fore

import ssh_manager

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()


from django.db.models import Q
from openai import OpenAI
from pydantic import BaseModel

import personal_key
from reviews.models import Review, ExtraReview

client = OpenAI(
    api_key=personal_key.OPEN_AI_API_KEY,
)


class IncentivizedResult(BaseModel):
    index: int
    is_incentivized_review: bool

class IncentivizedListResult(BaseModel):
    sentiments: List[IncentivizedResult]  # 각 감정 결과를 SentimentResult 모델로 정의

# def analyze_reviews(reviews):
#     messages = [{"role": "system", "content": "당신은 음식점에 작성된 리뷰에 기재된 '주문한 메뉴' 목록을 보고"
#                                               "해당 리뷰가 리뷰 작성을 대가로 추가적인 서비스를 제공받았는지 여부를 파악하는 AI입니다."
#                                               "'가성비갑', '리뷰이벤트', '포토리뷰'와 같은 항목은 해당 이름의 메뉴를 주문함으로써 대가를 제공받았음을 의미합니다."
#                                               "하지만 메뉴명이 '가성비'인 경우가 아닌, '가성비'라는 단어가 포함된 음식 메뉴라면 대가성 리뷰가 아닙니다."
#                                               "리뷰가 대가성 리뷰라고 판단되면 is_incentivized_review 값으로 True를, 아니라면 False를 반환해주세요."
#                                               "또한 대가성 리뷰라고 판단했다면 그 판단의 근거가 된 메뉴를 based_text로 반환해주세요."
#                                               "요청한 리뷰 메뉴들의 순서에 맞춰서 각 리뷰의 결과를 반환해주세요."}]
#
#     review_menus_str = ''
#     for index, review in enumerate(reviews):
#         review_menus_str += f'{index}번째 리뷰: {review.selected_menu}\n\n'
#     review_menus_str = review_menus_str.strip()
#     messages.append({"role": "user", "content": review_menus_str})
#
#     response = client.beta.chat.completions.parse(
#         model="gpt-4o",
#         messages=messages,
#         response_format=IncentivizedListResult
#     )
#     message = response.choices[0].message
#     content = message.content
#     data = json.loads(content)
#     return data
#
# def analyze_and_store_reviews(reviews):
#     data = json.loads(analyze_reviews(reviews).content)
#     print(json.dumps(data, indent=4, ensure_ascii=False))
#
#
def analyze_and_store_all_reviews():
    reviews = Review.objects.filter(
        Q(selected_menu__isnull=False) & ~Q(selected_menu='') & Q(manual_true_label_attempted=0)
    ).order_by('?')

    batch_size = 50
    total_reviews = len(reviews)  # QuerySet 전체 개수 계산
    offset = 0  # 시작점

    while offset < total_reviews:
        selected_reviews = reviews[offset:offset + batch_size]
        result = analyze_reviews(selected_reviews)

        print(json.dumps(result, indent=4, ensure_ascii=False))

        # 분석 결과 출력
        for i in range(len(selected_reviews)):
            print(f'{i + 1}. {selected_reviews[i].restaurant.name}')
            print(result['sentiments'][i]['is_incentivized_review'])
            print(selected_reviews[i].selected_menu)
            print()

        # offset을 batch_size만큼 증가
        offset += batch_size

        # 모든 데이터를 처리했다면 종료
        if len(selected_reviews) < batch_size:
            break

def analyze_and_store_reviews(size):
    reviews = Review.objects.filter(
        Q(selected_menu__isnull=False) & ~Q(selected_menu='') & Q(manual_true_label_attempted=0)
    ).order_by('?')[:size]

    for i, review in enumerate(reviews):
        restaurant_name = review.restaurant.name
        if any(item in review.selected_menu for item in ('리뷰', '이벤트', '포토', '별점', '중복')):
            print(f'{Fore.RED}{i} [{review.restaurant.name}] {review.selected_menu} ({review.id})')
            print(f'{review.content}')
            print(': FAKE')
            review.manual_is_true_review = False
        else:
            print(f'{Fore.GREEN}{i} [{review.restaurant.name}] {review.selected_menu} ({review.id})')
            print(f'{review.content}')
            print(': TRUE')
            review.manual_is_true_review = True
        review.manual_true_label_attempted = True
        review.save()
        print(Fore.RESET)


def get_length():
    reviews = Review.objects.filter(Q(selected_menu__isnull=False) & ~Q(selected_menu='') & Q(manual_true_label_attempted=0))
    print(len(reviews))

def analyze_and_store_only_fake_reviews(size):
    # reviews = ExtraReview.objects.filter(
    #     Q(selected_menu__isnull=False) & ~Q(selected_menu='') & Q(manual_true_label_attempted=0))[:3]

    # 검색 키워드 리스트
    keywords = ['리뷰', '이벤트', '포토', '별점', '중복', '500원']

    # 기본 필터 조건
    base_filter = Q(selected_menu__isnull=False) & ~Q(selected_menu='') & Q(manual_true_label_attempted=0)

    # 키워드 필터 조건
    keyword_filter = Q()
    for keyword in keywords:
        keyword_filter |= Q(selected_menu__icontains=keyword)

    # 최종 필터링
    reviews = ExtraReview.objects.filter(base_filter & keyword_filter)
    print(len(reviews))

    for i, review in enumerate(reviews):
        print(f'{Fore.RED}{i} {review.selected_menu} ({review.id})')
        print(f'{review.content}')
        print(': FAKE')
        review.manual_is_true_review = False
        review.manual_true_label_attempted = True
        review.save()
        print(Fore.RESET)


if __name__ == '__main__':
    # get_length()
    # for i in range(30):
    #     analyze_and_store_reviews(100)

    analyze_and_store_only_fake_reviews(109)

    # analyze_and_store_all_reviews()
