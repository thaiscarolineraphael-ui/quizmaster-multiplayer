"""
Módulo de Banco de Dados SQLite para sincronização multiplayer do Quiz Streamlit.
Permite múltiplas abas/navegadores jogarem na mesma sala e disputarem o ranking.
"""

import sqlite3
import time
import os
import random
from typing import List, Dict, Optional, Any

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz_multiplayer.db")


def get_connection():
    """Retorna uma conexão SQLite com timeout e WAL mode para suporte concorrente."""
    conn = sqlite3.connect(DB_PATH, timeout=15.0)
    conn.execute("PRAGMA journal_mode = WAL")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inicializa as tabelas do banco de dados se não existirem."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Tabela de Salas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                room_code TEXT PRIMARY KEY,
                room_name TEXT NOT NULL,
                host_player_id TEXT NOT NULL,
                category TEXT NOT NULL,
                num_questions INTEGER NOT NULL,
                seed INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'waiting', -- 'waiting', 'active', 'finished'
                created_at REAL NOT NULL
            )
        """)
        
        # Tabela de Jogadores na sala
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                player_id TEXT PRIMARY KEY,
                room_code TEXT NOT NULL,
                nickname TEXT NOT NULL,
                avatar TEXT NOT NULL,
                score INTEGER NOT NULL DEFAULT 0,
                correct_answers INTEGER NOT NULL DEFAULT 0,
                current_question_index INTEGER NOT NULL DEFAULT 0,
                is_finished INTEGER NOT NULL DEFAULT 0,
                total_time_seconds REAL NOT NULL DEFAULT 0.0,
                joined_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                FOREIGN KEY (room_code) REFERENCES rooms (room_code) ON DELETE CASCADE
            )
        """)
        
        # Tabela de Respostas individuais
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_code TEXT NOT NULL,
                player_id TEXT NOT NULL,
                question_id INTEGER NOT NULL,
                question_text TEXT,
                chosen_answer TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                is_correct INTEGER NOT NULL,
                points_awarded INTEGER NOT NULL,
                time_taken_seconds REAL NOT NULL,
                answered_at REAL NOT NULL
            )
        """)
        conn.commit()


def create_room(room_code: str, room_name: str, host_id: str, category: str, num_questions: int) -> bool:
    """Cria uma nova sala de quiz."""
    clean_code = room_code.strip().upper()
    seed = random.randint(1000, 999999)
    now = time.time()
    
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO rooms (room_code, room_name, host_player_id, category, num_questions, seed, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, 'waiting', ?)
            """, (clean_code, room_name.strip(), host_id, category, num_questions, seed, now))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def get_room(room_code: str) -> Optional[Dict[str, Any]]:
    """Busca dados de uma sala específica."""
    clean_code = room_code.strip().upper()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE room_code = ?", (clean_code,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None


def get_active_rooms() -> List[Dict[str, Any]]:
    """Lista todas as salas ativas ou aguardando jogadores."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, COUNT(p.player_id) as player_count 
            FROM rooms r
            LEFT JOIN players p ON r.room_code = p.room_code
            GROUP BY r.room_code
            ORDER BY r.created_at DESC
        """)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


def join_room(room_code: str, player_id: str, nickname: str, avatar: str) -> bool:
    """Insere ou atualiza um jogador na sala."""
    clean_code = room_code.strip().upper()
    now = time.time()
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Verifica se sala existe
        cursor.execute("SELECT status FROM rooms WHERE room_code = ?", (clean_code,))
        room = cursor.fetchone()
        if not room:
            return False
            
        cursor.execute("""
            INSERT INTO players (player_id, room_code, nickname, avatar, score, correct_answers, 
                                current_question_index, is_finished, total_time_seconds, joined_at, updated_at)
            VALUES (?, ?, ?, ?, 0, 0, 0, 0, 0.0, ?, ?)
            ON CONFLICT(player_id) DO UPDATE SET
                room_code = excluded.room_code,
                nickname = excluded.nickname,
                avatar = excluded.avatar,
                updated_at = excluded.updated_at
        """, (player_id, clean_code, nickname.strip(), avatar, now, now))
        conn.commit()
        return True


