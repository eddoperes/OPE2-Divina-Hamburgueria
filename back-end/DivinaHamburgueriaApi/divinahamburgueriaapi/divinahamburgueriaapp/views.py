from django.shortcuts import render
from rest_framework import generics
from .models import Usuario, Cliente, Fornecedor, Endereco, Telefone 
from .models import ItemDoCardapio, Cardapio, CardapioItemDoCardapio
from .models import Receita, Revenda
from .models import PedidoSalao, PedidoSalaoItemDoCardapio
from .models import PedidoDelivery, PedidoDeliveryItemDoCardapio
from .models import ItemDoEstoque, Estoque, Alarme, AlarmeE
from .models import PedidoDeCompra, PedidoDeCompraItemDoEstoque
from .serializers import UsuarioSerializer, UsuarioNoPasswordSerializer, ClienteSerializer, FornecedorSerializer, EnderecoSerializer, TelefoneSerializer
from .serializers import ItemDoCardapioSerializer, CardapioSerializer, CardapioItemDoCardapioSerializer 
from .serializers import ReceitaSerializer, RevendaSerializer
from .serializers import PedidoSalaoSerializer, PedidoSalaoItemDoCardapioSerializer
from .serializers import PedidoDeliverySerializer, PedidoDeliveryItemDoCardapioSerializer
from .serializers import ItemDoEstoqueSerializer, EstoqueSerializer, AlarmeSerializer, AlarmeESerializer
from .serializers import PedidoDeCompraSerializer, PedidoDeCompraItemDoEstoqueSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import random
import smtplib
from datetime import datetime
import hashlib 

# Create your views here.

