"""
Streamlit Quiz Multiplayer em Tempo Real com Ranking Final.
Permite múltiplos jogadores competirem em salas simultâneas em diversos temas.
"""

import streamlit as st
import time
import uuid
import urllib.parse
import database as db
import questions as qm

# Configuração da página Streamlit
st.set_page_config(
    page_title="QuizMaster Multiplayer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada
st.markdown("""
<style>
    /* Estilos gerais */
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4F46E5, #9333EA, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    
    /* Cartões de Questão */
    .question-card {
        background-color: rgba(79, 70, 229, 0.08);
        border: 2px solid rgba(79, 70, 229, 0.2);
        border-radius: 12px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
    }
    .question-header {
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #4F46E5;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .question-text {
        font-size: 1.35rem;
        font-weight: 700;
        line-height: 1.4;
        color: inherit;
    }
    
    /* Pódio de Vencedores */
    .podium-container {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 1.5rem;
        margin: 2rem 0;
    }
    .podium-card {
        border-radius: 12px;
        padding: 1.5rem 1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        min-width: 170px;
    }
    .podium-1 {
        background: linear-gradient(135deg, #FDE68A 0%, #F59E0B 100%);
        color: #78350F;
        border: 3px solid #D97706;
        height: 220px;
        order: 2;
    }
    .podium-2 {
        background: linear-gradient(135deg, #E5E7EB 0%, #9CA3AF 100%);
        color: #1F2937;
        border: 3px solid #6B7280;
        height: 190px;
        order: 1;
    }
    .podium-3 {
        background: linear-gradient(135deg, #FED7AA 0%, #D97706 100%);
        color: #451A03;
        border: 3px solid #B45309;
        height: 170px;
        order: 3;
    }
    .podium-avatar {
        font-size: 2.8rem;
        margin-bottom: 0.3rem;
    }
    .podium-name {
        font-weight: 800;
        font-size: 1.1rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .podium-score {
        font-size: 1.25rem;
        font-weight: 900;
        margin-top: 0.3rem;
    }

    /* Badges */
    .badge-category {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        background-color: #EEF2FF;
        color: #4338CA;
    }
</style>
""", unsafe_allow_html=True)

# Lista de Avatares disponíveis
AVATARS = ["🦊 Raposa", "🚀 Astronauta", "🧙‍♂️ Mago", "🎯 Mestre", "🐯 Tigre", "🤖 Robô", "🦁 Leão", "🦄 Unicórnio", "⚡ Relâmpago", "👑 Coroa"]

# Inicialização de Session State
if "player_id" not in st.session_state:
    st.session_state.player_id = str(uuid.uuid4())[:8]

if "nickname" not in st.session_state:
    random_suffix = st.session_state.player_id[:4]
    st.session_state.nickname = f"Player_{random_suffix}"

if "avatar" not in st.session_state:
    st.session_state.avatar = "🦊 Raposa"

if "room_code" not in st.session_state:
    st.session_state.room_code = None

if "game_phase" not in st.session_state:
    st.session_state.game_phase = "lobby"  # 'lobby', 'waiting', 'playing', 'finished'

if "current_question_idx" not in st.session_state:
    st.session_state.current_question_idx = 0

if "answered_current" not in st.session_state:
    st.session_state.answered_current = False

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None

if "question_start_time" not in st.session_state:
    st.session_state.question_start_time = time.time()


# -------------------------------------------------------------
# FUNÇÕES DE NAVEGAÇÃO E AÇÕES
# -------------------------------------------------------------
def handle_join_room(code: str, nickname: str, avatar: str):
    code_clean = code.strip().upper()
    if not code_clean:
        st.error("Por favor, informe o código da sala.")
        return
    if not nickname.strip():
        st.error("Por favor, informe seu apelido/nome.")
        return
    
    room = db.get_room(code_clean)
    if not room:
        st.error(f"Sala '{code_clean}' não encontrada. Verifique o código.")
        return
    
    clean_avatar = avatar.split()[0]
    db.join_room(code_clean, st.session_state.player_id, nickname.strip(), clean_avatar)
    st.session_state.room_code = code_clean
    st.session_state.nickname = nickname.strip()
    st.session_state.avatar = clean_avatar
    
    if room["status"] == "active":
        st.session_state.game_phase = "playing"
        st.session_state.current_question_idx = 0
        st.session_state.answered_current = False
        st.session_state.question_start_time = time.time()
    else:
        st.session_state.game_phase = "waiting"
    st.rerun()


def handle_create_room(name: str, code: str, category: str, num_questions: int, nickname: str, avatar: str):
    code_clean = code.strip().upper()
    name_clean = name.strip() if name.strip() else f"Sala de {nickname}"
    if not code_clean:
        st.error("Informe um código para a sala.")
        return
    if not nickname.strip():
        st.error("Informe seu apelido/nome.")
        return

    success = db.create_room(code_clean, name_clean, st.session_state.player_id, category, num_questions)
    if not success:
        st.error(f"Já existe uma sala com o código '{code_clean}'. Escolha outro código!")
        return
    
    clean_avatar = avatar.split()[0]
    db.join_room(code_clean, st.session_state.player_id, nickname.strip(), clean_avatar)
    st.session_state.room_code = code_clean
    st.session_state.nickname = nickname.strip()
    st.session_state.avatar = clean_avatar
    st.session_state.game_phase = "waiting"
    st.rerun()


def handle_exit_room():
    st.session_state.room_code = None
    st.session_state.game_phase = "lobby"
    st.session_state.current_question_idx = 0
    st.session_state.answered_current = False
    st.session_state.last_feedback = None
    st.rerun()


# -------------------------------------------------------------
# SIDEBAR: PERFIL DO JOGADOR & PLACAR EM TEMPO REAL
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### 👤 Seu Perfil")
    st.write(f"**ID da Sessão:** `{st.session_state.player_id}`")
    
    if st.session_state.game_phase == "lobby":
        st.session_state.nickname = st.text_input("Seu Nickname / Nome:", value=st.session_state.nickname)
        avatar_choice = st.selectbox("Escolha seu Avatar:", AVATARS, index=0)
        st.session_state.avatar = avatar_choice.split()[0]
    else:
        st.markdown(f"#### {st.session_state.avatar} **{st.session_state.nickname}**")
        st.info(f"**Sala Atual:** `{st.session_state.room_code}`")
        if st.button("🚪 Sair da Sala", use_container_width=True):
            handle_exit_room()

    if st.session_state.room_code:
        st.markdown("---")
        st.markdown("### 🏆 Placar ao Vivo")
        players = db.get_players_in_room(st.session_state.room_code)
        
        for idx, p in enumerate(players, start=1):
            is_me = p["player_id"] == st.session_state.player_id
            status_tag = "🏁 Terminou" if p["is_finished"] else f"Q{p['current_question_index']}"
            me_tag = " (Você)" if is_me else ""
            
            MarkdownStr = f"**{idx}º** {p['avatar']} **{p['nickname']}{me_tag}**  \n🎯 **{p['score']} pts** | {p['correct_answers']} acertos | `{status_tag}`"
            st.markdown(MarkdownStr)
            st.divider()


# -------------------------------------------------------------
# TELA 1: LOBBY (ENTRAR / CRIAR SALA)
# -------------------------------------------------------------
if st.session_state.game_phase == "lobby":
    st.markdown('<h1 class="main-title">🧠 QuizMaster Multiplayer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Desafie seus amigos em tempo real! Escolha uma sala ou crie uma nova para jogar juntos.</p>', unsafe_allow_html=True)

    tab_join, tab_create, tab_active = st.tabs(["🚀 Entrar em uma Sala", "➕ Criar Nova Sala", "📋 Salas Abertas"])

    with tab_join:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("#### Entrar com Código")
            join_code = st.text_input("Código da Sala (Ex: GERAL, AMIGOS):", placeholder="Código da sala").upper()
            if st.button("Entrar e Jogar 🎮", type="primary", use_container_width=True):
                handle_join_room(join_code, st.session_state.nickname, st.session_state.avatar)
        with col2:
            st.info("💡 **Dica:** Para jogar com amigos, todos devem digitar o mesmo código da sala!")

    with tab_create:
        st.markdown("#### Configurar Nova Sala")
        col_c1, col_c2 = st.columns(2)
        
        random_code = uuid.uuid4().hex[:4].upper()
        
        with col_c1:
            new_room_name = st.text_input("Nome da Sala:", value="Batalha dos Cérebros")
            new_room_code = st.text_input("Código da Sala:", value=f"SALA{random_code}").upper()
        
        with col_c2:
            new_category = st.selectbox("Categoria de Perguntas:", qm.CATEGORIES, index=0)
            new_num_q = st.slider("Número de Perguntas:", min_value=5, max_value=20, value=10, step=5)

        if st.button("Criar Sala e Ir para Sala de Espera ✨", type="primary", use_container_width=True):
            handle_create_room(new_room_name, new_room_code, new_category, new_num_q, st.session_state.nickname, st.session_state.avatar)

    with tab_active:
        st.markdown("#### Salas Disponíveis")
        rooms = db.get_active_rooms()
        if not rooms:
            st.write("Nenhuma sala aberta no momento. Crie uma na aba ao lado!")
        else:
            for r in rooms:
                c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
                with c1:
                    st.markdown(f"**{r['room_name']}** (`{r['room_code']}`)")
                with c2:
                    st.caption(f"Tema: {r['category']} | {r['num_questions']} perguntas")
                with c3:
                    st.caption(f"👥 {r['player_count']} jogadores")
                with c4:
                    if st.button("Entrar", key=f"join_list_{r['room_code']}"):
                        handle_join_room(r['room_code'], st.session_state.nickname, st.session_state.avatar)
                st.divider()


# -------------------------------------------------------------
# TELA 2: SALA DE ESPERA (WAITING ROOM)
# -------------------------------------------------------------
elif st.session_state.game_phase == "waiting":
    room = db.get_room(st.session_state.room_code)
    if not room:
        st.error("Sala não encontrada.")
        if st.button("Voltar ao Lobby"):
            handle_exit_room()
        st.stop()

    if room["status"] == "active":
        st.session_state.game_phase = "playing"
        st.session_state.current_question_idx = 0
        st.session_state.answered_current = False
        st.session_state.question_start_time = time.time()
        st.rerun()

    is_host = room["host_player_id"] == st.session_state.player_id
    players = db.get_players_in_room(st.session_state.room_code)

    st.markdown(f'<h1 class="main-title">⏳ Sala de Espera: {room["room_name"]}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">Código da Sala: <strong style="color: #4F46E5; font-size: 1.3rem;">{room["room_code"]}</strong></p>', unsafe_allow_html=True)

    col_meta1, col_meta2, col_meta3 = st.columns(3)
    col_meta1.metric("Tema", room["category"])
    col_meta2.metric("Total de Perguntas", room["num_questions"])
    col_meta3.metric("Jogadores Conectados", len(players))

    st.markdown("### 👥 Jogadores Conectados")
    player_cols = st.columns(4)
    for idx, p in enumerate(players):
        with player_cols[idx % 4]:
            host_tag = " 👑 (Anfitrião)" if p["player_id"] == room["host_player_id"] else ""
            st.success(f"{p['avatar']} **{p['nickname']}**{host_tag}")

    st.markdown("---")
    
    # Adicionada funcionalidade de convidar por e-mail com o link de acesso/aplicação
    st.markdown("### 📧 Convidar Amigos por E-mail")
    col_mail1, col_mail2 = st.columns([2, 1])
    with col_mail1:
        friend_email = st.text_input("E-mail do amigo:", placeholder="amigo@email.com", key="invite_email_input")
    with col_mail2:
        st.markdown("<br>", unsafe_allow_html=True)
        if friend_email:
            app_url = st.get_option("browser.serverAddress") or "localhost:8501"
            access_link = f"http://{app_url}"
            email_subject = "Convite para Batalha de Quiz no QuizMaster!"
            email_body = f"Olá! Venha jogar comigo no QuizMaster.\nAcesse o link: {access_link}\nE utilize o código da sala: {room['room_code']}"
            mail_to_link = f"mailto:{friend_email}?subject={urllib.parse.quote(email_subject)}&body={urllib.parse.quote(email_body)}"
            st.markdown(f'<a href="{mail_to_link}" target="_blank"><button style="background-color:#4F46E5;color:white;padding:0.6rem 1rem;border:none;border-radius:8px;font-weight:bold;cursor:pointer;width:100%;">📨 Enviar Convite</button></a>', unsafe_allow_html=True)
        else:
            st.button("📨 Enviar Convite", disabled=True, use_container_width=True)

    st.markdown("---")
    c_btn1, c_btn2 = st.columns([2, 1])

    with c_btn1:
        if is_host:
            st.info("Você é o anfitrião desta sala! Quando todos entrarem, clique no botão abaixo para iniciar.")
            if st.button("🚀 Iniciar Quiz para Todos!", type="primary", use_container_width=True):
                db.start_room(st.session_state.room_code)
                st.session_state.game_phase = "playing"
                st.session_state.current_question_idx = 0
                st.session_state.answered_current = False
                st.session_state.question_start_time = time.time()
                st.rerun()
        else:
            st.warning("Aguardando o anfitrião iniciar a partida... Clique em 'Atualizar' para verificar!")
            if st.button("🔄 Atualizar Status da Sala", use_container_width=True):
                st.rerun()

    with c_btn2:
        if st.button("🚪 Sair da Sala", use_container_width=True):
            handle_exit_room()


# -------------------------------------------------------------
# TELA 3: JOGO EM ANDAMENTO (QUIZ)
# -------------------------------------------------------------
elif st.session_state.game_phase == "playing":
    room = db.get_room(st.session_state.room_code)
    if not room:
        st.error("Sala não encontrada.")
        st.stop()

    questions = qm.get_questions_by_category(
        category=room["category"],
        limit=room["num_questions"],
        seed=room["seed"]
    )
    total_q = len(questions)
    curr_idx = st.session_state.current_question_idx

    if curr_idx >= total_q:
        db.set_player_finished(st.session_state.player_id)
        st.session_state.game_phase = "finished"
        st.rerun()

    q_data = questions[curr_idx]

    progress_val = (curr_idx) / total_q
    st.progress(progress_val, text=f"Pergunta {curr_idx + 1} de {total_q}")

    st.markdown(f"""
    <div class="question-card">
        <div class="question-header">
            <span class="badge-category">{q_data['categoria']}</span> &nbsp; • &nbsp; PERGUNTA {curr_idx + 1} DE {total_q}
        </div>
        <div class="question-text">{q_data['pergunta']}</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.answered_current:
        st.markdown("##### Escolha a sua resposta:")
        col_opts = st.columns(2)
        
        for i, opt in enumerate(q_data["opcoes"]):
            with col_opts[i % 2]:
                letter = chr(65 + i)
                btn_label = f"**{letter})** {opt}"
                if st.button(btn_label, key=f"opt_{curr_idx}_{i}", use_container_width=True):
                    time_taken = max(1.0, round(time.time() - st.session_state.question_start_time, 2))
                    is_correct = (opt == q_data["resposta"])
                    
                    speed_bonus = max(0, int(50 - (time_taken * 3))) if is_correct else 0
                    points_earned = (100 + speed_bonus) if is_correct else 0
                    
                    db.save_answer(
                        room_code=st.session_state.room_code,
                        player_id=st.session_state.player_id,
                        question_id=q_data["id"],
                        question_text=q_data["pergunta"],
                        chosen_answer=opt,
                        correct_answer=q_data["resposta"],
                        is_correct=is_correct,
                        points=points_earned,
                        time_taken=time_taken
                    )
                    
                    st.session_state.last_feedback = {
                        "is_correct": is_correct,
                        "chosen": opt,
                        "correct": q_data["resposta"],
                        "explanation": q_data["explicacao"],
                        "points": points_earned,
                        "time_taken": time_taken
                    }
                    st.session_state.answered_current = True
                    st.rerun()

    else:
        fb = st.session_state.last_feedback
        if fb["is_correct"]:
            st.success(f"🎉 **Resposta Correta!** Você ganhou **+{fb['points']} pontos** em {fb['time_taken']}s!")
        else:
            st.error(f"❌ **Resposta Incorreta!** A resposta certa era: **{fb['correct']}**.")
            st.caption(f"Sua resposta: {fb['chosen']}")

        st.info(f"💡 **Curiosidade:** {fb['explanation']}")

        is_last = (curr_idx + 1 >= total_q)
        btn_next_label = "🏆 Ver Resultado Final!" if is_last else "Próxima Pergunta ➡️"
        
        if st.button(btn_next_label, type="primary", use_container_width=True):
            st.session_state.current_question_idx += 1
            st.session_state.answered_current = False
            st.session_state.question_start_time = time.time()
            st.rerun()


# -------------------------------------------------------------
# TELA 4: RANKING FINAL & PÓDIO
# -------------------------------------------------------------
elif st.session_state.game_phase == "finished":
    room = db.get_room(st.session_state.room_code)
    leaderboard = db.get_room_leaderboard(st.session_state.room_code)
    
    st.markdown('<h1 class="main-title">🏆 Ranking Final do Quiz</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">Sala: <strong>{room["room_name"]}</strong> (`{room["room_code"]}`)</p>', unsafe_allow_html=True)

    if "balloons_shown" not in st.session_state:
        st.balloons()
        st.session_state.balloons_shown = True

    if len(leaderboard) >= 1:
        top1 = leaderboard[0]
        top2 = leaderboard[1] if len(leaderboard) > 1 else None
        top3 = leaderboard[2] if len(leaderboard) > 2 else None

        col_p2, col_p1, col_p3 = st.columns([1, 1.2, 1])

        with col_p2:
            if top2:
                st.markdown(f"""
                <div class="podium-card podium-2">
                    <div style="font-size: 1.5rem; font-weight: 800;">🥈 2º Lugar</div>
                    <div class="podium-avatar">{top2['avatar']}</div>
                    <div class="podium-name">{top2['nickname']}</div>
                    <div class="podium-score">{top2['score']} pts</div>
                    <div style="font-size: 0.85rem;">{top2['correct_answers']} acertos</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.write("")

        with col_p1:
            st.markdown(f"""
            <div class="podium-card podium-1">
                <div style="font-size: 1.8rem; font-weight: 900;">🥇 CAMPEÃO</div>
                <div class="podium-avatar">{top1['avatar']}</div>
                <div class="podium-name">{top1['nickname']}</div>
                <div class="podium-score">{top1['score']} pts</div>
                <div style="font-size: 0.9rem;">{top1['correct_answers']} acertos • {top1['total_time_seconds']:.1f}s</div>
            </div>
            """, unsafe_allow_html=True)

        with col_p3:
            if top3:
                st.markdown(f"""
                <div class="podium-card podium-3">
                    <div style="font-size: 1.4rem; font-weight: 800;">🥉 3º Lugar</div>
                    <div class="podium-avatar">{top3['avatar']}</div>
                    <div class="podium-name">{top3['nickname']}</div>
                    <div class="podium-score">{top3['score']} pts</div>
                    <div style="font-size: 0.85rem;">{top3['correct_answers']} acertos</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.write("")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 📊 Classificação Geral de Todos os Jogadores")
    table_data = []
    for rank, p in enumerate(leaderboard, start=1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}º"
        is_me = " (Você)" if p["player_id"] == st.session_state.player_id else ""
        table_data.append({
            "Posição": medal,
            "Avatar": p["avatar"],
            "Jogador": f"{p['nickname']}{is_me}",
            "Pontuação": f"{p['score']} pts",
            "Acertos": f"{p['correct_answers']}/{room['num_questions']}",
            "Tempo Total": f"{p['total_time_seconds']:.1f}s",
            "Status": "Concluído ✅" if p["is_finished"] else "Em andamento ⏳"
        })

    st.dataframe(table_data, use_container_width=True, hide_index=True)

    with st.expander("📝 Ver Revisão das Suas Respostas", expanded=False):
        history = db.get_player_history(st.session_state.room_code, st.session_state.player_id)
        if not history:
            st.write("Nenhuma resposta registrada.")
        else:
            for idx, ans in enumerate(history, start=1):
                icon = "✅" if ans["is_correct"] else "❌"
                st.markdown(f"**{idx}. {ans['question_text']}**")
                st.markdown(f"- Sua resposta: `{ans['chosen_answer']}` {icon}")
                if not ans["is_correct"]:
                    st.markdown(f"- Resposta correta: **{ans['correct_answer']}**")
                st.caption(f"Pontos obtidos: +{ans['points_awarded']} | Tempo: {ans['time_taken_seconds']:.1f}s")
                st.divider()

    st.markdown("---")
    c_act1, c_act2, c_act3 = st.columns(3)
    
    with c_act1:
        if st.button("🔄 Atualizar Ranking (Ver novos finalistas)", use_container_width=True):
            st.rerun()

    with c_act2:
        is_host = room["host_player_id"] == st.session_state.player_id
        if is_host:
            if st.button("🔁 Reiniciar Partida nesta Sala", type="primary", use_container_width=True):
                db.reset_room_game(st.session_state.room_code)
                st.session_state.game_phase = "waiting"
                st.session_state.current_question_idx = 0
                st.session_state.answered_current = False
                st.session_state.last_feedback = None
                if "balloons_shown" in st.session_state:
                    del st.session_state["balloons_shown"]
                st.rerun()

    with c_act3:
        if st.button("🚪 Voltar ao Lobby Inicial", use_container_width=True):
            if "balloons_shown" in st.session_state:
                del st.session_state["balloons_shown"]
            handle_exit_room()
