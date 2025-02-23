import pytest
from pyweber.utils.router import Router, Template, StaticTemplate

# Criar um fixture para a instância do Router
@pytest.fixture
def router():
    return Router()

# Testar a adição de uma rota com sucesso
def test_add_route(router):
    template = Template('Hello world')  # Um template de exemplo
    router.add_route('/home', template)
    assert '/home' in router.list_routes

# Testar a adição de rota inválida (sem a barra inicial)
def test_add_route_invalid_route(router):
    with pytest.raises(ValueError):
        router.add_route('home', Template('Hello world'))  # Rota sem barra inicial

# Testar a adição de uma rota existente
def test_add_route_existing(router):
    template = Template('Hello world')
    router.add_route('/home', template)
    with pytest.raises(ValueError):
        router.add_route('/home', Template('Hello world'))  # Rota já existente

# Testar a adição de uma rota com template inválido
def test_add_route_invalid_template(router):
    with pytest.raises(TypeError):
        router.add_route('/home', "invalid_template")  # Template não é uma instância de Template

# Testar a atualização de rota
def test_update_route(router):
    template = Template('Hello world')
    router.add_route('/home', template)
    new_template = Template('new_template.html')
    router.update_route('/home', new_template)
    assert router._Router__routes['/home'] is new_template

# Testar atualização de rota inexistente
def test_update_route_not_found(router):
    with pytest.raises(ValueError):
        router.update_route('/unknown', Template('Hello world'))  # Rota não encontrada

# Testar a remoção de uma rota
def test_remove_route(router):
    template = Template('Hello world')
    router.add_route('/home', template)
    router.remove_route('/home')
    assert '/home' not in router.list_routes

# Testar remoção de rota inexistente
def test_remove_route_not_found(router):
    with pytest.raises(ValueError):
        router.remove_route('/unknown')  # Rota não encontrada

# Testar o método exists
def test_exists(router):
    template = Template('Hello world')
    router.add_route('/home', template)
    assert router.exists('/home') is True
    assert router.exists('/unknown') is False

# Testar redirecionamento de rota
def test_redirect(router):
    from_template = Template('Hello world')
    to_template = Template('New Hello world')
    router.add_route('/home', from_template)
    router.add_route('/about', to_template)
    result = router.redirect('/home', '/about')
    assert result == to_template._Template__render_template

# Testar redirecionamento com rota de origem inexistente
def test_redirect_from_route_not_found(router):
    with pytest.raises(ValueError):
        router.redirect('/unknown', '/about')  # Rota de origem não existe

# Testar o método __get_route para rota existente
def test_get_route_existing(router):
    template = Template('Hello world')
    router.add_route('/home', template)
    result = router._Router__get_route('/home')
    assert result == template._Template__render_template

# Testar o método __get_route para rota inexistente
def test_get_route_not_found(router):
    result = router._Router__get_route('/unknown')
    assert result == StaticTemplate.error_template()