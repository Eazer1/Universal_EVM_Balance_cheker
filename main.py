import os
import json

from time import sleep
from web3 import Web3
from loguru import logger

from config import TOKEN_CONTRACT_ABI

#------------------------[User-friendly Utils]------------------------#

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_current_settings(token_type=None, network=None, contract_address=None, symbol=None):
    token_types = {
        0: "Нативный токен",
        1: "ERC-20",
        2: "ERC-721 (NFT)",
        3: "ERC-1155 (NFT)"
    }
    clear_screen()
    print(f"Creator: https://t.me/Eazercrypto")
    if token_type != None:
        print(f"Смотрим баланс: {token_types[token_type]}")
    if network:
        print(f"Сеть: {network['network_name']}")
    if contract_address:
        print(f"Адрес контракта: {contract_address}")
    if symbol:
        print(f"Символ токена: {symbol}")
    return

def get_user_input(prompt, input_type=int, valid_range=None, valid_set=None, retry_message='Произошла ошибка! Попробуйте снова'):
    while True:
        try:
            user_input = input_type(input(prompt))
            if valid_range and user_input not in valid_range:
                raise ValueError
            elif valid_set and user_input not in valid_set:
                raise ValueError
            return user_input
        except ValueError:
            display_current_settings()
            print(retry_message)

#------------------------[Web3 Functions]------------------------#

def native_check(web3, address, network_name):
    while True:
        try:
            wallet_balance = web3.eth.get_balance(address)
            wallet_balance_eth = wallet_balance / 10**18
            wallet_balance_eth_format = f"{wallet_balance_eth:.18f}"
            logger.success(f'[{address}][Native Checker] {wallet_balance_eth_format}')


            with open(f'native_{network_name.lower()}_result.txt', 'a') as f:
                f.write(f'{address};{wallet_balance_eth_format}\n')

            break
        except Exception as e:
            logger.error(f'[{address}][Native Checker] {e}')
            sleep(10)

def erc20_check(address, erc20_contract, decimals, symbol):
    while True:
        try:
            wallet_balance_erc20 = erc20_contract.functions.balanceOf(address).call()
            wallet_balance_erc20_token = wallet_balance_erc20 / 10**int(decimals)
            wallet_balance_eth_token_format = f"{wallet_balance_erc20_token:.{decimals}f}"
            logger.success(f'[{address}][Native Checker] {wallet_balance_eth_token_format} ${symbol}')

            with open(f'{symbol}_result.txt', 'a') as f:
                f.write(f'{address};{wallet_balance_eth_token_format}\n')

            break
        except Exception as e:
            logger.error(f'[{address}][ERC-20 Checker] {e}')
            sleep(10)

def erc721_check(address, erc721_contract, symbol="Unknown"):
    while True:
        try:
            wallet_balance_erc721 = erc721_contract.functions.balanceOf(address).call()
            logger.success(f'[{address}][Native Checker] {wallet_balance_erc721} ${symbol}')

            with open(f'{symbol}_result.txt', 'a') as f:
                f.write(f'{address};{wallet_balance_erc721}\n')

            break
        except Exception as e:
            logger.error(f'[{address}][ERC-721 Checker] {e}')
            sleep(10)

def erc1155_check(address, erc1155_contract, nft_id, symbol="Unknown"):
    while True:
        try:
            wallet_balance_erc1155 = erc1155_contract.functions.balanceOf(address, nft_id).call()
            logger.success(f'[{address}][Native Checker] {wallet_balance_erc1155} ${symbol}')

            with open(f'{symbol}_result.txt', 'a') as f:
                f.write(f'{address};{wallet_balance_erc1155}\n')

            break
        except Exception as e:
            logger.error(f'[{address}][ERC-1155 Checker] {e}')
            sleep(10)

#------------------------[Start Soft]------------------------#

def main():
    while True:
        display_current_settings()

        token_type = get_user_input(
            'Выберите какой вид баланса отслеживать:\n\n' +
            '[0] Нативный токен\n' +
            '[1] ERC-20\n' +
            '[2] ERC-721 (NFT)\n' +
            '[3] ERC-1155 (NFT)\n\nВаш выбор: ',
            valid_range=[0, 1, 2, 3],
            retry_message='Неверный выбор! Попробуйте снова.'
        )
        
        display_current_settings(token_type)

        with open('network_rpc.json', 'r') as network_json:
            networks = json.load(network_json)

        network_choices = [str(index) for index in range(len(networks))] + ['add']
        network_choice_message = 'Выберите сеть:\n\n' + \
                                '\n'.join(f'[{index}] {network["network_name"]}' for index, network in enumerate(networks)) + \
                                '\n[add] Добавить новую сеть' + \
                                '\n\nВаш выбор: '
        user_network_choice = get_user_input(
            network_choice_message,
            input_type=str,
            valid_set=set(network_choices),
            retry_message='Неверный выбор! Попробуйте снова.'
        )

        if user_network_choice == 'add':
            user_network_name = input('Введите название сети: ')
            user_network_rpc = input('Введите RPC сети: ')

            new_network = {
                "network_name": user_network_name,
                "RPC": user_network_rpc
            }

            networks.append(new_network)

            with open('network_rpc.json', 'w') as network_json:
                json.dump(networks, network_json, indent=4)
            continue

        else:
            user_network_choice = int(user_network_choice)

        selected_network = networks[user_network_choice]
        display_current_settings(token_type, selected_network)
        web3 = Web3(Web3.HTTPProvider(selected_network['RPC']))

        if token_type == 0:
            pass
        elif token_type in [1, 2, 3]:
            contract_address = input(f'Введите адрес контракта токена: ')
            try:
                contract_address = web3.to_checksum_address(contract_address)
                contract = web3.eth.contract(address=contract_address, abi=json.loads(TOKEN_CONTRACT_ABI))
            except:
                print('Ошибка! Адрес контракта не корректен. Попробуйте ещё раз')
                input('[Enter] Начать сначала...')
                continue
            display_current_settings(token_type, selected_network, contract_address)

            if token_type == 1:
                decimals = contract.functions.decimals().call()
                symbol = contract.functions.symbol().call()
            elif token_type == 2:
                symbol = "Unknown"
                try:
                    symbol = contract.functions.symbol().call()
                except Exception:
                    pass
            elif token_type == 3:
                nft_id = get_user_input(
                    f'Введите id ERC-1155 токена: ',
                    input_type=int,
                    retry_message='Ошибка! Некорректный ввод. Попробуйте снова.'
                )
                symbol = "Unknown"
                try:
                    symbol = contract.functions.symbol().call()
                except Exception:
                    pass
            
            display_current_settings(token_type, selected_network, contract_address, symbol)

        with open('wallets.txt', 'r') as file:
            addresses = file.read().splitlines()
            for address in addresses:
                address = web3.to_checksum_address(address)
                
                if token_type == 0:  # Нативный токен
                    native_check(web3, address, selected_network['network_name'])

                elif token_type == 1:  # ERC-20
                    erc20_check(address, contract, decimals, symbol)

                elif token_type == 2:  # ERC-721
                    erc721_check(address, contract, symbol)

                elif token_type == 3:  # ERC-1155
                    erc1155_check(address, contract, nft_id, symbol)

        print('\nПрограмма выполнена успешно!')
        input('[Enter] Начать сначала...')
        continue

if __name__ == "__main__":
    main()
