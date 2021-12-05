//-------------------------------------------------------------------------------------------
// Parâmetros no  url - inicio
//-------------------------------------------------------------------------------------------

function queryObj() {
    var result = {}, keyValuePairs = location.search.slice(1).split("&");
    keyValuePairs.forEach(function(keyValuePair) {
        keyValuePair = keyValuePair.split('=');
        result[decodeURIComponent(keyValuePair[0])] = decodeURIComponent(keyValuePair[1]) || '';
    });
    return result;
}

//-------------------------------------------------------------------------------------------
// Parâmetros no  url - fim
//-------------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------------
// Cookies e login - inicio
//-------------------------------------------------------------------------------------------

function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/" //+ ";secure";    
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {        
       var c = ca[i];
       while (c.charAt(0)==' ') c = c.substring(1,c.length);
       if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function doLogin(userId, userType, userName){
    setCookie("user_id_", userId, 1); //set "user_id" cookie, expires in 1 days
    setCookie("user_type_", userType, 1); //set "user_type" cookie, expires in 1 days
    setCookie("user_name_", userName, 1); //set "user_name" cookie, expires in 1 days
}

function doLogout(){
    var userId = getCookie("user_id_");
    setCookie("user_id_", userId, -1); //cancel "user_id" cookie, using -1 days
}

function getLoggedUserId(){
    var userId = getCookie("user_id_");			
    if (userId == null)			
        return -1; 			
    else
        return userId;
}

function getLoggedUserType(){
    var userType = getCookie("user_type_");			
    if (userType == null)			
        return -1; 			
    else
        return userType;
}

function getLoggedUserName(){
    var userName = getCookie("user_name_");			
    if (userName == null)			
        return ''; 			
    else
        return userName;
}

//-------------------------------------------------------------------------------------------
// Cookies e login - fim
//-------------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------------
// Auxiliar - inicio
//-------------------------------------------------------------------------------------------

function ValidarCPF(strCPF) {

    if (strCPF.length != 11)
        return false;

    var Soma;
    var Resto;
    Soma = 0;
    if (strCPF == "00000000000") return false;

    for (i=1; i<=9; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (11 - i);
        Resto = (Soma * 10) % 11;

        if ((Resto == 10) || (Resto == 11))  Resto = 0;
        if (Resto != parseInt(strCPF.substring(9, 10)) ) return false;

    Soma = 0;

    for (i = 1; i <= 10; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (12 - i);
        Resto = (Soma * 10) % 11;

    if ((Resto == 10) || (Resto == 11))  Resto = 0;
    if (Resto != parseInt(strCPF.substring(10, 11) ) ) return false;
    return true;
    
}

function ValidarCNPJ(cnpj) {

    cnpj = cnpj.replace(/[^\d]+/g,'');
 
    if(cnpj == '') return false;
     
    if (cnpj.length != 14)
        return false;
 
    /*
    // Elimina CNPJs invalidos conhecidos
    if (cnpj == "00000000000000" || 
        cnpj == "11111111111111" || 
        cnpj == "22222222222222" || 
        cnpj == "33333333333333" || 
        cnpj == "44444444444444" || 
        cnpj == "55555555555555" || 
        cnpj == "66666666666666" || 
        cnpj == "77777777777777" || 
        cnpj == "88888888888888" || 
        cnpj == "99999999999999")
        return false;
    */
         
    // Valida DVs
    tamanho = cnpj.length - 2
    numeros = cnpj.substring(0,tamanho);
    digitos = cnpj.substring(tamanho);
    soma = 0;
    pos = tamanho - 7;
    for (i = tamanho; i >= 1; i--) {
      soma += numeros.charAt(tamanho - i) * pos--;
      if (pos < 2)
            pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(0))
        return false;
         
    tamanho = tamanho + 1;
    numeros = cnpj.substring(0,tamanho);
    soma = 0;
    pos = tamanho - 7;
    for (i = tamanho; i >= 1; i--) {
      soma += numeros.charAt(tamanho - i) * pos--;
      if (pos < 2)
            pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(1))
          return false;
           
    return true;

}

//-------------------------------------------------------------------------------------------
// Auxiliar - fim
//-------------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------------
// Acesso web api - inicio
//-------------------------------------------------------------------------------------------

//var urlWebApi = 'http://192.168.0.26:8000';
var urlWebApi = 'https://divinahamburgueria.herokuapp.com';

// Generico
//-------------------------------------------------------------------------------------------

function WebApi_POST_Generico(data, callbackSucess, callbackComplete, url){
    data.tipousuario = getLoggedUserType();
    $.ajax({
        url: urlWebApi + '/' + url + '/',
        data: data,
        type: 'POST',
        crossDomain: true,
        success: callbackSucess,
        complete: callbackComplete     
    });
} 

function WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, url){
    data.tipousuario = getLoggedUserType();
    $.ajax({
        url: urlWebApi + '/' + url + '/' + id,
        data: data,
        type: 'PUT',
        crossDomain: true,
        success: callbackSucess,
        complete: callbackComplete,
    });
}

function WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, url){
    data = {};
    data.tipousuario = getLoggedUserType();
    $.ajax({
        url: urlWebApi + '/' + url + '/' + id,
        data: data,
        type: 'DELETE',
        crossDomain: true,
        success: callbackSucess,
        complete: callbackComplete     
    });
}

function WebApi_GET_Generico(id, callbackSucess, callbackComplete, url){
    data = {};
    data.tipousuario = getLoggedUserType();
    $.ajax({
        url: urlWebApi + '/' + url + '/' + id,
        data: data,
        type: 'GET',
        crossDomain: true,
        success: callbackSucess,
        complete: callbackComplete     
    });
}

function WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, url){
    data = {};
    data.tipousuario = getLoggedUserType();
    $.ajax({
        url: urlWebApi + '/' + url + '/' + filter,
        data: data,
        type: 'GET',
        crossDomain: true,
        success: callbackSucess,
        complete: callbackComplete     
    });
}

