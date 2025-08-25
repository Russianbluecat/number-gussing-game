import streamlit as st
import random
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# 상수 정의
class GameConfig:
    MIN_RANGE = 10
    MAX_RANGE = 1000
    MIN_ATTEMPTS = 3
    MAX_ATTEMPTS = 15
    DEFAULT_MAX_NUMBER = 100
    DEFAULT_MAX_ATTEMPTS = 5

# 페이지 설정
st.set_page_config(
    page_title=" 숫자 맞추기 게임",
    page_icon="🎯",
    layout="centered"
)

# CSS 스타일 (한 번만 로드)
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
    
    .main {
        padding-top: 1rem;
    }
    
    .game-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: fadeIn 0.5s ease-in;
    }
    
    .game-stats {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid var(--info-color);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    
    .game-stats:hover {
        transform: translateY(-2px);
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
        animation: slideIn 0.3s ease;
    }
    
    .message {
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
        font-weight: bold;
        animation: fadeIn 0.4s ease;
    }
    
    .message-success {
        background: #d4edda;
        color: #155724;
        border-left: 4px solid var(--success-color);
    }
    
    .message-hint {
        background: #fff3cd;
        color: #856404;
        border-left: 4px solid var(--warning-color);
    }
    
    .message-error {
        background: #f8d7da;
        color: #721c24;
        border-left: 4px solid var(--danger-color);
    }
    
    .message-info {
        background: #d1ecf1;
        color: #0c5460;
        border-left: 4px solid var(--info-color);
    }
    
    .attempts-remaining {
        background: linear-gradient(45deg, #ff6b6b, #ee5a52);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        text-align: center;
        font-weight: bold;
        margin: 15px 0;
        animation: pulse 2s infinite;
    }
    
    .difficulty-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        color: white;
        font-size: 0.9rem;
        font-weight: bold;
        margin: 5px;
    }
    
    .difficulty-easy { background: var(--success-color); }
    .difficulty-medium { background: var(--warning-color); }
    .difficulty-hard { background: var(--danger-color); }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideIn {
        from { transform: translateY(-10px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    </style>
    """

class GameStats:
    """게임 통계 관리 클래스"""
    
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
    """입력 검증 클래스"""
    
    @staticmethod
    def validate_guess(user_input, max_number, previous_guesses):
        try:
            guess = int(user_input)
            
            if guess < 1 or guess > max_number:
                return False, f"1부터 {max_number} 사이의 숫자를 입력해주세요!"
            
            if guess in previous_guesses:
                return False, f"{guess}은(는) 이미 시도한 숫자입니다!"
            
            return True, guess
            
        except (ValueError, TypeError):
            return False, "올바른 숫자를 입력해주세요!"

def initialize_session_state():
    """게임 상태 초기화"""
    defaults = {
        'game_active': False,
        'target_number': None,
        'max_number': GameConfig.DEFAULT_MAX_NUMBER,
        'max_attempts': GameConfig.DEFAULT_MAX_ATTEMPTS,
        'current_attempts': 0,
        'guesses': [],
        'game_won': False,
        'game_over': False,
        'message': "",
        'message_type': "info",
        'total_games': 0,
        'total_wins': 0,
        'game_history': [],
        'best_score': None,
        'show_hint': False,
        'difficulty_preset': 'custom'
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def start_new_game():
    """새 게임 시작"""
    st.session_state.target_number = random.randint(1, st.session_state.max_number)
    st.session_state.game_active = True
    st.session_state.current_attempts = 0
    st.session_state.guesses = []
    st.session_state.game_won = False
    st.session_state.game_over = False
    st.session_state.show_hint = False
    
    difficulty_text, _ = GameStats.calculate_difficulty(
        st.session_state.max_number, 
        st.session_state.max_attempts
    )
    
    st.session_state.message = f"🎯 게임 시작! (난이도: {difficulty_text})"
    st.session_state.message_type = "info"

def make_guess(guess):
    """추측 처리 및 게임 로직"""
    st.session_state.current_attempts += 1
    st.session_state.guesses.append(guess)
    
    if guess == st.session_state.target_number:
        # 정답!
        st.session_state.game_won = True
        st.session_state.game_over = True
        st.session_state.game_active = False
        st.session_state.total_games += 1
        st.session_state.total_wins += 1
        
        # 최고 기록 업데이트
        if (st.session_state.best_score is None or 
            st.session_state.current_attempts < st.session_state.best_score):
            st.session_state.best_score = st.session_state.current_attempts
        
        # 게임 히스토리 추가
        game_record = {
            'date': datetime.now().isoformat(),
            'attempts': st.session_state.current_attempts,
            'max_attempts': st.session_state.max_attempts,
            'max_number': st.session_state.max_number,
            'won': True,
            'target': st.session_state.target_number
        }
        st.session_state.game_history.append(game_record)
        
        st.session_state.message = f"🎉 축하합니다! {st.session_state.current_attempts}번 만에 정답!"
        st.session_state.message_type = "success"
        
    elif st.session_state.current_attempts >= st.session_state.max_attempts:
        # 게임 오버
        st.session_state.game_over = True
        st.session_state.game_active = False
        st.session_state.total_games += 1
        
        game_record = {
            'date': datetime.now().isoformat(),
            'attempts': st.session_state.current_attempts,
            'max_attempts': st.session_state.max_attempts,
            'max_number': st.session_state.max_number,
            'won': False,
            'target': st.session_state.target_number
        }
        st.session_state.game_history.append(game_record)
        
        st.session_state.message = f"💔 게임 오버! 정답: {st.session_state.target_number}"
        st.session_state.message_type = "error"
        
    else:
        # 힌트 제공
        if guess < st.session_state.target_number:
            st.session_state.message = f"📈 UP! {guess}보다 큽니다."
        else:
            st.session_state.message = f"📉 DOWN! {guess}보다 작습니다."
        
        st.session_state.message_type = "hint"
        
        # 절반 이상 시도했을 때 추가 힌트 활성화
        if st.session_state.current_attempts >= st.session_state.max_attempts // 2:
            st.session_state.show_hint = True

def get_smart_hint():
    """스마트 힌트 생성"""
    if not st.session_state.guesses:
        return ""
    
    target = st.session_state.target_number
    guesses = st.session_state.guesses
    
    # 범위 힌트
    lower_bound = max([g for g in guesses if g < target] + [0])
    upper_bound = min([g for g in guesses if g > target] + [st.session_state.max_number + 1])
    
    if lower_bound > 0 and upper_bound <= st.session_state.max_number:
        return f"💡 범위 힌트: {lower_bound + 1} ~ {upper_bound - 1} 사이에 있습니다!"
    elif lower_bound > 0:
        return f"💡 범위 힌트: {lower_bound + 1}보다 큽니다!"
    elif upper_bound <= st.session_state.max_number:
        return f"💡 범위 힌트: {upper_bound - 1}보다 작습니다!"
    
    return ""

def render_game_header():
    """게임 헤더 렌더링"""
    st.markdown("""
    <div class="game-header">
        <h1>🎯 숫자 맞추기 게임</h1>
        <p>컴퓨터가 선택한 숫자를 맞춰보세요!</p>
    </div>
    """, unsafe_allow_html=True)

def render_game_stats():
    """향상된 게임 통계"""
    if st.session_state.total_games > 0:
        win_rate = (st.session_state.total_wins / st.session_state.total_games) * 100
        achievement = GameStats.get_achievement_level(win_rate, st.session_state.total_games)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 게임", st.session_state.total_games)
        
        with col2:
            st.metric("승리", st.session_state.total_wins)
        
        with col3:
            st.metric("승률", f"{win_rate:.1f}%")
        
        with col4:
            st.metric("최고 기록", f"{st.session_state.best_score}번" if st.session_state.best_score else "없음")
        
        st.markdown(f"""
        <div class="game-stats">
            <strong>🏅 달성도: {achievement}</strong>
        </div>
        """, unsafe_allow_html=True)

def render_difficulty_presets():
    """난이도 프리셋"""
    st.markdown("### 🎮 난이도 선택")
    
    presets = {
        'easy': {'name': '🌟 쉬움', 'max_number': 50, 'max_attempts': 7},
        'medium': {'name': '⚡ 보통', 'max_number': 100, 'max_attempts': 5},
        'hard': {'name': '🔥 어려움', 'max_number': 200, 'max_attempts': 4},
        'expert': {'name': '💀 전문가', 'max_number': 500, 'max_attempts': 3},
        'custom': {'name': '⚙️ 사용자 설정', 'max_number': None, 'max_attempts': None}
    }
    
    preset_options = [presets[key]['name'] for key in presets.keys()]
    preset_keys = list(presets.keys())
    
    selected_preset = st.selectbox(
        "난이도를 선택하세요:",
        options=preset_options,
        index=preset_keys.index(st.session_state.difficulty_preset)
    )
    
    selected_key = preset_keys[preset_options.index(selected_preset)]
    st.session_state.difficulty_preset = selected_key
    
    if selected_key != 'custom':
        preset = presets[selected_key]
        st.session_state.max_number = preset['max_number']
        st.session_state.max_attempts = preset['max_attempts']
        
        difficulty_text, difficulty_class = GameStats.calculate_difficulty(
            st.session_state.max_number, st.session_state.max_attempts
        )
        
        st.markdown(f"""
        <span class="difficulty-badge difficulty-{difficulty_class}">
            범위: 1-{st.session_state.max_number}, 시도: {st.session_state.max_attempts}번
        </span>
        """, unsafe_allow_html=True)
    
    return selected_key == 'custom'

def render_custom_settings():
    """사용자 정의 설정"""
    st.markdown("### ⚙️ 사용자 설정")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_number = st.slider(
            "최대 숫자 범위",
            min_value=GameConfig.MIN_RANGE,
            max_value=GameConfig.MAX_RANGE,
            value=st.session_state.max_number,
            step=10
        )
        st.session_state.max_number = max_number
    
    with col2:
        max_attempts = st.slider(
            "최대 시도 횟수",
            min_value=GameConfig.MIN_ATTEMPTS,
            max_value=GameConfig.MAX_ATTEMPTS,
            value=st.session_state.max_attempts,
            step=1
        )
        st.session_state.max_attempts = max_attempts
    
    difficulty_text, difficulty_class = GameStats.calculate_difficulty(max_number, max_attempts)
    st.markdown(f"""
    <span class="difficulty-badge difficulty-{difficulty_class}">
        예상 난이도: {difficulty_text}
    </span>
    """, unsafe_allow_html=True)

def render_current_game():
    """현재 게임 진행 상황"""
    # 진행률 표시
    progress = st.session_state.current_attempts / st.session_state.max_attempts
    st.progress(progress)
    
    # 남은 시도 횟수
    remaining_attempts = st.session_state.max_attempts - st.session_state.current_attempts
    st.markdown(f"""
    <div class="attempts-remaining">
        🎯 남은 기회: {remaining_attempts}번 / {st.session_state.max_attempts}번
    </div>
    """, unsafe_allow_html=True)
    
    # 추측 히스토리 시각화
    if st.session_state.guesses:
        st.markdown("### 📊 추측 히스토리")
        
        # 시각적 표시
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(range(1, len(st.session_state.guesses) + 1)),
            y=st.session_state.guesses,
            mode='lines+markers',
            name='추측값',
            line=dict(color='blue', width=3),
            marker=dict(size=10)
        ))
        
        if not st.session_state.game_over:
            fig.add_hline(
                y=st.session_state.target_number, 
                line_dash="dash", 
                line_color="red",
                annotation_text="정답 (게임 종료 후 공개)"
            )
        else:
            fig.add_hline(
                y=st.session_state.target_number, 
                line_dash="dash", 
                line_color="red",
                annotation_text=f"정답: {st.session_state.target_number}"
            )
        
        fig.update_layout(
            title="추측 패턴",
            xaxis_title="시도 횟수",
            yaxis_title="추측값",
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 텍스트 히스토리
        guesses_text = " → ".join([str(g) for g in st.session_state.guesses])
        st.markdown(f"""
        <div class="guess-display">
            {guesses_text}
        </div>
        """, unsafe_allow_html=True)
    
    # 메시지 및 힌트 표시
    if st.session_state.message:
        st.markdown(f"""
        <div class="message message-{st.session_state.message_type}">
            {st.session_state.message}
        </div>
        """, unsafe_allow_html=True)
    
    # 스마트 힌트
    if st.session_state.show_hint and not st.session_state.game_over:
        hint = get_smart_hint()
        if hint:
            st.markdown(f"""
            <div class="message message-info">
                {hint}
            </div>
            """, unsafe_allow_html=True)

def render_game_history():
    """게임 히스토리 표시"""
    if st.session_state.game_history:
        with st.expander("📈 게임 히스토리", expanded=False):
            recent_games = st.session_state.game_history[-10:]  # 최근 10게임
            
            # 성과 트렌드 차트
            attempts_data = [game['attempts'] for game in recent_games if game['won']]
            if attempts_data:
                fig = px.line(
                    y=attempts_data,
                    title="최근 승리 게임의 시도 횟수 트렌드",
                    labels={'index': '게임 순서', 'y': '시도 횟수'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # 게임 목록
            for i, game in enumerate(reversed(recent_games)):
                date = datetime.fromisoformat(game['date']).strftime("%m/%d %H:%M")
                status = "🏆 승리" if game['won'] else "❌ 패배"
                st.write(f"**{len(recent_games)-i}.** {date} | {status} | "
                        f"{game['attempts']}/{game['max_attempts']}번 | "
                        f"범위: 1-{game['max_number']}")

def main():
    """메인 애플리케이션"""
    # CSS 적용
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # 세션 상태 초기화
    initialize_session_state()
    
    # 게임 헤더
    render_game_header()
    
    # 게임 통계
    render_game_stats()
    
    # 게임이 활성화되지 않은 경우
    if not st.session_state.game_active:
        show_custom = render_difficulty_presets()
        
        if show_custom:
            render_custom_settings()
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎮 게임 시작!", type="primary", use_container_width=True):
            start_new_game()
            st.rerun()
        
        # 게임 히스토리
        render_game_history()
    
    # 게임 진행 중
    else:
        render_current_game()
        
        # 입력 폼 (게임이 진행 중일 때만)
        if not st.session_state.game_over:
            with st.form(key="guess_form", clear_on_submit=True):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    user_input = st.number_input(
                        f"숫자 입력 (1-{st.session_state.max_number})",
                        min_value=1,
                        max_value=st.session_state.max_number,
                        key="guess_input",
                        help="Enter 키를 눌러도 제출됩니다!"
                    )
                
                with col2:
                    submitted = st.form_submit_button("🎯 제출", use_container_width=True)
                
                if submitted and user_input is not None:
                    is_valid, result = GameValidator.validate_guess(
                        user_input, st.session_state.max_number, st.session_state.guesses
                    )
                    
                    if is_valid:
                        make_guess(result)
                        st.rerun()
                    else:
                        st.error(result)
        
        # 게임 종료 후 옵션
        if st.session_state.game_over:
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 다시 하기", type="primary", use_container_width=True):
                    start_new_game()
                    st.rerun()
            
            with col2:
                if st.button("⚙️ 설정 변경", use_container_width=True):
                    st.session_state.game_active = False
                    st.session_state.message = ""
                    st.rerun()
            
            with col3:
                if st.button("📊 통계 보기", use_container_width=True):
                    st.session_state.show_stats = not st.session_state.get('show_stats', False)
                    st.rerun()
    
    # 푸터
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "🎯 개선된 숫자 맞추기 게임 v2.0 | Made with Streamlit & ❤️"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
