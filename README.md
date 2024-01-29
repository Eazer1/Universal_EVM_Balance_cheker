# Universal EVM Balance Checker (UEBC xD)

## Описание
Universal EVM Balance Checker — это инструмент для проверки балансов различных типов токенов на Ethereum Virtual Machine (EVM) совместимых блокчейнах. Он поддерживает проверку балансов нативных токенов (например, ETH для Ethereum), а также токенов стандартов ERC-20, ERC-721 и ERC-1155. Программа анализирует балансы всех адресов, указанных в файле `wallets.txt`.

## Особенности
- Поддержка различных типов токенов: Нативные, ERC-20, ERC-721, ERC-1155.
- Поддержка нескольких сетей: Ethereum, Binance Smart Chain и другие EVM-совместимые блокчейны.
- Возможность добавления новых сетей через консольный интерфейс.
- Проверка балансов всех адресов, указанных в файле `wallets.txt`.
- Логирование ошибок и результатов проверки в текстовые файлы.

## Установка
1. Клонируйте репозиторий:
   ```
   git clone https://github.com/Eazer1/Universal_EVM_Balance_cheker
   ```
2. Установите необходимые зависимости:
   ```
   pip install -r requirements.txt
   ```
3. Добавьте адреса кошельков, которые нужно проверить, в файл `wallets.txt`.

## Использование
- Для запуска скрипта используйте команду:
```
python main.py
```
- После запуска следуйте инструкциям в консоли для выбора сети, типа токена и ввода адресов для проверки балансов.
- В процессе отчекивания кошельков, программа создаст файлы `.txt` формата, где будет записан адрес кошелька и его баланс в выбранном вами токене

## Конфигурация
- Файл `network_rpc.json` содержит информацию о сетях и их RPC URL.
- Файл `config.py` должен содержать универсальный ABI для ERC-20, ERC-721, ERC-1155 контрактов.

## Лицензия
Этот проект распространяется под [MIT лицензией](LICENSE).

## Контакты
- Код был изготовлен для канала: https://t.me/Eazercrypto
- Чат канала: https://t.me/EazerChat
