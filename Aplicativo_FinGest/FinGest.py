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
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import os
import json
import webbrowser 
from kivy.clock import Clock

# classe principal do app
class FinGest(App):
    def build(self):
        Window.clearcolor = ( 4/255.0, 10/255.0, 56/255.0, 1)
        self.layout = FloatLayout()
        self.load_expenses() #carrega as despesas salvas
        self.show_welcome_screen()
        return self.layout

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.test_completed = False  # Variável de estado para rastrear se o teste foi concluído
        self.default_percentages = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]
    
  
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
                             on_press=App.get_running_app().stop)
    
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
                                    background_color=(84/255.0, 255/255.0, 4/255.0, 1),
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
                              pos_hint={"center_x": 0.4, "center_y": 0.8},
                              background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                              on_press=self.calculate_budget)
        
        Despesas_mes_button = Button(text='DESPESAS', size_hint=(0.3, 0.1),
                              font_size=40, color = (159/255.0,226/255.0,191/255.0,1),
                              pos_hint={"center_x": 0.4, "center_y": 0.61},
                              background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                              on_press= lambda instance: self.despesas(None))
        
        caridade_button = Button(text='DOAÇÃO', size_hint=(0.3, 0.1),
                              font_size=40, color = (159/255.0,226/255.0,191/255.0,1),
                              pos_hint={"center_x": 0.4, "center_y": 0.42},
                              background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                              on_press= lambda instance: self.show_category_caridade(None))
        
        investimento_button = Button(text='INVESTIMENTOS', size_hint=(0.3, 0.1),
                              font_size=40, color = (159/255.0,226/255.0,191/255.0,1),
                              pos_hint={"center_x": 0.4, "center_y": 0.24},
                              background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                              on_press=self.start_investment_profile_test)
        
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
        #self.layout.add_widget(quiz_button)
        self.layout.add_widget(back_button)
               
#função para voltar à tela inicial
    def go_back(self):
        self.layout.clear_widgets()
        self.show_welcome_screen()

#função para exibição da tabela em si
    def calculate_budget(self, instance):
        salary_text = self.salary_input.text

        try:
            salary = float(salary_text)
        except ValueError:
            self.layout.clear_widgets()  # Limpa os widgets anteriores
            self.layout.add_widget(Label(text='Insira APENAS números! (sem vírgula/ponto)', 
                                          font_size=40, color=(236/255.0, 5/255.0, 5/255.0, 1)))
            Clock.schedule_once(self.show_salary_input, 2)  # Chama show_salary_input após 2 segundos
            return
        
        self.layout.clear_widgets()
        
        grid = GridLayout(cols=2, padding=(100, 50), spacing=10)
        background = Image(source='FinGest_t.png', 
                           allow_stretch=True, 
                           keep_ratio=True)
        
        
        #essas são as categorias
        categories = ['','','','','','']
        #percentages = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]
        
        for category, percentage in zip(categories, self.default_percentages):
            category_label = Label(text=f'{category}')
            value_label = Label(text=f'R$ {salary * percentage:.2f}'.replace('.',','), 
                                bold = True, font_size = 40, 
                                color = (159/255.0,226/255.0,191/255.0,1))
            
            grid.add_widget(category_label)
            grid.add_widget(value_label)
        #botão volta para a tela inicial
        back_button = Button(text='Voltar',font_size = 25, 
                             background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                             color = (159/255.0,226/255.0,191/255.0),
                             size_hint = (0.07, 0.05),
                             pos_hint={"x":0.001, "y":0.001}, 
                             on_press=lambda instance: self.escolha(None))
        
        customize_button = Button(text='Personalizar', font_size = 25, 
                                  background_color=(84/255.0, 255/255.0, 4/255.0, 1),
                                  color = (159/255.0,226/255.0,191/255.0),
                                  size_hint=(None, None), size=(150, 50),
                                  pos=(Window.width - 151, 0.6),
                                  on_press=self.open_customize_popup)
        
        self.layout.add_widget(background)
        self.layout.add_widget(back_button)
        self.layout.add_widget(customize_button)
        self.layout.add_widget(grid)

