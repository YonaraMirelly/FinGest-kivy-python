from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
import os
import json
import webbrowser 

# classe principal do app
class FinGest(App):
    def build(self):
        Window.clearcolor = ( 4/255.0, 10/255.0, 56/255.0, 1)
        self.layout = FloatLayout()
        self.load_expenses() #carrega as despesas salvas
        self.show_welcome_screen()
        return self.layout
      
  
#função para tela inicial de boas-vindas  
    def show_welcome_screen(self):
        background = Image(source='FinGest_introduçao.png', 
                           allow_stretch=True, 
                           keep_ratio=True)
                           
        
        #esse botão direciona para a 2ª interface
        start_button = Button(text='Gerir Agora!', size_hint=(0.3, 0.1),
                              font_size=45, color = (159/255.0,226/255.0,191/255.0,1),
                              pos_hint={"center_x": 0.5, "center_y": 0.2},
                              background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                              on_press=self.show_salary_input)
        #esse botão sai do app
        exit_button = Button(text='Sair do App', size_hint=(0.3, 0.1),
                             font_size=45, color=(159/255.0, 226/255.0, 191/255.0, 1),
                             pos_hint={"center_x": 0.5, "center_y": 0.1},
                             background_color=(120/255.0, 5/255.0, 89/255.0, 1),
                             on_press=self.exit_app)
    
        self.layout.add_widget(background)
        self.layout.add_widget(start_button)
        self.layout.add_widget(exit_button)   

#tela pra o usuário adicionar o seu salário para análise
    def show_salary_input(self, instance):
        self.layout.clear_widgets()
        
        background = Image(source='FinGest_input.png', 
                           allow_stretch=True, 
                           keep_ratio=True)
        
        self.salary_input = TextInput(hint_text='Insira o salário', multiline=False,  
                                      pos_hint={"center_x": 0.5, "center_y": 0.5},
                                      background_color = (176/255.0, 252/255.0, 175/255.0,1),
                                      size_hint=(None,None), size = (300,50) ) #alterei aqui
        
        #botão que direciona para a interface que contém todos os cálculos exibidos
        self.submit_button = Button(text='Enviar', font_size = 50, size_hint = (0.2, 0.2),
                                    pos_hint={"center_x": 0.5, "y": 0.200},
                                    color = (159/255.0,226/255.0,191/255.0),
                                    background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                                    on_press=self.escolha)
        self.submit_button.parent = None 

        self.layout.add_widget(background)
        self.layout.add_widget(self.salary_input)
        self.layout.add_widget(self.submit_button)

#função para escolher entre - tabela, despesa, doação e investimentos        
    def escolha(self, instance):
        self.layout.clear_widgets()

        background = Image(source='FinGest_escolha.png', 
                           allow_stretch=True, 
                           keep_ratio=True)
        
        tabela_button = Button(text='TABELA', size_hint=(0.3, 0.1),
                              font_size=40, color = (159/255.0,226/255.0,191/255.0,1),
                              pos_hint={"center_x": 0.4, "center_y": 0.82},
                              background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                              on_press=self.calculate_budget)
        
        Despesas_mes_button = Button(text='DESPESAS', size_hint=(0.3, 0.1),
                              font_size=40, color = (159/255.0,226/255.0,191/255.0,1),
                              pos_hint={"center_x": 0.4, "center_y": 0.67},
                              background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                              on_press= lambda instance: self.despesas(None))
        
        caridade_button = Button(text='DOAÇÃO', size_hint=(0.3, 0.1),
                              font_size=40, color = (159/255.0,226/255.0,191/255.0,1),
                              pos_hint={"center_x": 0.4, "center_y": 0.52},
                              background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                              on_press= lambda instance: self.show_category_caridade(None))
        
        investimento_button = Button(text='INVESTIMENTOS', size_hint=(0.3, 0.1),
                              font_size=40, color = (159/255.0,226/255.0,191/255.0,1),
                              pos_hint={"center_x": 0.4, "center_y": 0.37},
                              background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                              on_press= lambda instance: self.show_category('Investimentos', None))
        
        quiz_button = Button(text='QUIZ', size_hint=(0.3, 0.1),
                              font_size=40, color = (159/255.0,226/255.0,191/255.0,1),
                              pos_hint={"center_x": 0.4, "center_y": 0.22},
                              background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                              on_press= lambda instance: self.PopQuizLayout(None))
        
        back_button = Button(text='Voltar', background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                             font_size = 30,
                             color = (159/255.0,226/255.0,191/255.0),
                             size_hint = (None, None),
                             size = (100,50),
                             pos_hint={"x":0, "y":0},
                             on_press=lambda instance: self.go_back())
        
        self.layout.add_widget(background)
        self.layout.add_widget(tabela_button)
        self.layout.add_widget(Despesas_mes_button)
        self.layout.add_widget(caridade_button)
        self.layout.add_widget(investimento_button)
        self.layout.add_widget(quiz_button)
        self.layout.add_widget(back_button)
               
