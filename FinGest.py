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
from kivy.uix.relativelayout import RelativeLayout
import webbrowser 

class FinGestApp(App):
    def build(self):
        Window.clearcolor = ( 5/255.0, 69/255.0, 4/255.0, 1)
        self.layout = BoxLayout(orientation='vertical')
        self.layout = RelativeLayout()
        self.show_welcome_screen()
        return self.layout
#tela inicial de boas-vindas
    def show_welcome_screen(self):
        background = Image(source='FinGest.png', allow_stretch=True, keep_ratio=False)
        
        #esse botão direciona para a 2ª interface
        start_button = Button(text='SIM!', size_hint=(0.3, 0.3),
                              font_size=45,
                              pos_hint={"center_x": 0.5, "center_y": 0.5},
                              background_color=(246/255.0, 249/255.0, 6/255.0, 1),
                              on_press=self.show_salary_input)
        start_button.pos = (Window.width / 2 - start_button.width / 2, Window.height / 2 - start_button.height / 2)
        start_button.size = (300, 100) 
        
        self.layout.clear_widgets()
        self.layout.add_widget(start_button)
        self.layout.add_widget(background)
#tela pra o usuário adicionar o seu salário para análise
    def show_salary_input(self, instance):
        self.layout.clear_widgets()
        
        self.salary_label = Label(text='Digite o seu salário', font_size = 80, bold = True, italic = True,
                                  pos_hint={"center_x": 0.5, "center_y": 0.9}, 
                                  color = (245/255.0,192/255.0,11/255.0,1))
        self.salary_input = TextInput(hint_text='Insira o salário', multiline=False,  
                                      pos_hint={"center_x": 0.5, "center_y": 0.6},
                                      background_color = (176/255.0, 252/255.0, 175/255.0,1),
                                      size_hint=(None,None), size = (300,50) ) #alterei aqui
        
        #botão que direciona para a interface que contém todos os cálculos exibidos
        self.submit_button = Button(text='Enviar', font_size = 50,size_hint = (0.3, 0.3),
                                    pos_hint={"center_x": 0.5, "y": self.salary_input.y + self.salary_input.height},
                                    background_color = (246/255.0,249/255.0,6/255.0,1),
                                    on_press=self.calculate_budget)

        self.layout.add_widget(self.salary_label)
        self.layout.add_widget(self.salary_input)
        self.layout.add_widget(self.submit_button)
