import streamlit as st
import random

# 세션 상태 초기화 및 게임 로직
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
        "last_result": None,
        "guess_history": [],
        "focus_input": True  # 새로운 플래그 추가
    }

def reset_game():
    """게임을 완전히 초기화합니다."""
    keys_to_delete = ['game_state', 'game_started', 'user_guess', 'input_counter', 'current_guess']
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]
    # 게임 재시작 시 포커스 플래그를 True로 설정
    st.session_state.game_state = create_new_game(st.session_state.game_state.get("max_number", 100), st.session_state.game_state.get("max_attempts", 5))

def clear_input():
    """입력 필드를 초기화합니다."""
    if 'current_guess' in st.session_state:
        del st.session_state.current_guess
    st.session_state.input_counter = st.session_state.get('input_counter', 0) + 1
    st.session_state.game_state["focus_input"] = True # 입력 필드 초기화 시 포커스 플래그 설정

def validate_input(guess, max_number):
    """입력값 유효성 검사"""
    if guess is None:
        return False, "숫자를 입력해주세요!"
    if guess < 1 or guess > max_number:
        return False, f"1부터 {max_number} 사이의 숫자를 입력해주세요!"
    return True, ""

# Streamlit 페이지 설정
st.set_page_config(
    page_title="숫자 맞추기 게임",
    page_icon="🎯",
    layout="centered"
)

