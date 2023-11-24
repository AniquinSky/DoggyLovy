from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import flaskr.db as db

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/chatWith-<string:other_user_id>')
def chatRoom(other_user_id):
    chat_room_id = generateChatRoomId(g.user_id, other_user_id)
    connDB = db.get_db()
    cur = connDB.cursor()
    try:
        cur.execute(
            "INSERT INTO chats VALUES (%s, %s, %s, default)",
            (chat_room_id, g.user_id, other_user_id),
        )
        connDB.commit()
    except connDB.IntegrityError as e:
        print(e)
        meessage = 'La sala ya existe.'
    except Exception as e:
        print(e)
        message = 'Ocurrio un error inesperado.'
    finally:
        cur.close()
        db.close_db()

    return render_template(
            'site/chat.html',
            other_user_id = other_user_id,
            chat_room_id = chat_room_id,
            chat_history = getChatHistory(chat_room_id)
            )

@bp.route('/chatsList')
def chatsList():
    return render_template('site/chats_list.html', chats = getChats())

def generateChatRoomId(id_creator, id_guest):
    return ''.join(sorted(id_creator + id_guest))

def getChats():
    chats = []
    connDB = db.get_db()
    cur = connDB.cursor()
    try:
        cur.execute(
            "SELECT * FROM chats WHERE id_creador = %s OR id_invitado = %s",
            (g.user_id, g.user_id),
        )
        chats = cur.fetchall()
    except Exception as e:
        print(e)
        chats = []
        flash('Ocurrio un error inesperado al obtener la lista de chats. Intentelo de nuevo mas tarde.')
    finally:
        cur.close()
        db.close_db()

    return chats


def getChatHistory(room):
    messages = []
    connDB = db.get_db()
    cur = connDB.cursor()
    try:
        cur.execute(
            "SELECT id_remitente, id_destinatario, mensaje FROM mensajes WHERE id_sala = %s ORDER BY id_mensaje ASC",
            (room,),
        )
        messages = cur.fetchall()
    except Exception as e:
        print(e)
        messages = []
        flash('Ocurrio un error inesperado al obtener el historial del chat. Intentelo de nuevo mas tarde.')
    finally:
        cur.close()
        db.close_db()

    return messages
