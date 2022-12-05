import time
from datetime import datetime
import schedule
import telebot
from telebot import types

# <--------------- Datos del bot ---------------------->
bot = telebot.TeleBot("tu_token")
# <---------------------------------------------------->

# <------------ Datos de zona horaria ----------------->
fecha_actual = datetime.now()
fecha_actual_str = fecha_actual.strftime('%d/%m/%Y, %H:%M:%S')
# <---------------------------------------------------->

# Función start del bot

@bot.message_handler(commands=['start', 'help'])
def start(message):
  bot.reply_to(message, f"Hola, soy un bot hecho por @yuyuuhok para programar mensajes.\n\nLa hora de México es: <code>{fecha_actual_str}</code>", parse_mode="html")

# Comando /schedule para programar mensaje

@bot.message_handler(commands=['schedule'])
def mensaje(message):
  markup = types.ForceReply(selective=False)
  
  # Se pide el mensaje a programar y el bot detecta el mensaje
  mensaje = bot.reply_to(message, "📝 Escribe el mensaje a programar", reply_markup=markup)
  bot.register_next_step_handler(mensaje, hora)

# Se pregunta la hora a enviar
def hora(message):
  markup = types.ForceReply(selective=False)
  global chat_id
  chat_id = message.chat.id
  global mensaje_enviar
  mensaje_enviar = message.text

  programar = bot.send_message(chat_id, "📅 Escribe la hora que quieras haga el recordatorio, por favor hazlo en formato de 24 horas.\n\nEjemplo (18:00 = 6 PM, 06:00 = 6 AM)\n\nRecuerda calcular la hora de tu país.", reply_markup=markup)
  bot.register_next_step_handler(programar, enviar)

# Se programa el mensaje y la hora 

def enviar(message):
  chat_id = message.chat.id
  global programar_texto
  programar_texto = message.text
  bot.send_message(chat_id, f"Listo! ✅\n\nEl mensaje a enviar es: <b>{mensaje_enviar}</b> y está programado para: <b>{programar_texto}</b>", parse_mode="html")
  
  # OPCIONAL: Se envia un mensaje de confirmación a un canal
  bot.send_message("id_canal", f"Nuevo recordatorio establecido:\n\nDe: {chat_id}\n\nMensaje: <b>{mensaje_enviar}</b>\nHora a enviar: <b>{programar_texto}</b>", parse_mode="html")

# Cuando llegue la hora del recordatorio se envia el mensaje

  def send_text():
    bot.send_message(chat_id, f"🔔 Hu Tao Scheduler 🔔\n\n<b>{programar_texto}</b>\n\nHola, este es un mensaje programado, el mensaje a recordarte es: <b>{mensaje_enviar}</b>", parse_mode="html")
    return schedule.CancelJob # La función schedule solo envia una vez el recordatorio y finaliza

  schedule.every().day.at(programar_texto).do(send_text) 
  while True:
    schedule.run_pending()
    time.sleep(1)
    

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()



if __name__ == '__main__':
  print("Listening...")
  bot.infinity_polling()