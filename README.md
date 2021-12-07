## InsideMarket 
Bot do telegram que busca informações do mercado financeiro brasileiro e internacional como as cotações
dos ativos, dividendos, gráficos, ajustes do dolar, indice, milho, boi, soja e diversas outras funcionalidades
como disparo de gatilho para compra e controle de carteira.
Foi idealizado por um grupo de pequenos investidores e está em constante desenvolvimento.

Você pode testar entrando neste grupo
https://t.me/testeMarketBot

Utilize o comando /help para verificar mais detalhes:
alguns comandos disponíveis:
 - /ajuste win
 - /ajuste wdo
 - /cotação petr4
 - /cotação vale3
 - /grafico petr4
 - /dividendos petr4
 - /ranking
 - /volume
 - /adr PBR
 - /adr ITUB
 - /crypto BTC
 - /crypto ETH



## Rodar a aplicação
Lembre-se de alterar o token na core/constant.py assim não haverá problema com o robo
prod

Para rodar/debugar esta aplicação é necessario instalar o python 3.8 ou superior
instalar as bibliotecas contidas no requirements.txt

#Arquivo .env
Crie o arquivo .env dentro da pasta insidemarketb3/.env
DATABASE_URL=xxx
TOKEN=xxx
...


#instalação das libs
pip install -f requirements.txt

#rodar o projeto
python manage.py runserver

ou se quiser publicar no docker
docker-compose up -d

#remover
docker-compose down --rmi all
