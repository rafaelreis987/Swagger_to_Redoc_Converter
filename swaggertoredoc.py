import os
import subprocess
import logging
from dotenv import load_dotenv

load_dotenv()

redoc_cli_path = os.getenv('REDOC_CLI_PATH')
input_directory = os.getenv('INPUT_DIRECTORY')
output_directory = os.getenv('OUTPUT_DIRECTORY')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def check_and_install_redoc_cli(redoc_cli_path):
    try:
        # Check if redoc-cli is installed by running the version command
        subprocess.run([redoc_cli_path, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"{redoc_cli_path} is already installed.")
    except subprocess.CalledProcessError:
        logging.info(f"{redoc_cli_path} is not installed. Installing now...")
        try:
            subprocess.run(['npm', 'install', '-g', 'redoc-cli'], check=True)
            logging.info(f"{redoc_cli_path} has been installed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install {redoc_cli_path}: {e}")
            raise


def convert_swagger_to_redoc(input_directory, output_directory, redoc_cli_path):
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
                logging.info(f"Success: {input_file} -> {output_file}")
            except subprocess.CalledProcessError as e:
                logging.error(f"Error converting {input_file}: {e}")
            except FileNotFoundError as e:
                logging.error(f"Redoc CLI not found: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    check_and_install_redoc_cli(redoc_cli_path)
    convert_swagger_to_redoc(input_directory, output_directory, redoc_cli_path)