// Login
//-------------------------------------------------------------------------------------------

function WebApi_POST_Login(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'usuario_login');
}

function WebApi_POST_EnviarToken(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'usuario_enviar_token');
}

function WebApi_POST_AlterarSenha(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'usuario_alterar_senha');
}

// Usuario
//-------------------------------------------------------------------------------------------

function WebApi_POST_Usuario(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'usuario_list');
}

function WebApi_PUT_Usuario(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'usuario_detail');
}

function WebApi_DELETE_Usuario(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'usuario_detail');
}

function WebApi_GET_Usuario(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'usuario_detail');
}

function WebApi_GET_LIST_Usuario(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'usuario_list');
}

// Item do cardápio
//-------------------------------------------------------------------------------------------

function WebApi_POST_ItemDoCardapio(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'itemdocardapio_list');  
}

function WebApi_PUT_ItemDoCardapio(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'itemdocardapio_detail');  
}

function WebApi_DELETE_ItemDoCardapio(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'itemdocardapio_detail');   
}

function WebApi_GET_ItemDoCardapio(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'itemdocardapio_detail');  
}

function WebApi_GET_LIST_ItemDoCardapio(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'itemdocardapio_list');   
}

// Cardápio
//-------------------------------------------------------------------------------------------

function WebApi_POST_Cardapio(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'cardapio_list');   
}

function WebApi_PUT_Cardapio(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'cardapio_detail');   
}

function WebApi_DELETE_Cardapio(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'cardapio_detail');  
}

function WebApi_GET_Cardapio(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'cardapio_detail');      
}

function WebApi_GET_LIST_Cardapio(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'cardapio_list');    
}

// Cardápio Item do Cardápio
//-------------------------------------------------------------------------------------------