#função para exibição da tabela em si
    def calculate_budget(self, instance):
        self.recado = Label(text = 'Insira um número válido!', font_size = 40,
                            bold = True, italic = True, color = (236/255.0,5/255.0,5/255.0,1)  )
        try:
            salary = float(self.salary_input.text)
        except ValueError:
            return self.layout.add_widget(self.recado)
        
        self.layout.clear_widgets()
        
        grid = GridLayout(cols=2)
        
        #esses são os botões específicos da tabela; para adicionar mais funcionalidades ao aplicativo
        charity_button = Button(text='Caridade ->', background_color = (7/255.0, 26/255.0, 215/255.0,1),
                                bold = True, font_size =40,
                                on_press=lambda instance: self.show_category_caridade('Caridade', salary * 0.1))
        investment_button = Button(text='Investimentos ->',  background_color = (7/255.0, 26/255.0, 215/255.0,1),
                                    bold = True,font_size =40,
                                   on_press=lambda instance: self.show_category('Investimentos', salary * 0.1))
        
        grid.add_widget(charity_button)
        grid.add_widget(Label(text=f'R$ {salary * 0.1:.2f}', font_size = 40, bold = True))
        grid.add_widget(investment_button)
        grid.add_widget(Label(text=f'R$ {salary * 0.1:.2f}', font_size = 40, bold = True))
        
        categories = ['Diversão', 'Despesas de Longo Prazo', 'Livros', 'Necessidades Básicas']
        percentages = [0.1, 0.1, 0.1, 0.5]
        
        for category, percentage in zip(categories, percentages):
            category_label = Label(text=f'{category} ->', bold = True, font_size = 40)
            value_label = Label(text=f'R$ {salary * percentage:.2f}', bold = True, font_size = 40)
            
            grid.add_widget(category_label)
            grid.add_widget(value_label)
        #botão volta para a tela inicial
        back_button = Button(text='Voltar',font_size = 30, 
                             background_color = (246/255.0,249/255.0,6/255.0,1),
                             size_hint = (None, None),
                             
                             pos_hint={"x":0.1, "y":0.1}, 
                             on_press=lambda instance: self.go_back())
        self.layout.add_widget(back_button)
        self.layout.add_widget(grid)
    #interface do botão "caridade"
    def show_category_caridade(self, category, amount):
        self.layout.clear_widgets()
        
        grid = GridLayout(cols=1)
        # botão volta para a tela com a tabela
        back_button = Button(text='Voltar', background_color = (246/255.0,249/255.0,6/255.0,1),
                             font_size = 30,
                             size_hint = (None, None),
                             size = (100,50),
                             pos_hint={"x":0, "y":0},
                             
                             on_press=lambda instance: self.calculate_budget(None))
        
        grid.add_widget(Label(text='"A caridade é um exercício espiritual... Quem pratica o bem, coloca em movimento as forças da alma."', 
                              font_size = 25,
                              italic = True))
        grid.add_widget(Label(text='Escolha um link e faça a sua doação:', font_size = 45, italic = True))
        charity_links = [
            "https://www.novosertao.org.br/",
            "https://www.aldeiasinfantis.org.br/",
            "https://aacd.org.br/",
            "https://habitatbrasil.org.br/quem-somos/nossa-historia/",
            "https://doe.msf.org.br/"
        ]

        for link in charity_links:
            charity_button = Button(text=f'{link}', background_color=(7/255.0, 26/255.0, 215/255.0,1))
            charity_button.bind(on_press=lambda instance, url=link: self.open_charity_link(url))
            grid.add_widget(charity_button)

        self.layout.add_widget(grid)
        self.layout.add_widget(back_button)
    #função para abrir os links de caridade
    def open_charity_link(self, url):
        webbrowser.open(url)
    #função para voltar à tela inicial
    def go_back(self):
        self.layout.clear_widgets()
        self.show_welcome_screen()


    #função da tela "investimentos"
    def show_category(self, category, amount):
        self.layout.clear_widgets()

        grid = GridLayout(cols=1)
        #botão volta para a tabela
        back_button = Button(text='Voltar', background_color=(246/255.0,249/255.0,6/255.0,1),
                             font_size = 30,
                             size_hint = (None, None),
                             size = (100,50),
                             pos_hint={"x":0, "y":0},
                             on_press=lambda instance: self.calculate_budget(None))
        
        grid.add_widget(back_button)

        if category == 'Investimentos':
            risk_label = Label(text='Qual o nível de risco que você está disposto a correr?', font_size = 40)
            grid.add_widget(risk_label)
            #questionário para conhecer o perfil do investidor
            risk_buttons = [
                ("Alto", lambda: self.show_investment_links("Alto")),
                ("Médio", lambda: self.show_investment_links("Médio")),
                ("Baixo", lambda: self.show_savings_advice())
            ]

            for risk, callback in risk_buttons:
                risk_button = Button(text=risk,background_color=(7/255.0, 26/255.0, 215/255.0,1), font_size = 40,
                                      pos_hint = {"center_x": 0.5, "y": 0.5}, size = (700,300) )
                risk_button.bind(on_press=lambda instance, cb=callback: cb())
                grid.add_widget(risk_button)

        self.layout.add_widget(grid)
    #função de acordo com a escolha do investidor (botão)
    def show_investment_links(self, risk_level):
        self.layout.clear_widgets()

        grid = GridLayout(cols=1)

        back_button = Button(text='Voltar', background_color=(246/255.0,249/255.0,6/255.0,1),
                             font_size = 30,
                             size_hint = (None, None),
                             size = (100,50),
                             pos_hint={"x":0, "y":0},
                             on_press=lambda instance: self.show_category('Investimentos', 0))
        
        if risk_level == "Alto":
            grid.add_widget(Label(text=f'AÇÕES', font_size = 50, italic = True, bold = True, outline_width =  10))
            grid.add_widget(Label(text=f'ALZR11 / HGCR11 / CPTS11 ', font_size = 30, italic = True, bold = True, outline_width =  10))
        elif risk_level == "Médio":
            grid.add_widget(Label(text=f'TÍTULOS DO GOVERNO', font_size = 50, italic = True, bold = True, outline_width =  10))
            
        # para mostrar links de acordo com o nível de risco
        if risk_level == "Alto":
            #links para investimentos de alto risco (ações)
            investment_links = [
                "https://www.fundsexplorer.com.br/funds/alzr11",
                "https://www.fundsexplorer.com.br/funds/hgcr11",
                "https://www.fundsexplorer.com.br/funds/cpts11"
            ]
            for link in investment_links:
                investment_button = Button(text=f'{link}', background_color=(7/255.0, 26/255.0, 215/255.0,1))
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
                investment_button = Button(text=f'{link}',background_color=(7/255.0, 26/255.0, 215/255.0,1))
                investment_button.bind(on_press=lambda instance, url=link: self.open_investment_link(url))
                grid.add_widget(investment_button)
        

        grid.add_widget(back_button)
        self.layout.add_widget(grid)
#função para pequeno risco - é mais um conselho
    def show_savings_advice(self):
        self.layout.clear_widgets()

        grid = GridLayout(cols=1)

        back_button = Button(text='Voltar', background_color=(246/255.0,249/255.0,6/255.0,1),
                             font_size = 30,
                             size_hint = (None, None),
                             size = (100,50),
                             pos_hint={"x":0, "y":0},
                             on_press=lambda instance: self.show_category('Investimentos', 0))
        grid.add_widget(Label(text='Deposite seu dinheiro na Poupança!', font_size = 50, italic = True, bold = True, outline_width =  10))
        grid.add_widget(Label(text='Por que investir na Poupança?\n 1ª)É seguro e protegido; \n 2ª)É uma opção muito acessível e de fácil abertura; \n 3ª)É isenta de Imposto de Renda; \n 4ª)Oferece uma rentabilidade estável.', font_size = 40))
        grid.add_widget(Label(text='-> É a melhor opção para quem busca um investimento de baixo risco.', font_size = 35, italic = True))
        grid.add_widget(back_button)
    
        self.layout.add_widget(grid)
#para abrir os links dos investimentos
    def open_investment_link(self, url):
        webbrowser.open(url)


if __name__ == '__main__':
    FinGestApp().run()