#---------------------------------------------------------------------------
# Usuario - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def usuario_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('nome', '')
        usuario =  Usuario.objects.filter(nome__icontains=filtro)		
        serializer = UsuarioNoPasswordSerializer(usuario, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode criar usuários', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = UsuarioSerializer(data = request.data)
        
        hash = hashlib.md5(request.data['senha'].encode()) 

        if serializer.is_valid():  
            if Usuario.objects.filter(nome=serializer.validated_data['nome']).exists():
                 return Response('Nome duplicado', status = status.HTTP_400_BAD_REQUEST)         
            serializer.save(senha = hash.digest())
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def usuario_detail(request, pk):
    try:
        usuario = Usuario.objects.get(id=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UsuarioNoPasswordSerializer(usuario)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode editar usuários', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = UsuarioNoPasswordSerializer(usuario, data=request.data)        
        if serializer.is_valid():
            if request.data["estado"] == "1":
               serializer.save(dataativado = datetime.today())
            else:
               serializer.save(datainativado = datetime.today())
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def usuario_login(request):  
    email = request.data['email']

    #senha = request.data['senha']
    hash = hashlib.md5(request.data['senha'].encode())    
    senha = hash.digest()	

    usuario = Usuario.objects.filter(email=email).first()
    if usuario is None:
        return Response('Usuário inválido', status=status.HTTP_404_NOT_FOUND)
    usuario = Usuario.objects.filter(email=email).filter(senha=senha).first()
    if usuario is None:
        return Response('Senha inválida', status=status.HTTP_404_NOT_FOUND)
    if usuario.estado == 0:
        return Response('Usuario inativo', status=status.HTTP_404_NOT_FOUND)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

@api_view(['POST'])
def usuario_enviar_token(request):  
    email = request.data['email']
    usuario = Usuario.objects.filter(email=email).first()
    if usuario is None:
        return Response('email não encontrado', status=status.HTTP_404_NOT_FOUND)
    random.seed()
    token = ""
    for i in range(6):
       token = token + str(random.randint(0,9))

    server = smtplib.SMTP('smtp.ctidealer.com.br', 587)
    server.login("email@ctidealer.com.br", "ctidealer08@")
    server.sendmail("email@ctidealer.com.br", email, "Subject: {}\n\n{}".format("Token", token))
    server.quit()

    usuario.token = token
    usuario.save()
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

@api_view(['POST'])
def usuario_alterar_senha(request):  
    email = request.data['email']
    usuario = Usuario.objects.filter(email=email).first()
    if usuario is None:
       return Response('email não encontrado', status=status.HTTP_404_NOT_FOUND)
    if usuario.token != request.data['token']:
       return Response('token inválido', status=status.HTTP_400_BAD_REQUEST)

    #usuario.senha = request.data['senha']
    hash = hashlib.md5(request.data['senha'].encode())    
    usuario.senha = hash.digest()
   
    usuario.save()
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

#---------------------------------------------------------------------------
# Usuario - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Cliente - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def cliente_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('nome', '')
        cliente =  Cliente.objects.filter(nome__icontains=filtro)		
        serializer = ClienteSerializer(cliente, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ClienteSerializer(data = request.data)
        if serializer.is_valid():          
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def cliente_detail(request, pk):
    try:
        cliente = Cliente.objects.get(id=pk)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ClienteSerializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Cliente - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Endereco - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def endereco_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('rua', '')
        endereco =  Endereco.objects.filter(logradouro__icontains=filtro)		
        serializer = EnderecoSerializer(endereco, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EnderecoSerializer(data = request.data)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def endereco_detail(request, pk):
    try:
        endereco = Endereco.objects.get(id=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = EnderecoSerializer(endereco)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = EnderecoSerializer(endereco, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        endereco.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Endereco - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Telefone - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def telefone_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('telefone', '')
        telefone =  Telefone.objects.filter(numero__icontains=filtro)		
        serializer = TelefoneSerializer(telefone, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TelefoneSerializer(data = request.data)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def telefone_detail(request, pk):
    try:
        telefone = Telefone.objects.get(id=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = TelefoneSerializer(telefone)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TelefoneSerializer(telefone, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        telefone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Telefone - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Fornecedor - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def fornecedor_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('nome', '')
        fornecedor =  Fornecedor.objects.filter(nome__icontains=filtro)		
        serializer = FornecedorSerializer(fornecedor, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = FornecedorSerializer(data = request.data)
        if serializer.is_valid():          
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def fornecedor_detail(request, pk):
    try:
        fornecedor = Fornecedor.objects.get(id=pk)
    except Fornecedor.DoesNotExist:
        return Response('NOT FOUND', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = FornecedorSerializer(fornecedor)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FornecedorSerializer(fornecedor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        fornecedor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Fornecedor - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Item do cardapio - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def itemdocardapio_list (request):
    if request.method == 'GET':
        itemdocardapio = []
        filtro = request.GET.get('estado', '')
        if filtro != '':
           cardapio_ativo = Cardapio.objects.filter(estado=filtro)	              
           for cardapio in cardapio_ativo:
              cardapioitemdocardapio_ativo =  CardapioItemDoCardapio.objects.filter(cardapio=cardapio.id, estado=1)
              for cardapioitemdocardapio in cardapioitemdocardapio_ativo:              
                 itemdocardapio.append(ItemDoCardapio.objects.get(id=cardapioitemdocardapio.itemdocardapio.id))
           serializer = ItemDoCardapioSerializer(itemdocardapio, many=True)
           return Response(serializer.data)
        else:
           filtro = request.GET.get('nome', '')
           itemdocardapio =  ItemDoCardapio.objects.filter(nome__icontains=filtro)		
           serializer = ItemDoCardapioSerializer(itemdocardapio, many=True)
           return Response(serializer.data)
    elif request.method == 'POST':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode criar itens do cardápio', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = ItemDoCardapioSerializer(data = request.data)
        if serializer.is_valid():  
            if ItemDoCardapio.objects.filter(nome=serializer.validated_data['nome']).exists():
                 return Response('Nome duplicado', status = status.HTTP_400_BAD_REQUEST)          
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def itemdocardapio_detail(request, pk):
    try:
        itemdocardapio = ItemDoCardapio.objects.get(id=pk)
    except ItemDoCardapio.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ItemDoCardapioSerializer(itemdocardapio)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode editar itens do cardápio', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = ItemDoCardapioSerializer(itemdocardapio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        itemdocardapio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Item do cardapio - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Revenda - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def revenda_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('itemdocardapio', '')
        if (filtro != ''):
           revenda =  Revenda.objects.filter(itemdocardapio=filtro)
        else:	
           revenda =  Revenda.objects.all()
        serializer = RevendaSerializer(revenda, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode criar revendas', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = RevendaSerializer(data = request.data)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def revenda_detail(request, pk):
    try:
        revenda = Revenda.objects.get(id=pk)
    except Revenda.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = RevendaSerializer(revenda)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode editar revendas', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = RevendaSerializer(revenda, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        revenda.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Revenda - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Receita - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def receita_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('itemdocardapio', '')
        if (filtro != ''):
           receita =  Receita.objects.filter(itemdocardapio=filtro)
        else:	
           receita =  Receita .objects.all()
        serializer = ReceitaSerializer(receita, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode criar receitas', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = ReceitaSerializer(data = request.data)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def receita_detail(request, pk):
    try:
        receita = Receita.objects.get(id=pk)
    except Receita.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReceitaSerializer(receita)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode editar receitas', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = ReceitaSerializer(receita, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        receita.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Receita - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Cardapio - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def cardapio_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('nome', '')
        cardapio =  Cardapio.objects.filter(nome__icontains=filtro)		
        serializer = CardapioSerializer(cardapio, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode criar cardápios', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = CardapioSerializer(data = request.data)
        if serializer.is_valid():  
            if Cardapio.objects.filter(nome=serializer.validated_data['nome']).exists():
                 return Response('Nome duplicado', status = status.HTTP_400_BAD_REQUEST) 
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def cardapio_detail(request, pk):
    try:
        cardapio = Cardapio.objects.get(id=pk)
    except Cardapio.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CardapioSerializer(cardapio)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode editar cardápios', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = CardapioSerializer(cardapio, data=request.data)
        if serializer.is_valid():
            if request.data["estado"] == "1":
               serializer.save(dataativado = datetime.today())
            else:
               serializer.save(datainativado = datetime.today())  
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        cardapio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Cardapio - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Cardapio Item do Cardapio - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def cardapioitemdocardapio_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('cardapio', '')
        if (filtro == ''):
            filtro = request.GET.get('itemdocardapio', '')
            cardapioitemdocardapio =  CardapioItemDoCardapio.objects.filter(itemdocardapio=filtro)		
        else:
            cardapioitemdocardapio =  CardapioItemDoCardapio.objects.filter(cardapio=filtro)		
        serializer = CardapioItemDoCardapioSerializer(cardapioitemdocardapio, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode criar cardápios', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = CardapioItemDoCardapioSerializer(data = request.data)
        if serializer.is_valid():          
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def cardapioitemdocardapio_detail(request, pk):
    try:
        cardapioitemdocardapio = CardapioItemDoCardapio.objects.get(id=pk)
    except CardapioItemDoCardapio.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CardapioItemDoCardapioSerializer(cardapioitemdocardapio)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode editar cardápios', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = CardapioItemDoCardapioSerializer(cardapioitemdocardapio, data=request.data)
        if serializer.is_valid():
            if request.data["estado"] == "1":
               serializer.save(dataativado = datetime.today())
            else:
               serializer.save(datainativado = datetime.today())  
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        cardapioitemdocardapio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Cardapio Item do Cardapio - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Pedido Salão - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def pedidosalao_list (request):
    if request.method == 'GET':


        dateini = request.GET.get('dateini', '').replace('-','')
        dateend = request.GET.get('dateend', '').replace('-','')
        if (dateini != ''):
            pedidosalao = PedidoSalao.objects.all()
            pedidofilter = [];
            for pedido in pedidosalao:                  
                datacur = pedido.dataemitido.strftime("%Y/%m/%d").replace('/','')
                if datacur >= dateini and datacur <= dateend:
                    pedidofilter.append(pedido) 
            serializer = PedidoSalaoSerializer(pedidofilter, many=True)
            return Response(serializer.data)



        filtro = request.GET.get('estado', '')
        if (filtro == ''):
            pedidosalao = PedidoSalao.objects.all()
        else:
            pedidosalao = PedidoSalao.objects.filter(estado=filtro)		
        serializer = PedidoSalaoSerializer(pedidosalao, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PedidoSalaoSerializer(data = request.data)
        if serializer.is_valid():          
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def pedidosalao_detail(request, pk):
    try:
        pedidosalao = PedidoSalao.objects.get(id=pk)
    except PedidoSalao.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PedidoSalaoSerializer(pedidosalao)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PedidoSalaoSerializer(pedidosalao, data=request.data)
        if serializer.is_valid():
            if request.data["estado"] == "1":
               serializer.save(dataemitido = datetime.today())
            elif request.data["estado"] == "2":
               serializer.save(datacancelado = datetime.today())
            else:
               serializer.save(dataentregue = datetime.today()) 
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        pedidosalao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Pedido Salão - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Pedido Salão Item do Cardapio - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def pedidosalaoitemdocardapio_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('pedidosalao', '')
        pedidosalaoitemdocardapio =  PedidoSalaoItemDoCardapio.objects.filter(pedidosalao=filtro)		
        serializer = PedidoSalaoItemDoCardapioSerializer(pedidosalaoitemdocardapio, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PedidoSalaoItemDoCardapioSerializer(data = request.data)
        if serializer.is_valid():          
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def pedidosalaoitemdocardapio_detail(request, pk):
    try:
        pedidosalaoitemdocardapio = PedidoSalaoItemDoCardapio.objects.get(id=pk)
    except PedidoSalaoItemDoCardapio.DoesNotExist:
        return Response('id não encontrado', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PedidoSalaoItemDoCardapioSerializer(pedidosalaoitemdocardapio)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PedidoSalaoItemDoCardapioSerializer(pedidosalaoitemdocardapio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        pedidosalaoitemdocardapio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Pedido Salão Item do Cardapio - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Pedido Delivery - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def pedidodelivery_list (request):
    if request.method == 'GET':

        dateini = request.GET.get('dateini', '').replace('-','')
        dateend = request.GET.get('dateend', '').replace('-','')
        if (dateini != ''):
            pedidodelivery = PedidoDelivery.objects.all()
            pedidofilter = [];
            for pedido in pedidodelivery:                  
                datacur = pedido.dataemitido.strftime("%Y/%m/%d").replace('/','')
                if datacur >= dateini and datacur <= dateend:
                    pedidofilter.append(pedido) 
            serializer = PedidoDeliverySerializer(pedidofilter, many=True)
            return Response(serializer.data)

        filtro = request.GET.get('estado', '')
        if (filtro == ''):
            pedidodelivery = PedidoDelivery.objects.all()
        else:
            pedidodelivery = PedidoDelivery.objects.filter(estado=filtro)		
        serializer = PedidoDeliverySerializer(pedidodelivery, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PedidoDeliverySerializer(data = request.data)
        if serializer.is_valid():          
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def pedidodelivery_detail(request, pk):
    try:
        pedidodelivery = PedidoDelivery.objects.get(id=pk)
    except PedidoDelivery.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PedidoDeliverySerializer(pedidodelivery)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PedidoDeliverySerializer(pedidodelivery, data=request.data)
        if serializer.is_valid():
            if request.data["estado"] == "1":
               serializer.save(dataemitido = datetime.today())
            elif request.data["estado"] == "2":
               serializer.save(datacancelado = datetime.today())
            elif request.data["estado"] == "3":
               serializer.save(dataembalado = datetime.today())
            else:
               serializer.save(dataentregue = datetime.today()) 
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        pedidodelivery.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Pedido Delivery - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Pedido Delivery Item do Cardapio - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def pedidodeliveryitemdocardapio_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('pedidodelivery', '')
        pedidodeliveryitemdocardapio =  PedidoDeliveryItemDoCardapio.objects.filter(pedidodelivery=filtro)		
        serializer = PedidoDeliveryItemDoCardapioSerializer(pedidodeliveryitemdocardapio, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PedidoDeliveryItemDoCardapioSerializer(data = request.data)
        if serializer.is_valid():          
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def pedidodeliveryitemdocardapio_detail(request, pk):
    try:
        pedidodeliveryitemdocardapio = PedidoDeliveryItemDoCardapio.objects.get(id=pk)
    except PedidoDeliveryItemDoCardapio.DoesNotExist:
        return Response('id não encontrado', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PedidoDeliveryItemDoCardapioSerializer(pedidodeliveryitemdocardapio)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PedidoDeliveryItemDoCardapioSerializer(pedidodeliveryitemdocardapio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        pedidodeliveryitemdocardapio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Pedido Delivery Item do Cardapio - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Item do Estoque - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def itemdoestoque_list (request):
    if request.method == 'GET':

        filtro = request.GET.get('exato', '')
        if filtro != '': 
           itemdoestoque =  ItemDoEstoque.objects.filter(nome=filtro)		
           serializer = ItemDoEstoqueSerializer(itemdoestoque, many=True)
           return Response(serializer.data)

        filtro = request.GET.get('tipo', '')
        if filtro != '':           
           itemdoestoque =  ItemDoEstoque.objects.filter(tipo=filtro)		
           serializer = ItemDoEstoqueSerializer(itemdoestoque, many=True)
           return Response(serializer.data)
        else:            
           filtro = request.GET.get('nome', '')
           itemdoestoque =  ItemDoEstoque.objects.filter(nome__icontains=filtro)		
           serializer = ItemDoEstoqueSerializer(itemdoestoque, many=True)
           return Response(serializer.data)
    elif request.method == 'POST':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode criar itens do estoque', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = ItemDoEstoqueSerializer(data = request.data)
        if serializer.is_valid():  
            #if ItemDoEstoque.objects.filter(nome=serializer.validated_data['nome']).exists():
            #     return Response('Nome duplicado', status = status.HTTP_400_BAD_REQUEST)          
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def itemdoestoque_detail(request, pk):
    try:
        itemdoestoque = ItemDoEstoque.objects.get(id=pk)
    except ItemDoEstoque.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ItemDoEstoqueSerializer(itemdoestoque)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode editar itens do estoque', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = ItemDoEstoqueSerializer(itemdoestoque, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        itemdoestoque.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Item do Estoque - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Pedido De Compra - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def pedidodecompra_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('estado', '')
        if (filtro == ''):
            pedidodecompra = PedidoDeCompra.objects.all()
        else:
            pedidodecompra = PedidoDeCompra.objects.filter(estado=filtro)		
        serializer = PedidoDeCompraSerializer(pedidodecompra, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode criar itens do estoque', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = PedidoDeCompraSerializer(data = request.data)
        if serializer.is_valid():          
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def pedidodecompra_detail(request, pk):
    try:
        pedidodecompra = PedidoDeCompra.objects.get(id=pk)
    except PedidoDeCompra.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PedidoDeCompraSerializer(pedidodecompra)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode editar pedido de compra', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = PedidoDeCompraSerializer(pedidodecompra, data=request.data)
        if serializer.is_valid():
            if request.data["estado"] == "1":
               serializer.save(datacotacao = datetime.today())
            elif request.data["estado"] == "2":
               serializer.save(dataemitido = datetime.today())
            elif request.data["estado"] == "3":
               serializer.save(datacancelado = datetime.today())
            elif request.data["estado"] == "4":
               serializer.save(dataentregue = datetime.today())
            else:
               serializer.save(dataestocado = datetime.today()) 
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        pedidodecompra.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Pedido De Compra - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Pedido De Compra Item do Estoque - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def pedidodecompraitemdoestoque_list (request):
    if request.method == 'GET':
        filtroA = request.GET.get('pedidodecompra', '')        
        pedidodecompraitemdoestoque =  PedidoDeCompraItemDoEstoque.objects.filter(pedidodecompra=filtroA)		

        filtroB = request.GET.get('estocado', '')
        if (filtroB != ''):
           pedidodecompraitemdoestoque = pedidodecompraitemdoestoque.filter(estocado=filtroB)
 

        serializer = PedidoDeCompraItemDoEstoqueSerializer(pedidodecompraitemdoestoque, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode criar itens do estoque', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = PedidoDeCompraItemDoEstoqueSerializer(data = request.data)
        if serializer.is_valid():          
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def pedidodecompraitemdoestoque_detail(request, pk):
    try:
        pedidodecompraitemdoestoque = PedidoDeCompraItemDoEstoque.objects.get(id=pk)
    except PedidoDeCompraItemDoEstoque.DoesNotExist:
        return Response('id não encontrado', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PedidoDeCompraItemDoEstoqueSerializer(pedidodecompraitemdoestoque)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1' and request.data["tipousuario"] != '2':
           return Response('Permissão negada. Somente um usuário do tipo chef ou auxiliar pode editar itens do estoque', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = PedidoDeCompraItemDoEstoqueSerializer(pedidodecompraitemdoestoque, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        pedidodecompraitemdoestoque.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Pedido De Compra Item do Estoque - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Estoque - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def estoque_list (request):
    if request.method == 'GET':
        filtro = request.GET.get('quantidade', -1)
        if (filtro != -1):
           estoque =  Estoque.objects.filter(quantidade__range=(0, int(filtro) - 1))
        filtro = request.GET.get('itemdoestoque', 0)		
        if (filtro != 0):
           estoque =  Estoque.objects.filter(itemdoestoque=filtro)		
        serializer = EstoqueSerializer(estoque, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode dar entrada no estoque', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = EstoqueSerializer(data = request.data)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def estoque_detail(request, pk):
    try:
        estoque = Estoque.objects.get(id=pk)
    except Estoque.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = EstoqueSerializer(estoque)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode editar o estoque', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = EstoqueSerializer(estoque, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        estoque.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Estoque - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# Alarme - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def alarme_list (request):
    if request.method == 'GET':          
        #alarme =  Alarme.objects.all()	

        filtro = request.GET.get('quantidademinima', -1)
        alarme =  Alarme.objects.filter(quantidademinima__range=(0, int(filtro) - 1))

        serializer = AlarmeSerializer(alarme, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode criar alarme', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = AlarmeSerializer(data = request.data)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def alarme_detail(request, pk):
    try:
        alarme = Alarme.objects.get(id=pk)
    except Alarme.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = AlarmeSerializer(alarme)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode editar o alarme', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = AlarmeSerializer(alarme, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        alarme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# Alarme - fim
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# AlarmeE - inicio
#---------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def alarmee_list (request):
    if request.method == 'GET':          
        #alarmee =  AlarmeE.objects.all()	

        filtro = request.GET.get('quantidademinima', -1)
        alarmee =  AlarmeE.objects.filter(quantidademinima__range=(0, int(filtro) - 1))

        serializer = AlarmeESerializer(alarmee, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode criar alarmee', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = AlarmeESerializer(data = request.data)
        if serializer.is_valid():            
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def alarmee_detail(request, pk):
    try:
        alarmee = AlarmeE.objects.get(id=pk)
    except AlarmeE.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = AlarmeESerializer(alarmee)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode editar o alarmee', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        serializer = AlarmeESerializer(alarmee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # Permissao ini ####################################################
        if request.data["tipousuario"] != '1':
           return Response('Permissão negada. Somente um usuário do tipo chef pode excluir', status=status.HTTP_403_FORBIDDEN)
        # Permissao end ####################################################
        alarmee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------
# AlarmeE - fim
#---------------------------------------------------------------------------