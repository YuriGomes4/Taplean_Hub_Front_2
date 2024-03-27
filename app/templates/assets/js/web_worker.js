// Diz o que fazer quando outro thread enviar uma mensagem
addEventListener('message', function(e) {
    var dados = e.data;
    if ( dados.funcao == "add_products" ) {
        add_products(dados.valor[0], dados.valor[1], dados.valor[2], dados.valor[3]); // Chama uma função demorada
        //postMessage({ resultado:ret }); // Manda o resultado como mensagem
    }
    // Outras funções, se aplicável
});

function add_products(produtos, session_id, remote_adr, base_url) {
    //var tr = document.createElement("tr");

    for (var produto in produtos) {
        var itemId = produtos[produto].id;

        var xhrp = new XMLHttpRequest();
        xhrp.open("GET", base_url+"/api/v1/meli/anuncio/"+itemId+"?range_vendas=true&visitas=30", false);
        xhrp.setRequestHeader('x-session-id', session_id);
        xhrp.setRequestHeader('x-remote-adr', remote_adr);;
        xhrp.onreadystatechange = function() {
            if (xhrp.readyState === 4 && xhrp.status === 200) {
                var response = JSON.parse(xhrp.responseText).result;
                // Manipulate response data here
                var produto = response;

                // se não tiver a key ID no produto

                if ("id" in produto) {
                    console.log(produto);

                    //"%Y-%m-%dT%H:%M:%S.%fZ"
                    var data_criacao = new Date(produto.date_created);
                    var data_atual = new Date();
                    var tempo_vida = Math.round((data_atual - data_criacao) / (1000 * 60 * 60 * 24))
                    var visitas_totais = 0;
                    var visitas_dia = [];
                    var visitasProd = produto.visitas.results;
                    for (var i = 0; i < visitasProd.length; i++) {
                        visitas_totais += visitasProd[i].total;
                        visitas_dia.push(visitasProd[i].total);
                    }
                    var media_visitas = (visitas_totais / visitasProd.length).toFixed();
                    //var variacao_total = 0;
                    var variacao = [];
                    for (var i = 1; i < visitas_dia.length; i++) {
                        if ((visitas_dia[i] - visitas_dia[i-1]) > 0) {
                            variacao.push((visitas_dia[i] - visitas_dia[i-1]));
                            //variacao_total += (visitas_dia[i] - visitas_dia[i-1]);
                        } else {
                            variacao.push((visitas_dia[i] - visitas_dia[i-1])*-1);
                            //variacao_total += ((visitas_dia[i] - visitas_dia[i-1])*-1);
                        }
                    }

                    //var media_variacao_percentual = (variacao_total / visitas_dia.length);
                    var media_variacao_percentual = (variacao.reduce((a, b) => a + b, 0) / variacao.length).toFixed(2);

                    pLojaOficial = ""

                    if (produto.official_store_id !== null) {
                        pLojaOficial = "color: #fd0d0d;";
                    } else {
                        pLojaOficial = "color: #fff;";
                    }

                    var tbodyy = `
                        <td id="${produto.id}-link"><a href="${produto.permalink}" target="_blank">Ver</a></td>
                        <td id="${produto.id}-foto"><img src="${produto.pictures[0].secure_url}" alt="Imagem do produto" width="70" height="70"></td>
                        <td id="${produto.id}-titulo" style="${pLojaOficial}">${produto.title}</td>
                        <td id="${produto.id}-preco">${produto.price}</td>
                        <td id="${produto.id}-tempo_vida">${tempo_vida} dias</td>
                        <td id="${produto.id}-range_vendas">${produto.range_vendas}</td>
                        <td id="${produto.id}-venda_mes">${((parseInt(produto.range_vendas)/tempo_vida)*30).toFixed()}</td>
                        <td id="${produto.id}-visitas_dia">${media_visitas}</td>
                        <td id="${produto.id}-variacao_visitas">${((media_variacao_percentual/media_visitas)*100).toFixed(2)}%</td>
                        <td id="${produto.id}-adicionar"><div class="form-check form-switch"><input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault"></div></td>
                        <div id="infos" categoria="${produto.category_id}" tipo_anuncio="${produto.listing_type_id}" taxa_fixa="${produto.sale_fee_fixed}" comissao="${produto.sale_fee}" frete_gratis="${produto.shipping.free_shipping}" custo_frete="${produto.shipping_free_cost}"></div>
                    `;

                    //tbodyy.innerHTML += tr.outerHTML;
                    postMessage({ funcao:'add_products', innerhtml:tbodyy, id:produto.id});
                    //return tbodyy;
                } else {
                    var tbodyy = `
                        <td id="${itemId}-link"><a href="https://www.mercadolivre.com.br/p/${itemId}" target="_blank">Ver</a></td>
                        <td id="${itemId}-foto"></td>
                        <td id="${itemId}-titulo">Produto ${itemId} é um catálogo</td>
                        <td id="${itemId}-preco"></td>
                        <td id="${itemId}-tempo_vida"></td>
                        <td id="${itemId}-range_vendas"></td>
                        <td id="${itemId}-venda_mes"></td>
                        <td id="${itemId}-visitas_dia"></td>
                        <td id="${itemId}-variacao_visitas"></td>
                        <td id="${itemId}-adicionar"><div class="form-check form-switch"><input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault" disabled></div></td>
                        <div id="infos" categoria="" tipo_anuncio="" taxa_fixa="" comissao="" frete_gratis="" custo_frete=""></div>
                    `;

                    postMessage({ funcao:'add_products', innerhtml:tbodyy, id:itemId});
                }
            }
        };
        xhrp.send();
    }

}