function WebApi_POST_CardapioItemDoCardapio(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'cardapioitemdocardapio_list');     
}

function WebApi_PUT_CardapioItemDoCardapio(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'cardapioitemdocardapio_detail');   
}

function WebApi_DELETE_CardapioItemDoCardapio(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'cardapioitemdocardapio_detail');   
}

function WebApi_GET_CardapioItemDoCardapio(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'cardapioitemdocardapio_detail');    
}

function WebApi_GET_LIST_CardapioItemDoCardapio(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'cardapioitemdocardapio_list'); 
}

// Pedido Salão
//-------------------------------------------------------------------------------------------

function WebApi_POST_PedidoSalao(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'pedidosalao_list');    
}

function WebApi_PUT_PedidoSalao(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'pedidosalao_detail');    
}

function WebApi_DELETE_PedidoSalao(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'pedidosalao_detail');   
}

function WebApi_GET_PedidoSalao(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'pedidosalao_detail');   
}

function WebApi_GET_LIST_PedidoSalao(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'pedidosalao_list');   
}

// Pedido Salão Item do Cardápio
//-------------------------------------------------------------------------------------------

function WebApi_POST_PedidoSalaoItemDoCardapio(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'pedidosalaoitemdocardapio_list');    
}

function WebApi_PUT_PedidoSalaoItemDoCardapio(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'pedidosalaoitemdocardapio_detail');   
}

function WebApi_DELETE_PedidoSalaoItemDoCardapio(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'pedidosalaoitemdocardapio_detail');   
}

function WebApi_GET_PedidoSalaoItemDoCardapio(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'pedidosalaoitemdocardapio_detail');     
}

function WebApi_GET_LIST_PedidoSalaoItemDoCardapio(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'pedidosalaoitemdocardapio_list');      
}

// Cliente
//-------------------------------------------------------------------------------------------

function WebApi_POST_Cliente(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'cliente_list');    
}

function WebApi_PUT_Cliente(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'cliente_detail');
}

function WebApi_DELETE_Cliente(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'cliente_detail');   
}

function WebApi_GET_Cliente(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'cliente_detail');   
}

function WebApi_GET_LIST_Cliente(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'cliente_list');     
}

// Endereco
//-------------------------------------------------------------------------------------------

function WebApi_POST_Endereco(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'endereco_list');       
}

function WebApi_PUT_Endereco(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'endereco_detail');   
}

function WebApi_DELETE_Endereco(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'endereco_detail');     
}

function WebApi_GET_Endereco(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'endereco_detail');      
}

function WebApi_GET_LIST_Endereco(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'endereco_list');       
}

// Telefone
//-------------------------------------------------------------------------------------------

function WebApi_POST_Telefone(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'telefone_list');        
}

function WebApi_PUT_Telefone(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'telefone_detail');   
}

function WebApi_DELETE_Telefone(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'telefone_detail');     
}

function WebApi_GET_Telefone(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'telefone_detail');   
}

function WebApi_GET_LIST_Telefone(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'telefone_list');   
}

// Pedido Delivery
//-------------------------------------------------------------------------------------------

function WebApi_POST_PedidoDelivery(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'pedidodelivery_list'); 
}

function WebApi_PUT_PedidoDelivery(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'pedidodelivery_detail');   
}

function WebApi_DELETE_PedidoDelivery(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'pedidodelivery_detail');    
}

function WebApi_GET_PedidoDelivery(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'pedidodelivery_detail');      
}

function WebApi_GET_LIST_PedidoDelivery(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'pedidodelivery_list'); 
}

// Pedido Delivery Item do Cardápio
//-------------------------------------------------------------------------------------------

function WebApi_POST_PedidoDeliveryItemDoCardapio(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'pedidodeliveryitemdocardapio_list');    
}

function WebApi_PUT_PedidoDeliveryItemDoCardapio(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'pedidodeliveryitemdocardapio_detail');
}

