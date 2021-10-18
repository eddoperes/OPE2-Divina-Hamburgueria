from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [

    url(r'^usuario_list/$', views.usuario_list, name='usuario_list'),
    path('usuario_detail/<int:pk>', views.usuario_detail),
    path('usuario_login/', views.usuario_login),
    path('usuario_enviar_token/', views.usuario_enviar_token),
    path('usuario_alterar_senha/', views.usuario_alterar_senha),

    url(r'^itemdocardapio_list/$', views.itemdocardapio_list, name='itemdocardapio_list'),    
    path('itemdocardapio_detail/<int:pk>', views.itemdocardapio_detail),

    url(r'^cardapio_list/$', views.cardapio_list, name='cardapio_list'),
    path('cardapio_detail/<int:pk>', views.cardapio_detail),

    url(r'^cardapioitemdocardapio_list/$', views.cardapioitemdocardapio_list, name='cardapioitemdocardapio_list'),
    path('cardapioitemdocardapio_detail/<int:pk>', views.cardapioitemdocardapio_detail),

    url(r'^cliente_list/$', views.cliente_list, name='cliente_list'),
    path('cliente_detail/<int:pk>', views.cliente_detail),

    url(r'^pedidosalao_list/$', views.pedidosalao_list, name='pedidosalao_list'),
    path('pedidosalao_detail/<int:pk>', views.pedidosalao_detail),

    url(r'^pedidosalaoitemdocardapio_list/$', views.pedidosalaoitemdocardapio_list, name='pedidosalaoitemdocardapio_list'),
    path('pedidosalaoitemdocardapio_detail/<int:pk>', views.pedidosalaoitemdocardapio_detail),

    url(r'^telefone_list/$', views.telefone_list, name='telefone_list'),
    path('telefone_detail/<int:pk>', views.telefone_detail),

    url(r'^endereco_list/$', views.endereco_list, name='endereco_list'),
    path('endereco_detail/<int:pk>', views.endereco_detail),

    url(r'^cliente_list/$', views.cliente_list, name='cliente_list'),
    path('cliente_detail/<int:pk>', views.cliente_detail),

    url(r'^pedidodelivery_list/$', views.pedidodelivery_list, name='pedidodelivery_list'),
    path('pedidodelivery_detail/<int:pk>', views.pedidodelivery_detail),

    url(r'^pedidodeliveryitemdocardapio_list/$', views.pedidodeliveryitemdocardapio_list, name='pedidodeliveryitemdocardapio_list'),
    path('pedidodeliveryitemdocardapio_detail/<int:pk>', views.pedidodeliveryitemdocardapio_detail),

    url(r'^itemdoestoque_list/$', views.itemdoestoque_list, name='itemdoestoque_list'),    
    path('itemdoestoque_detail/<int:pk>', views.itemdoestoque_detail),

    url(r'^fornecedor_list/$', views.fornecedor_list, name='fornecedor_list'),
    path('fornecedor_detail/<int:pk>', views.fornecedor_detail),

    url(r'^pedidodecompra_list/$', views.pedidodecompra_list, name='pedidodecompra_list'),
    path('pedidodecompra_detail/<int:pk>', views.pedidodecompra_detail),

    url(r'^pedidodecompraitemdoestoque_list/$', views.pedidodecompraitemdoestoque_list, name='pedidodecompraitemdoestoque_list'),
    path('pedidodecompraitemdoestoque_detail/<int:pk>', views.pedidodecompraitemdoestoque_detail),

    url(r'^estoque_list/$', views.estoque_list, name='estoque_list'),
    path('estoque_detail/<int:pk>', views.estoque_detail),

    url(r'^revenda_list/$', views.revenda_list, name='revenda_list'),
    path('revenda_detail/<int:pk>', views.revenda_detail),

    url(r'^receita_list/$', views.receita_list, name='receita_list'),
    path('receita_detail/<int:pk>', views.receita_detail),

]