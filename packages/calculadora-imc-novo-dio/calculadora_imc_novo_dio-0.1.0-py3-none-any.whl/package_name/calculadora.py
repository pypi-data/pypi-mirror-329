def calcular_imc(peso, altura):
    """Calcula o IMC com base no peso e altura fornecidos."""
    return peso / (altura ** 2)

def exibir_imc(imc):
    """Exibe o IMC com a classificação correspondente."""
    if imc < 18.5:
        print(f"\nSeu IMC é {imc:.2f}, Abaixo do Peso\n")
    elif 18.5 <= imc <= 24.9:
        print(f"\nSeu IMC é {imc:.2f}, Peso Normal\n")
    elif 25 <= imc <= 29.9:
        print(f"\nSeu IMC é {imc:.2f}, Sobrepeso\n")
    elif 30 <= imc <= 34.9:
        print(f"\nSeu IMC é {imc:.2f}, Obesidade Grau 1\n")
    elif 35 <= imc <= 39.9:
        print(f"\nSeu IMC é {imc:.2f}, Obesidade Grau 2\n")
    else:
        print(f"\nSeu IMC é {imc:.2f}, Obesidade Grau 3 (Mórbida)\n")

    print("\n==== Fim do cálculo. Obrigado por utilizar meu programa ====\n")