#função para voltar à tela inicial
    def go_back(self):
        self.layout.clear_widgets()
        self.show_welcome_screen()

#função para exibição da tabela em si
    def calculate_budget(self, instance):
        self.recado = Label(text = 'Insira APENAS números! (sem vírgula/ponto)', font_size = 40,
                            bold = True, italic = True, color = (236/255.0,5/255.0,5/255.0,1)  )
        
        salary_text = self.salary_input.text

        try:
            salary = float(salary_text)
        except ValueError:
            return self.layout.add_widget(self.recado)
        
        self.layout.clear_widgets()
        
        grid = GridLayout(cols=2)
        background = Image(source='FinGest_t.png', 
                           allow_stretch=True, 
                           keep_ratio=True)
        
        
        #essas são as categorias
        categories = ['','','','','','']
        percentages = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]
        
        for category, percentage in zip(categories, percentages):
            category_label = Label(text=f'{category}')
            value_label = Label(text=f'R$ {salary * percentage:.2f}'.replace('.',','), bold = True, font_size = 40, color = (159/255.0,226/255.0,191/255.0,1))
            
            grid.add_widget(category_label)
            grid.add_widget(value_label)
        #botão volta para a tela inicial
        back_button = Button(text='Voltar',font_size = 25, 
                             background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                             color = (159/255.0,226/255.0,191/255.0),
                             size_hint = (0.07, 0.05),
                             pos_hint={"x":0.001, "y":0.001}, 
                             on_press=lambda instance: self.escolha(None))
        
        self.layout.add_widget(background)
        self.layout.add_widget(back_button)
        self.layout.add_widget(grid)

#função para criar o arquivo json
    def load_expenses(self):
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r") as f:
                self.expense_values = json.load(f)
        else:
            self.expense_values = [""] * 20

#função para abrir o arquivo json
    def save_expenses(self):
        with open("expenses.json", "w") as f:
            json.dump(self.expense_values, f)

