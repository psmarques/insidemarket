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
