import streamlit as st
import random
from datetime import datetime

# --- 상수 정의 및 유틸리티 클래스 ---
class GameConfig:
    MIN_RANGE = 10
    MAX_RANGE = 1000
    MIN_ATTEMPTS = 3
    MAX_ATTEMPTS = 15
    DEFAULT_MAX_NUMBER = 100
    DEFAULT_MAX_ATTEMPTS = 5

class GameStats:
    @staticmethod
    def calculate_difficulty(max_number, max_attempts):
        ratio = max_number / max_attempts
        if ratio <= 20:
            return "쉬움", "easy"
        elif ratio <= 40:
            return "보통", "medium"
        else:
            return "어려움", "hard"
    
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

# --- CSS 스타일 (한 번만 로드) ---
@st.cache_data
def get_custom_css():
    return """
    <style>
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
        --info-color: #007bff;
    }
    .main { padding-top: 1rem; }
    .game-header { text-align: center; padding: 20px; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); border-radius: 15px; color: white; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); animation: fadeIn 0.5s ease-in; }
    .game-stats-container { background: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 4px solid var(--info-color); margin-bottom: 20px; transition: transform 0.2s ease; }
    .guess-display { background: #fff; padding: 20px; border-radius: 10px; border: 2px solid #e9ecef; text-align: center; margin-bottom: 20px; font-size: 1.5rem; font-weight: bold; animation: slideIn 0.3s ease; }
    .message { padding: 15px; border-radius: 10px; margin: 20px 0; text-align: center; font-weight: bold; animation: fadeIn 0.4s ease; }
    .attempts-remaining { background: linear-gradient(45deg, #ff6b6b, #ee5a52); color: white; padding: 10px 20px; border-radius: 25px; text-align: center; font-weight: bold; margin: 15px 0; animation: pulse 2s infinite; }
    .difficulty-badge { display: inline-block; padding: 5px 15px; border-radius: 20px; color: white; font-size: 0.9rem; font-weight: bold; margin: 5px; }
    .difficulty-easy { background: var(--success-color); }
    .difficulty-medium { background: var(--warning-color); }
    .difficulty-hard { background: var(--danger-color); }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes slideIn { from { transform: translateY(-10px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.02); } }
    </style>
    """

