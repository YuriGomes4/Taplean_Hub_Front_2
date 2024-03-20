// Diz o que fazer quando outro thread enviar uma mensagem
addEventListener('message', function(e) {
    var dados = e.data;
    if ( dados.funcao == "add_products" ) {
        add_products(dados.valor[0], dados.valor[1], dados.valor[2]); // Chama uma função demorada
        //postMessage({ resultado:ret }); // Manda o resultado como mensagem
    }
    // Outras funções, se aplicável
});

function add_products(produtos, token, base_url) {
    //var tr = document.createElement("tr");

    for (var produto in produtos) {
        var xhrp = new XMLHttpRequest();
        xhrp.open("GET", base_url+"/api/v1/meli/anuncio/"+produtos[produto].id+"?range_vendas=true&visitas=30", false);
        xhrp.setRequestHeader("x-access-token", token);
        xhrp.onreadystatechange = function() {
            if (xhrp.readyState === 4 && xhrp.status === 200) {
                var response = JSON.parse(xhrp.responseText).result;
                // Manipulate response data here
                var produto = response;

                //var tbodyy = document.querySelector("tbody");

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

                var tbodyy = `
                    <td id="${produto.id}-link"><a href="${produto.permalink}" target="_blank">Ver</a></td>
                    <td id="${produto.id}-foto"><img src="${produto.pictures[0].secure_url}" alt="Imagem do produto" width="70" height="70"></td>
                    <td id="${produto.id}-titulo">${produto.title}</td>
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
            }
        };
        xhrp.send();
    }

}