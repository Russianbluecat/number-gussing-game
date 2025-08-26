import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="숫자 맞추기 게임",
    page_icon="🎯",
    layout="centered"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #4a5568;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #718096;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .game-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .success-message {
        background: #c6f6d5;
        color: #276749;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #48bb78;
        margin: 1rem 0;
        font-weight: bold;
        text-align: center;
    }
    
    .hint-message {
        background: #fef5e7;
        color: #744210;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ed8936;
        margin: 1rem 0;
        font-weight: bold;
        text-align: center;
    }
    
    .error-message {
        background: #fed7d7;
        color: #742a2a;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #f56565;
        margin: 1rem 0;
        font-weight: bold;
        text-align: center;
    }
    
    .history-box {
        background: #f7fafc;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-weight: bold;
    }
    
    .stNumberInput > div > div > input {
        text-align: center;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'home'  # 'home', 'playing', 'game_over'

if 'target_number' not in st.session_state:
    st.session_state.target_number = None

if 'attempts' not in st.session_state:
    st.session_state.attempts = 5

if 'guess_history' not in st.session_state:
    st.session_state.guess_history = []

if 'message' not in st.session_state:
    st.session_state.message = ""

if 'message_type' not in st.session_state:
    st.session_state.message_type = ""

def start_game():
    """게임 시작 함수"""
    st.session_state.game_state = 'playing'
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 5
    st.session_state.guess_history = []
    st.session_state.message = ""
    st.session_state.message_type = ""

def make_guess(guess):
    """추측 처리 함수"""
    if guess < 1 or guess > 100:
        st.session_state.message = "1부터 100 사이의 숫자를 입력해주세요!"
        st.session_state.message_type = "error"
        return
    
    current_attempt = 6 - st.session_state.attempts
    
    # 정답을 맞춘 경우
    if guess == st.session_state.target_number:
        if st.session_state.attempts == 1:
            # 5번째 시도에서 맞춘 경우
            st.session_state.message = "🎉 축하합니다! 성공하셨습니다!"
            st.session_state.guess_history.append(f"{current_attempt}번째: {guess} → 정답!")
        else:
            # 1~4번째 시도에서 맞춘 경우
            st.session_state.message = f"🎉 축하합니다! {current_attempt}번째 시도만에 맞췄네요!"
            st.session_state.guess_history.append(f"{current_attempt}번째: {guess} → 정답!")
        
        st.session_state.message_type = "success"
        st.session_state.game_state = 'game_over'
        return
    
    # 틀린 경우
    st.session_state.attempts -= 1
    
    if guess > st.session_state.target_number:
        hint_message = f"📉 Down! {guess}보다 작습니다."
        history_result = "너무 큼"
    else:
        hint_message = f"📈 Up! {guess}보다 큽니다."
        history_result = "너무 작음"
    
    st.session_state.guess_history.append(f"{current_attempt}번째: {guess} → {history_result}")
    
    # 5번째 시도에서 틀린 경우 (게임 오버)
    if st.session_state.attempts == 0:
        st.session_state.message = f"💥 Game Over!\n\n정답은 {st.session_state.target_number}였습니다."
        st.session_state.message_type = "error"
        st.session_state.game_state = 'game_over'
    else:
        st.session_state.message = hint_message
        st.session_state.message_type = "hint"

def restart_game():
    """게임 재시작 함수"""
    start_game()

def go_home():
    """홈으로 가기 함수"""
    st.session_state.game_state = 'home'
    st.session_state.message = ""
    st.session_state.message_type = ""

# 메인 게임 로직
if st.session_state.game_state == 'home':
    # 홈 화면
    st.markdown('<div class="main-header">🎯 숫자 맞추기 게임</div>', unsafe_allow_html=True)
    st.markdown('''
    <div class="subtitle">
    1 ~ 100 사이의 숫자를<br>
    5번의 기회 안에 맞춰보세요!
    </div>
    ''', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎮 게임 시작", type="primary"):
            start_game()
            st.rerun()

elif st.session_state.game_state == 'playing':
    # 게임 화면
    st.markdown('<div class="main-header">🎯 숫자 맞추기</div>', unsafe_allow_html=True)
    
    # 게임 정보
    st.markdown(f'''
    <div class="game-info">
        <h3>남은 기회: {st.session_state.attempts}/5</h3>
        <p>범위: 1 ~ 100</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 숫자 입력
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        guess = st.number_input(
            "숫자를 입력하세요:",
            min_value=1,
            max_value=100,
            value=50,
            key="guess_input"
        )
        
        if st.button("🎯 확인", type="primary"):
            make_guess(guess)
            st.rerun()
    
    # 메시지 표시
    if st.session_state.message:
        if st.session_state.message_type == "success":
            st.markdown(f'<div class="success-message">{st.session_state.message}</div>', unsafe_allow_html=True)
        elif st.session_state.message_type == "hint":
            st.markdown(f'<div class="hint-message">{st.session_state.message}</div>', unsafe_allow_html=True)
        elif st.session_state.message_type == "error":
            st.markdown(f'<div class="error-message">{st.session_state.message}</div>', unsafe_allow_html=True)
    
    # 시도 기록
    if st.session_state.guess_history:
        st.markdown('''
        <div class="history-box">
            <h4>📝 시도 기록</h4>
        </div>
        ''', unsafe_allow_html=True)
        
        for history_item in st.session_state.guess_history:
            st.write(f"• {history_item}")

elif st.session_state.game_state == 'game_over':
    # 게임 종료 화면
    st.markdown('<div class="main-header">🎯 게임 결과</div>', unsafe_allow_html=True)
    
    # 최종 메시지
    if st.session_state.message_type == "success":
        st.markdown(f'<div class="success-message">{st.session_state.message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="error-message">{st.session_state.message}</div>', unsafe_allow_html=True)
    
    # 전체 시도 기록
    if st.session_state.guess_history:
        st.markdown('''
        <div class="history-box">
            <h4>📝 전체 시도 기록</h4>
        </div>
        ''', unsafe_allow_html=True)
        
        for history_item in st.session_state.guess_history:
            st.write(f"• {history_item}")
    
    # 버튼들
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 하기", type="primary"):
            restart_game()
            st.rerun()
    
    with col2:
        if st.button("🏠 Home"):
            go_home()
            st.rerun()

# 사이드바에 게임 설명
with st.sidebar:
    st.markdown("### 🎮 게임 방법")
    st.markdown("""
    1. 1~100 사이의 숫자를 생각해보세요
    2. 컴퓨터가 생각한 숫자를 맞춰보세요
    3. Up/Down 힌트를 참고하세요
    4. 5번의 기회 안에 맞춰야 합니다!
    """)
    
    st.markdown("### 🏆 게임 규칙")
    st.markdown("""
    - **Up**: 입력한 숫자보다 큰 숫자입니다
    - **Down**: 입력한 숫자보다 작은 숫자입니다
    - **정답**: 축하합니다! 🎉
    - **Game Over**: 5번 모두 실패하면 정답 공개
    """)
