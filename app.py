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
        "last_result": None,
        "guess_history": []  # 추측 히스토리 추가
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
    st.session_state.input_counter = st.session_state.get('input_counter', 0) + 1

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

# 개선된 CSS 스타일링
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

<script>
function focusNumberInput() {
    setTimeout(function() {
        const numberInputs = document.querySelectorAll('input[type="number"]');
        if (numberInputs.length > 0) {
            numberInputs[numberInputs.length - 1].focus();
            numberInputs[numberInputs.length - 1].select();
        }
    }, 100);
}

document.addEventListener('DOMContentLoaded', focusNumberInput);
window.addEventListener('load', focusNumberInput);

setInterval(function() {
    const numberInputs = document.querySelectorAll('input[type="number"]');
    if (numberInputs.length > 0 && document.activeElement !== numberInputs[numberInputs.length - 1]) {
        if (!document.activeElement || document.activeElement.tagName !== 'INPUT') {
            numberInputs[numberInputs.length - 1].focus();
        }
    }
}, 500);
</script>
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
    # 게임 설정 영역 (세로 배열로 변경)
    st.markdown('<div class="setup-container">', unsafe_allow_html=True)
    st.markdown("## ⚙️ 게임 설정")
    st.markdown('<p class="info-text">원하는 게임 설정을 입력하고 시작하세요!</p>', unsafe_allow_html=True)
    
    # 세로 배열로 변경
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
    
    # 게임 미리보기 정보
    st.info(f"🎮 설정: 1~{max_number} 범위, {max_attempts}번의 기회")
    
    # 게임 시작 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎮 게임 시작!", use_container_width=True, type="primary"):
            st.session_state.game_state = create_new_game(max_number, max_attempts)
            st.session_state.game_state["game_started"] = True
            st.session_state.input_counter = 0
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # 게임 플레이 영역
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    st.markdown("## 🎲 게임 플레이")
    
    game_state = st.session_state.game_state
    
    # 게임 정보 표시
    st.markdown(f'<div class="attempts-info">🎯 범위: 1 ~ {game_state["max_number"]} | ⏰ 남은 시도: {game_state["attempts_left"]}회</div>', unsafe_allow_html=True)
    
    # 추측 히스토리 표시 (게임 진행 중일 때)
    if not game_state["game_over"] and game_state.get("guess_history"):
        st.markdown("### 📝 지금까지의 추측")
        history_html = ""
        for i, (guess, result_type) in enumerate(game_state["guess_history"]):
            emoji = "📈" if result_type == "up" else "📉" if result_type == "down" else "🎯"
            history_html += f'<span class="history-item">{emoji} {guess}</span>'
        st.markdown(history_html, unsafe_allow_html=True)
    
    # 이전 결과 표시 (게임이 끝났을 때만)
    if game_state.get("last_result") and game_state["game_over"]:
        st.markdown(game_state["last_result"], unsafe_allow_html=True)
    
    if not game_state["game_over"]:
        st.markdown("### 숫자를 입력하세요")
        
        # 숫자 입력
        input_key = f"guess_input_{st.session_state.input_counter}"
        
        with st.form(key=f"guess_form_{st.session_state.input_counter}"):
            user_guess = st.number_input(
                "추측할 숫자:",
                min_value=1,
                max_value=game_state['max_number'],
                value=None,
                placeholder=f"1부터 {game_state['max_number']} 사이의 숫자를 입력하세요",
                help="숫자를 입력하고 '추측하기' 버튼을 클릭하거나 Enter를 누르세요"
            )
            
            # 이전 결과가 있고 게임이 진행 중인 경우 여기에 표시
            if not game_state["game_over"] and game_state.get("last_result"):
                st.markdown(game_state["last_result"], unsafe_allow_html=True)
            
            # 추측 버튼
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                guess_button = st.form_submit_button("🎯 추측하기!", use_container_width=True, type="primary")
        
        # 추측 처리
        if guess_button:
            is_valid, error_msg = validate_input(user_guess, game_state['max_number'])
            
            if not is_valid:
                st.error(f"⚠️ {error_msg}")
            else:
                # 히스토리에 추측 추가 (결과 판단 전)
                game_state["attempts_left"] -= 1
                game_state["attempts_used"] = game_state["max_attempts"] - game_state["attempts_left"]
                
                if user_guess == game_state["secret"]:
                    # 성공!
                    game_state["game_over"] = True
                    game_state["guess_history"].append((user_guess, "correct"))
                    game_state["last_result"] = f'<div class="result-success">🎉 <strong>정답입니다!!</strong><br>축하합니다! {game_state["attempts_used"]}번 만에 성공했습니다!<br>정답: <strong>{game_state["secret"]}</strong></div>'
                    
                elif game_state["attempts_left"] <= 0:
                    # 실패
                    game_state["game_over"] = True
                    result_type = "up" if user_guess < game_state["secret"] else "down"
                    game_state["guess_history"].append((user_guess, result_type))
                    game_state["last_result"] = f'<div class="result-fail">💀 <strong>게임 오버!</strong><br>정답은 <strong>{game_state["secret"]}</strong>이었습니다!<br>마지막 추측 <strong>{user_guess}</strong>은 정답보다 {"작았" if result_type == "up" else "컸"}습니다.</div>'
                    
                elif user_guess < game_state["secret"]:
                    # 더 큰 숫자
                    game_state["guess_history"].append((user_guess, "up"))
                    game_state["last_result"] = f'<div class="result-hint">📈 <strong>Up!</strong> <strong>{user_guess}</strong>보다 더 큰 숫자입니다!<br>남은 시도: {game_state["attempts_left"]}회</div>'
                    
                else:
                    # 더 작은 숫자
                    game_state["guess_history"].append((user_guess, "down"))
                    game_state["last_result"] = f'<div class="result-hint">📉 <strong>Down!</strong> <strong>{user_guess}</strong>보다 더 작은 숫자입니다!<br>남은 시도: {game_state["attempts_left"]}회</div>'
                
                # 상태 저장 및 입력 필드 초기화
                st.session_state.game_state = game_state
                if not game_state["game_over"]:
                    clear_input()
                st.rerun()
    
    else:
        # 게임 종료 후 통계 표시
        if game_state["attempts_used"] <= game_state["max_attempts"] and user_guess == game_state["secret"]:
            st.balloons()
        
        st.markdown('<div class="game-stats">', unsafe_allow_html=True)
        st.markdown("### 📊 게임 통계")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("정답", game_state["secret"])
        with col2:
            st.metric("사용한 시도", f"{game_state['attempts_used']}회")
        with col3:
            if game_state["attempts_used"] > 0:
                success = any(guess == game_state["secret"] for guess, _ in game_state.get("guess_history", []))
                success_rate = "100%" if success else "0%"
            else:
                success_rate = "0%"
            st.metric("성공률", success_rate)
        
        # 전체 히스토리 표시
        if game_state.get("guess_history"):
            st.markdown("### 📝 전체 추측 기록")
            history_text = ""
            for i, (guess, result_type) in enumerate(game_state["guess_history"]):
                emoji = "🎯" if result_type == "correct" else "📈" if result_type == "up" else "📉"
                result_text = "정답!" if result_type == "correct" else "Up" if result_type == "up" else "Down"
                history_text += f'<span class="history-item">{i+1}. {emoji} {guess} ({result_text})</span>'
            st.markdown(history_text, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
