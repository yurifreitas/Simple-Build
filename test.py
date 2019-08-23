from app import convert_float, calc_tax, calc_weight
import logging


# TEST CONVERT FLOAT
def test_convert_float():
    try:
        convert_float("2,00")
    except:
        print("O TESTE ENCONTROU UM ERRO EM convert_float")
        logging.error("O TESTE ENCONTROU UM ERRO EM convert_float")
        return False
    print("convert_float TESTE COM SUCESSO")
    return True


# TEST CALC WEIGHT
def test_calc_weight():
    try:
        calc_weight("0,75", "1,10", "0,60")
    except:
        print("O TESTE ENCONTROU UM ERRO EM calc_weight")
        logging.error("O TESTE ENCONTROU UM ERRO EM calc_weight")
        return False
    print("calc_weight TESTE COM SUCESSO")
    return True


# TEST CALC TAX
def test_calc_tax():
    try:
        calc_tax("0,75", "1,10", "0,60", "0,100", "150,00")
    except:
        print("O TESTE ENCONTROU UM ERRO EM calc_tax")
        logging.error("O TESTE ENCONTROU UM ERRO EM calc_tax")
        return False
    print("calc_tax TESTE COM SUCESSO ")
    return True


def run_test():
    test_convert_float()
    test_calc_weight()
    test_calc_tax()

run_test()