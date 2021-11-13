from django.db import models

# Create your models here.

class Interacao(models.Model):

    comando = models.CharField(max_length=100)
    saida = models.TextField()
    code = models.TextField()
    ativo = models.BooleanField(default=True)

    def __unicode__(self):
        return (self.comando)

    def execute(self):            
        exec(self.code, globals())
        dic = script()
        return dic

    def get_output(self, binds):
        return (self.saida.format(**binds))

    class Meta:
        db_table = 'interacao'


class Grupo(models.Model):

    chat_id = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)
    avisos = models.BooleanField(default=True)
    autorizado = models.BooleanField(default=False)

    def __str__(self):
        return (self.nome)

    def __unicode__(self):
        return (self.nome)

    class Meta:
        db_table = 'grupo'

class ComandoCache(models.Model):

    comando = models.CharField(max_length=100)
    datahora = models.DateTimeField(auto_now= True)
    saida = models.CharField(max_length=4096)

    class Meta:
        db_table = 'comando_cache'


class Carteira(models.Model):
    chat_id = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    usuario_id = models.CharField(max_length=100)
    papel = models.CharField(max_length=100)
    valor_compra = models.DecimalField(max_digits=5, decimal_places=2)
    valor_stop = models.DecimalField(max_digits=5, decimal_places=2)
    valor_tprofit = models.DecimalField(max_digits=5, decimal_places=2)
    resultado = models.DecimalField(max_digits=5, decimal_places=2)
    situacao = models.CharField(max_length=100)
    direcao = models.CharField(max_length=100, default='UP')

    class Meta:
        db_table = 'carteira'


class Papel(models.Model):
    papel = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    valor_anterior = models.DecimalField(max_digits=5, decimal_places=2)
    valor_maxima = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    valor_minima = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    datahora = models.DateTimeField(auto_now= True)

    class Meta:
        db_table = 'papel'


class Evento(models.Model):
    nome = models.CharField(max_length=100)
    datahora = models.DateField(auto_now=False)
    dataaviso = models.DateTimeField()
    aviso = models.CharField(max_length=300)

    class Meta:
        db_table = 'evento'

class Alarme(models.Model):
    chat_id = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    usuario_id = models.CharField(max_length=100)
    datahora = models.DateTimeField()
    situacao = models.CharField(max_length=100)

    class Meta:
        db_table = 'alarme'


class Feriado(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField(auto_now=False)

    class Meta:
        db_table = 'feriado'


class BlackList(models.Model):
    nome = models.CharField(max_length=100)
    usuarioid = models.CharField(max_length=100)
    datahora = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'blacklist'


class UsuarioChat(models.Model):
    usuario = models.CharField(max_length=100)
    usuario_id = models.CharField(max_length=100)

    class Meta:
        db_table = 'usuarioChat'


class Conversa(models.Model):
    pergunta = models.TextField()
    resposta = models.TextField()

    class Meta:
        db_table = 'conversa'