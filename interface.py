import tkinter as tk
from tkinter import scrolledtext

# Função para enviar mensagem
def send_message():
    user_message = user_input.get()
    if user_message.strip() != "":
        # Habilita temporariamente a área de chat para inserir texto
        chat_area.config(state="normal")
        
        # Exibe a mensagem do usuário na área de chat
        chat_area.insert(tk.END, f"Você: {user_message}\n")
        
        # Limpa o campo de entrada de texto
        user_input.delete(0, tk.END)
        
        # Aqui você pode adicionar a lógica para gerar a resposta da IA
        bot_response = "Resposta da IA aqui..."  # Exemplo de resposta
        
        # Exibe a resposta da IA na área de chat
        chat_area.insert(tk.END, f"IA: {bot_response}\n")
        
        # Rola o chat para o final
        chat_area.yview(tk.END)
        
        # Desabilita a área de chat novamente
        chat_area.config(state="disabled")

# Criação da janela principal
window = tk.Tk()
window.title("Chat com IA")
window.geometry("400x500")
window.config(bg="#f0f2f5")

# Cabeçalho
header = tk.Label(window, text="Conversa com IA", bg="#4a90e2", fg="white", font=("Arial", 16, "bold"))
header.pack(pady=10, fill=tk.X)

# Área de chat com rolagem
chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Arial", 12), bg="#ffffff", state="disabled")
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Caixa de entrada de texto
user_input = tk.Entry(window, font=("Arial", 12))
user_input.pack(padx=10, pady=5, fill=tk.X)

# Botão de envio
send_button = tk.Button(window, text="Enviar", command=send_message, bg="#4a90e2", fg="white", font=("Arial", 12))
send_button.pack(padx=10, pady=10)

# Evento de teclado para enviar com "Enter"
window.bind("<Return>", lambda event: send_message())

# Função principal do loop
window.mainloop()
