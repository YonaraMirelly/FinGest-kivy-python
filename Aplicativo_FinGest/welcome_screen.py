from kivy.uix.image import Image
from kivy.uix.button import Button

def show_welcome_screen(layout, show_salary_input, exit_app):
    background = Image(source='FinGest_melhor.png', 
                       allow_stretch=True, 
                       keep_ratio=True)

    # Botão para direcionar para a 2ª interface
    start_button = Button(text='Gerir Agora!', size_hint=(0.3, 0.1),
                          font_size=45, color=(159/255.0,226/255.0,191/255.0,1),
                          pos_hint={"center_x": 0.5, "center_y": 0.2},
                          background_color=(118/255.0, 215/255.0, 196/255.0, 1),
                          on_press=show_salary_input)

    # Botão para sair do app
    exit_button = Button(text='Sair do App', size_hint=(0.3, 0.1),
                         font_size=45, color=(159/255.0, 226/255.0, 191/255.0, 1),
                         pos_hint={"center_x": 0.5, "center_y": 0.1},
                         background_color=(120/255.0, 5/255.0, 89/255.0, 1),
                         on_press=exit_app)

    layout.add_widget(background)
    layout.add_widget(start_button)
    layout.add_widget(exit_button)