#função para exibir os inputs em formato de lista
    def despesas(self, instance):
        # Limpar widgets da tela atual
        self.layout.clear_widgets()
        background = Image(source='FinGest_despesas.png', 
                           allow_stretch=True, 
                           keep_ratio=True)
        self.layout.add_widget(background)

        back_button = Button(text='Voltar',font_size = 25, 
                             background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                             color = (159/255.0,226/255.0,191/255.0),
                             size_hint = (0.07, 0.05),
                             pos_hint={"x":0.001, "y":0.001}, 
                             on_press=lambda instance: self.escolha(None))
        self.layout.add_widget(back_button)

        self.expense_inputs = []  # Lista para armazenar os TextInput de despesas

        # Adiciona os TextInput de despesas ao layout
        for i in range(10):
            expense_input = TextInput(hint_text='R$00,00 - CURTO PRAZO', multiline=False,
                                      pos_hint={"center_x": 0.30, "center_y": 0.8 - i * 0.08},
                                      background_color=(176/255.0, 252/255.0, 175/255.0, 1),
                                      size_hint=(None, None), size=(350, 50),
                                      text=self.expense_values[i])  # Carrega o valor salvo
            expense_input.bind(text=lambda instance, value, index=i: self.update_expense_value(index, value))  # Atualiza o valor na lista quando houver mudança
            self.expense_inputs.append(expense_input)
            self.layout.add_widget(expense_input)

        for i in range(10):
            expense_input = TextInput(hint_text='R$00,00 - LONGO PRAZO', multiline=False,
                                      pos_hint={"center_x": 0.7, "center_y": 0.8 - i * 0.08},
                                      background_color=(176/255.0, 252/255.0, 175/255.0, 1),
                                      size_hint=(None, None), size=(350, 50),
                                      text=self.expense_values[i + 10])  # Carrega o valor salvo
            expense_input.bind(text=lambda instance, value, index=i+10: self.update_expense_value(index, value))  # Atualiza o valor na lista quando houver mudança
            self.expense_inputs.append(expense_input)
            self.layout.add_widget(expense_input)

        return self.layout

#função pra salvar os inputs
    def update_expense_value(self, index, value):
        if index < len(self.expense_values):
            self.expense_values[index] = value
            self.save_expenses()
        
#interface do botão "caridade"
    def show_category_caridade(self, instance):
        self.layout.clear_widgets()

        background = Image(source='FinGest_caridade.png', 
                           allow_stretch=True, 
                           keep_ratio=True)
        self.layout.add_widget(background)

        grid = GridLayout(cols=2)
        
        charity_links = [
            "https://www.novosertao.org.br",
            "https://www.aldeiasinfantis.org.br",
            "https://aacd.org.br",
            "https://habitatbrasil.org.br/quem-somos/nossa-historia",
            "https://doe.msf.org.br"
        ]

        # Adicionando os botões à esquerda da tela
        # Adicionando os botões à esquerda da tela
        for i, link in enumerate(charity_links[:5]):
            charity_button = Button(text=f'{link}', 
                                background_color=(7/255.0, 26/255.0, 215/255.0, 1),
                                font_size=30, color=(159/255.0, 226/255.0, 191/255.0, 1),
                                size_hint=(None, None), size=(200, 50),
                                pos=(self.layout.width * 0.2, self.layout.height * (0.7 - i * 0.1)))
            charity_button.bind(on_press=lambda instance, url=link: self.open_charity_link(url))
            grid.add_widget(charity_button)

    
        # Adicionando os botões à direita da tela
        for i, link in enumerate(charity_links[5:]):
            charity_button = Button(text=f'{link}', 
                                background_color=(7/255.0, 26/255.0, 215/255.0, 1),
                                font_size=30, color=(159/255.0, 226/255.0, 191/255.0, 1),
                                size_hint=(None, None), size=(200, 50),
                                pos=(self.layout.width * 0.7, self.layout.height * (0.7 - i * 0.1)))
            charity_button.bind(on_press=lambda instance, url=link: self.open_charity_link(url))
            grid.add_widget(charity_button)

        # botão volta para a tela com a tabela
        back_button = Button(text='Voltar', background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                             font_size = 30,
                             color = (159/255.0,226/255.0,191/255.0),
                             size_hint = (None, None),
                             size = (100,50),
                             pos_hint={"x":0, "y":0},
                             on_press=lambda instance: self.escolha(None))

        self.layout.add_widget(grid)
        self.layout.add_widget(back_button)

#função para abrir os links de caridade
    def open_charity_link(self, url):
        webbrowser.open(url)

