import streamlit as st

# 문제 저장소 (세션 상태로 관리)
if 'problem_set' not in st.session_state:
    st.session_state['problem_set'] = set()

if 'attempts' not in st.session_state:
    st.session_state['attempts'] = []

# 문제 풀기에서 선택된 버튼을 관리하는 상태 변수
if 'selected_buttons' not in st.session_state:
    st.session_state['selected_buttons'] = set()

# 각 버튼의 상태를 추적하기 위한 변수
if 'button_states' not in st.session_state:
    st.session_state['button_states'] = {}

# 탭 설정
tab1, tab2 = st.tabs(["문제 만들기", "문제 풀기"])

# 탭 1: 문제 만들기
with tab1:
    st.header("문제 만들기")
    st.write("3x3 버튼에서 문제로 낼 칸을 선택하세요.")

    # 3x3 버튼 생성
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            key = f"prob-{i}-{j}"
            
            # 버튼 상태를 세션 상태에 저장하여 상태를 추적
            if key not in st.session_state['button_states']:
                st.session_state['button_states'][key] = False

            # 버튼 클릭 이벤트에 따라 상태 변경
            if st.session_state['button_states'][key]:
                if cols[j].button("🔴", key=key):
                    st.session_state['problem_set'].remove((i, j))
                    st.session_state['button_states'][key] = False
            else:
                if cols[j].button("⬜", key=key):
                    st.session_state['problem_set'].add((i, j))
                    st.session_state['button_states'][key] = True

    st.write("현재 선택된 문제 칸:", st.session_state['problem_set'])
    
    # 문제 저장 버튼
    if st.button("문제 저장하기"):
        st.success("문제가 저장되었습니다!")

# 탭 2: 문제 풀기
with tab2:
    st.header("문제 풀기")
    st.write("문제의 정답을 맞춰보세요.")

    # 3x3 버튼 생성
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            key = f"ans-{i}-{j}"
            
            # 버튼 상태를 세션 상태에 저장하여 상태를 추적
            if key not in st.session_state['button_states']:
                st.session_state['button_states'][key] = False

            # 버튼 클릭 이벤트에 따라 상태 변경
            if st.session_state['button_states'][key]:
                if cols[j].button("🟩", key=key):
                    st.session_state['selected_buttons'].remove((i, j))
                    st.session_state['button_states'][key] = False
            else:
                if cols[j].button("⬜", key=key):
                    st.session_state['selected_buttons'].add((i, j))
                    st.session_state['button_states'][key] = True

    # 점수 계산 및 결과 표시
    if st.button("확인하기"):
        score = 0
        for button in st.session_state['selected_buttons']:
            if button in st.session_state['problem_set']:
                score += 3  # 정답 칸
            else:
                score -= 1  # 오답 칸
        
        # 시도 횟수 및 점수 저장
        st.session_state['attempts'].append({"score": score, "attempt": st.session_state['selected_buttons'].copy()})
        st.write(f"점수: {score}점")

    # 시도 기록 및 점수 표시
    st.write("### 시도 기록")
    for idx, attempt in enumerate(st.session_state['attempts']):
        st.write(f"시도 {idx + 1}: 점수 {attempt['score']}점, 선택된 칸: {attempt['attempt']}")

    # 다시 도전하기 버튼
    if st.button("다시 도전하기"):
        st.session_state['selected_buttons'].clear()
        for key in st.session_state['button_states']:
            if key.startswith("ans-"):
                st.session_state['button_states'][key] = False
        st.experimental_rerun()  # 페이지 새로고침으로 다시 도전

# 전체 페이지 스타일 조정
st.sidebar.title("게임 설명")
st.sidebar.write("이 게임은 사용자가 만든 문제를 풀며 강화학습의 기초 개념을 학습하는 게임입니다.")
