import os
import pytest
from pyweber.utils.template import Template  # Altere para o caminho correto da sua classe Template

@pytest.fixture
def setup_templates():
    """Fixture para configurar o diretório de templates e garantir que o ambiente esteja limpo."""
    # Cria a pasta 'templates' e um arquivo 'valid_template.html' para o teste
    os.makedirs('templates', exist_ok=True)
    with open('templates/valid_template.html', 'w', encoding='utf-8') as f:
        f.write('<html><body><h1>Valid Template</h1></body></html>')
    
    yield
    
    # Limpeza após o teste
    if os.path.exists('templates/valid_template.html'):
        os.remove('templates/valid_template.html')
    # if os.path.exists('templates'):
    #     os.rmdir('templates')

# Teste para template HTML válido
def test_render_valid_template(setup_templates):
    template = Template('valid_template.html')
    
    # Verificar se o template foi carregado corretamente
    result = template._Template__render_template
    assert '<html>' in result
    assert '<h1>Valid Template</h1>' in result

# Teste para template HTML inexistente
def test_render_invalid_template():
    template = Template('invalid_template.html')
    
    # Verificar se o FileNotFoundError é levantado
    with pytest.raises(FileNotFoundError):
        template._Template__render_template