def get_players_in_room(room_code: str) -> List[Dict[str, Any]]:
    """Obtém a lista de jogadores de uma sala com scores e status."""
    clean_code = room_code.strip().upper()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM players 
            WHERE room_code = ?
            ORDER BY score DESC, total_time_seconds ASC
        """, (clean_code,))
        rows = cursor.fetchall()
        return [dict(r) for r in rows]


def start_room(room_code: str):
    """Muda o estado da sala para 'active' para iniciar a partida."""
    clean_code = room_code.strip().upper()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE rooms SET status = 'active' WHERE room_code = ?", (clean_code,))
        conn.commit()


def finish_room(room_code: str):
    """Marca a sala como finalizada."""
    clean_code = room_code.strip().upper()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE rooms SET status = 'finished' WHERE room_code = ?", (clean_code,))
        conn.commit()


def save_answer(room_code: str, player_id: str, question_id: int, question_text: str,
                chosen_answer: str, correct_answer: str, is_correct: bool, points: int, time_taken: float):
    """Registra uma resposta do jogador e atualiza pontuação."""
    clean_code = room_code.strip().upper()
    now = time.time()
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO answers (room_code, player_id, question_id, question_text, chosen_answer,
                                correct_answer, is_correct, points_awarded, time_taken_seconds, answered_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (clean_code, player_id, question_id, question_text, chosen_answer, 
              correct_answer, 1 if is_correct else 0, points, time_taken, now))
        
        # Atualiza dados acumulados do jogador
        cursor.execute("""
            UPDATE players
            SET score = score + ?,
                correct_answers = correct_answers + ?,
                current_question_index = current_question_index + 1,
                total_time_seconds = total_time_seconds + ?,
                updated_at = ?
            WHERE player_id = ?
        """, (points, 1 if is_correct else 0, time_taken, now, player_id))
        
        conn.commit()


def set_player_finished(player_id: str):
    """Marca um jogador individual como tendo concluído o quiz."""
    now = time.time()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE players
            SET is_finished = 1, updated_at = ?
            WHERE player_id = ?
        """, (now, player_id))
        conn.commit()


def get_player_history(room_code: str, player_id: str) -> List[Dict[str, Any]]:
    """Retorna o histórico de respostas do jogador naquela sala."""
    clean_code = room_code.strip().upper()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM answers 
            WHERE room_code = ? AND player_id = ?
            ORDER BY id ASC
        """, (clean_code, player_id))
        return [dict(r) for r in cursor.fetchall()]


def get_room_leaderboard(room_code: str) -> List[Dict[str, Any]]:
    """Retorna o ranking completo da sala ordenado por pontuação decrescente."""
    clean_code = room_code.strip().upper()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT player_id, nickname, avatar, score, correct_answers, 
                   current_question_index, is_finished, total_time_seconds
            FROM players
            WHERE room_code = ?
            ORDER BY score DESC, total_time_seconds ASC
        """, (clean_code,))
        return [dict(r) for r in cursor.fetchall()]


def reset_room_game(room_code: str):
    """Reinicia a sala para uma nova partida com novo seed."""
    clean_code = room_code.strip().upper()
    new_seed = random.randint(1000, 999999)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE rooms 
            SET status = 'waiting', seed = ?
            WHERE room_code = ?
        """, (new_seed, clean_code))
        
        cursor.execute("""
            UPDATE players
            SET score = 0, correct_answers = 0, current_question_index = 0,
                is_finished = 0, total_time_seconds = 0.0, updated_at = ?
            WHERE room_code = ?
        """, (time.time(), clean_code))
        
        cursor.execute("DELETE FROM answers WHERE room_code = ?", (clean_code,))
        conn.commit()


# Inicializa DB automaticamente ao importar
init_db()
