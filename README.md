# 📄 Painel de análise de indicadores operacionais e financeiros em plantas industriais

## Introdução

Este documento tem o objetivo de introduzir as funcionalidades encontradas no **Painel de análise de indicadores operacionais e financeiros em plantas industriais**, desenvolvido como projeto para aplicação em diferentes cenários de indústrias. O projeto desenvolvido simula análises integradas dos indicadores OEE, para avaliação de desempenho operacional, e EBITDA, para avaliação de desempenho financeiro. A aplicação deste projeto se aplica a contextos de avaliação da saúde financeira do negócio, alocação de recursos e valoração.

## Metodologia

Como dados operacionais e gerenciais de empresas são protegidos por cláusulas de confidencialidade, a base de dados utilziada no projeto foi gerada de forma sintética buscando simular a realidade de processos industriais. Uilizou-se a plataforma Mostly.ai, dedicada à geração de bases sintéticas, para a geração dos dados iniciais, os quais foram expandidos utilizando o *chatbot* ChatGPT e posteriormente validados com métodos da biblioteca Pandas para que inconsistências fossem removidas. Esta base de dados foi salva localmente e se encontra no repositório do projeto no GitHub, o qual é acessado para que a aplicação desenvolvida para acesso do painel seja executada.

A manipulação dos dados é realizada integralmente por meio de um subrotinas escritas na linguagem Python, sendo destacado o uso da biblioteca Streamlit para elaboração do painel de visualização.

## Acesso ao painel e base de dados

O painel para visualização dos dados e aplicação pode ser acessado diretamente através [deste link](https://industrialkpi.onrender.com/).

Alternativamente, o repositório pode ser clonado para que as subrotinas sejam executadas localmente em um interpretador Python. Seguem as etapas:

```
git clone https://github.com/henriquecuryboaro/kpi_industria

```
Com o diretório clonado, instalam-se os pacotes necessários à execução do painel ao se executar o seguinte código no diretório em que os arquivos do projeto se encontram:

```
pip install -r requirements.txt
```

É recomendado o isolamento do ambiente em que o projeto será executado por meio da criação de ambiente virtual.

## Conteúdo do painel

O conteúdo do painel é dividido em duas seções principais:

* Indicadores de natureza operacional, contemplando análise de indicadores como OEE, tempo de inatividade e utilização da capacidade da planta
* Indicadores de natureza financeira, contemplando análise de indicadores como EBITDA (Lucro antes de Juros, Impostos, Depreciação e Amortização), o que leva a uma proposta para determinação do valor de mercado dos ativos sob análise

### Imagens

![This is an alt text.](/operacional.png "Informaçõs do painel de natureza operacional")

![This is an alt text.](/financeiro.png "Informaçõs do painel de natureza financeira")

## Conclusões

O objetivo do acesso *on-line* ao painel é permitir ao usuário navegar pelos dados de forma interativa, gerando seus próprios *insights*, mas algumas observações interessantes podem ser destacadas:

* Os dados tratam de operações envolvendo indústrias dos segmentos de polímeros, agroquímica e gases industriais
* A análise de valor de mercado foi realizada com o emprego do método dos múltiplios EV/EBITDA, considerando valores típicos para as estimativas de mercado (sete e dez múltiplos). A referência consultada pode ser encontrada [aqui](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html).
* Nota-se um valor maior do indicador de **produção por empregado** na planta que representa o setor de gases industriais, ilustrando um caso de operação pouco **trabalho-intensiva** em comparação com os demais ativos
* O ativo representativo do setor de gases industriais também apresenta um indicador de *performance*, dentro da avaliação de OEE, em patamar bastante elevado, o que é coerente com a observação de produtividade por empregado feita acima.
* Ainda, estes indicadores apresentados poderiam levar a considerações sobre implementações de mais metodologias de automação (especialmente em setores com indicadores relativamente mais baixos de produtividade)

## Projetos futuros

A conclusão deste painel oferece uma oportunidade para avaliação de indicadores operacionais de forma simples e intuitiva, destacando-se a possibilidade de comparações entre diferentes setores.

Como possibilidade de futuros desenvolvimentos, considera-se a possibilidade de aplicação de modelo preditivo para a obtenção de valores de EBITDA em função de indicadores como OEE ou outras variáveis, visto que este indicador financeiro é um dos mais relevantes para a avaliação da saúde financeira de um empreendimento.

