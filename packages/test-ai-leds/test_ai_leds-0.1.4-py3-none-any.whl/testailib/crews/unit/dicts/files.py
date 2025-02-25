from pathlib import Path
import difflib
import os

def read_file_path(file_path: str) -> str:
    file_path = file_path.strip("'").replace("\\\\", "\\")

    with open(file_path, 'r', encoding='utf-8-sig') as file:
        cs_file_content = file.read()

    return cs_file_content


##file_path = Path("leds-conectafapes-backend-admin-main\src\ConectaFapes\ConectaFapes.Application\Services\CadastroModalidadesBolsas\VersaoModalidadeService.cs")
#base_directory = "leds-conectafapes-backend-admin-main/src/ConectaFapes"

def find_file(base_directory: str, file_name: str) -> str:
    """
    Recursivamente procura por um arquivo no diretório fornecido e seus subdiretórios.
    Se não for encontrado uma correspondência exata, retorna a correspondência mais próxima usando correspondência difusa.
    """
    found_files = []
    for root, _, files in os.walk(base_directory):
        if file_name in files:
            # Retorna o caminho com '/' como separador
            return os.path.join(root, file_name).replace("\\", "/")
        
        # Adiciona os caminhos dos arquivos encontrados, substituindo '\\' por '/'
        found_files.extend([os.path.join(root, file).replace("\\", "/") for file in files])

    file_names = [os.path.basename(path) for path in found_files]
    closest_match = difflib.get_close_matches(file_name, file_names, n=1)
    
    if closest_match:
        for path in found_files:
            if os.path.basename(path) == closest_match[0]:
                return path  # O caminho já foi ajustado anteriormente
    
    return None


def process_test_and_related_files(found_paths: list):
    existing_test_content = ""
    
    # Verifica se o último caminho é um arquivo de teste
    if found_paths and "Test" in found_paths[-1]:
        test_file_path = found_paths.pop()
        try:
            with open(test_file_path, "r", encoding="utf-8-sig") as f:
                existing_test_content = f.read()
        except UnicodeDecodeError:
            # Se ocorrer erro de codificação, tenta outra codificação (windows-1252)
            with open(test_file_path, "r", encoding="windows-1252") as f:
                existing_test_content = f.read()

    related_files_content = []
    
    # Processa os arquivos relacionados
    for related_file in found_paths:
        # Ignora arquivos binários (ex: .dll, .exe)
        if related_file.endswith(('.dll', '.exe', '.pdb', '.so', '.obj', '.lib')):
            print(f"Ignorando arquivo binário: {related_file}")
            continue
        
        try:
            with open(related_file, "r", encoding="utf-8-sig") as f:
                related_files_content.append(f.read())
        except UnicodeDecodeError as e:
            # Se ocorrer erro de codificação, tenta outra codificação
            print(f"Erro ao abrir o arquivo {related_file}: {e}")
            try:
                with open(related_file, "r", encoding="windows-1252") as f:
                    related_files_content.append(f.read())
            except Exception as e:
                print(f"Erro ao abrir o arquivo {related_file} com windows-1252: {e}")

    related_files_content = "\n\n".join(related_files_content)

    return existing_test_content, related_files_content