#função da tela "investimentos"
    def show_category(self, category, amount):
        self.layout.clear_widgets()

        grid = GridLayout(cols=1)
        #botão volta para a tabela
        back_button = Button(text='Voltar', background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                             font_size = 30,
                             color = (159/255.0,226/255.0,191/255.0),
                             size_hint = (None, None),
                             size = (100,50),
                             pos_hint={"x":0, "y":0},
                             on_press=lambda instance: self.escolha(None))
        
        grid.add_widget(back_button)

        if category == 'Investimentos':
            risk_label = Label(text='Qual o nível de risco que você está disposto a correr?', 
                               font_size = 40,
                               color = (12/255.0,212/255.0,170/255.0,1),
                               italic = True, bold = True)
            grid.add_widget(risk_label)
            #questionário para conhecer o perfil do investidor
            risk_buttons = [
                ("Alto", lambda: self.show_investment_links("Alto")),
                ("Médio", lambda: self.show_investment_links("Médio")),
                ("Baixo", lambda: self.show_savings_advice())
            ]

            for risk, callback in risk_buttons:
                risk_button = Button(text=risk,background_color=(7/255.0, 26/255.0, 215/255.0,1), font_size = 40, color = (159/255.0,226/255.0,191/255.0,1),
                                      pos_hint = {"center_x": 0.5, "y": 0.5}, size = (700,300) )
                risk_button.bind(on_press=lambda instance, cb=callback: cb())
                grid.add_widget(risk_button)

        self.layout.add_widget(grid)

#função de acordo com a escolha do investidor (botão)
    def show_investment_links(self, risk_level):
        self.layout.clear_widgets()

        grid = GridLayout(cols=1)

        back_button = Button(text='Voltar', background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                             font_size = 30,
                             color = (159/255.0,226/255.0,191/255.0),
                             size_hint = (None, None),
                             size = (100,50),
                             pos_hint={"x":0, "y":0},
                             on_press=lambda instance: self.show_category('Investimentos', 0))
        
        if risk_level == "Alto":
            grid.add_widget(Label(text=f'AÇÕES', font_size = 50, color = (12/255.0,212/255.0,170/255.0,1), italic = True, bold = True, outline_width =  10))
            grid.add_widget(Label(text=f'ALZR11 / HGCR11 / CPTS11 ', font_size = 30, color = (12/255.0,212/255.0,170/255.0,1), italic = True, bold = True, outline_width =  10))
        elif risk_level == "Médio":
            grid.add_widget(Label(text=f'TÍTULOS DO GOVERNO', font_size = 50, color = (12/255.0,212/255.0,170/255.0,1), italic = True, bold = True, outline_width =  10))
            
        # para mostrar links de acordo com o nível de risco
        if risk_level == "Alto":
            #links para investimentos de alto risco (ações)
            investment_links = [
                "https://www.fundsexplorer.com.br/funds/alzr11",
                "https://www.fundsexplorer.com.br/funds/hgcr11",
                "https://www.fundsexplorer.com.br/funds/cpts11"
            ]
            for link in investment_links:
                investment_button = Button(text=f'{link}', color = (159/255.0,226/255.0,191/255.0,1),background_color=(7/255.0, 26/255.0, 215/255.0,1))
                investment_button.bind(on_press=lambda instance, url=link: self.open_investment_link(url))
                
                grid.add_widget(investment_button)

        #a mesma lógica
        if risk_level == "Médio":
            #links para investimentos de médio risco (títulos do governo)
            investment_links = [
                "https://www.gov.br/investidor/pt-br/investir/tipos-de-investimentos/titulos-publicos",
                "https://www.tesourodireto.com.br/",
                "https://www.bb.com.br/site/investimentos/tesouro-direto/"
            ]
            for link in investment_links:
                investment_button = Button(text=f'{link}', color = (159/255.0,226/255.0,191/255.0,1), background_color=(7/255.0, 26/255.0, 215/255.0,1))
                investment_button.bind(on_press=lambda instance, url=link: self.open_investment_link(url))
                grid.add_widget(investment_button)
        

        grid.add_widget(back_button)
        self.layout.add_widget(grid)

