import subprocess

def git_pull():
    try:
        # Salva temporariamente mudanças não preparadas
        subprocess.check_call(['git', 'stash', 'push'])
        print("Mudanças não preparadas salvas temporariamente.")

        # Atualiza o repositório local com as mudanças do remoto na branch correta
        subprocess.check_call(['git', 'pull', '--rebase', 'origin', 'main'])
        print("Repositório local atualizado com o remoto.")

        # Reaplica as mudanças salvas
        subprocess.check_call(['git', 'stash', 'pop'])
        print("Mudanças não preparadas reaplicadas.")

    except subprocess.CalledProcessError as e:
        print("Falha ao atualizar o repositório local:", e)
        return False
    return True

def git_push():
    if not git_pull():  # Primeiro tenta atualizar o repositório local
        return

    try:
        # Adiciona o arquivo CSV ao commit
        subprocess.check_call(['git', 'add', 'dadosdf_cripto.csv'])
        # Checa se há mudanças para commitar
        status_result = subprocess.check_output(['git', 'status', '--porcelain'])
        if status_result:
            # Cria um commit
            subprocess.check_call(['git', 'commit', '-m', 'Atualização automática dos dados'])
            print("Commit criado.")
        else:
            print("Nenhuma mudança para commitar.")

        # Faz o push do commit para o repositório
        subprocess.check_call(['git', 'push', 'origin', 'main'])
        print("Dados atualizados e enviados para o GitHub.")
    except subprocess.CalledProcessError as e:
        print("Falha ao enviar os dados para o GitHub:", e)

if __name__ == "__main__":
    git_push()