# 개선된 CSS 스타일링 (기존 코드와 동일)
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2c3e50;
        font-size: 2.8rem;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .setup-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .game-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    .result-success {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(86, 171, 47, 0.3);
    }
    .result-fail {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.3);
    }
    .result-hint {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }
    .info-text {
        text-align: center;
        color: #666;
        font-style: italic;
        margin: 15px 0;
        font-size: 1.1rem;
    }
    .attempts-info {
        background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
        font-size: 1.2rem;
        box-shadow: 0 4px 15px rgba(33, 147, 176, 0.3);
    }
    .setup-input {
        margin-bottom: 1.5rem;
    }
    .setup-label {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        display: block;
    }
    .game-stats {
        background: linear-gradient(135deg, #834d9b 0%, #d04ed6 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(131, 77, 155, 0.3);
    }
    .history-item {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem 1rem;
        margin: 0.3rem 0;
        border-radius: 8px;
        display: inline-block;
        margin-right: 0.5rem;
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
    st.markdown('<div class="setup-container">', unsafe_allow_html=True)
    st.markdown("## ⚙️ 게임 설정")
    st.markdown('<p class="info-text">원하는 게임 설정을 입력하고 시작하세요!</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="setup-input">', unsafe_allow_html=True)
    st.markdown('<span class="setup-label">🎯 최대 숫자 (1부터 이 숫자까지)</span>', unsafe_allow_html=True)
    max_number = st.number_input(
        "최대 숫자",
        min_value=2,
        max_value=10000,
        value=100,
        step=1,
        label_visibility="collapsed",
        help="1부터 이 숫자까지 중에서 정답이 정해집니다"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="setup-input">', unsafe_allow_html=True)
    st.markdown('<span class="setup-label">⏰ 시도 횟수</span>', unsafe_allow_html=True)
    max_attempts = st.number_input(
        "시도 횟수",
        min_value=1,
        max_value=100,
        value=5,
        step=1,
        label_visibility="collapsed",
        help="총 몇 번의 기회를 가질지 정하세요"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info(f"🎮 설정: 1~{max_number} 범위, {max_attempts}번의 기회")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎮 게임 시작!", use_container_width=True, type="primary"):
            st.session_state.game_state = create_new_game(max_number, max_attempts)
            st.session_state.game_state["game_started"] = True
            st.session_state.input_counter = 0
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    st.markdown("## 🎲 게임 플레이")
    
    game_state = st.session_state.game_state
    
    st.markdown(f'<div class="attempts-info">🎯 범위: 1 ~ {game_state["max_number"]} | ⏰ 남은 시도: {game_state["attempts_left"]}회</div>', unsafe_allow_html=True)
    
    if not game_state["game_over"] and game_state.get("guess_history"):
        st.markdown("### 📝 지금까지의 추측")
        history_html = "".join([
            f'<span class="history-item">{"📈" if result_type == "up" else "📉" if result_type == "down" else "🎯"} {guess}</span>'
            for guess, result_type in game_state["guess_history"]
        ])
        st.markdown(history_html, unsafe_allow_html=True)
    
    if game_state.get("last_result") and game_state["game_over"]:
        st.markdown(game_state["last_result"], unsafe_allow_html=True)
    
    if not game_state["game_over"]:
        st.markdown("### 숫자를 입력하세요")
        
        # 포커스 스크립트 실행 조건 확인
        if st.session_state.game_state["focus_input"]:
            st.markdown("""
            <script>
                function focusOnInput() {
                    const inputElement = document.querySelector('input[type="number"]');
                    if (inputElement) {
                        inputElement.focus();
                        // 입력창이 비어있지 않다면 내용 전체 선택
                        if (inputElement.value !== '') {
                            inputElement.select();
                        }
                    }
                }
                focusOnInput();
            </script>
            """, unsafe_allow_html=True)
            st.session_state.game_state["focus_input"] = False # 플래그 초기화
        
        with st.form(key=f"guess_form_{st.session_state.input_counter}"):
            user_guess = st.number_input(
                "추측할 숫자:",
                min_value=1,
                max_value=game_state['max_number'],
                value=None,
                placeholder=f"1부터 {game_state['max_number']} 사이의 숫자를 입력하세요",
                help="숫자를 입력하고 '추측하기' 버튼을 클릭하거나 Enter를 누르세요"
            )
            
            if not game_state["game_over"] and game_state.get("last_result"):
                st.markdown(game_state["last_result"], unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                guess_button = st.form_submit_button("🎯 추측하기!", use_container_width=True, type="primary")
        
        if guess_button:
            is_valid, error_msg = validate_input(user_guess, game_state['max_number'])
            
            if not is_valid:
                st.error(f"⚠️ {error_msg}")
            else:
                game_state["attempts_left"] -= 1
                game_state["attempts_used"] = game_state["max_attempts"] - game_state["attempts_left"]
                
                if user_guess == game_state["secret"]:
                    game_state["game_over"] = True
                    game_state["guess_history"].append((user_guess, "correct"))
                    game_state["last_result"] = f'<div class="result-success">🎉 <strong>정답입니다!!</strong><br>축하합니다! {game_state["attempts_used"]}번 만에 성공했습니다!<br>정답: <strong>{game_state["secret"]}</strong></div>'
                
                elif game_state["attempts_left"] <= 0:
                    game_state["game_over"] = True
                    result_type = "up" if user_guess < game_state["secret"] else "down"
                    game_state["guess_history"].append((user_guess, result_type))
                    game_state["last_result"] = f'<div class="result-fail">💀 <strong>게임 오버!</strong><br>정답은 <strong>{game_state["secret"]}</strong>이었습니다!<br>마지막 추측 <strong>{user_guess}</strong>은 정답보다 {"작았" if result_type == "up" else "컸"}습니다.</div>'
                    
                elif user_guess < game_state["secret"]:
                    game_state["guess_history"].append((user_guess, "up"))
                    game_state["last_result"] = f'<div class="result-hint">📈 <strong>Up!</strong> <strong>{user_guess}</strong>보다 더 큰 숫자입니다!<br>남은 시도: {game_state["attempts_left"]}회</div>'
                    
                else:
                    game_state["guess_history"].append((user_guess, "down"))
                    game_state["last_result"] = f'<div class="result-hint">📉 <strong>Down!</strong> <strong>{user_guess}</strong>보다 더 작은 숫자입니다!<br>남은 시도: {game_state["attempts_left"]}회</div>'
                
                st.session_state.game_state = game_state
                if not game_state["game_over"]:
                    clear_input()
                st.rerun()
    
    else:
        if any(result_type == "correct" for _, result_type in game_state.get("guess_history", [])):
            st.balloons()
            
        st.markdown('<div class="game-stats">', unsafe_allow_html=True)
        st.markdown("### 📊 게임 통계")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("정답", game_state["secret"])
        with col2:
            st.metric("사용한 시도", f"{game_state['attempts_used']}회")
        with col3:
            success_rate = "100%" if any(result_type == "correct" for _, result_type in game_state["guess_history"]) else "0%"
            st.metric("성공률", success_rate)
            
        if game_state.get("guess_history"):
            st.markdown("### 📝 전체 추측 기록")
            history_text = "".join([
                f'<span class="history-item">{i+1}. {"🎯" if result_type == "correct" else "📈" if result_type == "up" else "📉"} {guess} ({"정답!" if result_type == "correct" else "Up" if result_type == "up" else "Down"})</span>'
                for i, (guess, result_type) in enumerate(game_state["guess_history"])
            ])
            st.markdown(history_text, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 새 게임 시작", use_container_width=True):
            reset_game()
            st.rerun()

# 하단 정보
st.markdown("---")
st.markdown('<p class="info-text">🎮 재미있는 숫자 맞추기 게임을 즐겨보세요!</p>', unsafe_allow_html=True)