#função para abrir o popup de customização das porcentagens
    def open_customize_popup(self, instance):
    # Aqui você pode criar a popup para permitir que o usuário personalize as porcentagens
        popup_content = BoxLayout(orientation='horizontal')

        grid_left = GridLayout(cols=1, size_hint=(0.5, 1))
        grid_right = GridLayout(cols=1, size_hint=(0.5, 1))
        


        categories = ['Necessidades Básicas', 'Despesas Longo Prazo', 'Diversão', 'Investimentos', 'Conhecimento', 'Caridade']
    
        self.percentage_inputs = []
        for i, category in enumerate(categories):
            grid_left.add_widget(Label(text=category, size_hint_y=None, height=70))
            percentage_input = TextInput(text=str(self.default_percentages[i]), size_hint_y=None, height=70)
            self.percentage_inputs.append(percentage_input)
            grid_right.add_widget(percentage_input)

        popup_content.add_widget(grid_left)
        popup_content.add_widget(grid_right)
    
        popup = Popup(title='Customize', content=popup_content,
              size_hint=(None, None), size=(800, 500))
        popup.bind(on_dismiss=self.update_values)
        popup.open()

#função para atualizar a tabela de acordo com o que o usuário alterar
    def update_values(self, instance):
        # Atualize os valores das porcentagens com os valores digitados pelo usuário
        new_percentages = [float(input.text) for input in self.percentage_inputs]
        self.default_percentages = new_percentages
        self.calculate_budget(instance)

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

        box_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        charity_links = [
            "https://doeamor.hospitaldeamor.com.br/stn/?utm_source=google_gsn_doacao_st&gad_source=1&gclid=Cj0KCQiAw6yuBhDrARIsACf94RVktDjDT1hVBCPQ1vVOLSOa2eLCT4a_9JEDBi1V5mdGaJZnoDsEF5YaAkemEALw_wcB",
            "https://www.novosertao.org.br",
            "https://aacd.org.br",
            "https://help.unicef.org/pmax?gad_source=1&language=pt-br",
            "https://doe.msf.org.br",
            "https://www.fundacaoaio.org.br/projeto-samuel",
            "https://www.care.org/pt/",
            "https://colabore.cicv.org.br/israel-territorios-ocupados/?utm_source=google&utm_medium=search&utm_campaign=emergency-ilot-2023&gclid=Cj0KCQiAw6yuBhDrARIsACf94RX6D8rmgohy9KKvWV3CgGGtFlzVb-RoFVi2St0RYJHygCgrpj_lkMkaAjRnEALw_wcB",
            "https://www.petlove.com.br/doacoes"]
        
        charity_names = [
        "Hospital do Câncer",
        "Novo Sertão",
        "AACD",
        "UNICEF",
        "Médicos Sem Fronteiras",
        "Projeto Samuel",
        "CARE",
        "CICV",
        "PETLOVE"]


        for name, link in zip(charity_names, charity_links):
            charity_button = Button(text=name, 
                            background_color=(7/255.0, 26/255.0, 215/255.0, 1),
                            font_size=30, color=(159/255.0, 226/255.0, 191/255.0, 1),
                            size_hint=(None, None), size=(400, 60),
                            pos_hint={"center_x": 0.5}, 
                            valign='middle')  # Centraliza o texto verticalmente
            charity_button.bind(on_press=lambda instance, url=link: self.open_charity_link(url))
            box_layout.add_widget(charity_button)

        # botão volta para a tela com a tabela
        back_button = Button(text='Voltar', background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                             font_size = 30,
                             color = (159/255.0,226/255.0,191/255.0),
                             size_hint = (None, None),
                             size = (100,50),
                             pos_hint={"x":0, "y":0},
                             on_press=lambda instance: self.escolha(None))

        #self.layout.add_widget(grid)
        self.layout.add_widget(back_button)
        self.layout.add_widget(box_layout)

#função para abrir os links de caridade
    def open_charity_link(self, url):
        webbrowser.open(url)

