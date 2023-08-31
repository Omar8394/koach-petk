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
            name='Event_eventos',
            fields=[
                ('ideventos', models.SmallAutoField(primary_key=True, serialize=False)),
                ('fechainicio', models.DateField(blank=True, db_column='fechainicio', null=True)),
                ('lugar', models.TextField(blank=True, db_column='lugar', null=True)),
                ('tipoevento', models.CharField(blank=True, max_length=1, null=True)),
                ('temaprincipal', models.TextField(blank=True, db_column='temaprincipal', null=True)),
                ('fechafinalevento', models.DateField(blank=True, db_column='fechafinal', null=True)),
                ('fkmotivo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fk_motivo', to='App.conftablasconfiguracion')),
                ('fktipoevento', models.ForeignKey(db_column='fktipoevento', on_delete=django.db.models.deletion.DO_NOTHING, to='App.conftablasconfiguracion')),
                ('fktipomedio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fk_tipomedio', to='App.conftablasconfiguracion')),
            ],
        ),
        migrations.CreateModel(
            name='Pagos_regpagos',
            fields=[
                ('idregpagos', models.SmallAutoField(primary_key=True, serialize=False)),
                ('fechaPago', models.DateField(blank=True, db_column='fechapago', null=True)),
                ('referencia', models.TextField(blank=True, db_column='referencia', null=True)),
                ('confirmado', models.IntegerField(blank=True, db_column='confirmado', null=True)),
                ('montopagado', models.DecimalField(decimal_places=2, default=None, max_digits=11, null=True)),
                ('codigohash', models.TextField(blank=True, db_column='codigohash', null=True)),
                ('beneficiario', models.TextField(blank=True, db_column='beneficiario', null=True)),
                ('fkStatusPago', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fk_statuspago', to='App.conftablasconfiguracion')),
                ('fkconceptopago', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fk_conceptopago', to='App.conftablasconfiguracion')),
                ('fkmetodopago', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fk_metodopago', to='App.conftablasconfiguracion')),
                ('fkpublic', models.ForeignKey(db_column='fk_publico', on_delete=django.db.models.deletion.DO_NOTHING, to='App.apppublico')),
            ],
        ),
        migrations.CreateModel(
            name='Pagos_eventos',
            fields=[
                ('idpagoseventos', models.SmallAutoField(primary_key=True, serialize=False)),
                ('fk_ideventos', models.ForeignKey(db_column='fk_ideventos', on_delete=django.db.models.deletion.DO_NOTHING, to='Payments.event_eventos')),
                ('fk_idregpagos', models.ForeignKey(db_column='fk_idregpagos', on_delete=django.db.models.deletion.DO_NOTHING, to='Payments.pagos_regpagos')),
            ],
        ),
    ]
