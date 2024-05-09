import subprocess

def git_pull():
    try:
        subprocess.check_call(['git', 'stash', 'push'])
        print("Mudanças não preparadas salvas temporariamente.")

        subprocess.check_call(['git', 'pull', '--rebase', 'origin', 'main'])
        print("Repositório local atualizado com o remoto.")

        subprocess.check_call(['git', 'stash', 'pop'])
        print("Mudanças não preparadas reaplicadas.")
    except subprocess.CalledProcessError as e:
        print("Falha ao atualizar o repositório local:", e)
        return False
    return True

def git_push():
    if not git_pull():
        return

    try:
        subprocess.check_call(['git', 'add', 'dadosdf_cripto.csv'])
        status_result = subprocess.check_output(['git', 'status', '--porcelain'])
        print("Resultado do status:", status_result.decode())

        if status_result:
            subprocess.check_call(['git', 'commit', '-m', 'Atualização automática dos dados'])
            print("Commit criado.")
        else:
            print("Nenhuma mudança para commitar.")

        subprocess.check_call(['git', 'push', 'origin', 'main'])
        print("Dados atualizados e enviados para o GitHub.")
    except subprocess.CalledProcessError as e:
        print("Falha ao enviar os dados para o GitHub:", e)

if __name__ == "__main__":
    git_push()
