import tkinter as tk
from tkinter import messagebox
import json
import random


def carregar_perguntas():
    with open('perguntas.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def exibir_pergunta():
    global pergunta_atual

    if pergunta_atual < len(perguntas_filtradas):
        pergunta = perguntas_filtradas[pergunta_atual]
        pergunta_label.config(text=pergunta['pergunta'])

        for i in range(4):
            opcoes_button[i].config(text=pergunta['opcoes'][i])

    else:
        messagebox.showinfo(
            "Parabéns!", f"Você acertou {pontuacao} de {len(perguntas_filtradas)} perguntas!")
        tela_quiz.pack_forget()
        tela_resultado.pack(fill='both', expand=True)


def verificar_resposta(resposta):
    global pergunta_atual, pontuacao
    pergunta = perguntas_filtradas[pergunta_atual]

    if resposta == pergunta['resposta']:
        pontuacao += 1

    pergunta_atual += 1
    if pergunta_atual < len(perguntas_filtradas):
        exibir_pergunta()
    else:
        messagebox.showinfo(
            "Parabéns!", f"Você acertou {pontuacao} de {len(perguntas_filtradas)} perguntas!")
        tela_quiz.pack_forget()
        tela_resultado.pack(fill='both', expand=True)


def escolher_categoria_dificuldade():
    global perguntas_filtradas

    categoria = categoria_var.get()
    dificuldade = dificuldade_var.get()

    perguntas_filtradas = [p for p in perguntas if p['categoria']
                           == categoria and p['dificuldade'] == dificuldade]

    if len(perguntas_filtradas) == 0:
        messagebox.showwarning(
            "Sem Perguntas", "Não há perguntas para essa categoria e dificuldade!")
        return

    random.shuffle(perguntas_filtradas)
    pergunta_atual = 0
    pontuacao = 0
    exibir_pergunta()


def iniciar_quiz():
    escolher_categoria_dificuldade()
    if len(perguntas_filtradas) > 0:
        tela_inicial.pack_forget()
        tela_quiz.pack(fill='both', expand=True)
    else:
        tela_inicial.pack(fill='both', expand=True)


def voltar_inicial():
    global pergunta_atual, pontuacao
    pergunta_atual = 0
    pontuacao = 0
    tela_resultado.pack_forget()
    tela_inicial.pack(fill='both', expand=True)


perguntas = carregar_perguntas()
pergunta_atual = 0
pontuacao = 0
perguntas_filtradas = []

root = tk.Tk()
root.title("Quiz Interativo de Futebol")
root.geometry("500x400")
root.config(bg="#f0f0f0")

tela_inicial = tk.Frame(root, bg="#006400")
tela_inicial.pack(fill='both', expand=True)

categoria_var = tk.StringVar()
dificuldade_var = tk.StringVar()

categoria_label = tk.Label(tela_inicial, text="Escolha a Categoria", font=(
    "Arial", 14), bg="#006400", fg="white")
categoria_label.pack(pady=10)

categoria_menu = tk.OptionMenu(
    tela_inicial, categoria_var, "Copa do Mundo", "Jogadores", "Clubes", "História")
categoria_menu.config(font=("Arial", 12), width=20)
categoria_menu.pack(pady=5)

dificuldade_label = tk.Label(tela_inicial, text="Escolha a Dificuldade", font=(
    "Arial", 14), bg="#006400", fg="white")
dificuldade_label.pack(pady=10)

dificuldade_menu = tk.OptionMenu(
    tela_inicial, dificuldade_var, "fácil", "médio", "difícil")
dificuldade_menu.config(font=("Arial", 12), width=20)
dificuldade_menu.pack(pady=5)

iniciar_button = tk.Button(tela_inicial, text="Iniciar Quiz", command=iniciar_quiz, font=(
    "Arial", 14), bg="#228B22", fg="white", width=20)
iniciar_button.pack(pady=20)

tela_quiz = tk.Frame(root, bg="#f3f0fa")

pergunta_label = tk.Label(tela_quiz, text="", wraplength=400, font=(
    "Arial", 14), bg="#f3f0fa", fg="#333")
pergunta_label.pack(pady=20)

opcoes_button = []
for i in range(4):
    button = tk.Button(tela_quiz, text="", font=("Arial", 12), bg="#32CD32", fg="white", width=40,
                       height=2, command=lambda i=i: verificar_resposta(opcoes_button[i].cget("text")))
    button.pack(pady=5)
    opcoes_button.append(button)

tela_resultado = tk.Frame(root, bg="#006400")
resultado_label = tk.Label(tela_resultado, text="Parabéns!", font=(
    "Arial", 24), bg="#006400", fg="white")
resultado_label.pack(pady=20)

pontuacao_label = tk.Label(tela_resultado, text="", font=(
    "Arial", 18), bg="#006400", fg="white")
pontuacao_label.pack(pady=10)

voltar_button = tk.Button(tela_resultado, text="Voltar ao Início",
                          command=voltar_inicial, font=("Arial", 14), bg="#228B22", fg="white")
voltar_button.pack(pady=20)

root.mainloop()