#função para pequeno risco - é mais um conselho
    def show_savings_advice(self):
        self.layout.clear_widgets()

        grid = GridLayout(cols=1)

        back_button = Button(text='Voltar', background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                             font_size = 30,
                             color = (159/255.0,226/255.0,191/255.0),
                             size_hint = (None, None),
                             size = (100,50),
                             pos_hint={"x":0, "y":0},
                             on_press=lambda instance: self.show_category('Investimentos', 0))
        grid.add_widget(Label(text='Deposite seu dinheiro na Poupança!', 
                              font_size = 50, 
                              color = (12/255.0,212/255.0,170/255.0,1), 
                              italic = True, bold = True, outline_width =  10))
        grid.add_widget(Label(text='Simulador da Poupança', 
                              font_size = 40, 
                              color = (12/255.0,212/255.0,170/255.0,1)))
        grid.add_widget(Label(text='A poupança oferece segurança e liquidez imediata,\nideal para preservar seu capital e atender a metas de curto prazo.', 
                              font_size = 23, 
                              color = (12/255.0,212/255.0,170/255.0,1)))
        grid.add_widget(Label(text='Considere diversificar no futuro, enquanto acompanhamos juntos o crescimento do seu patrimônio.', 
                              font_size = 25, 
                              color = (12/255.0,212/255.0,170/255.0,1)))
        grid.add_widget(Label(text='Continue economizando com inteligência para alcançar seus objetivos financeiros!', 
                              font_size = 25, 
                              color = (12/255.0,212/255.0,170/255.0,1)))
        grid.add_widget(back_button)
    
        self.layout.add_widget(grid)

#para abrir os links dos investimentos
    def open_investment_link(self, url):
        webbrowser.open(url)


questions = [
    {
        "question": "What is the smallest country in the world?",
        "possible_answers": ["Vatican City", "Monaco", "San Marino", "Liechtenstein"],
        "correct_answer": "Vatican City"
    },
    {
        "question": "What is the highest mountain in the world?",
        "possible_answers": ["Mount Kilimanjaro","Mount Everest", "Mount McKinley", "Mount Fuji"],
        "correct_answer": "Mount Everest"
    },
    {
        "question": "Who invented the telephone?",
        "possible_answers": ["Thomas Edison", "Nikola Tesla", "Guglielmo Marconi", "Alexander Graham Bell"],
        "correct_answer": "Alexander Graham Bell"
    },
]


game_state = {
    "question_index": 0,
    "score": 0
}


class PopQuizLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.next_question()


    def next_question(self):
        question_index = game_state["question_index"]

        if question_index >= len(questions): 
            self.game_over() 
            return

        current_question = questions[question_index]
        self.ids.question_count.text = f"Q: {question_index+1}/{len(questions)}"
        self.ids.question_text.text = current_question["question"]
        for i in range(4):
            self.ids[f"answer_btn_{i+1}"].text = current_question["possible_answers"][i]

        game_state["question_index"] += 1

    def game_over(self):
        self.ids.question_text.text = f"Game Over! Your Score: {game_state['score']}/{len(questions)}"
        self.ids.answer_grid.clear_widgets()
        self.ids.answer_grid.add_widget(Button(text="Retry", on_press=self.start_over))

    def answer_callback(self, answer):
        def func(_):
            return self.answer_handler(answer)
        return func

    def start_over(self, _):
        self.ids.answer_grid.clear_widgets()
        for i in range(4):
            button = Button(text="Loading text...", on_press=self.answer_callback(i+1))
            self.ids[f"answer_btn_{i+1}"] = button
            self.ids.answer_grid.add_widget(button)

        game_state["question_index"] = 0
        game_state["score"] = 0

        self.next_question()

    def answer_handler(self, answer):
        question_index = game_state["question_index"]-1
        if questions[question_index]["correct_answer"] == questions[question_index]["possible_answers"][answer-1]:
            game_state["score"] += 1

        self.next_question()

class PopQuizApp(App):
    def build(self):
        return PopQuizLayout()  

#função pra sair do app
    def exit_app(self, instance):
        App.get_running_app().stop()

if __name__ == '__main__':
    FinGest().run()
