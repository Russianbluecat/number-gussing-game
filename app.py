import streamlit as st
import random

def create_new_game(max_number=100, max_attempts=5):
    return {
        "secret": random.randint(1, max_number),
        "attempts_left": max_attempts,
        "game_over": False,
        "max_number": max_number,
        "max_attempts": max_attempts,
        "game_started": False,
        "attempts_used": 0,
        "last_result": None,
        "guess_history": []
    }

def reset_game():
    keys_to_delete = ['game_state', 'game_started', 'user_guess', 'input_counter', 'current_guess']
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]

def clear_input():
    if 'current_guess' in st.session_state:
        del st.session_state.current_guess
    st.session_state.input_counter = st.session_state.get('input_counter', 0) + 1

def validate_input(guess, max_number):
    if guess is None:
        return False, "숫자를 입력해주세요!"
    if guess < 1 or guess > max_number:
        return False, f"1부터 {max_number} 사이의 숫자를 입력해주세요!"
    return True, ""

# 페이지 설정
st.set_page_config(page_title="숫자 맞추기 게임", page_icon="🎯", layout="centered")

# CSS (스타일만 유지)
st.markdown("""
<style>
    .main-header { text-align: center; font-size: 2.8rem; margin-bottom: 1.5rem; }
    .setup-container, .game-container { padding: 2rem; border-radius: 15px; margin-bottom: 2rem; }
    .game-container { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; }
    .result-success, .result-fail, .result-hint {
        padding:1.5rem; border-radius:12px; margin:1rem 0; text-align:center; font-weight:bold;
    }
    .result-success { background: linear-gradient(135deg,#56ab2f 0%,#a8e6cf 100%); }
    .result-fail { background: linear-gradient(135deg,#ff416c 0%,#ff4b2b 100%); }
    .result-hint { background: linear-gradient(135deg,#f093fb 0%,#f5576c 100%); }
    .attempts-info { background: linear-gradient(135deg,#2193b0 0%,#6dd5ed 100%); padding:1rem; border-radius:12px; text-align:center; margin:1rem 0; font-weight:bold; }
    .history-item { background:rgba(255,255,255,0.1); padding:0.5rem 1rem; margin:0.3rem; border-radius:8px; display:inline-block; }
</style>
""", unsafe_allow_html=True)

# 게임 상태 초기화
if 'game_state' not in st.session_state:
    st.session_state.game_state = create_new_game()
if 'input_counter' not in st.session_state:
    st.session_state.input_counter = 0

# 메인 제목
st.markdown('<h1 class="main-header">🎯 숫자 맞추기 게임!</h1>', unsafe_allow_html=True)

# 게임 설정
if not st.session_state.game_state["game_started"]:
    st.markdown('<div class="setup-container">', unsafe_allow_html=True)
    st.markdown("## ⚙️ 게임 설정")
    
    max_number = st.number_input("최대 숫자", min_value=2, max_value=10000, value=100, step=1)
    max_attempts = st.number_input("시도 횟수", min_value=1, max_value=100, value=5, step=1)
    
    st.info(f"🎮 설정: 1~{max_number} 범위, {max_attempts}번의 기회")
    
    if st.button("🎮 게임 시작!", type="primary", use_container_width=True):
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
    
    if not game_state["game_over"]:
        input_key = f"guess_input_{st.session_state.input_counter}"
        
        with st.form(key=f"guess_form_{st.session_state.input_counter}"):
            user_guess = st.number_input(
                "추측할 숫자:",
                min_value=1,
                max_value=game_state['max_number'],
                value=None,
                placeholder=f"1부터 {game_state['max_number']} 사이의 숫자를 입력하세요",
                key=input_key
            )
            guess_button = st.form_submit_button("🎯 추측하기!", type="primary", use_container_width=True)
        
        # 🚀 입력창 자동 포커스
        st.markdown(f"""
        <script>
        setTimeout(function() {{
            var el = document.querySelector('input[id*="{input_key}"]');
            if (el) {{
                el.focus();
                el.select();
            }}
        }}, 100);
        </script>
        """, unsafe_allow_html=True)
        
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
                    game_state["last_result"] = f'<div class="result-success">🎉 정답입니다!!</div>'
                elif game_state["attempts_left"] <= 0:
                    game_state["game_over"] = True
                    game_state["guess_history"].append((user_guess, "fail"))
                    game_state["last_result"] = f'<div class="result-fail">💀 게임 오버! 정답은 {game_state["secret"]}이었습니다!</div>'
                elif user_guess < game_state["secret"]:
                    game_state["guess_history"].append((user_guess, "up"))
                    game_state["last_result"] = f'<div class="result-hint">📈 {user_guess}보다 큰 숫자!</div>'
                else:
                    game_state["guess_history"].append((user_guess, "down"))
                    game_state["last_result"] = f'<div class="result-hint">📉 {user_guess}보다 작은 숫자!</div>'
                
                st.session_state.game_state = game_state
                if not game_state["game_over"]:
                    clear_input()
                st.rerun()
    
    else:
        st.markdown(game_state["last_result"], unsafe_allow_html=True)
        if any(g == game_state["secret"] for g, t in game_state["guess_history"] if t=="correct"):
            st.balloons()
        if st.button("🔄 새 게임 시작", use_container_width=True):
            reset_game()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

