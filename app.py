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
        "attempts_used": 0,
        "last_result": None  # 마지막 결과 저장
    }

def reset_game():
    """게임을 완전히 초기화합니다."""
    keys_to_delete = ['game_state', 'game_started', 'user_guess', 'input_counter', 'current_guess']
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]

def clear_input():
    """입력 필드를 초기화합니다."""
    if 'current_guess' in st.session_state:
        del st.session_state.current_guess
    # 카운터를 증가시켜 새로운 입력 위젯 생성
    st.session_state.input_counter = st.session_state.get('input_counter', 0) + 1

# Streamlit 페이지 설정
st.set_page_config(
    page_title="숫자 맞추기 게임",
    page_icon="🎯",
    layout="centered"
)

# CSS 스타일링 (동일)
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

# 게임 상태 초기화
if 'game_state' not in st.session_state:
    st.session_state.game_state = create_new_game()

if 'input_counter' not in st.session_state:
    st.session_state.input_counter = 0

# 메인 제목
st.markdown('<h1 class="main-header">🎯 숫자 맞추기 게임!</h1>', unsafe_allow_html=True)

# 게임 설정 또는 플레이 영역
if not st.session_state.game_state["game_started"]:
    # 게임 설정 영역
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
            step=1,
            label_visibility="collapsed",
            help="1부터 이 숫자까지 중에서 정답이 정해집니다"
        )
    
    with col2:
        st.markdown("**시도 횟수**")
        max_attempts = st.number_input(
            "시도 횟수",
            min_value=1,
            max_value=100,
            value=5,
            step=1,
            label_visibility="collapsed",
            help="총 몇 번의 기회를 가질지 정하세요"
        )
    
    # 게임 미리보기 정보
    st.info(f"🎮 설정: 1~{max_number} 범위, {max_attempts}번의 기회")
    
    # 게임 시작 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎮 게임 시작!", use_container_width=True, type="primary"):
            # 새 게임 생성
            st.session_state.game_state = create_new_game(max_number, max_attempts)
            st.session_state.game_state["game_started"] = True
            st.session_state.input_counter = 0  # 입력 카운터 초기화
            st.rerun()

else:
    # 게임 플레이 영역
    st.markdown("## 🎲 게임 플레이")
    
    game_state = st.session_state.game_state
    
    # 게임 정보 표시
    st.markdown(f'<div class="attempts-info">🎯 범위: 1 ~ {game_state["max_number"]} | ⏰ 남은 시도: {game_state["attempts_left"]}회</div>', unsafe_allow_html=True)
    
    # 이전 결과 표시 (있는 경우)
    if game_state.get("last_result"):
        st.markdown(game_state["last_result"], unsafe_allow_html=True)
    
    if not game_state["game_over"]:
        st.markdown("### 숫자를 입력하세요")
        
        # 숫자 입력 (개선된 방식)
        input_key = f"guess_input_{st.session_state.input_counter}"
        
        user_guess = st.number_input(
            "추측할 숫자:",
            min_value=1,
            max_value=game_state['max_number'],
            value=None,
            placeholder=f"1부터 {game_state['max_number']} 사이의 숫자를 입력하세요",
            key=input_key,
            help="숫자를 입력하고 '추측하기' 버튼을 클릭하거나 Enter를 누르세요"
        )
        
        # 추측 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            guess_button = st.button("🎯 추측하기!", use_container_width=True, type="primary", disabled=(user_guess is None))
        
        # 추측 처리
        if guess_button and user_guess is not None:
            game_state["attempts_left"] -= 1
            game_state["attempts_used"] = game_state["max_attempts"] - game_state["attempts_left"]
            
            if user_guess == game_state["secret"]:
                # 성공!
                game_state["game_over"] = True
                game_state["last_result"] = f'<div class="result-success">🎉 <strong>정답입니다!!</strong><br>축하합니다! {game_state["attempts_used"]}번 만에 성공했습니다!</div>'
                
            elif game_state["attempts_left"] <= 0:
                # 실패
                game_state["game_over"] = True
                game_state["last_result"] = f'<div class="result-fail">💀 <strong>게임 오버!</strong><br>정답은 <strong>{game_state["secret"]}</strong>이었습니다!</div>'
                
            elif user_guess < game_state["secret"]:
                # 더 큰 숫자
                game_state["last_result"] = f'<div class="result-hint">📈 <strong>Up!</strong> <strong>{user_guess}</strong>보다 더 큰 숫자입니다!<br>남은 시도: {game_state["attempts_left"]}회</div>'
                
            else:
                # 더 작은 숫자
                game_state["last_result"] = f'<div class="result-hint">📉 <strong>Down!</strong> <strong>{user_guess}</strong>보다 더 작은 숫자입니다!<br>남은 시도: {game_state["attempts_left"]}회</div>'
            
            # 상태 저장 및 입력 필드 초기화 (게임이 끝나지 않은 경우)
            st.session_state.game_state = game_state
            if not game_state["game_over"]:
                clear_input()  # 입력 필드 초기화
            st.rerun()
        
        elif guess_button and user_guess is None:
            st.error("⚠️ 숫자를 입력해주세요!")
    
    else:
        # 게임 종료 후 통계 표시
        if game_state["attempts_used"] <= game_state["max_attempts"]:
            st.balloons()  # 성공 시 풍선 효과
        
        st.markdown("### 📊 게임 통계")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("정답", game_state["secret"])
        with col2:
            st.metric("사용한 시도", f"{game_state['attempts_used']}회")
        with col3:
            success_rate = "100%" if game_state["attempts_used"] <= game_state["max_attempts"] and not game_state["attempts_used"] == 0 else "0%"
            st.metric("성공률", success_rate)
    
    # 새 게임 시작 버튼
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 새 게임 시작", use_container_width=True):
            reset_game()
            st.rerun()

# 하단 정보
st.markdown("---")
st.markdown('<p class="info-text">🎮 재미있는 숫자 맞추기 게임을 즐겨보세요!</p>', unsafe_allow_html=True)