function WebApi_DELETE_PedidoDeliveryItemDoCardapio(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'pedidodeliveryitemdocardapio_detail');    
}

function WebApi_GET_PedidoDeliveryItemDoCardapio(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'pedidodeliveryitemdocardapio_detail');       
}

function WebApi_GET_LIST_PedidoDeliveryItemDoCardapio(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'pedidodeliveryitemdocardapio_list');
}

// Item do estoque
//-------------------------------------------------------------------------------------------

function WebApi_POST_ItemDoEstoque(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'itemdoestoque_list');  
}

function WebApi_PUT_ItemDoEstoque(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'itemdoestoque_detail');  
}

function WebApi_DELETE_ItemDoEstoque(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'itemdoestoque_detail');   
}

function WebApi_GET_ItemDoEstoque(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'itemdoestoque_detail');  
}

function WebApi_GET_LIST_ItemDoEstoque(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'itemdoestoque_list');   
}

// Fornecedor
//-------------------------------------------------------------------------------------------

function WebApi_POST_Fornecedor(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'fornecedor_list');  
}

function WebApi_PUT_Fornecedor(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'fornecedor_detail');  
}

function WebApi_DELETE_Fornecedor(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'fornecedor_detail');   
}

function WebApi_GET_Fornecedor(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'fornecedor_detail');  
}

function WebApi_GET_LIST_Fornecedor(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'fornecedor_list');   
}

// Pedido De Compra
//-------------------------------------------------------------------------------------------

function WebApi_POST_PedidoDeCompra(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'pedidodecompra_list'); 
}

function WebApi_PUT_PedidoDeCompra(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'pedidodecompra_detail');   
}

function WebApi_DELETE_PedidoDeCompra(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'pedidodecompra_detail');    
}

function WebApi_GET_PedidoDeCompra(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'pedidodecompra_detail');      
}

function WebApi_GET_LIST_PedidoDeCompra(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'pedidodecompra_list'); 
}

// Pedido de Compra Item do Estoque
//-------------------------------------------------------------------------------------------

function WebApi_POST_PedidoDeCompraItemDoEstoque(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'pedidodecompraitemdoestoque_list');    
}

function WebApi_PUT_PedidoDeCompraItemDoEstoque(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'pedidodecompraitemdoestoque_detail');
}

function WebApi_DELETE_PedidoDeCompraItemDoEstoque(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'pedidodecompraitemdoestoque_detail');    
}

function WebApi_GET_PedidoDeCompraItemDoEstoque(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'pedidodecompraitemdoestoque_detail');       
}

function WebApi_GET_LIST_PedidoDeCompraItemDoEstoque(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'pedidodecompraitemdoestoque_list');
}

// Estoque
//-------------------------------------------------------------------------------------------

function WebApi_POST_Estoque(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'estoque_list');    
}

function WebApi_PUT_Estoque(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'estoque_detail');
}

function WebApi_DELETE_Estoque(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'estoque_detail');    
}

function WebApi_GET_Estoque(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'estoque_detail');       
}

function WebApi_GET_LIST_Estoque(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'estoque_list');
}

// Revenda
//-------------------------------------------------------------------------------------------

function WebApi_POST_Revenda(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'revenda_list');    
}

function WebApi_PUT_Revenda(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'revenda_detail');
}

function WebApi_DELETE_Revenda(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'revenda_detail');    
}

function WebApi_GET_Revenda(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'revenda_detail');       
}

function WebApi_GET_LIST_Revenda(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'revenda_list');
}

// Receita
//-------------------------------------------------------------------------------------------

function WebApi_POST_Receita(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'receita_list');    
}

function WebApi_PUT_Receita(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'receita_detail');
}

function WebApi_DELETE_Receita(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'receita_detail');    
}

function WebApi_GET_Receita(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'receita_detail');       
}

function WebApi_GET_LIST_Receita(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'receita_list');
}