#função da tela "investimentos" - teste de perfil_investidor
    def start_investment_profile_test(self, instance):
        if not self.test_completed: # Verifique se o teste já foi realizado
            self.layout.clear_widgets()

            grid = GridLayout(cols=1)
        
            back_button = Button(text='Voltar', background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                             font_size = 30,
                             color = (159/255.0,226/255.0,191/255.0),
                             size_hint = (None, None),
                             size = (100,50),
                             pos_hint={"x":0, "y":0},
                             on_press=lambda instance: self.escolha(None))
        
            grid.add_widget(back_button)
        

            self.questions = [
            ("Qual é o seu horizonte de investimento?", ["Curto prazo", "Médio prazo", "Longo prazo"]),
            ("Qual é a sua tolerância ao risco?", ["Baixa", "Média", "Alta"]),
            ("Qual é o seu objetivo financeiro principal?", ["Preservação de capital", "Crescimento moderado", "Crescimento máximo"]),
            ]
            self.answers = []
            self.show_question(0)
        #botão volta para a tabela
        else:
        # Se o teste já foi concluído, vá diretamente para a tela de resultado
            self.show_investment_advice(self.get_saved_risk_level())
        
    #função para aparição de cada pergunta
    def show_question(self, question_index):
        self.layout.clear_widgets()  # Limpa os widgets anteriores
    
        grid = GridLayout(cols=1, padding=(330, 50), spacing=20)

        question_label = Label(text=self.questions[question_index][0],
                            font_size = 50,
                            color = (174/255.0,214/255.0,241/255.0,1), 
                           italic = True, bold = True, 
                           outline_width =  10)  # Definir a altura do rótulo da pergunta
        grid.add_widget(question_label)

        options = self.questions[question_index][1]
        for option in options:
            option_button = Button(text=option, 
                               font_size=50, 
                               color=(174/255.0,214/255.0,241/255.0,1),
                               size_hint=(None, None),
                               size=(550, 200),
                               background_color=(118/255.0, 215/255.0, 296/255.0,1),
                               pos_hint={"center_x": 0.5, "center_y": 0.5})
            option_button.bind(on_press=lambda instance, option=option: self.process_answer(option, question_index))
            grid.add_widget(option_button)  # Adiciona o botão de opção ao GridLayout
        
        self.layout.add_widget(grid) 
    
    #função para apresentar perguntas e coletar respostas
    def process_answer(self, answer, question_index):
        self.answers.append(answer)

        if question_index < len(self.questions) - 1:
            self.layout.clear_widgets()
            self.show_question(question_index + 1)
        else:
            self.layout.clear_widgets()
            self.process_answers()

    #função para calcular o resultado
    def process_answers(self):
        score = 0
        for answer in self.answers:
            if answer in ["Curto prazo", "Baixa", "Preservação de capital"]:
                score += 1
            elif answer in ["Médio prazo", "Média", "Crescimento moderado"]:
                score += 2
            elif answer in ["Longo prazo", "Alta", "Crescimento máximo"]:
                score += 3

        if score <= 4:
            risk_level = "Conservador"
        elif score <= 7:
            risk_level = "Moderado"
        else:
            risk_level = "Arrojado"
        
        self.save_risk_level(risk_level)
        # Marque o teste como concluído
        self.test_completed = True
        # Exiba o resultado
        self.show_investment_advice(risk_level)

    #função para exibir a tela final de acordo com o resultado do teste
    def show_investment_advice(self, risk_level):
        self.layout.clear_widgets()
        grid = GridLayout(cols=1, padding=(490, 420), spacing=20)


        if risk_level == "Conservador":
            background = Image(source='FinGest_conservador.png', 
                           allow_stretch=True, 
                           keep_ratio=True)
            self.layout.add_widget(background)
            investment_links = [
                "https://www.idinheiro.com.br/calculadoras/calculadora-rendimento-da-poupanca/",
                "https://www.santander.com.br/investimentos-e-previdencia/poupanca",
                "https://www.itau.com.br/investimentos/poupanca",
                "https://www.bb.com.br/site/investimentos/poupanca/?gad_source=1&gclid=Cj0KCQiA5rGuBhCnARIsAN11vgShYtpmN2AEshCZYgt0yrl1jMtZu4OVl3ypXVxuFo2vTDlxpmFF8NsaAjchEALw_wcB"
            ]
            invest_names = [
            "SIMULADOR",
            "SANTANDER",
            "ITAÚ",
            "BB"]
            for name, link in zip(invest_names, investment_links):
                investment_button = Button(text=name, font_size=30, size_hint=(None, None), 
                                           color = (174/255.0,214/255.0,241/255.0,1),
                                           size=(200, 100),
                                           background_color=(118/255.0, 215/255.0, 296/255.0,1))
                investment_button.bind(on_press=lambda instance, url=link: self.open_investment_link(url))
                grid.add_widget(investment_button)


        elif risk_level == "Moderado":
            background = Image(source='FinGest_moderado.png', 
                           allow_stretch=True, 
                           keep_ratio=True)
            self.layout.add_widget(background)
            investment_links = [
                "https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm",
                "https://www.bb.com.br/site/investimentos/tesouro-direto/?gad_source=1&gclid=Cj0KCQiA5rGuBhCnARIsAN11vgR4QMaW8rfQDKNpZxZE0buaBaqRwY6YKONqsmrKeAw0T4Ypp3ODdEUaAuTcEALw_wcB",
                "https://www.caixa.gov.br/voce/poupanca-e-investimentos/tesouro-direto/Paginas/default.aspx",
                "https://www.agorainvestimentos.com.br/html/investimentos/renda-fixa/tesouro-direto.html"
            ]
            invest_names = [
            "SIMULADOR",
            "BB",
            "CAIXA",
            "ÁGORA"]
            for name, link in zip(invest_names, investment_links):
                investment_button = Button(text=name, font_size=30, size_hint=(None, None), 
                                           color = (174/255.0,214/255.0,241/255.0,1),
                                           size=(200, 100),
                                           background_color=(118/255.0, 215/255.0, 296/255.0,1))
                investment_button.bind(on_press=lambda instance, url=link: self.open_investment_link(url))
                grid.add_widget(investment_button)

        elif risk_level == "Arrojado":
            background = Image(source='FinGest_arrojado.png', 
                           allow_stretch=True, 
                           keep_ratio=True)
            self.layout.add_widget(background)
            investment_links = [
                "https://investnews.com.br/ferramentas/simuladores/simulador-carteira-de-acoes/",
                "https://www.xpi.com.br/produtos/acoes/",
                "https://www.nuinvest.com.br/",
                "https://www.rico.com.vc/produtos/fundos-imobiliarios/?campaignid=18578302741&adgroupid=161839022784&feeditemid=&targetid=aud-896835459498:kwd-900845052163&loc_interest_ms=&loc_physical_ms=1031556&matchtype=b&network=g&device=c&devicemodel=&ifmobile=&ifmobile=0&ifsearch=1&ifsearch=&ifcontent=0&ifcontent=&creative=678627166745&keyword=comprar%20cotas%20fundo%20imobiliario&placement=&target=&utm_source=google&utm_medium=cpc&utm_term=comprar%20cotas%20fundo%20imobiliario&utm_campaign=GGLE_PESQ_Brand_Geral&hsa_tgt=aud-896835459498:kwd-900845052163&hsa_net=adwords&hsa_kw=comprar%20cotas%20fundo%20imobiliario&hsa_grp=161839022784&hsa_acc=7134496929&hsa_ver=3&hsa_ad=678627166745&hsa_cam=312991906&hsa_mt=b&hsa_src=g&gclid=Cj0KCQiA5rGuBhCnARIsAN11vgRqK4rjkQ6WukQ3VJCStwmp1u8fdYmT4z9OrUzp-ib7LE2H8-bzaOsaAhSmEALw_wcB"
            ]
            invest_names = [
            "SIMULADOR",
            "XP - ações",
            "NUInvest",
            "RICO - FIIs"]
            for name, link in zip(invest_names, investment_links):
                investment_button = Button(text=name, font_size=30, size_hint=(None, None), 
                                           color = (174/255.0,214/255.0,241/255.0,1),
                                           size=(200, 100),
                                           background_color=(118/255.0, 215/255.0, 296/255.0,1))
                investment_button.bind(on_press=lambda instance, url=link: self.open_investment_link(url))
                grid.add_widget(investment_button)

        self.layout.add_widget(grid)

        back_button = Button(text='Voltar', background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                             font_size = 30,
                             color = (159/255.0,226/255.0,191/255.0),
                             size_hint = (None, None),
                             size = (100,50),
                             pos_hint={"x":0, "y":0},
                             on_press=lambda instance: self.escolha(None))
        self.layout.add_widget(back_button)

        if self.test_completed:
            redo_button = Button(text='Refazer teste', background_color=(84/255.0, 255/255.0, 4/255.0, 1),
                         font_size=30,
                         color=(159/255.0, 226/255.0, 191/255.0),
                         size_hint=(None, None),
                         size=(200, 50),
                         pos_hint={"center_x": 0.92},
                         on_press=lambda instance: self.reset_test())
            self.layout.add_widget(redo_button)
    
    #lógica para RECUPERAR o nível de risco salvo
    def get_saved_risk_level(self):
        return self.saved_risk_level
  
    #lógica para SALVAR o nível de risco 
    def save_risk_level(self, risk_level):
        self.saved_risk_level = risk_level
    
    #função para refazer o teste_investidor
    def reset_test(self):
        self.test_completed = False
        self.saved_risk_level = None
        self.start_investment_profile_test(None)
    
    #função para abrir os links de investimentos
    def open_investment_link(self, url):
        webbrowser.open(url)

if __name__ == '__main__':
    FinGest().run()
