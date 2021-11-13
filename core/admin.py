from django.contrib import admin
from core.models import Interacao, Grupo, ComandoCache, Carteira, Papel, Evento, Alarme, Feriado, BlackList, UsuarioChat, Conversa

@admin.register(Interacao)
# Register your models here.
class InteracaoAdmin(admin.ModelAdmin):
    list_display = ['id', 'comando']

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_id', 'nome', 'ativo', 'autorizado']

@admin.register(ComandoCache)
class ComandoCacheAdmin(admin.ModelAdmin):
    list_display = ['id', 'comando', 'datahora']

@admin.register(Carteira)
class CarteiraAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_id', 'papel', 'usuario']

@admin.register(Papel)
class PapelAdmin(admin.ModelAdmin):
    list_display = ['id', 'papel', 'valor', 'datahora']

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'datahora']

@admin.register(Alarme)
class AlarmeAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat_id', 'usuario', 'datahora', 'situacao']

@admin.register(Feriado)
class FeriadoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'data']

@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'usuarioid', 'datahora']

@admin.register(UsuarioChat)
class UsuarioChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'usuario_id']

@admin.register(Conversa)
class ConversaAdmin(admin.ModelAdmin):
    list_display = ['id', 'pergunta']