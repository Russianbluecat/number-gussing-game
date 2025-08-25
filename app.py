import streamlit as st
import random

# Streamlit 페이지 설정
st.set_page_config(
    page_title="숫자 맞추기 게임",
    page_icon="🎯",
    layout="centered"
)

# 사용자 정의 CSS (디자인 유지)
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #333;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .attempts-info {
        background-color: #e9ecef;
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 1. 게임 상태 초기화 함수
def init_game_state(max_number=100, max_attempts=5):
    """게임 상태를 초기화합니다."""
    st.session_state.secret = random.randint(1, max_number)
    st.session_state.attempts_left = max_attempts
    st.session_state.game_over = False
    st.session_state.max_number = max_number
    st.session_state.max_attempts = max_attempts
    st.session_state.attempts_used = 0
    st.session_state.last_result = None

# 2. 추측 처리 함수 (콜백 함수)
def check_guess():
    """사용자의 추측을 확인하고 게임 상태를 업데이트합니다."""
    # st.session_state.user_guess는 number_input의 key를 통해 자동으로 접근 가능
    user_guess = st.session_state.user_guess
    
    if user_guess is None:
        st.error("⚠️ 숫자를 입력해주세요!")
        return

    st.session_state.attempts_left -= 1
    st.session_state.attempts_used += 1

    if user_guess == st.session_state.secret:
        st.session_state.game_over = True
        st.session_state.last_result = "success"
    elif st.session_state.attempts_left <= 0:
        st.session_state.game_over = True
        st.session_state.last_result = "fail"
    elif user_guess < st.session_state.secret:
        st.session_state.last_result = "up"
    else:
        st.session_state.last_result = "down"
    
    # 입력 필드 초기화 (폼 제출 후)
    st.session_state.user_guess = None

# 게임이 시작되지 않았다면 초기 상태로 설정
if 'game_over' not in st.session_state:
    init_game_state()

# 메인 제목
st.markdown('<h1 class="main-header">🎯 숫자 맞추기 게임!</h1>', unsafe_allow_html=True)

# 게임 시작 화면
if not st.session_state.get('game_started', False):
    st.markdown("## ⚙️ 게임 설정")
    st.markdown('<p class="info-text">원하는 게임 설정을 입력하고 시작하세요!</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**최대 숫자** (1부터 이 숫자까지)")
        max_number = st.number_input(
            "최대 숫자",
            min_value=2,
            max_value=10000,
            value=100,
