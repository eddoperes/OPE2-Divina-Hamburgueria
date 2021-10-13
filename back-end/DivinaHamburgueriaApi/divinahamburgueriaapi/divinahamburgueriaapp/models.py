from django.db import models
from django.utils import timezone

# Create your models here.

class Endereco(models.Model):

    class Meta:
        db_table = 'endereco'

    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=100)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=50, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return self.logradouro

class Telefone(models.Model):

    class Meta:
        db_table = 'telefone'

    ddd = models.CharField(max_length=2)
    numero = models.CharField(max_length=9)

    def __str__(self):
        return self.numero

class Cliente(models.Model):

    class Meta:
        db_table = 'cliente'

    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11, null=True)
    endereco = models.ForeignKey('Endereco', default=1, null=True ,related_name='enderecos_clientes', on_delete=models.CASCADE)
    telefone = models.ForeignKey('Telefone', default=1, null=True ,related_name='telefones_clientes', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Fornecedor(models.Model):

    class Meta:
        db_table = 'fornecedor'

    nome = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=14)
    endereco = models.ForeignKey('Endereco', null=True, related_name='enderecos_fornecedores', on_delete=models.CASCADE)
    telefone = models.ForeignKey('Telefone', null=True, related_name='telefones_fornecedores', on_delete=models.CASCADE)
    estado = models.IntegerField(default=1)  
    datacriado = models.DateTimeField(auto_now_add=True)
    dataativado = models.DateTimeField(auto_now_add=True)   
    datainativado = models.DateTimeField(null=True)

    def __str__(self):
        return self.nome

class Usuario(models.Model):

    class Meta:
        db_table = 'usuario'

    nome = models.CharField(max_length=200)
    tipo = models.IntegerField()
    email = models.CharField(max_length=200)
    senha = models.CharField(max_length=200)
    token = models.CharField(max_length=200, default='')
    estado = models.IntegerField(default=1)  
    datacriado = models.DateTimeField(auto_now_add=True)
    dataativado = models.DateTimeField(auto_now_add=True)   
    datainativado = models.DateTimeField(null=True)

    def __str__(self):
        return self.nome

class Cardapio(models.Model):

    class Meta:
        db_table = 'cardapio'

    nome = models.CharField(max_length=200)
    descricao = models.CharField(max_length=400)
    estado = models.IntegerField(default=1)  
    datacriado = models.DateTimeField(auto_now_add=True)
    dataativado = models.DateTimeField(auto_now_add=True)   
    datainativado = models.DateTimeField(null=True)
	
    def __str__(self):
        return self.nome

class ItemDoCardapio(models.Model):

    class Meta:
        db_table = 'itemdocardapio'

    nome = models.CharField(max_length=200)
    descricao = models.CharField(max_length=400)
    fotografia = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class CardapioItemDoCardapio(models.Model):

    class Meta:
        db_table = 'cardapioitemdocardapio'

    cardapio = models.ForeignKey('Cardapio', default=1, related_name='cardapios', on_delete=models.CASCADE)
    itemdocardapio = models.ForeignKey('ItemDoCardapio', default=1, related_name='itensdocardapio', on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.IntegerField(default=1)  
    datacriado = models.DateTimeField(auto_now_add=True)
    dataativado = models.DateTimeField(auto_now_add=True)   
    datainativado = models.DateTimeField(null=True)

    def __str__(self):
        return self.itemdocardapio.nome

class PedidoSalao(models.Model):

    class Meta:
        db_table = 'pedidosalao'

    usuario = models.ForeignKey('Usuario', default=1, related_name='pedidossalao_usuarios', on_delete=models.CASCADE)
    estado = models.IntegerField(default=1)
    dataemitido = models.DateTimeField(auto_now_add=True)
    datacancelado = models.DateTimeField(null=True)
    dataentregue = models.DateTimeField(null=True)
    observacao = models.CharField(max_length=400, null=True)
    cliente = models.ForeignKey('Cliente', null=True, related_name='pedidossalao_clientes', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.id

class PedidoSalaoItemDoCardapio(models.Model):

    class Meta:
        db_table = 'pedidoalaoitemdocardapio'

    pedidosalao = models.ForeignKey('PedidoSalao', default=1, related_name='pedidossalao', on_delete=models.CASCADE)
    itemdocardapio = models.ForeignKey('ItemDoCardapio', default=1, related_name='pedidossalao_itemdocardapio', on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.CharField(max_length=400,null=True)

    def __str__(self):
        return self.id

class PedidoDelivery(models.Model):

    class Meta:
        db_table = 'pedidodelivery'

    usuario = models.ForeignKey('Usuario', default=1, related_name='pedidosdelivery_usuarios', on_delete=models.CASCADE)
    estado = models.IntegerField(default=1)
    dataemitido = models.DateTimeField(auto_now_add=True)
    datacancelado = models.DateTimeField(null=True)
    dataembalado = models.DateTimeField(null=True)
    dataentregue = models.DateTimeField(null=True)
    observacao = models.CharField(max_length=400, null=True)
    estadopagamento = models.IntegerField(default=0)
    datapagamento = models.DateTimeField(null=True)
    cliente = models.ForeignKey('Cliente', default=1, related_name='pedidosdelivery_clientes', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.id

class PedidoDeliveryItemDoCardapio(models.Model):

    class Meta:
        db_table = 'pedidodeliveryitemdocardapio'

    pedidodelivery = models.ForeignKey('PedidoDelivery', default=1, related_name='pedidosdelivery', on_delete=models.CASCADE)
    itemdocardapio = models.ForeignKey('ItemDoCardapio', default=1, related_name='pedidosdelivery_itemdocardapio', on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.CharField(max_length=400, null=True)

    def __str__(self):
        return self.id

class ItemDoEstoque(models.Model):

    class Meta:
        db_table = 'itemdoestoque'

    nome = models.CharField(max_length=200)
    descricao = models.CharField(max_length=400)
    conteudo = models.IntegerField(default=1)
    unidade =  models.CharField(max_length=10, default='')
    estoqueminimo = models.IntegerField(default=1)

    def __str__(self):
        return self.nome

class PedidoDeCompra(models.Model):

    class Meta:
        db_table = 'pedidodecompra'

    fornecedor = models.ForeignKey('Fornecedor', default=1, related_name='fornecedores', on_delete=models.CASCADE)
    estado = models.IntegerField(default=1)
    observacao = models.CharField(max_length=400, null=True)
    datacotacao = models.DateTimeField(auto_now_add=True)
    dataemitido = models.DateTimeField(null=True)
    datacancelado = models.DateTimeField(null=True)
    dataentregue = models.DateTimeField(null=True)
    dataestocado = models.DateTimeField(null=True)
    estadopagamento = models.IntegerField(default=0)
    datapagamento = models.DateTimeField(null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.id

class PedidoDeCompraItemDoEstoque(models.Model):

    class Meta:
        db_table = 'itemdoestoquepedidodecompra'

    itemdoestoque = models.ForeignKey('ItemDoEstoque', default=1, related_name='itensdoestoque', on_delete=models.CASCADE)
    pedidodecompra = models.ForeignKey('PedidoDeCompra', default=1, related_name='pedidosdecompra', on_delete=models.CASCADE)
    precounitario = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    quantidade = models.IntegerField(default=1)
    precototal = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    estocado = models.BooleanField(default=False)

    def __str__(self):
        return self.id

class Estoque(models.Model):

    class Meta:
        db_table = 'estoque'

    itemdoestoque = models.ForeignKey('ItemDoEstoque', default=1, related_name='itensdoestoque_estocados', on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return self.id