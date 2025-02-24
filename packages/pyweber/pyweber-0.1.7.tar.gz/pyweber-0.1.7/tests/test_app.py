from unittest.mock import patch
from pyweber import run  # Substitua pelo nome correto do seu módulo
from pyweber.utils.server import Server
from pyweber.utils.router import Router
from threading import Thread

def target(r: Router):
    return True

# Teste de inicialização e execução da classe run
def test_run_initialization():
    # Cria uma instância de Router e Server diretamente

    with patch.object(run, '_run__run', lambda x: None):
        app = run(target=target, route='/test', port=8000, reload=False)
    
        # Verificar se a instância da classe foi criada corretamente
        assert app.route == '/test'  # Verifica se o route foi passado corretamente
        assert app.port == 8000  # Verifica se a porta foi passada corretamente
        assert app.reload is False  # Verifica se o reload foi passado corretamente
        assert isinstance(app.router, Router)  # Verifica se o router é o correto

def test_run_with_default_values():
    # Usando os valores padrão
    with patch.object(run, '_run__run', lambda x: None):
        app = run(target=target)
    
        # Verificar se os valores padrão foram aplicados corretamente
        assert app.route == '/'  # Valor padrão de route
        assert app.port == 5555  # Valor padrão de port
        assert app.reload is True  # Valor padrão de reload