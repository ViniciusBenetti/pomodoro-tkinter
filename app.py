from tkinter import *
from tkinter import ttk
import datetime
import pickle
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox




Entry_personalizado = None
canvas_widget = None
fig = None



   
def carregar_tempo():
    diretorio_projeto = os.path.dirname(os.path.abspath(__file__))
    arquivo_path = os.path.join(diretorio_projeto, 'tempo_passado.pkl')
    try:
        with open(arquivo_path, 'rb') as arquivo:
            tempo_passado = pickle.load(arquivo)
            return tempo_passado
    except (FileNotFoundError, EOFError):
        tempo_passado = 0
        with open(arquivo_path, 'wb') as arquivo:
            pickle.dump(tempo_passado, arquivo)
        return tempo_passado


def salvar_tempo(tempo_passado):
    diretorio_projeto = os.path.dirname(os.path.abspath(__file__))
    arquivo_path = os.path.join(diretorio_projeto, 'tempo_passado.pkl')
    with open(arquivo_path, 'wb') as arquivo:
        pickle.dump(tempo_passado, arquivo)


segundos_passados = carregar_tempo()

def carregar_datas():
    arquivo_path = "datas_salvas.pkl"

    if os.path.exists(arquivo_path):
        with open(arquivo_path, "rb") as arquivo:
            datas_salvas = pickle.load(arquivo)
            return datas_salvas
    else:
        return []

def salvar_data(data):
    global segundos_passados
    datas_salvas = carregar_datas()
    

    if datas_salvas:
        if data[0] == datas_salvas[-1][0]:
            datas_salvas[-1][0] = data[0]
            datas_salvas[-1][1] = str(segundos_passados)
        else:
            segundos_passados = 0
            datas_salvas.append([data[0], str(segundos_passados)])
    else:
        segundos_passados = 0
        datas_salvas.append([data[0], str(segundos_passados)])

    arquivo_path = "datas_salvas.pkl"

    with open(arquivo_path, "wb") as arquivo:
        pickle.dump(datas_salvas, arquivo)


data_atual = [str(datetime.date.today())] + [str(segundos_passados)]
datas_salvas = carregar_datas()
salvar_data(data_atual)
print(datas_salvas)
print(segundos_passados)



pausado = False
estado = "trabalho" 
tempo_total_trabalho = 25*60
tempo_total_intervalo = 5*60
tempo_restante = tempo_total_trabalho
timer_id = None
sugestoes = [
    "Sugestão: Fazer alongamentos rápidos\n para relaxar os músculos.",
    "Sugestão: Respirar profundamente e\n praticar a meditação por alguns minutos.",
    "Sugestão: Beber um copo d'água\n para se manter hidratado.",
    "Sugestão: Anotar suas tarefas em andamento\n e fazer um plano para\n o próximo ciclo Pomodoro.",
    "Sugestão: Fazer um lanche saudável\n para recarregar sua energia.",
    "Sugestão: Levantar-se e caminhar um pouco\n para ativar a circulação.",
    "Sugestão: Ler um artigo interessante\n por alguns minutos.",
    "Sugestão: Anotar suas conquistas até\n agora para manter o ânimo.",
    "Sugestão: Respirar ar fresco em uma\n janela aberta por um momento.",
    "Sugestão: Fazer um exercício de foco\n ou concentração, como\n quebra-cabeças ou palavras cruzadas."
]

indice_sugestao = -1
data_combobox = None
Entry_personalizado= None