// Alarme
//-------------------------------------------------------------------------------------------

function WebApi_POST_Alarme(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'alarme_list');    
}

function WebApi_PUT_Alarme(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'alarme_detail');
}

function WebApi_DELETE_Alarme(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'alarme_detail');    
}

function WebApi_GET_Alarme(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'alarme_detail');       
}

function WebApi_GET_LIST_Alarme(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'alarme_list');
}

// AlarmeE
//-------------------------------------------------------------------------------------------

function WebApi_POST_AlarmeE(data, callbackSucess, callbackComplete){
    WebApi_POST_Generico(data, callbackSucess, callbackComplete, 'alarmee_list');    
}

function WebApi_PUT_AlarmeE(id, data, callbackSucess, callbackComplete){
    WebApi_PUT_Generico(id, data, callbackSucess, callbackComplete, 'alarmee_detail');
}

function WebApi_DELETE_AlarmeE(id, callbackSucess, callbackComplete){
    WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, 'alarmee_detail');    
}

function WebApi_GET_AlarmeE(id, callbackSucess, callbackComplete){
    WebApi_GET_Generico(id, callbackSucess, callbackComplete, 'alarmee_detail');       
}

function WebApi_GET_LIST_AlarmeE(filter, callbackSucess, callbackComplete){
    WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, 'alarmee_list');
}

//-------------------------------------------------------------------------------------------
// Acesso web api - fim
//-------------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------------
// Conversões de unidade - inicio
//-------------------------------------------------------------------------------------------

function EncontrarUnidadeComparacao(unidade){
	if (unidade == 'g' || unidade == 'gr' || unidade == 'kg')
		return 'g';
	if (unidade == 'ml' || unidade == 'l')
		return 'ml';
	if (unidade == 'un' || unidade == 'dz' || unidade == 'fl')
		return 'un';
}

function EncontrarFuncaoConversao(unidade){
	if (unidade == 'g' || unidade == 'gr')
		return ConverterParaGramas;
	if (unidade == 'ml')
		return ConverterParaMililitros;
	if (unidade == 'un')
		return ConverterParaUnidades;
	if (unidade == 'kg')
		return ConverterParaKilogramas;
	if (unidade == 'l')
		return ConverterParaLitros;
	if (unidade == 'dz')
		return ConverterParaDuzias;
	if (unidade == 'fl')
		return ConverterParaFolhas;
}

function ConverterParaGramas(qtde, unidade) {
	if (unidade == 'g' || unidade == 'gr')
		return qtde;
	if (unidade == 'kg')
		return qtde * 1000;
}

function ConverterParaKilogramas(qtde, unidade) {
	if (unidade == 'g' || unidade == 'gr')
		return qtde / 1000;
	if (unidade == 'kg')
		return qtde;
}

function ConverterParaMililitros(qtde, unidade) {
	if (unidade == 'ml')
		return qtde;
	if (unidade == 'l')
		return qtde * 1000;
}

function ConverterParaLitros(qtde, unidade) {
	if (unidade == 'ml')
		return qtde * 1000;
	if (unidade == 'l')
		return qtde;
}

function ConverterParaUnidades(qtde, unidade) {
	if (unidade == 'un')
		return qtde;
	if (unidade == 'dz')
		return qtde * 12;
	if (unidade == 'fl')
		return qtde / 30;
}

function ConverterParaDuzias(qtde, unidade) {
	if (unidade == 'un')
		return qtde * 12;
	if (unidade == 'dz')
		return qtde;
}

function ConverterParaFolhas(qtde, unidade) {
	if (unidade == 'un')
		return qtde * 30;
	if (unidade == 'fl')
		return qtde;
}

//-------------------------------------------------------------------------------------------
// Conversões de unidade - fim
//-------------------------------------------------------------------------------------------

//-------------------------------------------------------------------------------------------
// Baixa automática estoque - inicio
//-------------------------------------------------------------------------------------------

