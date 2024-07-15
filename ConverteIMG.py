import os
import requests
import time

def remover_fundo(caminho_imagem_entrada, caminho_imagem_saida, chave_api_remove_bg):
    tentativas = 0
    while tentativas < 3:
        with open(caminho_imagem_entrada, 'rb') as arquivo:
            resposta = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': arquivo},
                data={'size': 'auto'},
                headers={'X-Api-Key': chave_api_remove_bg},
            )
        
        if resposta.status_code == requests.codes.ok:
            with open(caminho_imagem_saida, 'wb') as arquivo_saida:
                arquivo_saida.write(resposta.content)
            print(f"Fundo removido de {caminho_imagem_entrada} e salvo em {caminho_imagem_saida}")
            return True  # Saia da função se bem-sucedido
        else:
            print(f"Erro: {resposta.status_code}, {resposta.text}. Tentando novamente em 30 segundos...")
            tentativas += 1
            time.sleep(30)
    
    print(f"Falha ao remover o fundo de {caminho_imagem_entrada} após 3 tentativas.")
    return False  # Retorne False se todas as tentativas falharem

def processar_imagens(pasta_raiz, chave_api_remove_bg):
    contagem_imagens = 0
    imagens_erro = []
    
    for subdir, _, arquivos in os.walk(pasta_raiz):
        if 'Background_Removed' in [d.lower() for d in os.listdir(subdir)]:
            print(f"Pasta {subdir} ignorada porque contém 'Background_Removed'")
            continue
        
        print(f"Atualmente na pasta: {subdir}")
        
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(subdir, arquivo)
            if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                pasta_saida = os.path.join(subdir, 'Background_Removed')
                os.makedirs(pasta_saida, exist_ok=True)
                caminho_imagem_saida = os.path.join(pasta_saida, arquivo)
                
                sucesso = remover_fundo(caminho_arquivo, caminho_imagem_saida, chave_api_remove_bg)
                if not sucesso:
                    imagens_erro.append(caminho_arquivo)
                else:
                    contagem_imagens += 1

                if contagem_imagens % 3 == 0:
                    print("Pausando por 1 minuto para evitar limite de taxa...")
                    time.sleep(60)

    if imagens_erro:
        print("As seguintes imagens falharam ao processar:")
        for imagem_erro in imagens_erro:
            print(imagem_erro)

# Uso do exemplo
chave_api_remove_bg = '##################'
pasta_raiz = input("Por favor, insira o caminho para a pasta raiz contendo as imagens: ")

processar_imagens(pasta_raiz, chave_api_remove_bg)
