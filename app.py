import streamlit as st
import random
from datetime import datetime

# --- 상수 정의 ---
class GameConfig:
    FIXED_MAX_NUMBER = 100
    FIXED_MAX_ATTEMPTS = 5

# --- 게임 통계 ---
class GameStats:
    @staticmethod
    def get_achievement_level(win_rate, total_games):
        if total_games < 5:
            return "🌱 초보자"
        elif win_rate >= 80:
            return "🏆 마스터"
        elif win_rate >= 60:
            return "⭐ 전문가"
        elif win_rate >= 40:
            return "📈 숙련자"
        else:
            return "💪 도전자"

# --- 유효성 검사 ---
class GameValidator:
    @staticmethod
    def validate_guess(user_input, max_number, previous_guesses):
        try:
            guess = int(user_input)
            if not 1 <= guess <= max_number:
                return False, f"1부터 {max_number} 사이의 숫자를 입력해주세요!"
            if guess in previous_guesses:
                return False, f"{guess}은(는) 이미 시도한 숫자입니다!"
            return True, guess
        except (ValueError, TypeError):
            return False, "올바른 숫자를 입력해주세요!"

# --- CSS ---
@st.cache_data
def get_custom_css():
    return """
    <style>
    .game-header { 
        text-align: center; 
        padding: 20px; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 15px; 
        color: white; 
        margin-bottom: 30px; 
    }
    </style>
    """

# --- 세션 초기화 ---
def initialize_session_state():
    defaults = {
        'game_active': False,
        'target_number': None,
        'max_number': GameConfig.FIXED_MAX_NUMBER,
        'max_attempts': GameConfig.FIXED_MAX_ATTEMPTS,
        'current_attempts': 0,
        'guesses': [],
        'game_won': False,
        'game_over': False,
        'total_games': 0,
        'total_wins': 0,
        'best_score': None,
        'feedback_message': None,
        'feedback_type': None,
        'temp_guess': ""   # 입력 필드 값 관리
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# --- 게임 시작 ---
def start_new_game():
    st.session_state.target_number = random.randint(1, st.session_state.max_number)
    st.session_state.game_active = True
    st.session_state.current_attempts = 0
    st.session_state.guesses = []
    st.session_state.game_won = False
    st.session_state.game_over = False
    st.session_state.feedback_message = None
    st.session_state.feedback_type = None
    st.session_state.temp_guess = ""

# --- 추측 처리 ---
def make_guess(guess):
    st.session_state.current_attempts += 1
    st.session_state.guesses.append(guess)

    if guess == st.session_state.target_number:
        st.session_state.game_won = True
        st.session_state.game_over = True
        st.session_state.total_games += 1
        st.session_state.total_wins += 1

        if (st.session_state.best_score is None or 
            st.session_state.current_attempts < st.session_state.best_score):
            st.session_state.best_score = st.session_state.current_attempts

        st.session_state.feedback_message = f"🎉 정답! {st.session_state.current_attempts}번 만에 맞췄습니다!"
        st.session_state.feedback_type = "success"

    elif st.session_state.current_attempts >= st.session_state.max_attempts:
        st.session_state.game_over = True
        st.session_state.total_games += 1
        st.session_state.feedback_message = f"💔 실패! 정답은 {st.session_state.target_number}였습니다."
        st.session_state.feedback_type = "error"

    else:
        if guess > st.session_state.target_number:
            st.session_state.feedback_message = f"📉 Down! {guess}보다 작습니다."
            st.session_state.feedback_type = "warning"
        else:
            st.session_state.feedback_message = f"📈 Up! {guess}보다 큽니다."
            st.session_state.feedback_type = "info"

# --- 메시지 출력 ---
def display_feedback_message():
    if st.session_state.feedback_message and st.session_state.feedback_type:
        getattr(st, st.session_state.feedback_type)(st.session_state.feedback_message)

# --- 헤더 ---
def render_game_header():
    st.markdown("""<div class="game-header"><h1>🎯 숫자 맞추기 게임</h1><p>컴퓨터가 선택한 숫자를 맞춰보세요!</p></div>""", unsafe_allow_html=True)

# --- 메인 ---
def main():
    st.set_page_config(page_title="🎯 숫자 맞추기 게임", page_icon="🎯", layout="centered")
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    initialize_session_state()
    render_game_header()

    if not st.session_state.game_active:
        st.info("1에서 100 사이의 숫자를 5번 안에 맞춰보세요!")
        if st.button("🎮 게임 시작!", type="primary", use_container_width=True):
            start_new_game()
            st.rerun()
    else:
        remaining = st.session_state.max_attempts - st.session_state.current_attempts
        st.progress(st.session_state.current_attempts / st.session_state.max_attempts,
                   text=f"남은 기회: {remaining}번")

        display_feedback_message()

        if not st.session_state.game_over:
            st.markdown("### 🎯 숫자를 입력하세요")

            user_input = st.text_input(
                f"1부터 {st.session_state.max_number} 사이의 숫자",
                value=st.session_state.temp_guess,
                placeholder="숫자를 입력하세요...",
                key="guess_text_input"
            )

            col1, col2 = st.columns([3, 1])
            with col2:
                submit_button = st.button("🎯 제출", type="primary", use_container_width=True)

            # 제출 처리 (버튼 or 엔터)
            if submit_button or (user_input and user_input.strip() and user_input != st.session_state.temp_guess):
                is_valid, result = GameValidator.validate_guess(
                    user_input.strip(),
                    st.session_state.max_number,
                    st.session_state.guesses
                )
                if is_valid:
                    make_guess(result)
                    st.session_state.temp_guess = ""  # 🔑 입력창 초기화
                    st.rerun()
                else:
                    st.error(result)
                    st.session_state.temp_guess = ""  # 잘못된 입력도 초기화
                    st.rerun()

            # --- 자동 포커스 ---
            st.markdown("""
                <script>
                const input = window.parent.document.querySelector('input[type="text"]');
                if (input) { input.focus(); }
                </script>
            """, unsafe_allow_html=True)

        else:
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 다시 하기", type="primary", use_container_width=True):
                    start_new_game()
                    st.rerun()
            with col2:
                if st.button("⚙️ 메인으로", use_container_width=True):
                    st.session_state.game_active = False
                    st.session_state.game_over = False
                    st.rerun()

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666;'>🎯 숫자 맞추기 게임 | Made with Streamlit</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

