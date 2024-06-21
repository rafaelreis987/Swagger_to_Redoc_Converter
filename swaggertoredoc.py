import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

redoc_cli_path = os.getenv('REDOC_CLI_PATH')
input_directory = os.getenv('INPUT_DIRECTORY')
output_directory = os.getenv('OUTPUT_DIRECTORY')


def convert_swagger_to_redoc(input_directory, output_directory):
    # Verifica se o diretório de saída existe, caso contrário, cria-o
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Percorre todos os arquivos no diretório de entrada
    for filename in os.listdir(input_directory):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, filename.replace(".yaml", ".html").replace(".yml", ".html"))

            # Comando para converter o arquivo .yaml para .html usando o Redoc CLI
            command = [redoc_cli_path, "bundle", input_file, "-o", output_file]

            # Executa o comando e verifica se a conversão foi bem-sucedida
            try:
                subprocess.run(command, check=True)
                print(f"Sucesso: {input_file} -> {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao converter {input_file}: {e}")


if __name__ == "__main__":
    convert_swagger_to_redoc(input_directory, output_directory)
