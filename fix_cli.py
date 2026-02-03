import sys

with open('blurtpy/cli.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # 381: passphrase = click.prompt("Password to unlock wallet (Will be stored in keyring)", confirmation_prompt=False, hide_input=True)
    # 382: passphrase = keyring.set_password("blurtpy", "wallet", password)
    if 'passphrase = keyring.set_password("blurtpy", "wallet", password)' in line:
        line = line.replace('passphrase = keyring.set_password("blurtpy", "wallet", password)', 'keyring.set_password("blurtpy", "wallet", passphrase)')

    # createwallet block
    if 'password = None' in line and 'def createwallet():' in ''.join(new_lines[-10:]):
        line = line.replace('password = None', 'passphrase = None')
    if 'stm.wallet.create(password)' in line:
        line = line.replace('stm.wallet.create(password)', 'stm.wallet.create(passphrase)')
    if 'passphrase = keyring.set_password("blurtpy", "wallet", password)' in line:
         line = line.replace('passphrase = keyring.set_password("blurtpy", "wallet", password)', 'keyring.set_password("blurtpy", "wallet", passphrase)')

    # changewalletpassphrase block
    if 'newpassword = None' in line:
        line = line.replace('newpassword = None', 'newpassphrase = None')
    if 'if not bool(newpassword):' in line:
        line = line.replace('if not bool(newpassword):', 'if not bool(newpassphrase):')
    if 'keyring.set_password("blurtpy", "wallet", newpassword)' in line:
        line = line.replace('keyring.set_password("blurtpy", "wallet", newpassword)', 'keyring.set_password("blurtpy", "wallet", newpassphrase)')
    if 'stm.wallet.changePassphrase(newpassword)' in line:
        line = line.replace('stm.wallet.changePassphrase(newpassword)', 'stm.wallet.changePassphrase(newpassphrase)')

    # passwordgen block
    if 'import_passphrase = click.prompt("Enter password"' in line:
        line = line.replace('import_passphrase = click.prompt("Enter password"', 'import_password = click.prompt("Enter password"')

    # newaccount block
    if 'import_passphrase = click.prompt("Keys were not given - Passphrase is used to create keys\\n New Account Passphrase"' in line:
        line = line.replace('import_passphrase = click.prompt("Keys were not given - Passphrase is used to create keys\\n New Account Passphrase"', 'import_password = click.prompt("Keys were not given - Passphrase is used to create keys\\n New Account Passphrase"')

    # importaccount block
    if 'passphrase = click.prompt("Account Passphrase"' in line:
        line = line.replace('passphrase = click.prompt("Account Passphrase"', 'password = click.prompt("Account Passphrase"')
    if 'if not password:' in line and 'def importaccount' in ''.join(new_lines[-20:]):
        line = line.replace('if not password:', 'if not password:') # no change needed but just to track

    new_lines.append(line)

with open('blurtpy/cli.py', 'w') as f:
    f.writelines(new_lines)