def criar_graf(dias):
    global segundos_passados, canvas_widget, tempo_estudado,datas_salvas
    
    try:
        dias = int(dias)
    except:
        dias = 99
  
    if canvas_widget is not None:
        canvas_widget.place_forget()
        canvas_widget = None

    try:
        with open('tempo_estudado.pkl', 'rb') as f:
            tempo_estudado = pickle.load(f)
            if len(tempo_estudado) > (dias - 1):
                tempo_estudado = tempo_estudado[:dias-1]
            elif len(tempo_estudado) < (dias-1):
                tempo_estudado.extend([0] * ((dias - 1) - len(tempo_estudado)))
            
    except FileNotFoundError:

        tempo_estudado = [0] * (dias - 1)

    exemplo_tempo_estudado = []

    if len(exemplo_tempo_estudado) < dias - 1:
        exemplo_tempo_estudado.extend([0] * (dias - 1 - len(exemplo_tempo_estudado)))



    for i in range(dias - 1): 
       for j in range(len(datas_salvas)):
           if i == j and i > 0:
                tempo_estudado[i] = int(datas_salvas[-i-1][1]) / 3600
           if i == j and i == 0:
                tempo_estudado[i] = int(datas_salvas[i-1][1]) / 3600
               


    with open('tempo_estudado.pkl', 'wb') as f:
        pickle.dump(tempo_estudado, f)

    fig = Figure(figsize=(5, 4), dpi=100)
    subplot = fig.add_subplot(111)

    x = list(range(1, dias))
    y = tempo_estudado

    subplot.set_ylim(0, 24)

    subplot.bar(x, y)
    subplot.set_xlabel("dias")
    subplot.set_ylabel("Tempo Estudado (horas)")
    subplot.set_title("Tempo Estudado por dia")

    canvas = FigureCanvasTkAgg(fig, master=janela_filha)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.place(x=160, y=30)


def combobox_mudou(event, Entry_personalizado, valor_entry_personalizado):
    global data_combobox, fig


    if Entry_personalizado is not None:
        Entry_personalizado.place_forget()

    if event == "personalizado":
        Entry_personalizado.place(x=7, y=110)
        if valor_entry_personalizado != "":

            if int(valor_entry_personalizado) < 3500 and int(valor_entry_personalizado) > 1:
                criar_graf(valor_entry_personalizado)
            else:
                tkinter.messagebox.showwarning('aviso:','digite um valor entre 2 e 3500')
        
        

    if event == "semanal":
        criar_graf(8)


    if event == "mensal":
        criar_graf(31)
    

    if event == "anual":
        criar_graf(366)

    try:
        with open('tempo_estudado.pkl', 'rb') as f:
            tempo_estudado = pickle.load(f)
            horas_semana = sum(tempo_estudado[:7]) 
            horas_mes = sum(tempo_estudado[:30]) 
            horas_ano = sum(tempo_estudado[:365]) 
    except:
        horas_semana = 0
        horas_mes = 0
        horas_ano = 0
    


    horas_smn = Label(janela_filha,text=f'horas concentradas\nna semana: {horas_semana:.2f}',bg="black",fg="white",font="Arial 12")
    horas_smn.place(x=7,y=160)
    horas_ms = Label(janela_filha,text=f'horas concentradas\nno mes: {horas_mes:.2f}',bg="black",fg="white",font="Arial 12")
    horas_ms.place(x=7,y=220)
    horas_an = Label(janela_filha,text=f'horas concentradas\nno ano: {horas_ano:.2f}',bg="black",fg="white",font="Arial 12")
    horas_an.place(x=7,y=280)
    
             

def validar_numero(P):
    if P == "":
        return True
    try:
        float(P)
        return True
    except ValueError:
        return False


def window2():
    global janela_filha 
    janela_filha = Toplevel(window) 
    janela_filha.title("historico")
    janela_filha.config(background="black")
    janela_filha.resizable(width=False,height=True)
    janela_filha.geometry("800x500+300+100")
    label = Label(janela_filha, text="Histórico",bg="black",fg="white",font="Arial 12")
    label.pack()
    label2 = Label(janela_filha,text="escolha a data:",bg="black",fg="white",font="Arial 12")
    label2.place(x=7,y=50)
    data_combobox = ttk.Combobox(janela_filha, values=("semanal","mensal","anual","personalizado"),state="readonly")
    data_combobox.place(x=7, y=80)
    data_combobox.set("")
    Entry_personalizado = Entry(janela_filha)
    Entry_personalizado.config(validate="key", validatecommand=(Entry_personalizado.register(validar_numero), '%P'))
    
    data_combobox.bind("<<ComboboxSelected>>", lambda event: combobox_mudou(data_combobox.get(), Entry_personalizado, Entry_personalizado.get()))


    button = Button(janela_filha, text="Fechar",width=7, height=2, font="Times-New-Roman 9 normal", relief="raised", bg="#4267ff", border=4,command=janela_filha.withdraw)
    button.place(x=7,y=450)





