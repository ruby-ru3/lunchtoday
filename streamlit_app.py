import streamlit as st
import random
from transformers import pipeline

# GPT-2 모델 로드
@st.cache_resource
def load_model():
    return pipeline('text-generation', model='gpt2', tokenizer='gpt2')

menu_generator = load_model()

# 메뉴 카테고리
menu_categories = {
    "한식": ["비빔밥", "불고기", "김치찌개", "된장찌개", "순두부찌개", "칼국수", "해장국", "부대찌개", "쌈밥", "잡채", "갈비탕", "삼계탕", "수육", "제육볶음", "감자탕"],
    "양식": ["피자", "햄버거", "스파게티", "스테이크", "샐러드", "리조또", "파스타", "치킨윙", "그라탱", "오믈렛", "로스트 치킨", "클럽 샌드위치", "페투치니", "치즈버거", "프렌치 토스트"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마파두부", "볶음밥", "고추잡채", "깐풍기", "꿔바로우", "양장피", "북경오리", "차돌짬뽕", "멘보샤", "팔보채", "유린기", "게살볶음밥", "마라탕"],
    "일식": ["초밥", "라멘", "덴푸라", "카츠동", "우동", "오코노미야키", "타코야키", "카레라이스", "규동", "돈카츠", "냉소바", "스키야키", "야키니쿠", "오야코동", "사케동"],
    "분식": ["떡볶이", "김밥", "라면", "순대", "어묵탕", "돈가스", "붕어빵", "호떡", "핫도그", "쫄면", "떡꼬치", "순대볶음", "소떡소떡", "만두"],
    "간편식": ["샌드위치", "컵라면", "도시락", "핫도그", "토스트", "베이글", "시리얼", "크로와상", "머핀", "그래놀라 바", "스콘", "치킨너겟", "미트볼", "핫케이크"]
}

# 날씨 기반 추천 메뉴
weather_menus = {
    "맑음": ["샐러드", "초밥", "샌드위치", "아이스크림", "생과일주스", "그릭 요거트", "카프레제", "냉파스타", "아보카도 토스트", "아이스티"],
    "비": ["파전", "수제비", "김치전", "칼국수", "뜨거운 커피", "부침개", "떡국", "김치수제비", "우동", "비빔국수", "김치볶음밥", "감자전", "배추전", "어묵탕"],
    "눈": ["호빵", "어묵", "고구마", "호떡", "온국수", "따뜻한 코코아", "팥죽", "순두부찌개", "닭곰탕", "갈비탕", "전골", "누룽지탕", "설렁탕", "군밤", "라떼"],
    "더움": ["냉면", "빙수", "콩국수", "과일빙수", "아이스커피", "냉국", "냉모밀", "냉우동", "아이스크림", "수박", "토마토 냉국", "레몬에이드", "아이스초코", "망고빙수", "과일주스"],
    "추움": ["뜨거운 라면", "국밥", "순대국", "감자탕", "만두", "전골", "곰탕", "삼계탕", "설렁탕", "불고기전골", "차돌된장찌개", "육개장", "칼국수", "된장찌개", "사골국"]
}

# Streamlit 앱
st.title("오늘의 점심 추천봇 😊")

# 사용자가 입장했을 때 인사
st.write("안녕하세요! 오늘 점심 메뉴를 추천해드리겠습니다. 무엇을 도와드릴까요? 😊")

# 사용자 입력 저장 및 복원
if "preferred_category" not in st.session_state:
    st.session_state.preferred_category = "상관없음"

if "disliked_category" not in st.session_state:
    st.session_state.disliked_category = "상관없음"

if "previous_meal" not in st.session_state:
    st.session_state.previous_meal = ""

if "weather" not in st.session_state:
    st.session_state.weather = "상관없음"

preferred_category = st.selectbox(
    "원하는 음식 분야를 선택해주세요:",
    ["상관없음", "한식", "양식", "중식", "일식", "분식", "간편식"],
    index=["상관없음", "한식", "양식", "중식", "일식", "분식", "간편식"].index(st.session_state.preferred_category),
    help="선호하는 음식 분야를 선택해주세요."
)
st.session_state.preferred_category = preferred_category

disliked_category = st.selectbox(
    "싫어하는 음식 분야가 있나요?",
    ["상관없음", "한식", "양식", "중식", "일식", "분식", "간편식"],
    index=["상관없음", "한식", "양식", "중식", "일식", "분식", "간편식"].index(st.session_state.disliked_category),
    help="싫어하는 음식 분야가 있다면 선택해주세요."
)
st.session_state.disliked_category = disliked_category

previous_meal = st.text_input(
    "오늘 드신 식사를 알려주세요:",
    value=st.session_state.previous_meal,
    help="오늘 이미 드신 음식을 입력해주세요."
)
st.session_state.previous_meal = previous_meal

exclude_previous_meal = st.checkbox(
    "이전 식사를 제외하고 추천받기 원하시나요?",
    help="오늘 이미 드신 음식을 제외하고 추천을 받으시려면 체크해주세요."
)

weather = st.selectbox(
    "현재 날씨는 어떤가요?",
    ["상관없음", "맑음", "비", "눈", "더움", "추움"],
    index=["상관없음", "맑음", "비", "눈", "더움", "추움"].index(st.session_state.weather),
    help="현재 날씨를 선택해주세요."
)
st.session_state.weather = weather

# 필터링된 메뉴 리스트 가져오기
def get_filtered_menus():
    menus = []

    if st.session_state.preferred_category != "상관없음":
        menus.extend(menu_categories.get(st.session_state.preferred_category, []))
    else:
        for category in menu_categories.values():
            menus.extend(category)

    if st.session_state.disliked_category != "상관없음":
        menus = [menu for menu in menus if menu not in menu_categories.get(st.session_state.disliked_category, [])]

    if exclude_previous_meal and st.session_state.previous_meal:
        menus = [menu for menu in menus if st.session_state.previous_meal not in menu]

    if st.session_state.weather != "상관없음":
        menus += weather_menus.get(st.session_state.weather, [])

    # 중복 제거
    return list(set(menus))

filtered_menus = get_filtered_menus()

# 메뉴 추천 함수 수정
def recommend_menu(menus):
    if menus:
        recommendations = random.sample(menus, min(3, len(menus)))
        return recommendations
    else:
        return []

# GPT-2를 이용한 설명 생성
def generate_menu_description(recommendations):
    descriptions = []
    for menu in recommendations:
        prompt = f"{menu}는 어떤 음식인가요?"
        response = menu_generator(prompt, max_length=50, num_return_sequences=1)
        description = response[0]['generated_text']
        descriptions.append(description)
    return descriptions

# 추천 메뉴 출력
if st.button("추천받기"):
    try:
        recommendations = recommend_menu(filtered_menus)
        if recommendations:
            descriptions = generate_menu_description(recommendations)
            for desc in descriptions:
                st.write(desc)
        else:
            st.write("추천할 메뉴가 없네요. 다른 카테고리를 선택해보세요!")
    except Exception as e:
        st.error(f"추천 과정에서 문제가 발생했습니다. 잠시 후 다시 시도해주세요. 오류: {e}")

st.write("언제든지 메뉴를 골라 드려요! 오늘도 좋은 하루 되세요! 😊")
