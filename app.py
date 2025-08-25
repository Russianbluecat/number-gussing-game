import streamlit as st
import random

# Streamlit 페이지 설정
st.set_page_config(
    page_title="숫자 맞추기 게임",
    page_icon="🎯",
    layout="centered"
)

# 사용자 정의 CSS (옵션, 기존 코드를 유지)
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
    .stForm > div > div {
        display: flex;
        justify-content: center;
        align-items: center;
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

# 게임이 시작되지 않았다면 초기 상태로 설정
if 'game_over' not in st.session_state:
    init_game_state()

# 메인 제목
st.markdown('<h1 class="main-header">🎯 숫자 맞추기 게임!</h1>', unsafe_allow_html=True)

# 2. 추측 처리 함수 (콜백 함수로 분리)
def check_guess():
    """사용자의 추측을 확인하고 게임 상태를 업데이트합니다."""
    # st.session_state.user_guess는 form submit 시 자동으로 업데이트 됨
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
    
    # 3. 입력 필드 자동 초기화 및 포커스
    # on_change 핸들러가 자동으로 input 값을 초기화하는 효과를 줄 수 있음
    st.session_state.user_guess = None # form 제출 후 입력 필드 값을 None으로 초기화

# 게임 플레이 로직
if st.session_state.game_over:
    # 게임 종료 후
    if st.session_state.last_result == "success":
        st.balloons()
        st.success(f"🎉 **정답입니다!** {st.session_state.attempts_used}번 만에 성공했습니다!")
    else:
        st.error(f"💀 **게임 오버!** 정답은 **{st.session_state.secret}**이었습니다!")

    st.markdown("---")
    st.markdown("### 📊 게임 통계")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("정답", st.session_state.secret)
    with col2:
        st.metric("사용한 시도", f"{st.session_state.attempts_used}회")

    if st.button("🔄 새 게임 시작", use_container_width=True):
        init_game_state(st.session_state.max_number, st.session_state.max_attempts)
        st.experimental_rerun()

else:
    # 게임 진행 중
    st.markdown(f'<div class="attempts-info">🎯 범위: 1 ~ {st.session_state.max_number} | ⏰ 남은 시도: {st.session_state.attempts_left}회</div>', unsafe_allow_html=True)

    # 힌트 메시지 표시
    if st.session_state.last_result == "up":
        st.info("📈 **Up!** 더 큰 숫자입니다!")
    elif st.session_state.last_result == "down":
        st.info("📉 **Down!** 더 작은 숫자입니다!")

    with st.form(key="guess_form"):
        user_guess = st.number_input(
            "숫자를 입력하세요:",
            min_value=1,
            max_value=st.session_state.max_number,
            value=None, # 입력 필드 초기화
            placeholder=f"1부터 {st.session_state.max_number} 사이의 숫자",
            key="user_guess",
            help="숫자를 입력하고 Enter를 누르거나 버튼을 클릭하세요."
        )
        st.form_submit_button("🎯 추측하기!", on_click=check_guess, use_container_width=True)

# 하단 정보
st.markdown("---")
st.markdown('<p class="info-text">🎮 재미있는 숫자 맞추기 게임을 즐겨보세요!</p>', unsafe_allow_html=True)
