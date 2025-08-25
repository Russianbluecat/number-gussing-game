import streamlit as st
import random
import time
import streamlit.components.v1 as components

# ====================
# 1. 상수 및 페이지 설정
# ====================
st.set_page_config(
    page_title=" 숫자 맞추기 게임",
    page_icon="🎯",
    layout="centered"
)

# 게임 기본 설정 상수
DEFAULT_MAX_NUMBER = 100
DEFAULT_MAX_ATTEMPTS = 5

# ====================
# 2. 유틸리티 함수
# ====================
def get_custom_css():
    """커스텀 CSS 스타일을 반환합니다."""
    return """
    <style>
    .main {
        padding-top: 2rem;
    }
    .game-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .game-stats {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin-bottom: 20px;
    }
    .guess-display {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        text-align: center;
        margin-bottom: 20px;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .message-success {
        background: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 20px 0;
        text-align: center;
        font-weight: bold;
    }
    .message-hint {
        background: #fff3cd;
        color: #856404;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 20px 0;
        text-align: center;
        font-weight: bold;
    }
    .message-error {
        background: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 20px 0;
        text-align: center;
        font-weight: bold;
    }
    .game-over {
        background: #e2e3e5;
        color: #383d41;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #6c757d;
        text-align: center;
        margin: 20px 0;
    }
    .attempts-remaining {
        background: linear-gradient(45deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        text-align: center;
        font-weight: bold;
        margin: 15px 0;
    }
    </style>
    """

def get_auto_focus_script():
    """입력 필드에 자동으로 포커스를 맞추는 스크립트를 반환합니다."""
    return """
    <script>
    function focusInput() {
        setTimeout(function() {
            const inputs = window.parent.document.querySelectorAll('input[type="number"]');
            if (inputs.length > 0) {
                inputs[inputs.length - 1].focus();
            }
        }, 100);
    }
    focusInput();
    </script>
    """

def initialize_session_state():
    """게임 세션 상태를 초기화합니다."""
    defaults = {
        'game_active': False,
        'target_number': None,
        'max_number': DEFAULT_MAX_NUMBER,
        'max_attempts': DEFAULT_MAX_ATTEMPTS,
        'current_attempts': 0,
        'guesses': [],
        'game_won': False,
        'game_over': False,
        'message': "",
        'message_type': "info",
        'total_games': 0,
        'total_wins': 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def start_new_game():
    """새 게임을 시작합니다."""
    st.session_state.target_number = random.randint(1, st.session_state.max_number)
    st.session_state.game_active = True
    st.session_state.current_attempts = 0
    st.session_state.guesses = []
    st.session_state.game_won = False
    st.session_state.game_over = False
    st.session_state.message = f"1부터 {st.session_state.max_number}까지의 숫자를 맞춰보세요!"
    st.session_state.message_type = "info"

def make_guess(guess):
    """사용자 추측을 처리하고 게임 상태를 업데이트합니다."""
    st.session_state.current_attempts += 1
    st.session_state.guesses.append(guess)
    
    if guess == st.session_state.target_number:
        st.session_state.game_won = True
        st.session_state.game_over = True
        st.session_state.game_active = False
        st.session_state.total_games += 1
        st.session_state.total_wins += 1
        st.session_state.message = f"🎉 축하합니다! 정답입니다! ({st.session_state.current_attempts}번 만에 맞췄습니다)"
        st.session_state.message_type = "success"
        
    elif st.session_state.current_attempts >= st.session_state.max_attempts:
        st.session_state.game_over = True
        st.session_state.game_active = False
        st.session_state.total_games += 1
        st.session_state.message = f"😭 게임 오버! 정답은 **{st.session_state.target_number}**였습니다."
        st.session_state.message_type = "error"
        
    elif guess < st.session_state.target_number:
        st.session_state.message = f"📈 UP! {guess}보다 큽니다."
        st.session_state.message_type = "hint"
        
    else:
        st.session_state.message = f"📉 DOWN! {guess}보다 작습니다."
        st.session_state.message_type = "hint"

# ====================
# 3. 렌더링 함수 (코드 구조 개선)
# ====================
def render_game_header():
    """게임 헤더를 렌더링합니다."""
    st.markdown(f"""
    <div class="game-header">
        <h1> 숫자 맞추기 게임</h1>
        <p>컴퓨터가 선택한 숫자를 맞춰보세요!</p>
    </div>
    """, unsafe_allow_html=True)

def render_game_stats():
    """게임 통계를 렌더링합니다."""
    if st.session_state.total_games > 0:
        win_rate = (st.session_state.total_wins / st.session_state.total_games) * 100
        st.markdown(f"""
        <div class="game-stats">
            <strong>📊 게임 통계</strong><br>
            총 게임: {st.session_state.total_games}회 | 
            승리: {st.session_state.total_wins}회 | 
            승률: {win_rate:.1f}%
        </div>
        """, unsafe_allow_html=True)

def render_start_screen():
    """게임 시작 화면(설정)을 렌더링합니다."""
    st.markdown("### ⚙️ 게임 설정")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_number = st.number_input(
            "최대 숫자 (범위: 1 ~ ?)",
            min_value=10,
            max_value=1000,
            value=st.session_state.max_number,
            step=10
        )
        st.session_state.max_number = max_number
    
    with col2:
        max_attempts = st.number_input(
            "최대 시도 횟수",
            min_value=3,
            max_value=15,
            value=st.session_state.max_attempts,
            step=1
        )
        st.session_state.max_attempts = max_attempts

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎮 게임 시작!", type="primary", use_container_width=True):
        start_new_game()
        st.rerun()

def render_playing_game():
    """게임 진행 화면을 렌더링합니다."""
    remaining_attempts = st.session_state.max_attempts - st.session_state.current_attempts
    st.markdown(f"""
    <div class="attempts-remaining">
        🎯 남은 기회: {remaining_attempts}번 / {st.session_state.max_attempts}번
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.guesses:
        st.markdown("### 📝 이전 추측들")
        guesses_text = " → ".join([str(g) for g in st.session_state.guesses])
        st.markdown(f"""
        <div class="guess-display">
            {guesses_text}
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.message:
        message_class = f"message-{st.session_state.message_type}"
        st.markdown(f"""
        <div class="{message_class}">
            {st.session_state.message}
        </div>
        """, unsafe_allow_html=True)

    if not st.session_state.game_over:
        components.html(get_auto_focus_script(), height=0)
        with st.form(key="guess_form", clear_on_submit=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                user_input = st.number_input(
                    f"숫자를 입력하세요 (1-{st.session_state.max_number})",
                    min_value=1,
                    max_value=st.session_state.max_number,
                    step=1,
                    key="guess_input"
                )
            with col2:
                submitted = st.form_submit_button("🎯 추측하기", use_container_width=True)
            
            if submitted and user_input is not None:
                make_guess(int(user_input))

    else:
        render_end_game_options()

def render_end_game_options():
    """게임 종료 후 다시 플레이/설정 변경 버튼을 렌더링합니다."""
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 플레이", type="primary", use_container_width=True):
            start_new_game()
    with col2:
        if st.button("⚙️ 설정 변경", use_container_width=True):
            st.session_state.game_active = False
            st.session_state.message = ""

# ====================
# 4. 메인 애플리케이션
# ====================
def main():
    """메인 애플리케이션 진입점"""
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    initialize_session_state()
    render_game_header()
    render_game_stats()

    if not st.session_state.game_active:
        render_start_screen()
    else:
        render_playing_game()

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        " 숫자 맞추기 게임 | Made with Streamlit"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

