# Generated by Django 3.2.6 on 2023-08-25 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='atributosxfichaxbloque',
            fields=[
                ('id_atribxfichaxbloq', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_atrib', models.CharField(default='', max_length=50, null=True)),
                ('listaValores', models.TextField(default=None, null=True)),
                ('min', models.IntegerField(default=0)),
                ('max', models.IntegerField(default=0)),
                ('status', models.SmallIntegerField(default=1)),
                ('orden_presentacion', models.SmallIntegerField(default=0)),
                ('fk_atribxfichaxbloq_padre', models.ForeignKey(db_column='fk_tabla_padre', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Planning.atributosxfichaxbloque')),
            ],
            options={
                'ordering': ['orden_presentacion'],
            },
        ),
        migrations.CreateModel(
            name='fichas',
            fields=[
                ('id_ficha', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_ficha', models.TextField()),
                ('mostrar', models.SmallIntegerField()),
                ('ordenamiento', models.SmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['ordenamiento'],
            },
        ),
        migrations.CreateModel(
            name='public_fichas_datos',
            fields=[
                ('id_publicFichasDatos', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.TextField(default=None, null=True)),
                ('id_atributo_fichaBloque', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Planning.atributosxfichaxbloque')),
                ('id_public', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='App.apppublico')),
            ],
        ),
        migrations.CreateModel(
            name='fichas_listas',
            fields=[
                ('id_fichas_listas', models.SmallAutoField(primary_key=True, serialize=False)),
                ('pais', models.SmallIntegerField()),
                ('region', models.SmallIntegerField()),
                ('Descripcion', models.TextField()),
                ('fk_fichalista_padre', models.ForeignKey(db_column='fk_tabla_padre', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Planning.fichas_listas')),
                ('fk_tipo_lista', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='App.conftablasconfiguracion')),
            ],
        ),
        migrations.CreateModel(
            name='fichas_bloques',
            fields=[
                ('id_bloquexficha', models.AutoField(primary_key=True, serialize=False)),
                ('descrip_bloque', models.TextField()),
                ('ordenamiento', models.SmallIntegerField(default=0)),
                ('fk_idficha', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Planning.fichas')),
            ],
            options={
                'ordering': ['ordenamiento'],
            },
        ),
        migrations.AddField(
            model_name='atributosxfichaxbloque',
            name='fk_ficha_bloque',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Planning.fichas_bloques'),
        ),
        migrations.AddField(
            model_name='atributosxfichaxbloque',
            name='fk_tipodato',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='App.conftablasconfiguracion'),
        ),
    ]
