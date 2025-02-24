import os
import pytest
from typer.testing import CliRunner
from pyweber.utils.pyweber_cli import app

runner = CliRunner()

# Teste para o comando `create-new`
@pytest.fixture
def clean_up():
    """Função que deleta o diretório do projeto após cada teste para evitar conflitos."""
    yield
    if os.path.exists("test_project"):
        for root, dirs, files in os.walk("test_project", topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir("test_project")

def test_create_new_project():
    """Teste para o comando create-new"""
    # Simulando a execução do comando
    result = runner.invoke(app, ['create-new', 'test_project'])
    
    # Verificar se o comando foi bem-sucedido
    assert result.exit_code == 0
    assert '✅ Projeto test_project criado com sucesso!' in result.output

    # Verificar se os diretórios e arquivos foram criados corretamente
    assert os.path.exists('test_project/src/style')
    assert os.path.exists('test_project/templates')
    assert os.path.exists('test_project/main.py')
    assert os.path.exists('test_project/templates/index.html')
    assert os.path.exists('test_project/src/style/style.css')

def test_create_existing_project():
    """Teste para o comando create-new quando o diretório já existe"""
    os.makedirs('existing_project')

    result = runner.invoke(app, ['create-new', 'existing_project'])
    
    assert result.exit_code == 0
    assert '❌ O diretório existing_project já existe!' in result.output

    # Limpar diretório após teste
    os.rmdir('existing_project')

# Teste para o comando `run`
def test_run_project():
    """Teste para o comando run"""
    # os.chdir('test_project')
    result = runner.invoke(app, ['run', '--file', 'main.py'])

    # Verificar se o comando foi executado
    assert result.exit_code == 0  # Verifica se o subprocess não falhou

def test_run_invalid_file(clean_up):
    """Teste para o comando run com um arquivo inválido"""
    result = runner.invoke(app, ['run', '--file', 'invalid_file.py'])

    # Verificar se houve um erro ao tentar executar um arquivo inexistente
    assert '❌ Error' in result.output