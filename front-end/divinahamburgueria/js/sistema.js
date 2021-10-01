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
    document.cookie = name + "=" + (value || "")  + expires + "; path=/" + ";secure";
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

function getLoggedUserId(){
    var userId = getCookie("user_id");			
    if (userId == null)			
        return -1; 			
    else
        return userId;
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

var urlWebApi = 'http://127.0.0.1:8000';

// Generico
//-------------------------------------------------------------------------------------------

function WebApi_POST_Generico(data, callbackSucess, callbackComplete, url){
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
    $.ajax({
        url: urlWebApi + '/' + url + '/' + id,
        data: data,
        type: 'PUT',
        crossDomain: true,
        success: callbackSucess,
        complete: callbackComplete     
    });
}

function WebApi_DELETE_Generico(id, callbackSucess, callbackComplete, url){
    $.ajax({
        url: urlWebApi + '/' + url + '/' + id,
        data: {},
        type: 'DELETE',
        crossDomain: true,
        success: callbackSucess,
        complete: callbackComplete     
    });
}

function WebApi_GET_Generico(id, callbackSucess, callbackComplete, url){
    $.ajax({
        url: urlWebApi + '/' + url + '/' + id,
        data: {},
        type: 'GET',
        crossDomain: true,
        success: callbackSucess,
        complete: callbackComplete     
    });
}

function WebApi_GET_LIST_Generico(filter, callbackSucess, callbackComplete, url){
    $.ajax({
        url: urlWebApi + '/' + url + '/' + filter,
        data: {},
        type: 'GET',
        crossDomain: true,
        success: callbackSucess,
        complete: callbackComplete     
    });
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

//-------------------------------------------------------------------------------------------
// Acesso web api - fim
//-------------------------------------------------------------------------------------------