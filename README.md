# Documentação do Protocolo

## Sobre o Protocolo

###Tipos de mensagens trocadas

  register_message: registra o cliente como área de pedidos prontos ou cozinha.
  new_order_message: envia os itens dos pedidos ao servidor.
	update_order_message: atualiza um pedido como concluído e notifica a área de pedidos prontos.
	canceled_order_message: atualiza um pedido como cancelado.
	notice_new_order_message: notifica a cozinha de novo pedido.
	notice_ready_area_message: notifica a área de pedidos prontos sobre pedido concluído.		

Sintaxe das mensagens

  register_message: {'type': 'register', 'role': 'ready_area'} e {'type': 'register', 'role': 'kitchen'}
  new_order_message: {'type': 'new_order', 'item': item}
  update_order_message: {'type': 'update_order', 'order_id': order['id']}
  canceled_order_message: {'type': 'canceled_order', 'order_id': order['id']}
  notice_new_order_message: {'type': 'new_order', 'order': pedido}
  notice_ready_area_message: {'type': 'order_ready', 'order_id':mensagem['order_id']}

Semântica das mensagens

  register_message: 'type': 'register' significa que um novo registro foi feito para a área de pedidos prontos (ready_area) ou cozinha (kitchen), 'role': ready_area' significa que a função é de área de                        pedidos prontos e  'role': 'kitchen' significa que é de área de pedidos da cozinha.
  new_order_message: 'type': 'new_order' significa que um novo pedido foi feito e 'item': item significa um item do pedido.
  update_order_message: 'type': 'update_order' significa que o tipo de mensagem é de atualização de pedido para concluído e 'order_id': order['id'] significa o identificador do pedido.
  canceled_order_message: 'type': 'canceled_order' significa que o tipo de mensagem é de pedido cancelado e 'order_id': order['id'] significa o identificador do pedido.
  notice_new_order_message: 'type': 'new_order' significa que um novo pedido foi feito e 'order': pedido são os dados do pedido.
  notice_ready_area_message: 'type': 'order_ready' significa que é uma mensagem de notificação de pedido para o totem de pedidos prontos e 'order_id': mensagem['order_id'] é o identificador do pedido.
	
Regras de envio e resposta

  Registro de Usuário:

    - Cliente (área de pedidos prontos ou cozinha): após se conectar ao servidor, envia uma mensagem do tipo "register" para informar sua função.

    - Exemplo:
        - Cliente: {'type': 'register', 'role': 'ready_area'}

  Novo Pedido:

    - Cliente (cardápio): seleciona e adiciona os itens do pedido à lista e, depois que o botão de "Enviar Pedido" é clicado, os itens do pedido são enviados como um único pedido.
    - Servidor: recebe os dados do pedido, adiciona um identificador, o status de "preparando" e envia a mensagem do tipo new_order para o cliente da cozinha.
    
    Exemplo:
      - Cliente: {'type': 'new_order', 'item': 'café'}
      - Servidor: {'type': 'new_order', 'order': {'id': 1, 'item': 'café', 
            'status': 'preparando}}

  Atualização do Pedido:

    - Cliente (totem da cozinha): após o pedido ser marcado como concluído, é enviada uma mensagem ao servidor com o identificador dele.
    - Servidor: atualiza o status do pedido para pronto e envia uma mensagem com o identificador do pedido ao cliente totem de pedidos prontos
    
    - Exemplo:
      - Cliente: {'type': 'update_order', 'order_id': 1}
      - Servidor: {'type': 'order_ready', 'order_id': 1}

  Cancelamento do Pedido:

    - Cliente (totem da cozinha): após o pedido ser marcado como cancelado, é enviada uma mensagem ao servidor com o identificador dele.
    
    - Exemplo:
      - Cliente: {'type': 'canceled_order', 'order_id': 2}
    		
  Notificação à área de pedidos prontos:
    
    - Servidor: envia os pedidos concluídos com o identificador ao cliente totem de pedidos prontos.
    
    - Exemplo: 
      - Servidor: {'type': 'order_ready', 'order_id': 1}

Tipo do protocolo

  O tipo do protocolo criado é proprietário, pois é específico para este sistema de padaria.
