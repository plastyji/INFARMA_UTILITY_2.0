import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
import querys as DB

janela = ctk.CTk()

class Application:
    def  __init__(self):        
        self.tema()
        self.tela()
        self.telaLogin()
        janela.mainloop()
    def tema(self):       
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
    #Back-door , tamanho , icones"
    def tela(self):
        janela.geometry("700x400")
        janela.title("Login Infarma Utility")
        janela.iconbitmap('12.ico')
        janela.resizable(False,False)
    #First Tela - Interaction of users
    def telaLogin(self):
        # Carregar a imagem como CTkImage
        self.img = PhotoImage(file="1.png")

        # Exibir a imagem usando um CTkLabel
        self.label_img = ctk.CTkButton(master=janela, image=self.img, hover_color='none', bg_color='transparent'
                                , fg_color=None, text=None, hover=None)
        self.label_img.place(x=35, y=65)
        labeltt = ctk.CTkLabel(master=janela, text="Bem vindo \n ao \n Infarma Utility",
                                        font=("Arial", 25))
        labeltt.place(x=185 ,  y=150) 
        #frame
        self.login_frame= ctk.CTkFrame(master=janela, width=350, height=396)
        self.login_frame.pack(side=RIGHT)
        #Interaction of Users
        label = ctk.CTkLabel(master=self.login_frame, text="Tela Login", text_color='white', font=('roboto', 35 ,'bold'))
        label.place(x=55, y=15)
        User_entry = ctk.CTkEntry(master=self.login_frame, placeholder_text="Usuario" , width=300, 
                                        font=("Roboto", 14))
        User_entry.place(x=25, y=105)

        username_label = ctk.CTkLabel(master=self.login_frame, text="Nome de usuario obrigatorio" ,
                                        text_color=("white"),font=("Roboto", 8)).place(x=25, y=135)
        senha_entry = ctk.CTkEntry(master=self.login_frame, placeholder_text="Senha" , width=300, 
                                        font=("Roboto", 14), show="*")
        senha_entry.place(x=25, y=175)
        password_label = ctk.CTkLabel(master=self.login_frame, text="Senha de usuario obrigatorio" ,
                                        text_color=("white"),font=("Roboto", 8)).place(x=25, y=205)
        checkbox = ctk.CTkCheckBox(master=self.login_frame, text="Lembrar a senha").place(x=25, y=235)
       
        #Autentication the 
        def dadosLogin():
            user1 = 'infarma'
            senha1 = 'infarma2015.1'
            #Remover o frame de login 
            if User_entry.get() == ""and senha_entry.get() == "":
                messagebox.showerror(title='Erro', message='Por favor preencher todos os campos')
            else:
                if User_entry.get() != user1:
                    messagebox.showerror(title='Erro', message="Usuario invalido!")
                elif senha_entry.get() != senha1:
                    messagebox.showerror(title='Erro', message="Senha invalido!")
                elif User_entry.get() == user1 and senha_entry.get() == senha1:
                    self.login_frame.pack_forget()
                    self.label_img.destroy()
                    labeltt.destroy()
                    nextwindow()
        login_button = ctk.CTkButton(master=self.login_frame, text="Login", width= 300, command=dadosLogin)
        login_button.place(x=25, y=285) 
       
        def nextwindow():
            janela.title("Infarma Utility")
            janela.title("Opções")
            janela.geometry("700x400")
            janela.configure(bg="white")
            new_frame = ctk.CTkFrame(master=janela, width=700, height=400)
            new_frame.pack(side=ctk.RIGHT)
            def connectdatabase():
                    try:
                        DB.Querys.connectBanco()  
                        msg = messagebox.showinfo(title="Sucesso", message="Banco Conectado com sucesso!")                        
                    except Exception as e:                        
                        msg = messagebox.showerror(title="Erro", message="Erro do conectar ao banco de dados \nVerifique os log")
            def closeday():
                    try:        
                        DB.Querys.closeday()
                        msg = messagebox.showinfo(title="Sucesso", message="Alteração feita com sucesso!")
                    except:
                        msg = messagebox.showerror(title="Erro", message="Erro ao realizar as alterações \nVerifique os log")
            def alterregsms():
                    try:        
                        DB.Querys.ajustregsms()
                        msg = messagebox.showinfo(title="Sucesso", message="Alteração feita com sucesso!")
                    except:
                        msg = messagebox.showerror(title="Erro", message="Erro ao realizar as alterações \nVerifique os log")
            def insertass():
                    new_frame.pack_forget()
                    new_framee = ctk.CTkFrame(master=janela, width=700, height=400)
                    new_framee.pack(side=RIGHT)
                    ctk.CTkLabel(master=new_framee, text="Insira a chave de vinculação AC!", font=("Roboto", 25)).place(x=180, y=5)
                    msg = ctk.CTkEntry(master=new_framee, placeholder_text="Chave de vinculação AC", text_color="White", font=("Arial", 15), width=250)
                    msg.place(x=230,y=150)
                    def rollback():
                        new_framee.pack_forget()
                        nextwindow()
                    def inserir():
                        try: 
                            retorno = msg.get()                   
                            DB.Querys.InsertAC(retorno)
                            msg1 = messagebox.showinfo(title="Sucesso", message="Informação atualizada com sucesso!")
                        except:
                            msg1= messagebox.showerror(title="Erro", message="Erro ao realizar as alterações \nVerifique os log")
                    button = ctk.CTkButton(master=new_framee, text="Inserir", text_color="white", width=250, command=inserir)
                    button.place(x=230, y=190)
                    ctk.CTkButton(master=new_framee, text="Voltar", text_color="white", width=250, command=rollback).place(x=230, y=230)
            def inserttls():
                # try:
                    DB.Querys.emitirnota()
                    msg1 = messagebox.showinfo(title="Sucesso", message="Informação atualizada com sucesso!")
                # except:
                #     msg1= messagebox.showerror(title="Erro", message="Erro ao realizar as alterações \nVerifique os log")
            janela.msg = ctk.CTkLabel(master=new_frame, text="Escolha uma opção abaixo", font=("Roboto", 25))
            janela.msg.place(x=200, y=5)
            ctk.CTkButton(master=new_frame, text="Conectar no banco de dados", width=250, command=connectdatabase).place(x=95, y=85)            
            ctk.CTkButton(master=new_frame, text="Abertura Caixa Geral", width=250, command=closeday).place(x=355, y=85)                                                                                                                         
            ctk.CTkButton(master=new_frame, text="Ajuste registro MS", width=250, command=alterregsms).place(x=95, y=125)
            ctk.CTkButton(master=new_frame, text="Coloca a chave vinculação AC", width=250, command=insertass).place(x=355, y=125)
            ctk.CTkButton(master=new_frame, text="Primeira emissão Nf-e (TLS)", width=250, command=inserttls).place(x=95, y=165)
            ctk.CTkButton(master=new_frame, text="Reduzir Log Do Banco", width=250).place(x=355, y=165)
            ctk.CTkButton(master=new_frame, text="Opções Nf", width=250).place(x=95, y=205)
            ctk.CTkButton(master=new_frame, text="Cria usuario(VMDApp)", width=250).place(x=355, y=205)
            ctk.CTkButton(master=new_frame, text="Opções caixa", width=250).place(x=95, y=245)
            ctk.CTkButton(master=new_frame, text="Opções de plano de conta contabil", width=250).place(x=355, y=245)
            ctk.CTkButton(master=new_frame, text="Alterações produto", width=250).place(x=95, y=285)
            ctk.CTkButton(master=new_frame, text="Outras Opções", width=250).place(x=355, y=285)

        


                    
                    
                    
                    

        
    
                        
               
Application()