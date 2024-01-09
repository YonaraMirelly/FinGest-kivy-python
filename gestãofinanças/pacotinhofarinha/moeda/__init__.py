def dividir10(pr = 0,t = 0, formato = False):
    menos50 = pr/2
    res = menos50 * (t/100)
    return res if not formato else moeda(res)

def diminuir50(pr = 0,t = 0, formato = False):
    res = pr -(pr * t/100)
    return res if not formato else moeda(res)

def moeda(pr = 0, moeda = 'R$'):
    return f'{moeda}{pr:.2f}'.replace('.', ',')

def resumo(pr = 0, taxaa = 20, taxar = 50 ):
    print('-'*50)
    print('O SEGREDO DA MENTE MILIONÁRIA'.center(50))
    print('-'*50)
    print(f'Salário analisado: \t\t\033[1;32m{moeda(pr)}\033[m')
    print('^~'*25)
    print(f'10% CARIDADE: \t\t\t{dividir10(pr,taxaa, True)}')
    print(f'10% INVESTIMENTO: \t\t{dividir10(pr,taxaa,True)}')
    print(f'10% DIVERSÃO: \t\t\t{dividir10(pr,taxaa,True)}')
    print(f'10% DESPESAS DE LONGO PRAZO: \t{dividir10(pr,taxaa,True)}')
    print(f'10% INSTRUÇÃO FINANCEIRA: \t{dividir10(pr,taxaa,True)}')
    print('^~'*25)
    print(f'50% NECESSIDADES BÁSICAS: \t{diminuir50(pr, taxar, True)}')
    print('-'*50)