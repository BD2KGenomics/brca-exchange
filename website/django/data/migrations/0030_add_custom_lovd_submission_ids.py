# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-05-09 15:52


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0029_new_lovd_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='Submission_ID_LOVD',
            field=models.TextField(default=b'-'),
        ),
        migrations.RunSQL(
            """
            DROP MATERIALIZED VIEW IF EXISTS currentvariant;
            CREATE MATERIALIZED VIEW currentvariant AS (
                SELECT * FROM "variant" WHERE (
                    "id" IN ( SELECT DISTINCT ON ("Genomic_Coordinate_hg38") "id" FROM "variant" ORDER BY "Genomic_Coordinate_hg38" ASC, "Data_Release_id" DESC )
                )
            );
            """
        ),
    ]