def iniciar():
    global tempo_restante, timer_id, estado
    tempo_restante = tempo_total_trabalho
    if timer_id:
        window.after_cancel(timer_id)
    timer_id = window.after(1000, atualizar_tempo)
    botao_iniciar.place(x=330, y=370)
    botao_pausar.place(x=410, y=370)
    estado = "trabalho"  

def pausar():
    global pausado, timer_id
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None
        pausado = True
    else:
        timer_id = window.after(1000, atualizar_tempo)
        pausado = False

def atualizar_tempo():
    global tempo_restante, timer_id, estado,segundos_passados
    if tempo_restante > 0 and not pausado:
        minutos = tempo_restante // 60
        segundos = tempo_restante % 60
        tempo_formatado = f"{minutos:02d}:{segundos:02d}"
        tempo_label.config(text=tempo_formatado)
        tempo_restante -= 1
        if estado == "trabalho":
            segundos_passados += 1
        salvar_tempo(segundos_passados)
        timer_id = window.after(1000, atualizar_tempo)

            
    else:
        if tempo_restante == 0:
            if estado == "trabalho":
                tkinter.messagebox.showwarning("Aviso", "O tempo  de trabalho acabou!")
                tempo_label.config(text="05:00")
                tempo_restante = tempo_total_intervalo
                estado = "intervalo"
                imagem_label.place_forget()
                botao_iniciar.place_forget()
                botao_pausar.place_forget()
                atualizar_sugestao()
            else:
                tkinter.messagebox.showwarning("Aviso", "O tempo  de descanso acabou!")     
                estado = "trabalho"
                tempo_restante = tempo_total_trabalho
                botao_iniciar.place(x=330, y=370)
                botao_pausar.place(x=410, y=370)
                imagem_label.place(x=320,y=150)
                sugestao_label.place_forget()

            minutos = tempo_restante // 60
            segundos = tempo_restante % 60

            tempo_formatado = f"{minutos:02d}:{segundos:02d}"
            tempo_label.config(text=tempo_formatado)
            timer_id = window.after(1000, atualizar_tempo)

        timer_id = None

def atualizar_sugestao():
    global indice_sugestao
    indice_sugestao +=1
    if indice_sugestao >9:
        indice_sugestao = 0
    
    sugestao_label.config(text=sugestoes[indice_sugestao])
    sugestao_label.place(x=220, y=200)

window = Tk()
window.config(background="black")
window.title('pomodoro')
window.geometry("800x500+300+100")
window.resizable(width=False, height=True)

imagem = PhotoImage(file="pomodoro.gif")
imagem_label = Label(window, image=imagem, background="black")
imagem_label.image = imagem
imagem_label.place(x=320, y=150)

Titulo = Label(window, text="POMODORO", font="Comic-Sans-MS 28 ", foreground="white", background="black").place(x=280, y=45)
Descricao = Label(window, text='"Maximize seu foco com apenas um clique."', foreground="white", background="black", font="Comic-Sans-MS 12 italic").place(x=240, y=99)

botao_iniciar = Button(window, text="PLAY/R", width=7, height=2, font="Courier-New 9 bold", relief="raised", bg="#4267ff", border=4, command=iniciar)
botao_pausar = Button(window, text="PAUSE/C", width=7, height=2, font="Courier-New 9 bold", relief="raised", bg="#4267ff", border=4, command=pausar)
botao_iniciar.place(x=330, y=370)
botao_pausar.place(x=410, y=370)

Historico = Button(window, text="histórico", width=5, height=1, font="Times-New-Roman 7 normal", relief="raised", bg="#4267ff", border=4,command=window2)
Historico.place(x=4, y=4)

tempo_label = Label(window, text="25:00", font="Courier-New 18 bold", fg="white", bg="black")
tempo_label.place(x=370, y=330)

sugestao_label = Label(window, text="", font="Courier-New 12 bold", fg="white", bg="black")


window.mainloop()
