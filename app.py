import streamlit as st
import random

def create_new_game(max_number=100, max_attempts=5):
    """새 게임 상태를 생성합니다."""
    return {
        "secret": random.randint(1, max_number),
        "attempts_left": max_attempts,
        "game_over": False,
        "max_number": max_number,
        "max_attempts": max_attempts,
        "game_started": False,
        "attempts_used": 0
    }

def reset_game():
    """게임을 완전히 초기화합니다."""
    for key in ['game_state', 'game_started', 'user_guess']:
        if key in st.session_state:
            del st.session_state[key]

# Streamlit 페이지 설정
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
        color: #333;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .setup-container {
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    .game-container {
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    .result-success {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .result-fail {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
    }
    .result-hint {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    .info-text {
        text-align: center;
        color: #666;
        font-style: italic;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# 게임 상태 초기화
if 'game_state' not in st.session_state:
    st.session_state.game_state = create_new_game()

# 메인 제목
st.markdown('<h1 class="main-header">🎯 Playing Customizable Number Guessing Game!</h1>', unsafe_allow_html=True)

# 게임 설정 또는 플레이 영역
if not st.session_state.game_state["game_started"]:
    # 게임 설정 영역
    st.markdown("## ⚙️ 게임 설정")
    st.markdown('<p class="info-text">원하는 게임 설정을 입력하고 시작하세요!</p>', unsafe_allow_html=True)
    
    st.markdown("**Last Number** (1부터 이 숫자까지)")
    max_number = st.number_input(
        "Last Number",
        min_value=2,
        max_value=10000,
        value=100,
        step=1,
        label_visibility="collapsed"
    )
    st.markdown('<p class="info-text">기본값: 100</p>', unsafe_allow_html=True)
    
    st.markdown("**시도 횟수**")
    max_attempts = st.number_input(
        "시도 횟수",
        min_value=1,
        max_value=100,
        value=5,
        step=1,
        label_visibility="collapsed"
    )
    st.markdown('<p class="info-text">기본값: 5회</p>', unsafe_allow_html=True)
    
    # 게임 시작 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎮 게임 시작!", use_container_width=True, type="primary"):
            # 새 게임 생성
            st.session_state.game_state = create_new_game(max_number, max_attempts)
            st.session_state.game_state["game_started"] = True
            st.rerun()

else:
    # 게임 플레이 영역
    st.markdown("## 🎲 게임 플레이")
    
    game_state = st.session_state.game_state
    
    if not game_state["game_over"]:
        st.markdown(f"**🎯 1부터 {game_state['max_number']} 사이의 숫자를 맞춰보세요!**")
        st.markdown(f"**⏰ 남은 시도 횟수: {game_state['attempts_left']}회**")
        
        # 숫자 입력 (틀렸을 때 자동으로 초기화되도록 key 변경)
        input_key = f"user_guess_{game_state.get('attempts_used', 0)}"
        user_guess = st.number_input(
            "숫자를 입력하세요:",
            min_value=1,
            max_value=game_state['max_number'],
            value=None,
            placeholder=f"1부터 {game_state['max_number']} 사이의 숫자",
            key=input_key,
            on_change=lambda: st.session_state.update({"enter_pressed": True})
        )
        
        # 추측 버튼 또는 엔터 처리
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            guess_button = st.button("🎯 추측하기!", use_container_width=True, type="primary")
        
        # 엔터키 또는 버튼 클릭 시 처리
        if (guess_button or st.session_state.get("enter_pressed", False)) and user_guess is not None:
            game_state["attempts_left"] -= 1
            game_state["attempts_used"] = game_state["max_attempts"] - game_state["attempts_left"]
            
            if user_guess == game_state["secret"]:
                # 성공!
                game_state["game_over"] = True
                st.markdown(f'<div class="result-success">🎉 <strong>정답입니다!!</strong><br>축하해요! ({game_state["attempts_used"]}번 만에 성공!)</div>', unsafe_allow_html=True)
                
            elif game_state["attempts_left"] <= 0:
                # 실패
                game_state["game_over"] = True
                st.markdown(f'<div class="result-fail">💀 <strong>Game Over!</strong><br>정답은 {game_state["secret"]}이었습니다!</div>', unsafe_allow_html=True)
                
            elif user_guess < game_state["secret"]:
                # 더 큰 숫자
                st.markdown(f'<div class="result-hint">📈 <strong>Up!</strong> 더 큰 숫자입니다!<br>남은 시도: {game_state["attempts_left"]}회</div>', unsafe_allow_html=True)
                
            else:
                # 더 작은 숫자
                st.markdown(f'<div class="result-hint">📉 <strong>Down!</strong> 더 작은 숫자입니다!<br>남은 시도: {game_state["attempts_left"]}회</div>', unsafe_allow_html=True)
            
            # 상태 업데이트
            st.session_state.game_state = game_state
            # 엔터 상태 초기화
            if "enter_pressed" in st.session_state:
                del st.session_state["enter_pressed"]
            
        elif (guess_button or st.session_state.get("enter_pressed", False)) and user_guess is None:
            st.error("⚠️ 숫자를 입력해주세요!")
            # 엔터 상태 초기화
            if "enter_pressed" in st.session_state:
                del st.session_state["enter_pressed"]
    
    # 새 게임 시작 버튼 (항상 표시)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 새 게임 시작", use_container_width=True):
            reset_game()
            st.rerun()

# 하단 정보
st.markdown("---")
st.markdown('<p class="info-text">🎮 나만의 숫자 맞추기 게임을 즐겨보세요!</p>', unsafe_allow_html=True)