function DescontarEstoque(itemdocardapio){
    	
    WebApi_GET_LIST_Revenda
    (
        "?itemdocardapio=" + itemdocardapio,
        function sucess(data) {
            //console.log(data);
            var revenda_list = data;
            if (revenda_list.length > 0){                
                EncontrarEstoqueRevenda(revenda_list[0]);
	    }
        },
        function complete(xhr, text) {
            console.log(xhr.status);
            //console.log(xhr.responseText);
        }
    );
			
    WebApi_GET_LIST_Receita
    (
        "?itemdocardapio=" + itemdocardapio,
        function sucess(data) {
            //console.log(data);
            var receita_list = data;
            if (receita_list.length > 0){
                EncontrarItemDoEstoqueReceita(receita_list);													
	    }
        },
        function complete(xhr, text) {
            console.log(xhr.status);
            //console.log(xhr.responseText);
        }
    );				
			
}	

// Revenda
//-------------------------------------------------------------------------------------------

function EncontrarEstoqueRevenda(revenda){

    WebApi_GET_Estoque
    (
        revenda.itemdoestoque,
        function sucess(data) {
            //console.log(data);
            BaixarEstoqueRevenda(revenda, data);
        },
        function complete(xhr, text) {
            console.log(xhr.status);
            //console.log(xhr.responseText);
        }
    );

}

function BaixarEstoqueRevenda(revenda, estoque){

    var qtde_descontada = estoque.quantidade - 1;

    if (qtde_descontada < 0)
        qtde_descontada = 0;

    WebApi_PUT_Estoque
    (
        estoque.id,
        {itemdoestoque : estoque.itemdoestoque , quantidade : qtde_descontada},
        function success(data){
            //console.log(data);
        },
        function complete(xhr, text){
            console.log(xhr.status);
            //console.log(xhr.responseText);
        }
    );

}

// Receita
//-------------------------------------------------------------------------------------------

function EncontrarItemDoEstoqueReceita(receita_list){

    for(var k=0; k < receita_list.length; k++){

	var k_cur = receita_list[k];

        WebApi_GET_LIST_ItemDoEstoque
        (
            '?exato=' + k_cur.nome , 
            function success(data) {			
                //console.log(data);	
		for(j=0; j < data.length; j++){
			var receita = receita_list.find(r => r.nome == data[j].nome);	
			EncontrarEstoqueReceita(receita, data[j],  data.length);
		}
            },
            function complete(xhr, text) {
                console.log(xhr.status);
                //console.log(xhr.responseText);			
            }     
        );		

    }	

}

function EncontrarEstoqueReceita(receita, itemdoestoque, divisor){
        
        WebApi_GET_Estoque
        (
            itemdoestoque.id,
            function sucess(data) {
                //console.log(data);
                BaixarEstoqueReceita(receita, itemdoestoque, data, divisor);
            },
            function complete(xhr, text) {
                console.log(xhr.status);
                //console.log(xhr.responseText);
            }
        );

}

function BaixarEstoqueReceita(receita, itemdoestoque, estoque, divisor){

    var f = EncontrarFuncaoConversao(itemdoestoque.unidade);    
    var qtde = f(receita.quantidade, receita.unidade) /  divisor;

    var qtde_total = (itemdoestoque.conteudo * estoque.quantidade) - qtde;
    var qtde_descontada = qtde_total / itemdoestoque.conteudo;

    if (qtde_descontada < 0)
        qtde_descontada = 0;

    WebApi_PUT_Estoque
    (
        estoque.id,
        {itemdoestoque : estoque.itemdoestoque , quantidade : qtde_descontada},
        function success(data){
            //console.log(data);
        },
        function complete(xhr, text){
            console.log(xhr.status);
            //console.log(xhr.responseText);
        }
    );

}

//-------------------------------------------------------------------------------------------
// Baixa automática estoque - fim
//-------------------------------------------------------------------------------------------

