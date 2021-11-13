# Generated by Django 2.1.3 on 2018-12-15 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_carteira_usuario_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('datahora', models.DateField()),
                ('dataaviso', models.DateTimeField()),
                ('aviso', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'evento',
            },
        ),
    ]
