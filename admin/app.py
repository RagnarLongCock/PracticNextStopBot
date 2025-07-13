from flask import Flask, jsonify, request, render_template

import subprocess
from nlu_for_admin import *
import sys
import psutil
import psycopg2
import os
import io
import pandas as pd
from flask import send_file

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"), static_folder=os.path.join(BASE_DIR, "static"))

# === NLU ===
# теперь все функции в файле nlu_for_admin.py

# === ROUTES ===
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
#База данных
def admin_panel():
    conn = get_db()
    cur = conn.cursor()
    #вывод таблицы сообщений из базы данных
    cur.execute("""
        SELECT
        type_name AS "отправитель",
        (data::jsonb) ->> 'text' AS "сообщение",
        to_timestamp(timestamp) AS "Время отправления", intent_name AS "имя интента"
        FROM events
        WHERE type_name IN ('user', 'bot')
        AND (data::jsonb) ? 'text'
        ORDER BY timestamp ASC;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("admin.html", rows=rows)


# Рендер веб страниц
@app.route("/GPT")
def indexs():
    return render_template("GPT.html")



@app.route("/api/intents", methods=["GET"])
def get_intents():
    return jsonify(list(load_nlu().keys()))

@app.route("/api/intents/<intent>", methods=["GET"])
def get_examples(intent):
    return jsonify(load_nlu().get(intent, []))

@app.route("/api/intents", methods=["POST"])
def add_intent():
    name = request.json.get("name")
    intents = load_nlu()
    if name in intents:
        return jsonify({"message": "Интент уже существует"}), 409

    intents[name] = []
    save_nlu(intents)
    update_domain_with_intent(name)
    add_rule_for_custom_action(name)

    responses = load_responses()
    responses[f"action_{name}"] = {"default": ""}
    save_responses(responses)

    append_action_to_file(name)

    return jsonify({"message": f"Интент '{name}' добавлен"}), 201

@app.route("/api/intents/<intent>", methods=["POST"])
def add_example(intent):
    text = request.json.get("text")
    intents = load_nlu()
    if intent not in intents:
        return jsonify({"error": "Интент не найден"}), 404
    if text and text not in intents[intent]:
        intents[intent].append(text)
        save_nlu(intents)
    return jsonify({"message": "Фраза добавлена"})

@app.route("/api/intents/<intent>/<int:index>", methods=["DELETE"])
def delete_example(intent, index):
    intents = load_nlu()
    if intent not in intents or index >= len(intents[intent]):
        return jsonify({"error": "Неверный интент или индекс"}), 404
    intents[intent].pop(index)
    save_nlu(intents)
    return jsonify({"message": "Фраза удалена"})

@app.route("/api/responses", methods=["GET"])
def get_responses():
    return jsonify(load_responses())

@app.route("/api/responses/<action>", methods=["POST"])
def update_response(action):
    text = request.json.get("text", "")
    responses = load_responses()
    if isinstance(responses.get(action), dict):
        responses[action]["default"] = text
    else:
        responses[action] = {"default": text}
    save_responses(responses)
    return jsonify({"message": f"Ответ для '{action}' обновлён"})

@app.route("/api/train", methods=["POST"])
def train_model():
    try:
        result = subprocess.run([sys.executable, "-m", "rasa", "train"], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": "✅ Модель успешно переобучена"})
        else:
            return jsonify({"message": f"❌ Ошибка при обучении:\n{result.stderr}"}), 500
    except Exception as e:
        return jsonify({"message": f"❌ {str(e)}"}), 500

# === BOT CONTROL ===
bot_process = None
actions_process = None

def kill_process_tree(pid):
    try:
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
        return True
    except Exception:
        return False

@app.route("/api/start-bot", methods=["POST"])
def start_bot():
    global bot_process, actions_process

    try:
        if bot_process is None:
            bot_process = subprocess.Popen([
                "rasa", "run", "--enable-api", "-p", "5010", "--cors", "*"
            ])
        if actions_process is None:
            actions_process = subprocess.Popen([
                "rasa", "run", "actions", "-p", "5055"
            ])
        return jsonify({"message": "✅ Бот и actions запущены"})
    except Exception as e:
        return jsonify({"message": f"❌ Ошибка запуска: {str(e)}"}), 500

@app.route("/api/stop-bot", methods=["POST"])
def stop_bot():
    global bot_process, actions_process
    try:
        stopped = []
        if bot_process:
            if kill_process_tree(bot_process.pid):
                stopped.append("бот")
            bot_process = None
        if actions_process:
            if kill_process_tree(actions_process.pid):
                stopped.append("actions")
            actions_process = None
        if not stopped:
            return jsonify({"message": "⚠️ Бот и actions уже остановлены"})
        return jsonify({"message": f"🛑 Остановлено: {', '.join(stopped)}"})
    except Exception as e:
        return jsonify({"message": f"❌ Ошибка остановки: {str(e)}"}), 500


#========================GPT module(GIGA chat)==========================
from GPT_intents.giga import generate_examples
from GPT_intents.nlu_utils import *


from GPT_intents.redis_cache import cache_response

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    intent = data.get("intent")
    description = data.get("description")

    if not intent or not description:
        return jsonify({"error": "Missing 'intent' or 'description'"}), 400

    cached = cache_response.get(intent)
    if cached:
        return jsonify({"intent": intent, "examples": cached, "cached": True})

    examples = generate_examples(description)

    if not examples or not isinstance(examples, list):
        return jsonify({"error": "Failed to generate examples"}), 500

    # Очистка кавычек и нумерации
    cleaned = [e.strip().lstrip("0123456789. ").strip("\"") for e in examples]
    joined = "\n".join(f"- {e}" for e in cleaned)

    try:
        nlu = loads_nlu()
        validate_nlu(nlu)
        backup_nlu()

        nlu['nlu'].append({
            "intent": intent,
            "examples": LiteralString(joined)
        })

        saves_nlu(nlu)

        # === ДОБАВЛЯЕМ ПОДДЕРЖКУ ОТВЕТА И ACTION ===
        responses = load_responses()
        responses[f"action_{intent}"] = {"default": ""}
        save_responses(responses)
        append_action_to_file(intent)

        cache_response.set(intent, cleaned)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"intent": intent, "examples": cleaned})


@app.route('/api/preview', methods=['POST'])
def preview():
    description = request.json.get("description")
    if not description:
        return jsonify({"error": "Missing description"}), 400
    examples = generate_examples(description)
    cleaned = [e.strip().lstrip("0123456789. ").strip("\"") for e in examples]
    return jsonify({"preview": cleaned})

@app.route('/api/rollback', methods=['POST'])
def rollback():
    try:
        rollback_nlu()
        return jsonify({"status": "Rolled back to previous version"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#===============================================================================

#===========================================Кнопки БД========================================
@app.route("/api/cleanup", methods=["POST"])
def cleanup():
    try:
        conn = get_db()
        cur = conn.cursor()

        # Пробуем удалить события старше 30 дней
        delete_query = """
            DELETE FROM events
            WHERE timestamp < EXTRACT(EPOCH FROM (NOW() - INTERVAL '30 days'));
        """
        cur.execute(delete_query)
        deleted_rows = cur.rowcount

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "message": f"🧹 Удалено {deleted_rows} старых событий"
        })

    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500



from datetime import datetime
@app.route("/api/backup", methods=["POST"])
def backup():
    try:
        backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backup_bd")
        os.makedirs(backup_dir, exist_ok=True)

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(backup_dir, f"rasa_db_backup_{now}.sql")

        # Параметры из окружения (передаём через .env в docker-compose)
        db_user = os.environ.get("POSTGRES_USER", "postgres")
        db_name = os.environ.get("POSTGRES_DB", "rasa_db")
        db_host = os.environ.get("PGHOST", "db")
        db_port = os.environ.get("PGPORT", "5432")
        db_pass = os.environ.get("POSTGRES_PASSWORD", "")

        # Формируем команду
        cmd = [
            "pg_dump",
            "-h", db_host,
            "-p", db_port,
            "-U", db_user,
            "-d", db_name,
            "-f", output_file
        ]

        # Передаём пароль через окружение
        env = os.environ.copy()
        env["PGPASSWORD"] = db_pass

        result = subprocess.run(cmd, env=env, capture_output=True, text=True)

        if result.returncode == 0:
            return jsonify({"message": f"💾 Резервная копия создана: {output_file}"})
        else:
            return jsonify({"error": "❌ Ошибка при создании резервной копии"}), 500
    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route("/api/download_excel", methods=["GET"])
def download_excel():
    conn = get_db()
    cur = conn.cursor()

    # Получаем данные
    cur.execute("""
        SELECT
        type_name AS "отправитель",
        (data::jsonb) ->> 'text' AS "сообщение",
        to_timestamp(timestamp) AS "Время отправления", intent_name AS "имя интента"
        FROM events
        WHERE type_name IN ('user', 'bot')
        AND (data::jsonb) ? 'text'
        ORDER BY timestamp ASC;
    """)

    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["role", "message", "sent_at", "intent_name"])

    # Убираем временную зону, если она есть
    if pd.api.types.is_datetime64tz_dtype(df["sent_at"]):
        df["sent_at"] = df["sent_at"].dt.tz_localize(None)

    # Подготовка Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="dialogs")
    output.seek(0)

    return send_file(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="dialogs.xlsx"
    )


def get_db():
    return psycopg2.connect(
        dbname="rasa_db",
        user="postgres",
        password="HatsuneGoyda",
        host="db",
        port=5432
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)