# --- 게임 로직 함수 ---
def initialize_session_state():
    defaults = {
        'game_active': False,
        'target_number': None,
        'max_number': GameConfig.DEFAULT_MAX_NUMBER,
        'max_attempts': GameConfig.DEFAULT_MAX_ATTEMPTS,
        'current_attempts': 0,
        'guesses': [],
        'game_won': False,
        'game_over': False,
        'total_games': 0,
        'total_wins': 0,
        'best_score': None,
        'difficulty_preset': 'custom'
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def start_new_game():
    st.session_state.target_number = random.randint(1, st.session_state.max_number)
    st.session_state.game_active = True
    st.session_state.current_attempts = 0
    st.session_state.guesses = []
    st.session_state.game_won = False
    st.session_state.game_over = False

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
        
        st.success(f"🎉 축하합니다! {st.session_state.current_attempts}번 만에 정답!")
        
    elif st.session_state.current_attempts >= st.session_state.max_attempts:
        st.session_state.game_over = True
        st.session_state.total_games += 1
        st.error(f"💔 게임 오버! 정답은 {st.session_state.target_number}였습니다.")
        
    else:
        if guess < st.session_state.target_number:
            st.info(f"📈 UP! {guess}보다 큽니다.")
        else:
            st.info(f"📉 DOWN! {guess}보다 작습니다.")

# --- 렌더링 함수 ---
def render_game_header():
    st.markdown("""<div class="game-header"><h1>🎯 숫자 맞추기 게임</h1><p>컴퓨터가 선택한 숫자를 맞춰보세요!</p></div>""", unsafe_allow_html=True)

def render_game_stats():
    st.subheader("📊 게임 통계")
    if st.session_state.total_games > 0:
        win_rate = (st.session_state.total_wins / st.session_state.total_games) * 100
        achievement = GameStats.get_achievement_level(win_rate, st.session_state.total_games)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("총 게임", st.session_state.total_games)
        with col2: st.metric("승리", st.session_state.total_wins)
        with col3: st.metric("승률", f"{win_rate:.1f}%")
        with col4: st.metric("최고 기록", f"{st.session_state.best_score}번" if st.session_state.best_score else "없음")
        
        st.markdown(f"""<div class="game-stats-container"><strong>🏅 달성도: {achievement}</strong></div>""", unsafe_allow_html=True)
    else:
        st.info("아직 플레이한 게임이 없습니다. 지금 바로 시작해보세요!")

def render_difficulty_presets():
    st.markdown("### 🎮 난이도 선택")
    presets = {
        'easy': {'name': '🌟 쉬움', 'max_number': 50, 'max_attempts': 7},
        'medium': {'name': '⚡ 보통', 'max_number': 100, 'max_attempts': 5},
        'hard': {'name': '🔥 어려움', 'max_number': 200, 'max_attempts': 4},
        'custom': {'name': '⚙️ 사용자 설정', 'max_number': None, 'max_attempts': None}
    }
    
    preset_options = [presets[key]['name'] for key in presets.keys()]
    preset_keys = list(presets.keys())
    
    selected_preset_name = st.selectbox("난이도 프리셋:", options=preset_options, index=preset_keys.index(st.session_state.difficulty_preset), key="preset_select")
    selected_key = preset_keys[preset_options.index(selected_preset_name)]
    
    if selected_key != st.session_state.difficulty_preset:
        st.session_state.difficulty_preset = selected_key
        if selected_key != 'custom':
            st.session_state.max_number = presets[selected_key]['max_number']
            st.session_state.max_attempts = presets[selected_key]['max_attempts']
        st.experimental_rerun()

    if selected_key != 'custom':
        difficulty_text, difficulty_class = GameStats.calculate_difficulty(st.session_state.max_number, st.session_state.max_attempts)
        st.markdown(f"""<span class="difficulty-badge difficulty-{difficulty_class}">범위: 1-{st.session_state.max_number}, 시도: {st.session_state.max_attempts}번</span>""", unsafe_allow_html=True)
    return selected_key == 'custom'

def render_custom_settings():
    st.markdown("### ⚙️ 사용자 정의")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.max_number = st.slider("최대 숫자 범위", min_value=GameConfig.MIN_RANGE, max_value=GameConfig.MAX_RANGE, value=st.session_state.max_number, step=10, key='custom_max_number')
    with col2:
        st.session_state.max_attempts = st.slider("최대 시도 횟수", min_value=GameConfig.MIN_ATTEMPTS, max_value=GameConfig.MAX_ATTEMPTS, value=st.session_state.max_attempts, step=1, key='custom_max_attempts')
    difficulty_text, difficulty_class = GameStats.calculate_difficulty(st.session_state.max_number, st.session_state.max_attempts)
    st.markdown(f"""<span class="difficulty-badge difficulty-{difficulty_class}">예상 난이도: {difficulty_text}</span>""", unsafe_allow_html=True)

# --- 메인 앱 ---
def main():
    st.set_page_config(page_title="🎯 숫자 맞추기 게임", page_icon="🎯", layout="centered")
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    initialize_session_state()
    render_game_header()

    if not st.session_state.game_active:
        show_custom = render_difficulty_presets()
        if show_custom:
            render_custom_settings()
        
        if st.button("🎮 게임 시작!", type="primary", use_container_width=True):
            start_new_game()
        
        with st.expander("📊 게임 통계 보기"):
            render_game_stats()

    else:
        remaining = st.session_state.max_attempts - st.session_state.current_attempts
        st.progress(st.session_state.current_attempts / st.session_state.max_attempts, text=f"남은 기회: {remaining}번")
        
        if st.session_state.guesses:
            guesses_text = " → ".join([str(g) for g in st.session_state.guesses])
            st.markdown(f"""<div class="guess-display">{guesses_text}</div>""", unsafe_allow_html=True)
            
        if not st.session_state.game_over:
            user_input = st.number_input(f"숫자 입력 (1-{st.session_state.max_number})", min_value=1, max_value=st.session_state.max_number, step=1, key="guess_input_active", help="Enter 키를 눌러도 제출됩니다!")
            
            if st.button("🎯 제출", use_container_width=True):
                is_valid, result = GameValidator.validate_guess(user_input, st.session_state.max_number, st.session_state.guesses)
                if is_valid:
                    make_guess(result)
                else:
                    st.error(result)
        
        if st.session_state.game_over:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 다시 하기", type="primary", use_container_width=True):
                    start_new_game()
            with col2:
                if st.button("⚙️ 설정 변경", use_container_width=True):
                    st.session_state.game_active = False
                    st.session_state.game_over = False

    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666;'>🎯 개선된 숫자 맞추기 게임 | Made with Streamlit & ❤️</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
