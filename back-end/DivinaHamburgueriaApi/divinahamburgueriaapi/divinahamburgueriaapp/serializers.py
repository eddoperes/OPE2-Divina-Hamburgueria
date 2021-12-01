from rest_framework import serializers
from .models import Usuario, Cliente, Fornecedor, Endereco, Telefone 
from .models import ItemDoCardapio, Cardapio, CardapioItemDoCardapio
from .models import PedidoSalao, PedidoSalaoItemDoCardapio
from .models import PedidoDelivery, PedidoDeliveryItemDoCardapio
from .models import ItemDoEstoque, Estoque
from .models import PedidoDeCompra, PedidoDeCompraItemDoEstoque
from .models import Receita, Revenda

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:

        model = Usuario
        fields = '__all__'
        #exclude = ('token', 'senha', )

class UsuarioNoPasswordSerializer(serializers.ModelSerializer):

    class Meta:

        model = Usuario
        #fields = '__all__'
        exclude = ('token', 'senha', )

class CardapioSerializer(serializers.ModelSerializer):

    class Meta:

        model = Cardapio
        fields = '__all__'

class ItemDoCardapioSerializer(serializers.ModelSerializer):

    class Meta:

        model = ItemDoCardapio
        fields = '__all__'

class CardapioItemDoCardapioSerializer(serializers.ModelSerializer):

    class Meta:

        model = CardapioItemDoCardapio
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:

        model = Cliente
        fields = '__all__'

class FornecedorSerializer(serializers.ModelSerializer):

    class Meta:

        model = Fornecedor
        fields = '__all__'

class PedidoSalaoSerializer(serializers.ModelSerializer):

    class Meta:

        model = PedidoSalao
        fields = '__all__'

class PedidoSalaoItemDoCardapioSerializer(serializers.ModelSerializer):

    class Meta:

        model = PedidoSalaoItemDoCardapio
        fields = '__all__'

class PedidoDeliverySerializer(serializers.ModelSerializer):

    class Meta:

        model = PedidoDelivery
        fields = '__all__'

class PedidoDeliveryItemDoCardapioSerializer(serializers.ModelSerializer):

    class Meta:

        model = PedidoDeliveryItemDoCardapio
        fields = '__all__'

class TelefoneSerializer(serializers.ModelSerializer):

    class Meta:

        model = Telefone
        fields = '__all__'

class EnderecoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Endereco
        fields = '__all__'


class ItemDoEstoqueSerializer(serializers.ModelSerializer):

    class Meta:

        model = ItemDoEstoque
        fields = '__all__'

class PedidoDeCompraSerializer(serializers.ModelSerializer):

    class Meta:

        model = PedidoDeCompra
        fields = '__all__'

class PedidoDeCompraItemDoEstoqueSerializer(serializers.ModelSerializer):

    class Meta:

        model = PedidoDeCompraItemDoEstoque
        fields = '__all__'

class EstoqueSerializer(serializers.ModelSerializer):

    class Meta:

        model = Estoque
        fields = '__all__'

class ReceitaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Receita
        fields = '__all__'

class RevendaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Revenda
        fields = '__all__'